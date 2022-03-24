import e3db
from e3db.types import Search
import sys
import os
import json

# check number of records for a given search


def rnd_check(res):
    i = 0
    for rec in res:
        i += 1
    return i

# function assumes there will only be one record for any given round


def results(res, key):
    for rec in res:
        value = rec.data[key]
    return value

# function checks if a round exists when a player is choosing a round to make a move for 


def chk_4_round(client, player, roundnum):
    flag = True

    while flag == True:
        rnd_query = Search(include_data=True, include_all_writers=True). \
            match(condition="AND", strategy="EXACT", values=[roundnum, player])

        search = client.search(rnd_query)
        num = rnd_check(search)
        if num == 0:
            flag = False
        else:
            roundnum = input("This round already exists, please enter new round number: ")
    return roundnum

#  function makes sure player move input is correct


def chk_move(move2chk):
    flag = True

    while flag == True:
        if move2chk == 'rock' or move2chk == 'scissors' or move2chk == 'paper':
            flag = False
        else:
            print("incorrect input(note: lowercase only)")
            move2chk = input("Whats your move, rock, paper, or scissors?: ")
    return move2chk

# function initializes client credentials and makes sure path exists 


def chk_credentials(file_path):
    credentials_path = file_path # your e3db credentialss
    if os.path.exists(credentials_path):
        client = e3db.Client(json.load(open(credentials_path)))
        return client
    else:
        print("Filepath doesn't not exist")
        quit()

# function submits a move for the player for a given round 


def submit_move(client, client_name, move, roundnum):
    record_type = "moves"

    data = {'Move': move}
    meta_data = {
        'Round': roundnum,
        'Name': client_name
    }
    record = client.write(record_type, data, meta_data)
    print("Round {0} Move {1} submitted for {2} ".format(roundnum, move, client_name))

# function checks if a round has been judged, used when judge inputs which round he/she wants to judge


def isRoundJudged(client, roundnum):
    flag = True
    while (flag == True):
        rnd_query = Search(include_data=True, include_all_writers=True). \
            match(condition="AND", strategy="EXACT", record_types=["Result"], values=[roundnum])

        search = client.search(rnd_query)
        num = rnd_check(search)

        if num == 0:
            flag = False
        else:
            roundnum = input("This round has been judged, please enter new round number: ")
    return roundnum

# used by player to see if a round has been judged, when choosing which round to get a result from 


def player_rnd_chk(client, resultRound):
    query = Search(include_data=True, include_all_writers=True). \
        match(condition="AND", strategy="EXACT", record_types=["Result"], values=[resultRound])

    rnd_result = client.search(query)

    num1 = rnd_check(rnd_result)
    if num1 == 0:
        print("This round has yet to be judged.")
        quit()
    return rnd_result

# this function searches for moves based on player name and round number meta-data, used by judge


def search4moves(client, player_name, roundnum):
    query = Search(include_data=True, include_all_writers=True). \
        match(condition="AND", strategy="EXACT", values=[roundnum, player_name])

    # judge performs searches for records from Alicia and Bruce for the round chosen
    result = client.search(query)

    return result

# checks if a move had been made by both players for a given round, used by judge before judging any round


def chk_if_moves_made(player1_results, player2_results):
    num1 = rnd_check(player1_results)
    num2 = rnd_check(player2_results)
    if num1 == 0 or num2 == 0:
        print("One or two players have yet to make a move for this round")
        quit()

# this function judges and submits result according to player moves 


