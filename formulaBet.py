import json
import os


def formulaOneBet(year, round, userBets):
    response = os.popen("curl http://ergast.com/api/f1/{0}/{1}/driverStandings.json".format(year,round)).read()
    response_in_dict = json.loads((response))
    
    bets_won = {}
    user_bets = {}
    user_profits = {}
    overall_wager = 0

    for index,user_bet_list in enumerate(userBets):
        bets_won[index] = []
        user_bets[index] = 0
        for bet in user_bet_list:
            driver,position,wager = bet
            wager = int(wager)
            position = int(position)

            if response_in_dict['MRData']["StandingsTable"]["StandingsLists"][0]["DriverStandings"][position]["Driver"]["driverId"] == driver:
                #User won the bet
                bets_won[index].append(wager)
            
            user_bets[index] += wager
            overall_wager = overall_wager + wager

        if len(bets_won[index]) == 0:
            bets_won.pop(index)

    ##Calculate the sum of all the won bets
    overall_won_money = 0
    for list_of_won_bets in bets_won.values():
        overall_won_money = overall_won_money + sum(list_of_won_bets)
    
    coefficent = overall_wager / overall_won_money
    
    for user_id in bets_won:
        user_profits[user_id] = sum(map(lambda n : n * coefficent,bets_won[user_id])) - sum(bets_won[user_id])

    return max(user_profits.values())
        


print(formulaOneBet(2008,5,[[["massa","2","200"],["webber","7","100"],["alonso","1","100"]], 
 [["massa","1","200"]]]))