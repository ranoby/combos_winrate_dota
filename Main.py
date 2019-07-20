import requests
import time

# Api ulrs
api_teams = 'https://api.opendota.com/api/teams'
api_matches = 'https://api.opendota.com/api/teams/{}/matches'
api_heroes = 'https://api.opendota.com/api/heroes'
api_match_info = 'https://api.opendota.com/api/matches/{}'
# Some variables for future using
team_id = None

ts = time.time()

period_of_time = 0

DAY_seconds = 86400
WEEK_seconds = 604800
MONTH_seconds = 2628000
THREE_MONTHS_seconds = 7884000

# Lists for JSON data
teamsJSON_Data = []
teamMatchesJSON_Data = []
heroesJSON_Data = []

# Lists of data for user
team_names = []
teamMatchesIDs = []
allMatchesIDs = []
heroesIDs = []

def check(side, matchInfoJSON, userHeroes):

    if side == True:
        team_side = 0
    else:
        team_side = 1

    try:
        pick = [matchInfoJSON['picks_bans'][i]['hero_id'] \
                for i in range(0, 22) if matchInfoJSON['picks_bans'][i]['team'] == team_side\
                                        and matchInfoJSON['picks_bans'][i]['is_pick'] == True]
        check_items = all(item in pick for item in userHeroes)
    except:
        pass

    return check_items


def matchInfo(matchesIDes, userHeroes):
    matchesInfo = []

    for k in range(0, len(matchesIDes)):
        # cycle if we have several teams thats mean more than 1 list of matches IDs

        wins = 0
        total = 0

        team_id = matchesIDes[k][0]
        for i in matchesIDes[k][1:]:
            print(i)

            matchInfoJSON = requests.get(api_match_info.format(str(i))).json()

            # Who win radiant or dire?
            try:
                whoWin = matchInfoJSON['radiant_win']
            except:
                continue

            # Where is my team, my team win?, does my team have a combo pick?
            if team_id == matchInfoJSON['radiant_team_id']:
                my_team_side = True
            else:
                my_team_side = False

            # For radiant
            if check(my_team_side, matchInfoJSON, userHeroes):
                # Heroes I'm searching for in pick?
                total += 1

                if whoWin == my_team_side:
                    wins += 1

        matchesInfo.append([total, wins])

    return matchesInfo



# function for list of team names
def teamNames():
    # Request for teams list
    teamsJSON_Data = requests.get(api_teams).json()

    # Create a list of team names for user
    team_names = [teamsJSON_Data[i]['name'] for i in range(0, len(teamsJSON_Data))]

    team_number = int(input("How many team names from top do you want to get? "))

    return team_names[:team_number]

# function for list of matches for one team or teams for period
def matches():
    while(True):
        # User should choice a team by typing its name
        user_team_choice = input("Please enter the team name: ")
        team_id = 0
        teamsJSON_Data = requests.get(api_teams).json()
        # Request for matches of the team that user have chosen
        for i in range(0, len(teamsJSON_Data)):
            if user_team_choice == teamsJSON_Data[i]['name']:
                team_id = teamsJSON_Data[i]['team_id']
                if len(str(team_id)) > 0:
                    break

        # Data about matches
        teamMatchesJSON_Data = requests.get(api_matches.format(team_id)).json()

        # User should choose the period in which he interested
        user_period_choice = int(input("Please enter the number of the period day(1)/week(2)/month(3)/3months(4)/all(0): "))

        # Calculate time
        if user_period_choice == 1:
            period_of_time = ts - DAY_seconds
        elif user_period_choice == 2:
            period_of_time = ts - WEEK_seconds
        elif user_period_choice == 3:
            period_of_time = ts - MONTH_seconds
        elif user_period_choice == 4:
            period_of_time = ts - THREE_MONTHS_seconds
        elif user_period_choice == 0:
            period_of_time = 0

        # List of matches IDs for period
        teamMatchesIDs = [teamMatchesJSON_Data[i]['match_id'] \
                          for i in range(0, len(teamMatchesJSON_Data)) if teamMatchesJSON_Data[i]['start_time'] > period_of_time]

        teamMatchesIDs = [team_id] + teamMatchesIDs

        allMatchesIDs.append(teamMatchesIDs)

        user_answer = input("One more team (n/y)?   ")
        if user_answer == 'n':
            return allMatchesIDs

# function for list of heroes {'name': id}
def heroes():

    heroesJSON_Data = requests.get(api_heroes).json()

    heroesIDs = [{heroesJSON_Data[i]['id'], heroesJSON_Data[i]['localized_name']} for i in range(0, len(heroesJSON_Data))]

    return  heroesIDs