def judge_round(client, player1, player2, move1, move2, roundnum):
    record_type = "Result"

    if move1 == move2:
        judge_data = {
            "Winner": "Draw"
        }
        meta = {
            "Round": roundnum
        }
        record = client.write(record_type, judge_data, meta)

    elif (move1 == "rock") and (move2 == "paper"):
        judge_data = {
            "Winner": player2
        }
        meta = {
            "Round": roundnum
        }
        record = client.write(record_type, judge_data, meta)

    elif (move1 == "rock") and (move2 == "scissors"):
        judge_data = {
            "Winner": player1
        }
        meta = {
            "Round": roundnum
        }
        record = client.write(record_type, judge_data, meta)

    elif (move1 == "paper") and (move2 == "rock"):
        judge_data = {
            "Winner": player1
        }
        meta = {
            "Round": roundnum
        }
        record = client.write(record_type, judge_data, meta)

    elif (move1 == "paper") and (move2 == "scissors"):
        judge_data = {
            "Winner": player2
        }
        meta = {
            "Round": roundnum
        }
        record = client.write(record_type, judge_data, meta)

    elif (move1 == "scissors") and (move2 == "rock"):
        judge_data = {
            "Winner": player2
        }
        meta = {
            "Round": roundnum
        }
        record = client.write(record_type, judge_data, meta)

    elif (move1 == "scissors") and (move2 == "paper"):
        judge_data = {
            "Winner": player1
        }
        meta = {
            "Round": roundnum
        }
        record = client.write(record_type, judge_data, meta)

    print("Round Judged: ", roundnum)

api_url = "https://api.e3db.com"


# client.share("moves", clientID2) Alice sharing records with Judge
# client3.share("moves", clientID2) Bruce sharing records with Judge
#client2.share("Result", clientID3) Judge sharing records with Bruce
#client2.share("Result", clientID) Judge sharing records with Alice

# start of program

if sys.argv[1] == 'move' or sys.argv[1] == 'Move':
    name = input('enter the name of the player: ')

    if (name == "Alicia") or (name == "alicia"):
        client = chk_credentials(sys.argv[2])               # get credentials 
        client_name = "Alicia"

        temp = input("Enter the round number: ")    
        roundNum = chk_4_round(client, client_name, temp)   # get round number 

        temp = input("Whats your move, rock, paper, or scissors?: ")
        move = chk_move(temp)                                # get move 

        submit_move(client, client_name, move, roundNum)     # submit move 

    elif (name == "Bruce") or (name == "bruce"):
        client3 = chk_credentials(sys.argv[2])               # get credentials 
        client_name3 = "Bruce"

        temp = input("Enter the round number: ")
        roundNum = chk_4_round(client3, client_name3, temp)  # get round number

        temp = input("Whats your move, rock, paper, or scissors?: ")
        move = chk_move(temp)                                # get move

        submit_move(client3, client_name3, move, roundNum)   # submit move 
    else:
        print("Player does not exist")
elif sys.argv[1] == "judge" or sys.argv[1] == "Judge":
    client2 = chk_credentials(sys.argv[2])

    temp = input("enter number of round you want to judge: ")
    round2judge = isRoundJudged(client2, temp)              # get round to judge 

    results1 = search4moves(client2, "Bruce", round2judge)  # search for move made by both players 
    results2 = search4moves(client2, "Alicia", round2judge)

    chk_if_moves_made(results1, results2)                   # check if moves have been made by both players 

    b_move = results(results1, 'Move')                      # get moves 
    a_move = results(results2, 'Move')

    print("Alicia move: ", a_move)
    print("Bruce move: ", b_move)

    judge_round(client2, "Bruce", "Alicia", b_move, a_move, round2judge)    # submit judged round 

elif sys.argv[1] == "result" or sys.argv[1] == "Result":        # get credentials 
    client = chk_credentials(sys.argv[2])

    resultRound = input('Enter round number to get result of: ')    # get round number and player name 
    name = input("Enter your name (Alicia or Bruce): ")

    if name == "alicia" or name == "Alicia":
        result = player_rnd_chk(client, resultRound)                # check if round has been judged 

        winner = results(result, 'Winner')                          # get and print winner 
        print("Alicia read result for round {0}, Winner: {1}".format(resultRound, winner))

    elif name == "bruce" or name == "Bruce":
        result = player_rnd_chk(client, resultRound)                # check if round has been judged 

        winner = results(result, 'Winner')                          # get and print winner 
        print("Bruce read result for round {0}, Winner: {1}".format(resultRound, winner))
    else:
        print("Player does not exist")
else:
    print('Only parameters "move" , "result" , or "judge" are available')
