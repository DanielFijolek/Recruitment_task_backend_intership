from FetchClass import Fetch
from typing import List, Dict


class GroupTeams:
    def __init__(self):
        self.fetch: Fetch = Fetch()
        self.teams: List[Dict[str, str]] = []
        self.group: Dict[str, List[str]] = {}

    def get_teams(self):
        self.teams = self.fetch.get_teams()

    def print_group(self):
        for key in self.group:
            print(key)
            for team in self.group[key]:
                print(f"      {team}")

    def creat_group(self):
        for team in self.teams:
            if team['division'] in self.group:
                list_of_teams: List[str] = self.group[team['division']]
                list_of_teams.append(f"{team['full_name']} ({team['abbreviation']})")
                self.group[team['division']] = list_of_teams
            else:
                self.group[team['division']] = [f"{team['full_name']} ({team['abbreviation']})"]

    def start_grouping(self):
        self.get_teams()
        self.creat_group()
        self.print_group()
