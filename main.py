# import packages
import collections
import random

# set global variables
settings = {}                   # dictionary that will hold the game settings
human_players = {}              # dictionary that will contain a list of all human players and their stats
computer_players = {}           # dictionary that will contain a list of all the computer players and their stats
continue_playing = True         # Determines whether a new Farkle game should be started


# pre-game setup
def pre_game_setup():

    # select settings for the game
    def select_game_settings():
        game_settings = {"computer_players": 0, "game_type": 0, "win_condition": 0, "human_players": 0}

        # set number of human players
        def number_of_human_players():
            players = 0
            x = 0
            while x == 0:
                try:
                    players = int(input("Enter number of human players (1-3): "))
                except ValueError:
                    print("Please select a number from 1 to 3.")
                    continue
                if 1 <= players <= 3:
                    break
                else:
                    print("Please select a number from 1 to 3.")
                    continue
            return players

        # select number of computer players
        def number_of_computer_players():
            number_of_computers = 0
            x = 0
            while x == 0:
                try:
                    number_of_computers = int(
                        input("Enter number of AI computer_players you would like to face (0-5): "))
                except ValueError:
                    print("Please select a number from 0 to 5.")
                    continue
                if 0 <= number_of_computers <= 5:
                    break
                else:
                    print("Please select a number from 0 to 5.")
                    continue
            return number_of_computers

        # select whether to play a score-based or turn-based game
        def select_game_type():
            print("   -----   ")
            print("Please select the type of Farkle game you wish to play.")
            print("Turns: Game will last a set number of turns for each player. \
Player with highest score at the end wins")
            print("Score: Game will continue until one of the players reaches a set score.")

            game = 0
            x = 0
            while x == 0:
                choice = input("Please select either turns or score: ")
                if choice == "turns":
                    game = 1
                    break
                if choice == "score":
                    game = 2
                    break
                else:
                    print("Invalid selection. Please enter turns or score.")
                    continue
            return game

        # set the win condition for the type of game that was selected
        def select_win_condition(game_type):
            x = 0
            if game_type == 1:
                while x == 0:
                    try:
                        turns = int(input("Enter number of turns for the game (5-10): "))
                    except ValueError:
                        print("Please select a number from 5 to 10.")
                        continue

                    if 5 <= turns <= 10:
                        return turns
                    else:
                        print("Please select a number from 5 to 10.")
                        continue
            if game_type == 2:
                while x == 0:
                    try:
                        winning_score = int(input("Enter the score required to win the game (1000-2000): "))
                    except ValueError:
                        print("Please select a number from 1000 to 2000.")
                        continue

                    if 1000 <= winning_score <= 2000:
                        return winning_score
                    else:
                        print("Please select a number from 1000 to 2000.")
                        continue

        # perform game setup and return results
        game_settings["human_players"] = number_of_human_players()
        game_settings["computer_players"] = number_of_computer_players()
        game_settings["game_type"] = select_game_type()
        game_settings["win_condition"] = select_win_condition(game_settings["game_type"])
        return game_settings

    # print beginning of game message
    print("Welcome to the game of Farkle. Before the game begins you must select some settings.")

    # create global variables
    global settings
    settings = select_game_settings()

    global human_players
    human_players = create_human_players(settings["human_players"])

    if settings["computer_players"] > 0:
        global computer_players
        computer_players = create_computer_players(settings["computer_players"])


# create list of computer players
def create_computer_players(number_of_computer_players):
    class AiOpponent:
        def __init__(self, name, number, total_score, round_score):
            self.name = name
            self.number = number
            self.total_score = total_score
            self.round_score = round_score

    opponent_list = {}
    for x in range(number_of_computer_players):
        computer_number = x + 1
        number_str = str(computer_number)
        computer_name = "Computer Player " + number_str
        opponent_list[x] = AiOpponent(computer_name, computer_number, 0, 0)
    return opponent_list


