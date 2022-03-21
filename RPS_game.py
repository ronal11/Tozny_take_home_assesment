import e3db
from e3db.types import Search
import sys



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


api_url = "https://api.e3db.com"
# credentials for Alicia
client_name = 'Alicia'
clientID = "c319cd6f-ac62-4092-adf7-5b5c3a588385"
apiKeyID = "4ea62ead2b09f57032db940f4109d7d3f4c1f964476201d0e781b517d4c5925f"
apiSecret = "8d6b12046d7bbaf17194f4302da096a874da9d1a15444b473cc26e88dd004b7c"
publicKey = "0Btda54-NibL9OIuqQ8U5GtIZJsYZQF5QHMke_z4028"
privateKey = "yg091RB1ay6bV9ZrjpK9Qg-NatlyM2V8B3qIr_vyAFY"

config = e3db.Config(
    clientID,
    apiKeyID,
    apiSecret,
    publicKey,
    privateKey,
    api_url
)
client = e3db.Client(config())    # config for Alicia

# credentials for Clarence
client_name2 = 'Clarence'
clientID2 = "d8cf355f-b54d-4e33-ba07-984280f5690e"
apiKeyID2 = "a10813f22b9bcbade3ad9e9611e18ce115d681eccc21e8bf5c10bc93ba3931a9"
apiSecret2 = "846837bd7fa6840726402dcef18a81bc37a790f0179da6f11aca9995bd283ece"
publicKey2 = "i8_dqpiOLiYU4UutdtnCzbnwigt7p8vJQR-sCOeuy1Y"
privateKey2 = "0qd0xOsmvov_3fO1aLbtr_2_BK97sTzcSJQE8_47dfE"


config2 = e3db.Config(
    clientID2,
    apiKeyID2,
    apiSecret2,
    publicKey2,
    privateKey2,
    api_url
)
client2 = e3db.Client(config2())        # config for Clarence

# Credentials for Bruce
client_name3 = 'Bruce'
clientID3 = "5cd1b4d3-f92c-4a9a-907a-b71557a1adce"
apiKeyID3 = "f9cd8d03a36f6b94926412a4b74354e7faf3d48199c492735a0886c29b796ba7"
apiSecret3 = "8baaed16b14c4448d2673a5096a40ce830a857384e6661464a88395ae612fed7"
publicKey3 = "i8D_gWfdui3mgw3j8blbDPINn7AjdKl4BdSWMfMVkiw"
privateKey3 = "nCFfOATneN0l9OE2gZSTkQZ7lcnQxDyvbWNehoYcG08"

config3 = e3db.Config(
    clientID3,
    apiKeyID3,
    apiSecret3,
    publicKey3,
    privateKey3,
    api_url
)
client3 = e3db.Client(config3())    # config for bruce

# client.share("moves", clientID2) Alice sharing records with Judge
# client3.share("moves", clientID2) Bruce sharing records with Judge
# client2.share("Result", clientID3) Judge sharing records with Bruce
# client2.share("Result", clientID) Judge sharing records with Alice

if sys.argv[1] == 'move' or sys.argv[1] == 'Move':
    name = input('enter the name of the player: ')
    flag = True
    rndcheck = True

    if (name == "Alicia") or (name == "alicia"):
        record_type = 'moves'

        roundNum = input("Enter the round number: ")

        while(rndcheck == True):
            rnd_query = Search(include_data=True, include_all_writers=True). \
                match(condition="AND", strategy="EXACT", values=[roundNum, "Alicia"])

            search = client.search(rnd_query)
            num = rnd_check(search)
            if num == 0:
                rndcheck = False
            else:
                roundNum = input("This round already exists, please enter new round number: ")

        move = input("Whats your move, rock, paper, or scissors?: ")
        while flag == True:
            if move == 'rock' or move == 'scissors' or move == 'paper':
                flag = False
                print("correct input")
            else:
                print("incorrect input(note: lowercase only)")
                move = input("Whats your move, rock, paper, or scissors?: ")

        data = {'Move': move}
        meta_data = {
            'Round': roundNum,
            'Name': client_name
        }
        record = client.write(record_type, data, meta_data)

    elif (name == "Bruce") or (name == "bruce"):
        record_type = 'moves'

        roundNum = input("Enter the round number: ")

        while (rndcheck == True):
            rnd_query = Search(include_data=True, include_all_writers=True). \
                match(condition="AND", strategy="EXACT", values=[roundNum, "Bruce"])

            search = client3.search(rnd_query)
            num = rnd_check(search)


            if num == 0:
                rndcheck = False
            else:
                roundNum = input("This round already exists, please enter new round number: ")

        move = input("Whats your move, rock, paper, or scissors?: ")
        while flag == True:
            if move == 'rock' or move == 'scissors' or move == 'paper':
                flag = False
                print("correct input")
            else:
                print("incorrect input(note: lowercase only)")
                move = input("Whats your move, rock, paper, or scissors?: ")

        data = {'Move': move}
        meta_data = {
            'Round': roundNum,
            'Name': client_name3
        }
        record = client3.write(record_type, data, meta_data)
    else:
        print("Player does not exist")
