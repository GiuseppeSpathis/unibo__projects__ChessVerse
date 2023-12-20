import unittest
from unittest import TestCase, IsolatedAsyncioTestCase
from unittest import mock
from unittest.mock import AsyncMock, PropertyMock

import sys
import random
import chess
import socketio

sys.path.append("../..")
from PVEGame import PVEGame
from Game import Game
from const import MODE_RANKED_PT_DIFF

import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
target_dir = "/".join(project_root.split("/")[:-1])
os.chdir(target_dir)

class TestInitialization(TestCase):
    @mock.patch("Game.confighandler.gen_start_fen", return_value=chess.STARTING_FEN)
    def setUp(self, mock_gen_start_fen):
        self.player = "".join(random.choice("0123456789abcdef") for _ in range(16))
        self.sid = "".join(random.choice("0123456789abcdef") for _ in range(16))
        self.rank = 1
        self.depth = 5
        self.time = 100
        Game.games[self.sid] = PVEGame(self.player, self.rank, self.depth, self.time)

    def test_player_init(self):
        self.assertEqual(Game.games[self.sid].players[0], self.player)

    def test_fen_init(self):
        self.assertEqual(Game.games[self.sid].fen, chess.STARTING_FEN)

    def test_bot_init(self):
        self.assertIsNone(Game.games[self.sid].bot)

    def test_depth_init(self):
        self.assertEqual(Game.games[self.sid].depth, self.depth)

    def test_turn_init(self):
        self.assertEqual(Game.games[self.sid].turn, 0)


class TestGetNewRanked(unittest.TestCase):
    def setUp(self):
        self.cur_ranked = 1

    def test_with_outcome_none(self):
        self.assertEqual(self.cur_ranked + MODE_RANKED_PT_DIFF[1], PVEGame.get_new_ranked(self.cur_ranked, None))

    def test_with_outcome_true(self):
        self.assertEqual(self.cur_ranked + MODE_RANKED_PT_DIFF[0], PVEGame.get_new_ranked(self.cur_ranked, True))

    def test_with_outcome_false(self):
        self.assertEqual(self.cur_ranked + MODE_RANKED_PT_DIFF[2], PVEGame.get_new_ranked(self.cur_ranked, False))


class TestStart(IsolatedAsyncioTestCase):
    @mock.patch("Game.confighandler.gen_start_fen", return_value=chess.STARTING_FEN)
    def setUp(self, mock_gen_start_fen):
        self.player = "".join(random.choice("0123456789abcdef") for _ in range(16))
        self.sid = "".join(random.choice("0123456789abcdef") for _ in range(16))
        self.rank = 1
        self.depth = 5
        self.time = 100
        Game.sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
        self.mock_emit = AsyncMock()
        Game.sio.emit = self.mock_emit

    async def test_missing_fields(self):
        await PVEGame.start(self.sid, {})
        Game.sio.emit.assert_called_once_with(
            "error", {"cause": "Missing fields", "fatal": True}, room=self.sid
        )

    async def test_invalid_rank(self):
        data = {"rank": 150, "depth": self.depth, "time": self.time}
        await PVEGame.start(self.sid, data)
        Game.sio.emit.assert_called_once_with(
            "error", {"cause": "Invalid rank", "fatal": True}, room=self.sid
        )

    async def test_invalid_depth(self):
        data = {"rank": self.rank, "depth": 30, "time": self.time}
        await PVEGame.start(self.sid, data)
        Game.sio.emit.assert_called_once_with(
            "error", {"cause": "Invalid bot strength", "fatal": True}, room=self.sid
        )

    async def test_invalid_time(self):
        data = {"rank": self.rank, "depth": self.depth, "time": 0}
        await PVEGame.start(self.sid, data)
        Game.sio.emit.assert_called_once_with(
            "error", {"cause": "Invalid clocktime", "fatal": True}, room=self.sid
        )

    async def test_sid_already_used(self):
        data = {"rank": self.rank, "depth": self.depth, "time": self.time}
        Game.sid_to_id[self.sid] = self.sid
        await PVEGame.start(self.sid, data)
        self.assertTrue(self.sid in Game.sid_to_id)
        Game.sio.emit.assert_called_once_with(
            "error", {"cause": "SID already used", "fatal": True}, room=self.sid
        )

    @mock.patch("PVEGame.PVEGame.instantiate_bot", new=AsyncMock("some_bot"))
    async def test_correct_start(self):
        data = {"rank": self.rank, "depth": self.depth, "time": self.time}
        await PVEGame.start(self.sid, data)
        Game.sio.emit.assert_called_once_with(
            "config", {"fen": Game.games[self.sid].fen, "rank": -1}, room=self.sid
        )


class TestDisconnect(IsolatedAsyncioTestCase):
    @mock.patch("Game.confighandler.gen_start_fen", return_value=chess.STARTING_FEN)
    def setUp(self, mock_gen_start_fen):
        self.player = "guest"
        self.rank = 1
        self.depth = 5
        self.time = 100
        self.sid = "test_sid"
        Game.sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
        self.mock_emit = AsyncMock()
        Game.sio.emit = self.mock_emit

        # Game instantiation
        Game.sid_to_id[self.sid] = self.sid
        self.game = Game.games[self.sid] = PVEGame(
            self.sid, self.rank, self.depth, self.time
        )
        self.mock_bot = self.game.bot = AsyncMock()

    async def test_bot_quit(self):
        await self.game.disconnect(self.sid)
        self.mock_bot.quit.assert_called_once()

    async def test_game_deletion(self):
        await self.game.disconnect(self.sid)
        self.assertNotIn(self.sid, Game.games.keys())
        self.assertNotIn(self.sid, Game.sid_to_id.keys())