# create list of human players
def create_human_players(number_of_players):
    class HumanPlayers:
        def __init__(self, name, total_score, round_score):
            self.name = name
            self.total_score = total_score
            self.round_score = round_score

    player_dict = {}
    choice_list = ["first", "second", "third", "fourth", "fifth", "sixth"]
    for y in range(number_of_players):
        x = 0
        while x == 0:
            player_name = input("Enter " + choice_list[y] + " player name: ")
            if len(player_name) <= 20:
                player_dict[y] = HumanPlayers(player_name, 0, 0)
                break
            else:
                print("Error: User name cannot exceed 20 characters!")
                continue
    return player_dict


# roll a provided number of dice; return result as list
def roll_dice(number_of_dice, player_name):
    dice_list = []
    for x in range(number_of_dice):
        roll_result = random.randint(1, 6)
        dice_list.append(roll_result)
    dice_list = sorted(dice_list)
    print(player_name, "rolled", number_of_dice, "dice with the following result:", dice_list)
    return dice_list


# allow user to select which dice they want to keep; return dice list
def human_dice_selection(available_dice):

    # have user enter the amount of dice they want to keep; return number of dice
    def dice_number(starting_dice):
        starting_dice = len(starting_dice)
        number_of_dice = 0
        x = 0
        while x == 0:
            try:
                number_of_dice = int(input("Enter a number of dice you are going to keep : "))
            except ValueError:
                print("Please select a number less than or equal to", starting_dice, ": ")
                continue
            if 0 < number_of_dice <= starting_dice:
                break
            else:
                print("Please select a number less than or equal to", starting_dice, ": ")
                continue
        return number_of_dice

    # have user identify the values of the dice they are keeping; return list of dice values
    def create_dice_list(number_of_dice):
        kept_dice = []
        choice_list = ["first", "second", "third", "fourth", "fifth", "sixth"]
        for z in range(number_of_dice):
            x = 0
            while x == 0:
                try:
                    die = int(input("Enter the value of the " + choice_list[z] + " die you are keeping: "))
                    if 0 < die < 7:
                        kept_dice.append(die)
                        break
                    else:
                        print("Please select a number from 1 to 6.")
                        continue
                except ValueError:
                    print("Error: Please try again and enter a number.")
        return kept_dice

    # confirm that user has entered a valid selection of dice; return True or False
    def validate_dice_list(kept_dice):
        # initial variables
        valid_selection = 0      # this number will be set to 6 if the dice the user selected are valid choices
        error_code_1 = 0         # reports error if incorrect number of dice with values of 1 or 5 were chosen
        error_code_2 = 0         # reports error if incorrect number of dice with values of 2, 3, 4, or, 6 were chosen
        list_one = [1, 5]
        list_two = [2, 3, 4, 6]

        # create dictionaries to compare dice lists
        kept_dice_dict = collections.Counter(kept_dice)
        available_dice_dict = collections.Counter(available_dice)

        # check for six in a row
        if sorted(kept_dice) == [1, 2, 3, 4, 5, 6]:
            valid_selection = 6
        else:
            # confirm that user selected a valid number of dice with the values of one and five
            for x in range(len(list_one)):
                if kept_dice_dict[list_one[x]] > 0:
                    if kept_dice_dict[list_one[x]] <= available_dice_dict[list_one[x]]:
                        valid_selection += 1
                    else:
                        error_code_1 = error_code_1 + list_one[x]
                        continue
                else:
                    valid_selection += 1

            # confirm the user selected a valid number of dice with the values of two, three, four, and six
            for x in range(len(list_two)):
                if 0 < kept_dice_dict[list_two[x]] < 3 or 3 < kept_dice_dict[list_two[x]] < 6:
                    valid_selection -= 1
                    error_code_2 = 1
                elif kept_dice_dict[list_two[x]] == 3:
                    if available_dice_dict[list_two[x]] >= 3:
                        valid_selection += 1
                    else:
                        valid_selection -= 1
                elif kept_dice_dict[list_two[x]] == 6:
                    if available_dice_dict[list_two[x]] == 6:
                        valid_selection += 1
                    else:
                        valid_selection -= 1
                else:
                    valid_selection += 1

        # determine if dice selection was correct. Display error codes if user selections were invalid.
        if valid_selection == 6:
            return True
        else:
            print("Invalid dice selection.")
            if error_code_1 == 1:
                print("Error: You selected too many dice with the value of one.")
            elif error_code_1 == 5:
                print("Error: You selected too many dice with the value of five.")
            elif error_code_1 == 6:
                print("Error: You selected too many dice with the values of one and five.")
            elif error_code_2 == 1:
                print(
                    "Error: Dice with a value of two, three, four, and six can only be selected in quantities of three and six.")
            print("   -----   ")
            return False

    # print list of available dice
    def print_available_dice(available_dice_list):
        print("The available dice are:", available_dice_list)

    # loop through process of selecting dice until user has confirmed a valid selection
    y = 0
    dice = []
    while y == 0:
        number_to_keep = dice_number(available_dice)
        dice = create_dice_list(number_to_keep)
        result = validate_dice_list(dice)
        if not result:
            print_available_dice(available_dice)
            continue
        if result:
            break
    return dice


