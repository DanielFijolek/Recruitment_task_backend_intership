from GroupedTeams import GroupTeams
from PlayersStats import PlayerStats
from TeamsStats import TeamStats
import argparse
from typing import Dict


def main():
    ap = argparse.ArgumentParser(description='List task and arguments')
    ap.add_argument('Task', metavar="task", help='Task for program',
                    type=str)
    ap.add_argument('-n', '--name', help='Name of player (Required if using grouped-teams)',
                    metavar='Player_name', type=str, required=False)
    ap.add_argument('--season', help='Season year (Required if using teams-stats))',
                    metavar='Player_name', type=int, required=False)
    ap.add_argument('--output', help='Name of player (Used for teams-stats)',
                    metavar='Player_name', type=str, required=False)

    args: Dict[str, str] = vars(ap.parse_args())

    task: str = args["Task"]
    player: str = args["name"]
    if args["season"]:
        try:
            season: int = int(args["season"])
        except TypeError:
            print("Season must be number")
            return -1

    output: str = args["output"]

    if task == "grouped-teams":
        group_teams = GroupTeams()
        group_teams.start_grouping()

    if task == "players-stats":
        if player:
            player_stat = PlayerStats(player)
            player_stat.get_stats()
        else:
            print("Argument --name required")
            return -1

    if task == "teams-stats":
        if season:
            if output:
                team_stat = TeamStats(season, output)
            else:
                team_stat = TeamStats(season)
            team_stat.get_stats()

        else:
            print("Argument --season required")
            return -1


if __name__ == '__main__':
    main()
