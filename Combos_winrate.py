# Created by Ranoby
# Date 7/19/19

# This script use open dota api and give information about heroes combination winrate
# for period that user chose ( from pro matches )
import Main

def comboWinrate(matchesIDes, userHeroes):
    matchesInfo = Main.matchInfo(matchesIDes, userHeroes)
    for i in range(0, len(matchesInfo)):
        if matchesInfo[i][0] > 0:
            winrate = matchesInfo[i][1]/matchesInfo[i][0]
            print ("total {} winrate {:2.2%}".format(matchesInfo[i][0], winrate))

    return 0


matchesIDes = []
userHeroes = []
# Welcome and codes for actions
welcome = '#' * 5 + " Hi, I'm dota combos winrate programm " + '#' * 5
code_team_names = " 0 - for list of team names "
code_matches_period = " 1 - for matches for period "
code_heroes = " 2 - for list of heroes ids "
code_heroes_choose = " 3 - to choose heroes "

number_of_symbols = len(welcome)

print(number_of_symbols * '#')
print(welcome)
print('#' * ((number_of_symbols - len(code_team_names))//2) + code_team_names + '#' * ((number_of_symbols - len(code_team_names))//2))
print('#' * ((number_of_symbols - len(code_matches_period))//2) + code_matches_period+ '#' * ((number_of_symbols - len(code_matches_period))//2))
print('#' * ((number_of_symbols - len(code_heroes))//2) + code_heroes + '#' * ((number_of_symbols - len(code_heroes))//2))
print('#' * ((number_of_symbols - len(code_heroes_choose))//2) + code_heroes_choose+ '#' * ((number_of_symbols - len(code_heroes_choose))//2))
#    team_names = Main.teamNames()
#    MatchesIDs = Main.matches()

while True:
    user_choice = input("Your choice: ")
    if( user_choice == '0'):
        print(' || '.join(Main.teamNames()))

    elif( user_choice == '1'):
        matchesIDes = Main.matches()
        print(matchesIDes)

    elif( user_choice == '2'):
    # print ides and hero names from list of dictionaries
    # where (idk why) elements is mixed
        for k,v in Main.heroes():
            try:
                int(k)
            except:
                a = k
                k = v
                v = a

            print(f'{k:3d}: {v:15}')

    elif( user_choice == '3'):
        userHeroes = [int(i) for i in input("Your heroes ").rsplit()]
        comboWinrate(matchesIDes, userHeroes)

    user_answer = input("Do you want to continue? (y/n): ")

    if user_answer == 'n':
        break