# calculate the score of a dice roll; return score
def calculate_score(dice_list):
    # set initial score value
    score = 0

    # check for six in a row
    dice_list = sorted(dice_list)
    if dice_list == [1, 2, 3, 4, 5, 6]:
        score = score + 1500
    else:
        dice_count = collections.Counter(dice_list)

        # check for three or six ones
        if 3 <= dice_count[1] < 6:
            score = score + 1000
            dice_count[1] = dice_count[1] - 3
        elif dice_count[1] == 6:
            score = score + 2000
            dice_count[1] = dice_count[1] - 6

        # check for additional three of a kinds
        x = 2
        while x < 7:
            if 3 <= dice_count[x] < 6:
                score = score + 100 * x
                dice_count[x] = dice_count[x] - 3
            elif dice_count[x] == 6:
                score = score + 200 * x
                dice_count[x] = dice_count[x] - 6
            x = x + 1

        # calculate score of remaining ones and fives
        score = score + dice_count[5] * 50
        score = score + dice_count[1] * 100
    return score


# select dice computer player will keep; return list of dice
def computer_dice_selection(dice_list):
    # set initial list of dice to be kept
    ai_dice_list = []

    # check for six in a row
    dice_list = sorted(dice_list)
    if dice_list == [1, 2, 3, 4, 5, 6]:
        ai_dice_list = [1, 2, 3, 4, 5, 6]
    else:
        dice_count = collections.Counter(dice_list)

        # check for three or six ones
        if 3 <= dice_count[1] < 6:
            for x in range(3):
                ai_dice_list.append(1)
            dice_count[1] = dice_count[1] - 3
        elif dice_count[1] == 6:
            for x in range(6):
                ai_dice_list.append(1)
            dice_count[1] = dice_count[1] - 6

        # check for additional three of a kinds
        x = 2
        while x < 7:
            if 3 <= dice_count[x] < 6:
                for y in range(3):
                    ai_dice_list.append(x)
                dice_count[x] = dice_count[x] - 3
            elif dice_count[x] == 6:
                for y in range(6):
                    ai_dice_list.append(x)
                dice_count[x] = dice_count[x] - 6
            x = x + 1

        # check for remaining ones and fives
        for x in range(dice_count[5]):
            ai_dice_list.append(5)
        for x in range(dice_count[1]):
            ai_dice_list.append(1)

        # remove unneeded fives (optimal strategy for Farkle)
        ai_dice_list_collection = collections.Counter(ai_dice_list)
        if len(dice_list) - len(ai_dice_list) > 1:
            if ai_dice_list_collection[1] > 0:
                if 0 < ai_dice_list_collection[5] < 3:
                    for y in range(ai_dice_list_collection[5]):
                        ai_dice_list.remove(5)
            if ai_dice_list_collection[5] == 2:
                try:
                    ai_dice_list.remove(5)
                except ValueError:
                    pass
    return ai_dice_list


# user decides if they want to end their turn.
def human_keep_going(turn_score, total_score, number_of_dice):
    print("   -----   ")
    print("Score for the turn:", turn_score)
    potential_game_score = turn_score + total_score
    print("Score for the game if you stop:", potential_game_score)
    print("Number of dice available for the next roll:", number_of_dice)
    x = 0
    while x == 0:
        choice = input("Would you like to roll again? (y/n): ")
        if choice == "y":
            print("   ---   ")
            return True
        elif choice == "n":
            print("   ---   ")
            return False
        else:
            print('Invalid response. Please enter either "y" or "n".')
            continue


