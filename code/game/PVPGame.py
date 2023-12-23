from Game import Game
from time import perf_counter
import json
import random
from const import TIME_OPTIONS, MIN_RANK, MAX_RANK
import chess


class PVPGame(Game):
    waiting_list: dict[str, list[list[str]]] = {
        key: [[] for _ in range(6)] for key in TIME_OPTIONS
    }

    @classmethod
    async def start(cls, sid:str, data: dict[str, str]) -> None:
        if not await cls.validate_data(sid, data):
            return
        rank = cls.calculate_rank(data["rank"])
        time = data["time"]
        index = cls.calculate_index(rank)

        if sid in Game.sid_to_id:
            await cls.emit_error("Started Matching", sid)
            return

        await cls.process_matching(sid, time, rank, index)

    @classmethod
    async def validate_data(cls, sid:str, data: dict[str, str]) -> bool:
        if "rank" not in data or "time" not in data:
            await cls.emit_error("Missing fields", sid)
            return False

        if not cls.check_int(data, "rank", MIN_RANK, MAX_RANK):
            await cls.emit_error("Invalid rank", sid)
            return False

        if not cls.check_options(data, "time", TIME_OPTIONS):
            await cls.emit_error("Invalid clocktime", sid)
            return False
        
        return True

    @staticmethod
    def check_int(data, key, inf, sup):
        try:
            v = int(data[key])
            return inf <= v <= sup
        except (ValueError, TypeError):
            return False

    @staticmethod
    def check_options(data, key, options):
        try:
            value = int(data[key])
            return value in options
        except (ValueError, TypeError, KeyError):
            return False

    @staticmethod
    def calculate_rank(rank):
        return round(max(min(int(rank), 100), 0) / 10) * 10
    
    @staticmethod
    def calculate_index(rank):
        return (10 - (rank // 10)) % 6 if rank // 10 > 5 else (rank // 10) % 6

    @classmethod
    async def process_matching(cls, sid, time, rank, index):
        if (
            len(cls.waiting_list[time][index]) > 0
            and cls.waiting_list[time][index][0]["rank"] == 100 - rank
        ):
            # se c'è un match
            await cls.setup_game_with_existing_player(sid, time, rank, index)
        else:
            await cls.add_player_to_waiting_list(sid, time, rank, index)

    @classmethod
    async def setup_game_with_existing_player(cls, sid, time, rank, index):
        session = await Game.sio.get_session(sid)
        found_guest = None
        for waiting in cls.waiting_list[time][index]:
            if abs(waiting["elo"] - session["elo"]) < 100:
                found_guest = waiting
                break
        if found_guest is None:
            await cls.add_player_to_waiting_list(sid, time, rank, index)
            return
        first = random.randint(0, 1)
        players = [sid, found_guest["sid"]] if first else [found_guest["sid"], sid]
        game_id = "".join(random.choice("0123456789abcdef") for _ in range(16))
        cls.games[game_id] = cls(
            players, rank if first else 100 - rank, time
        )
        cls.waiting_list[time][index].remove(found_guest)
        cls.sid_to_id[players[0]] = game_id
        cls.sid_to_id[players[1]] = game_id
        current = await Game.sio.get_session(players[0])
        opponent = await Game.sio.get_session(players[1])
        usernames = [obj["username"] for obj in [current, opponent]]
        elos = [obj["elo"] for obj in [current, opponent]]
        await Game.sio.emit(
            "config",
            {
                "fen": cls.games[game_id].fen,
                "id": game_id,
                "color": "white",
                "elo": elos,
                "username": usernames[1]
            },
            room=players[0],
        )
        await Game.sio.emit(
            "config",
            {
                "fen": cls.games[game_id].fen,
                "id": game_id,
                "color": "black",
                "elo": elos,
                "username": usernames[0]
            },
            room=players[1],
        )

    @classmethod
    async def add_player_to_waiting_list(cls, sid, time, rank, index):
        session = await Game.sio.get_session(sid)
        cls.waiting_list[time][index].append(
            {"sid": sid, "rank": rank, "elo": session["elo"]}
        )
        # serve per eliminarlo dalla entry
        Game.sid_to_id[sid] = {"time": time, "index": index}

    @classmethod
    async def emit_error(cls, cause, sid, fatal=True):
        await Game.sio.emit("error", {"cause": cause, "fatal": fatal}, room=sid)


    # @classmethod
    # async def start(cls, sid: str, data: dict[str, str]) -> None:
    #     def check_int(key, inf, sup):
    #         try:
    #             v = int(data[key])
    #             return inf <= v <= sup
    #         except (ValueError, TypeError):
    #             return False

    #     def check_options(key, options):
    #         try:
    #             value = int(data[key])
    #             return value in options
    #         except (ValueError, TypeError, KeyError):
    #             return False

    #     # Check for data validity
    #     if "rank" not in data or "time" not in data:
    #         await Game.sio.emit(
    #             "error", {"cause": "Missing fields", "fatal": True}, room=sid
    #         )
    #         return
    #     if not check_int("rank", MIN_RANK, MAX_RANK):
    #         await Game.sio.emit(
    #             "error", {"cause": "Invalid rank", "fatal": True}, room=sid
    #         )
    #         return
    #     if not check_options("time", TIME_OPTIONS):
    #         await Game.sio.emit(
    #             "error", {"cause": "Invalid clocktime", "fatal": True}, room=sid
    #         )
    #         return

    #     # se non loggato, se loggato devo pure vedere il database
    #     time = data["time"]
    #     rank = round(max(min(int(data["rank"]), 100), 0) / 10) * 10
    #     # vedere se ci sta il complementare
    #     index = (10 - (rank // 10)) % 6 if rank // 10 > 5 else (rank // 10) % 6
    #     if sid in Game.sid_to_id:
    #         await Game.sio.emit(
    #             "error", {"cause": "Started Matching", "fatal": True}, room=sid
    #         )
    #     elif (
    #         len(Game.waiting_list[time][index]) > 0
    #         and Game.waiting_list[time][index][0]["rank"] == 100 - rank
    #     ):
    #         session = await Game.sio.get_session(sid)
    #         found_guest = None
    #         for waiting in Game.waiting_list[time][index]:
    #             if abs(waiting["elo"] - session["elo"]) < 100:
    #                 found_guest = waiting
    #                 break
    #         if found_guest is not None:
    #             first = random.randint(0, 1)
    #             players = (
    #                 [sid, found_guest["sid"]] if first else [found_guest["sid"], sid]
    #             )
    #             game_id = "".join(random.choice("0123456789abcdef") for _ in range(16))
    #             Game.games[game_id] = cls(
    #                 players, rank if first else 100 - rank, data["time"]
    #             )
    #             Game.waiting_list[time][index].remove(found_guest)
    #             Game.sid_to_id[players[0]] = game_id
    #             Game.sid_to_id[players[1]] = game_id
    #             current = await Game.sio.get_session(players[0])
    #             opponent = await Game.sio.get_session(players[1])
    #             usernames = [obj["username"] for obj in [current, opponent]]
    #             elos = [obj["elo"] for obj in [current, opponent]]
    #             await Game.sio.emit(
    #                 "config",
    #                 {
    #                     "fen": Game.games[game_id].fen,
    #                     "id": game_id,
    #                     "color": "white",
    #                     "elo": elos,
    #                     "username": usernames[1]
    #                 },
    #                 room=players[0],
    #             )
    #             await Game.sio.emit(
    #                 "config",
    #                 {
    #                     "fen": Game.games[game_id].fen,
    #                     "id": game_id,
    #                     "color": "black",
    #                     "elo": elos,
    #                     "username": usernames[0]
    #                 },
    #                 room=players[1],
    #             )
    #         else:
    #             session = await Game.sio.get_session(sid)
    #             Game.waiting_list[time][index].append(
    #                 {"sid": sid, "rank": rank, "elo": session["elo"]}
    #             )
    #             # serve per eliminarlo dalla entry
    #             Game.sid_to_id[sid] = {"time": time, "index": index}

    #         # togliere l'id dal frontend
    #     else:
    #         session = await Game.sio.get_session(sid)
    #         Game.waiting_list[time][index].append(
    #             {"sid": sid, "rank": rank, "elo": session["elo"]}
    #         )
    #         # serve per eliminarlo dalla entry
    #         Game.sid_to_id[sid] = {"time": time, "index": index}

    def __init__(self, players: [str], rank: [], timer):
        super().__init__(players, rank, timer)
        self.timer = 1
        self.isTimed = timer != -1

    def swap(self):
        self.popped = False
        self.turn = (self.turn + 1) % 2

    def is_player_turn(self, sid):
        return self.current.sid == sid

    async def disconnect(self, sid: str, send_to_disconnected: bool = True) -> None:
        await self.update_win_database(self.opponent(sid).sid, False)
        print("Sto disconnettendo il giocatore", sid)
        if send_to_disconnected:
            await Game.sio.emit("end", {"winner": False}, room=sid)
        await Game.sio.emit("end", {"winner": True}, room=self.opponent(sid).sid)
        # await Game.sio.disconnect(sid=self.opponent(sid).sid)
        if sid not in Game.sid_to_id:
            return
        elif Game.sid_to_id[sid] in Game.games:
            if self.opponent(sid).sid in Game.sid_to_id:
                del Game.sid_to_id[self.opponent(sid).sid]
            del Game.games[Game.sid_to_id[sid]]
            del Game.sid_to_id[sid]

    async def pop(self, sid: str) -> None:
        if sid not in Game.sid_to_id:
            await PVPGame.emit_error("Missing id", sid)
        if not await self.game_found(sid, Game.sid_to_id[sid]):
            return
        if not self.is_player_turn(sid):
            await PVPGame.emit_error("It's not your turn", sid)
            return
        if self.popped:
            await PVPGame.emit_error("You have already popped", sid)
            return
        if self.board.fullmove_number == 1:
            await PVPGame.emit_error("No moves to undo", sid)
            return
        else:
            self.board.pop()
            self.board.pop()
            await Game.sio.emit(
                "pop",
                {"time": self.get_times()},
                room=[player.sid for player in self.players],
            )
            self.popped = True

    async def move(self, sid: str, data: dict[str, str]) -> None:
        if sid not in Game.sid_to_id:
            await Game.sio.emit("error", {"cause": "No games found"}, room=sid)
        if "san" not in data:
            await Game.sio.emit("error", {"cause": "Missing fields"}, room=sid)
            return
        if data["san"] is None:
            await Game.sio.emit("error", {"cause": "Encountered None value"}, room=sid)
            return
        if not self.is_player_turn(sid):
            await Game.sio.emit("error", {"cause": "It's not your turn"}, room=sid)
            return
        if not self.current.has_time():
            return
        try:
            uci_move = self.board.parse_san(data["san"]).uci()
        except (chess.InvalidMoveError, chess.IllegalMoveError):
            await Game.sio.emit("error", {"cause": "Invalid move"}, room=sid)
            return
        if chess.Move.from_uci(uci_move) not in self.board.legal_moves:
            await Game.sio.emit("error", {"cause": "Invalid move"}, room=sid)
            return
        uci_move = self.board.parse_uci(self.board.parse_san(data["san"]).uci())
        san_move = self.board.san(uci_move)
        self.board.push_uci(uci_move.uci())
        outcome = self.board.outcome()
        if outcome is not None:
            await Game.sio.emit(
                "move",
                {"san": san_move, "time": self.get_times()},
                room=self.current.sid,
            )
            await Game.sio.emit(
                "move", {"san": san_move, "time": self.get_times()}, room=self.next.sid
            )
            elos = await self.update_win_database(sid, outcome.winner)
            await Game.sio.emit(
                "end",
                {
                    "winner": True if outcome.winner is not None else outcome.winner,
                    "elo": elos[self.turn],
                },
                room=self.current.sid,
            )
            await Game.sio.emit(
                "end",
                {
                    "winner": False if outcome.winner is not None else outcome.winner,
                    "elo": elos[1 - self.turn],
                },
                room=self.next.sid,
            )
            await self.disconnect(self.next.sid)
            return
        self.popped = False
        await Game.sio.emit("ack", {"time": self.get_times()}, room=self.current.sid)
        self.swap()
        self.current.latest_timestamp = perf_counter()
        await Game.sio.emit(
            "move", {"san": san_move, "time": self.get_times()}, room=self.current.sid
        )
