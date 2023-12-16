/*
 * api specs, e.g. paths, methods, codes, data fields (req/res)
 */

export const API = {
	login : {
		endpoint : "backend/login/",
		method : "POST",
		codes : {
			"ok" : 200,
			"unauthorized" : 401
		},
		data : [
			"username",
			"password"
		],
		response : [
			"message",
			"token"
		]
	},
	signout : {
		endpoint: "backend/signout/",
		method: "POST",
		codes : {
			"ok" : 200
		}
	},
	signup : {
		endpoint : "backend/signup/",
		method : "POST",
		codes : {
			"ok" : 200,
			"bad request" : 400,
			"internal server error" : 500
		},
		data : [
			"username",
			"password",
			"eloReallyBadChess",
		],
		response : [
			"message"
		]
	},
	addGuest : {
		endpoint: "backend/add_guest/",
		method: "POST",
	},
	dailyLeaderboard: {
		endpoint: "backend/get_daily_leaderboard",
		method: "GET",
		codes: {
			"ok": 200,
			"internal server error": 500,
			"invalid request": 405
		}
	},
	weeklyLeaderboard: {
		endpoint: "backend/get_weekly_leaderboard",
		method: "GET",
		codes: {
			"ok": 200,
			"internal server error": 500,
			"invalid request": 405
		}
	},
	rankedLeaderboard: {
		endpoint: "...",
		method: "...",
		codes: "..."
	},
	checkStartDaily: {
		endpoint: "backend/check_start_daily",
		method: "GET",
		codes: {
			"ok": 200,
			"maximum reached": 400,
			"internal server error": 500,
			"invalid request": 405
		}
	},
	multiplayerLeaderboard: {
		endpoint: "backend/get_multiplayer_leaderboard",
		method: "GET",
		codes: {
			"ok": 200,
			"internal server error": 500,
			"invalid request": 405
		}
	}
};