# determines whether ai player will roll again.
# provides score for computer player to stop at, but also a chance that the computer will keep going anyway
def computer_keep_going(turn_score, number_of_dice, computer_number):
    random_number = random.randint(1, 25)

    if number_of_dice >= 5:
        return True
    elif number_of_dice == 4:
        if turn_score < 1050:
            return True
        else:
            return False
    elif number_of_dice == 3:
        if turn_score < 450:
            return True
        else:
            if (computer_number + 2) >= random_number:
                return True
            else:
                return False
    elif number_of_dice == 2:
        if turn_score < 250:
            return True
        else:
            if (computer_number + 1) >= random_number:
                return True
            else:
                return False
    elif number_of_dice == 1:
        if turn_score < 300:
            return True
        else:
            if computer_number >= random_number:
                return True
            else:
                return False


# run a single turn of Farkle for a human player
def single_human_turn(local_game_score, local_turn_number, player_name):
    # re-set variables for the turn
    continue_turn = True
    numberOfDice = 6
    turn_score = 0

    # provide stats prior to start of turn
    print("   -----   ")
    print(player_name, "is beginning turn", local_turn_number)
    print(player_name, "has a score of", local_game_score, "for the game.")

    # begin new turn
    while continue_turn:
        # perform dice roll and calculate score
        dice_list = roll_dice(numberOfDice, player_name)
        initial_score = calculate_score(dice_list)
        print_max_score(initial_score)
        if initial_score == 0:
            print("Roll of ", dice_list, " resulted in 0 points. Turn is over.")
            turn_score = 0
            break

        # if score is greater than 0, select which dice to keep, calculate remaining dice
        new_dice_list = human_dice_selection(dice_list)
        new_score = calculate_score(new_dice_list)
        turn_score = turn_score + new_score
        numberOfDice = numberOfDice - len(new_dice_list)
        if numberOfDice == 0:
            numberOfDice = 6

        # decide whether to keep rolling or to end the turn
        result = human_keep_going(turn_score, local_game_score, numberOfDice)
        if not result:
            print("Your score for the turn was: ", turn_score)
            break
        if result:
            continue
    return turn_score


# run a turn for a computer player
def single_computer_turn(computer_number, computer_name):
    # re-set variables for the turn
    continue_turn = True
    numberOfDice = 6
    turn_score = 0

    while continue_turn:
        # perform dice roll and calculate score
        dice_list = roll_dice(numberOfDice, computer_name)
        initial_score = calculate_score(dice_list)
        print("The roll has a score of", initial_score)
        if initial_score == 0:
            print("Roll of ", dice_list, " resulted in 0 points. Turn is over.")
            turn_score = 0
            break

        # if score is greater than 0, select which dice to keep, calculate remaining dice
        new_dice_list = computer_dice_selection(dice_list)
        new_score = calculate_score(new_dice_list)
        print(computer_name, "kept these dice:", new_dice_list)
        turn_score = turn_score + new_score
        numberOfDice = numberOfDice - len(new_dice_list)
        if numberOfDice == 0:
            numberOfDice = 6

        # decide whether to keep rolling or to end the turn
        result = computer_keep_going(turn_score, numberOfDice, computer_number)
        if not result:
            print(computer_name, "scored", turn_score, "points for the turn.")
            break
        if result:
            continue
    return turn_score


# print scores
def print_scores(score, name):
    print(name, ":", score)


# print the highest potential score for the dice roll
def print_max_score(max_roll_score):
    print("The roll has a maximum score of", max_roll_score)


