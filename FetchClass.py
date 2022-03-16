from requests import get


class Fetch:
    def __init__(self):
        self.url = "https://www.balldontlie.io/api/v1"

    def get_player(self):
        player_promise = get(f"{self.url}/players")
        return player_promise.json()["data"]

    def get_teams(self):
        teams_promise = get(f"{self.url}/teams")
        return teams_promise.json()["data"]

    def get_games(self, season: int):
        games_promise = get(f"{self.url}/games?seasons[]={season}")
        return games_promise.json()["data"]