class TestInstantiateBot(IsolatedAsyncioTestCase):
    @mock.patch("Game.confighandler.gen_start_fen", return_value=chess.STARTING_FEN)
    def setUp(self, mock_gen_start_fen):
        self.player = "guest"
        self.rank = 1
        self.depth = 5
        self.time = 100
        self.sid = "test_sid"
        Game.sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
        self.mock_emit = AsyncMock()
        Game.sio.emit = self.mock_emit

        # Game instantiation
        Game.sid_to_id[self.sid] = self.sid
        self.game = Game.games[self.sid] = PVEGame(
            self.sid, self.rank, self.depth, self.time
        )

    '''
    @mock.patch('chess.engine.popen_uci')
    async def test(self, mock_popen):
        await self.game.instantiate_bot()([call(1, 2, 3))
        mock_popen.assert_called_once_with('./stockfish')
    '''


class TestMove(IsolatedAsyncioTestCase):
    @mock.patch("Game.confighandler.gen_start_fen", return_value=chess.STARTING_FEN)
    def setUp(self, mock_gen_start_fen):
        self.player = "guest"
        self.rank = 1
        self.depth = 5
        self.time = 100
        self.sid = "test_sid"
        Game.sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
        self.mock_emit = AsyncMock()
        Game.sio.emit = self.mock_emit

        # Game instantiation
        Game.sid_to_id[self.sid] = self.sid
        self.game = Game.games[self.sid] = PVEGame(
            self.sid, self.rank, self.depth, self.time
        )
        self.mock_bot = self.game.bot = AsyncMock()

        self.test_move = "e2e4"

    async def test_san_not_in_data(self):
        await self.game.move(self.sid, {})
        Game.sio.emit.assert_called_once_with(
            "error", {"cause": "Missing fields"}, room=self.sid
        )

    async def test_data_san_is_none(self):
        await self.game.move(self.sid, {"san": None})
        Game.sio.emit.assert_called_once_with(
            "error", {"cause": "Encountered None value"}, room=self.sid
        )

    async def test_invalid_move(self):
        await self.game.move(self.sid, {"san": "err_move"})
        Game.sio.emit.assert_called_once_with(
            "error", {"cause": "Invalid move"}, room=self.sid
        )

    @mock.patch("chess.Board.outcome")
    async def test_case_game_terminates(self, mock_board_outcome):
        type(mock_board_outcome.return_value).winner = PropertyMock(
            return_value=chess.WHITE
        )
        await self.game.move(self.sid, {"san": self.test_move})
        Game.sio.emit.assert_called_once_with(
            "end", {"winner": chess.WHITE}, room=self.sid
        )

    """
    @mock.patch('chess.engine.SimpleEngine.play')
    async def test_correct_move(self, mock_bot_play):
        await self.game.move(self.sid, {'san': self.test_move})
        Game.sio.emit.assert_called_once_with(
            "move",
            {"move": chess.Board.san(move=mock_bot_play.return_value)},
            sid=self.sid
        )
    """


class TestPop(IsolatedAsyncioTestCase):
    @mock.patch("Game.confighandler.gen_start_fen", return_value=chess.STARTING_FEN)
    def setUp(self, mock_gen_start_fen):
        self.player = "guest"
        self.rank = 1
        self.depth = 5
        self.time = 100
        self.sid = "test_sid"
        Game.sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
        self.mock_emit = AsyncMock()
        Game.sio.emit = self.mock_emit

        # Game instantiation
        Game.sid_to_id[self.sid] = self.sid
        self.game = Game.games[self.sid] = PVEGame(
            self.sid, self.rank, self.depth, self.time
        )
        self.mock_bot = self.game.bot = AsyncMock()

        self.test_move = "e2e4"

    async def test_already_popped(self):
        self.game.popped = True
        await self.game.pop(self.sid)
        Game.sio.emit.assert_called_once_with(
            "error", {"cause": "You have already popped"}, room=self.sid
        )

    async def test_no_moves_to_undo(self):
        self.game.popped = False
        await self.game.pop(self.sid)
        Game.sio.emit.assert_called_once_with(
            "error", {"cause": "No moves to undo"}, room=self.sid
        )

    @mock.patch("Game.Game.get_times", return_value=[1, 2, 3])
    async def test_correct_pop(self, mock_get_times):
        self.game.popped = False
        self.game.board.push_uci("e2e4")
        self.game.board.push_uci("e7e5")
        self.game.board.fullmove_number = 2

        await self.game.pop(self.sid)
        self.assertTrue(self.game.popped)
        Game.sio.emit.assert_called_once_with("pop", {"time": [1, 2, 3]}, room=self.sid)


if __name__ == "__main__":
    unittest.main()