# determine winner
def determine_winner(local_computer_players, local_settings, local_human_players):
    winning_ai_score = 0
    winning_ai = 0
    winning_human = "x"
    winning_human_score = 0

    # compare ai scores to each other to determine which one has the highest score
    for x in range(local_settings["computer_players"]):
        win_count = 0
        for y in range(local_settings["computer_players"]):
            if local_computer_players[x].total_score >= local_computer_players[y].total_score:
                win_count += 1
                if win_count == (local_settings["computer_players"]):
                    winning_ai = local_computer_players[x].name
                    winning_ai_score = local_computer_players[x].total_score
                    break
                else:
                    continue
            else:
                break

    # compare human scores to each other to determine which one has the highest score
    if local_settings["human_players"] > 0:
        for x in range(local_settings["human_players"]):
            win_count = 0
            for y in range(local_settings["human_players"]):
                if local_human_players[x].total_score >= local_human_players[y].total_score:
                    win_count += 1
                    if win_count == (local_settings["human_players"]):
                        winning_human = local_human_players[x].name
                        winning_human_score = local_human_players[x].total_score
                        break
                    else:
                        continue
                else:
                    break

    print("   -----   ")
    if settings["win_condition"] == 2:
        print("Game Over: The score of", settings["win_condition"], "has been reached!")
    else:
        print("The final round has concluded.")
    print("The final scores are: ")
    # print opponent scores, if applicable
    if local_settings["computer_players"] > 0:
        for x in range(local_settings["computer_players"]):
            print_scores(local_computer_players[x].total_score, local_computer_players[x].name)
    # print human scores
    for x in range(local_settings["human_players"]):
        print_scores(human_players[x].total_score, human_players[x].name)
    print("   -----   ")
    print("   -----   ")

    # compare highest ai score to user score to determine winner of the game
    if winning_ai_score > winning_human_score:
        print(winning_ai, "has won the game.")
    else:
        print("Congratulations!", winning_human, "has won the game!")

    x = 0
    while x == 0:
        choice = input("Would you like to play again? (y/n): ")
        if choice == "y":
            print("   ---   ")
            global continue_playing
            continue_playing = True
            break
        elif choice == "n":
            print("   ---   ")
            continue_playing = False
            break
        else:
            print('Invalid response. Please enter either "y" or "n".')
            continue


# run game
def farkle_game():
    continue_current_game = True        # determine whether current game should be continue to the next round
    turn_number = 0
    while continue_current_game:
        # set turn number
        turn_number += 1

        # begin turn for computer players
        if settings["computer_players"] > 0:
            for b in range(settings["computer_players"]):
                print("   -----   ")
                computer_players[b].total_score = computer_players[b].total_score + single_computer_turn(computer_players[b].number, computer_players[b].name)

        # print current scores
        if settings["computer_players"] > 0:
            print("   -----   ")
            print("Current scores during turn", turn_number)
            for b in range(settings["computer_players"]):
                print_scores(computer_players[b].total_score, computer_players[b].name)
        for b in range(settings["human_players"]):
            print_scores(human_players[b].total_score, human_players[b].name)

        # print scores and begin turns for human players
        for b in range(settings["human_players"]):

            # print current scores
            if settings["computer_players"] > 0:
                print("   -----   ")
                print("Current scores during turn", turn_number)
                for c in range(settings["computer_players"]):
                    print_scores(computer_players[c].total_score, computer_players[c].name)
            for d in range(settings["human_players"]):
                print_scores(human_players[d].total_score, human_players[d].name)

            # begin turn for human player
            print("   -----   ")
            human_players[b].total_score = human_players[b].total_score + single_human_turn(human_players[b].total_score, turn_number, human_players[b].name)

        # check for win condition if turn-based game
        if settings["game_type"] == 1 and turn_number == settings["win_condition"]:
            determine_winner(computer_players, settings, human_players)
            continue_current_game = False

        # check for win condition if score-based game
        if settings["game_type"] == 2:

            # determine if one of the computer players reached a winning score
            if settings["computer_players"] > 0:
                for b in range(settings["computer_players"]):
                    if computer_players[b].total_score >= settings["win_condition"]:
                        determine_winner(computer_players, settings, human_players)
                        continue_current_game = False
                        break
                    else:
                        continue
            # determine if one of the human players has reached a winning score
            for b in range(settings["human_players"]):
                if human_players[b].total_score >= settings["win_condition"]:
                    determine_winner(computer_players, settings, human_players)
                    continue_current_game = False
                    break
                else:
                    continue


# initialize the game
def main():
    while continue_playing:
        pre_game_setup()
        farkle_game()


main()
