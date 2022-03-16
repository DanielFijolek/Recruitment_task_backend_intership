from sqlite3 import Error
from FetchClass import Fetch
from typing import List, Dict
import json
import csv
import sqlite3


class TeamStats:
    def __init__(self, season: int, output: str = "stdout"):
        self.fetch: Fetch = Fetch()
        self.season: int = season
        self.output: str = output
        self.games: List[Dict[str, str]] = []
        self.scores: Dict[str, Dict[str, int]] = {}
        self.list_of_scores: List[Dict[str, str]] = []

    def get_players(self):
        self.games = self.fetch.get_games(self.season)

    def calculate_scores(self):
        for game in self.games:

            home_team: str = game['home_team']['full_name']
            if game['home_team_score']:
                home_team_score: int = int(game['home_team_score'])
            else:
                continue

            visitor_team: str = game['visitor_team']['full_name']
            if game['home_team_score']:
                visitor_team_score: int = int(game['visitor_team_score'])
            else:
                continue

            if home_team_score > visitor_team_score:

                if home_team not in self.scores:
                    self.scores[home_team] = {
                        'w_as_home_town': 1,
                        'w_as_visitor': 0,
                        'l_as_home_town': 0,
                        'l_as_visitor': 0,
                    }
                else:
                    self.scores[home_team]['w_as_home_town'] = self.scores[home_team]['w_as_home_town'] + 1

                if visitor_team not in self.scores:
                    self.scores[visitor_team] = {
                        'w_as_home_town': 0,
                        'w_as_visitor': 0,
                        'l_as_home_town': 0,
                        'l_as_visitor': 1,
                    }
                else:
                    self.scores[visitor_team]['l_as_visitor'] = \
                        self.scores[visitor_team]['l_as_visitor'] + 1

                if home_team_score < visitor_team_score:

                    if home_team not in self.scores:
                        self.scores[home_team] = {
                            'w_as_home_town': 0,
                            'w_as_visitor': 0,
                            'l_as_home_town': 1,
                            'l_as_visitor': 0,
                        }
                    else:
                        self.scores[home_team]['l_as_home_town'] = \
                            self.scores[home_team]['l_as_home_town'] + 1

                    if visitor_team not in self.scores:
                        self.scores[visitor_team] = {
                            'w_as_home_town': 0,
                            'w_as_visitor': 1,
                            'l_as_home_town': 0,
                            'l_as_visitor': 0,
                        }
                    else:
                        self.scores[visitor_team]['w_as_visitor'] = \
                            self.scores[visitor_team]['w_as_visitor'] + 1

    def create_list_of_scores(self):
        for team in self.scores:
            self.list_of_scores.append({
                "team_name": team,
                "won_games_as_home_team": self.scores[team]['w_as_home_town'],
                "won_games_as_visitor_team": self.scores[team]['w_as_visitor'],
                "lost_games_as_home_team": self.scores[team]['l_as_home_town'],
                "lost_games_as_visitor_team": self.scores[team]['l_as_visitor']
            })

    def print_stdout(self):
        for team in self.scores:
            print(team)
            print(f"   won games as home team: {self.scores[team]['w_as_home_town']}")
            print(f"   won games as visitor team: {self.scores[team]['w_as_visitor']}")
            print(f"   lost games as home team: {self.scores[team]['l_as_home_town']}")
            print(f"   lost games as visitor team: {self.scores[team]['l_as_visitor']}")

    def save_json(self):
        self.create_list_of_scores()
        try:
            with open("data_file.json", "w") as write_file:
                json.dump(self.list_of_scores, write_file)
        except IOError:
            print("I/O error")

    def save_csv(self):
        self.create_list_of_scores()
        csv_columns: List[str] = ["team_name",
                                  "won_games_as_home_team",
                                  "won_games_as_visitor_team",
                                  "lost_games_as_home_team",
                                  "lost_games_as_visitor_team"]

        try:
            with open("data_file.csv", 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in self.list_of_scores:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

    def create_sqlite(self):
        conn = None
        try:
            conn = sqlite3.connect("./data_file.db")
            return conn

        except Error as e:
            print(e)

        return conn

    def create_table(self, conn):

        sql_create_teams_stats_table = """ CREATE TABLE IF NOT EXISTS teams_stats (
                                            team_name text PRIMARY KEY,
                                            won_games_as_home_team text,
                                            won_games_as_visitor_team text,
                                            lost_games_as_home_team text,
                                            lost_games_as_visitor_team text
                                        ); """
        try:
            c = conn.cursor()
            c.execute(sql_create_teams_stats_table)

        except Error as e:
            print(e)

    def insert_to_sqlite(self, conn):

        insert = ''' INSERT INTO teams_stats(team_name,won_games_as_home_team,won_games_as_visitor_team,
                  lost_games_as_home_team,lost_games_as_visitor_team)
                  VALUES(?,?,?,?,?) '''
        c = conn.cursor()

        for data in self.list_of_scores:
            c.execute(insert, (data["team_name"], data["won_games_as_home_team"], data["won_games_as_visitor_team"],
                               data["lost_games_as_home_team"], data["lost_games_as_visitor_team"]))
        conn.commit()

    def save_sqlite(self):
        self.create_list_of_scores()
        conn = self.create_sqlite()
        self.create_table(conn)
        self.insert_to_sqlite(conn)

    def get_stats(self):
        self.get_players()
        self.calculate_scores()
        if self.output == "stdout":
            self.print_stdout()

        if self.output == "json":
            self.save_json()

        if self.output == "csv":
            self.save_csv()

        if self.output == "sqlite":
            self.save_sqlite()
