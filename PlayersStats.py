from FetchClass import Fetch
from typing import List, Dict


class PlayerStats:
    def __init__(self, player: str):
        self.fetch: Fetch = Fetch()
        self.player: str = player
        self.players: List[Dict[str, str]] = []
        self.tallest: Dict[str, str] = {}
        self.heaviest: Dict[str, str] = {}

    def get_players(self):
        self.players = self.fetch.get_player()

    def sort_players_by_name(self):
        temp_list: List[Dict[str, str]] = []
        for player in self.players:
            if (player['first_name'] == self.player) | (player['last_name'] == self.player):
                temp_list.append(player)
        self.players = temp_list

    def set_stats(self):
        for player in self.players:
            if player['height_feet']:
                if not self.tallest:
                    self.tallest = player
                if self.tallest['height_feet'] < player['height_feet']:
                    self.tallest = player
            if player['weight_pounds']:
                if not self.heaviest:
                    self.heaviest = player
                if self.heaviest['weight_pounds'] < player['weight_pounds']:
                    self.heaviest = player

    def print_stats(self):
        if self.tallest:
            print(f"The tallest player: {self.tallest['first_name']} "
                  f"{self.tallest['last_name']} {self.tallest['height_feet']} Feet")
        else:
            print(f"The tallest player: Not found ")

        if self.heaviest:
            print(f"The heaviest player: {self.tallest['first_name']} "
                  f"{self.tallest['last_name']} {self.tallest['weight_pounds']} Pounds ")
        else:
            print(f"The heaviest player: Not found ")

    def get_stats(self):
        self.get_players()
        self.sort_players_by_name()
        self.set_stats()
        self.print_stats()