elif sys.argv[1] == "judge" or sys.argv[1] == "Judge":
    check = True
    round2judge = input("enter number of round you want to judge: ")

    while (check == True):
        rnd_query = Search(include_data=True, include_all_writers=True). \
            match(condition="AND", strategy="EXACT", record_types=["Result"], values=[round2judge])

        search = client2.search(rnd_query)
        num = rnd_check(search)

        if num == 0:
            check = False
        else:
            round2judge = input("This round has been judged, please enter new round number: ")

    bruce_query = Search(include_data=True, include_all_writers=True).\
        match(condition="AND", strategy="EXACT", values=[round2judge, "Bruce"])

    alicia_query = Search(include_data=True, include_all_writers=True). \
        match(condition="AND", strategy="EXACT", values=[round2judge, "Alicia"])

    # judge performs searches for records from Alicia and Bruce for the round chosen
    results1 = client2.search(bruce_query)
    results2 = client2.search(alicia_query)

    num1 = rnd_check(results1)
    num2 = rnd_check(results2)
    if num1 == 0 or num2 == 0:
        print("One or two players have yet to make a move for this round")
        quit()

    b_move = results(results1, 'Move')
    a_move = results(results2, 'Move')

    print("Alicia move: ", a_move)
    print("Bruce move: ", b_move)
    record_type = "Result"

    if b_move == a_move:
        judge_data = {
            "Winner": "Draw"
        }
        meta = {
            "Round": round2judge
        }
        record = client2.write(record_type, judge_data, meta)
        print(record)
    elif (b_move == "rock") and (a_move == "paper"):
        judge_data = {
            "Winner": "Alicia"
        }
        meta = {
            "Round": round2judge
        }
        record = client2.write(record_type, judge_data, meta)
        print(record)
    elif (b_move == "rock") and (a_move == "scissors"):
        judge_data = {
            "Winner": "Bruce"
        }
        meta = {
            "Round": round2judge
        }
        record = client2.write(record_type, judge_data, meta)
        print(record)
    elif (b_move == "paper") and (a_move == "rock"):
        judge_data = {
            "Winner": "Bruce"
        }
        meta = {
            "Round": round2judge
        }
        record = client2.write(record_type, judge_data, meta)
        print(record)
    elif (b_move == "paper") and (a_move == "scissors"):
        judge_data = {
            "Winner": "Alicia"
        }
        meta = {
            "Round": round2judge
        }
        record = client2.write(record_type, judge_data, meta)
        print(record)
    elif (b_move == "scissors") and (a_move == "rock"):
        judge_data = {
            "Winner": "Alicia"
        }
        meta = {
            "Round": round2judge
        }
        record = client2.write(record_type, judge_data, meta)
        print(record)
    elif (b_move == "scissors") and (a_move == "paper"):
        judge_data = {
            "Winner": "Bruce"
        }
        meta = {
            "Round": round2judge
        }
        record = client2.write(record_type, judge_data, meta)
        print(record)
    print("Round Judged: ", round2judge)

elif sys.argv[1] == "result" or sys.argv[1] == "Result":
    resultRound = input('Enter round number to get result of: ')
    name = input("Enter your name (Alicia or Bruce): ")

    if name == "alicia" or name == "Alicia":
        alica_search = Search(include_data=True, include_all_writers=True). \
            match(condition="AND", strategy="EXACT", record_types=["Result"], values=[resultRound])

        rnd_result = client.search(alica_search)

        num1 = rnd_check(rnd_result)
        if num1 == 0:
            print("This round has yet to be judged.")
            quit()

        winner = results(rnd_result, 'Winner')
        print("Alicia read result for round {0}, Winner: {1}".format(resultRound, winner))

    elif name == "bruce" or name == "Bruce":
        bruce_search = Search(include_data=True, include_all_writers=True). \
            match(condition="AND", strategy="EXACT", record_types=["Result"], values=[resultRound])

        rnd_result = client3.search(bruce_search)

        num1 = rnd_check(rnd_result)
        if num1 == 0:
            print("This round has yet to be judged.")
            quit()

        winner = results(rnd_result, 'Winner')
        print("Bruce read result for round {0}, Winner: {1}".format(resultRound, winner))
    else:
        print("Player does not exist")
else:
    print('Only parameters "move" , "result" , or "judge" are available')
