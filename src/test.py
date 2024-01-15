import random

decks = ['heima'] * 10 + ['sanshen'] * 5 + ['singlestrike'] * 2
player_deck = ['singlestrike']
win_rate = {('heima', 'sanshen'): 0.7, ('sanshen', 'singlestrike'):0.4, ('heima','singlestrike'):0.67}
num_rounds = 4


random.shuffle(decks)
decks = player_deck + decks
class SwissRoundSimulatorFinal:
    def __init__(self, decks, win_rate):
        self.win_rate = win_rate
        self.players = [{'deck': deck, 'id': i, 'wins': 0, 'losses': 0, 'tiebreakers': 0, 'opponents': []} for i, deck
                        in enumerate(decks)]
        self.user_id = 0  # 假设用户的ID为0

    def simulate_round(self):
        self.match_opponents()
        self.handle_bye_round()  # 处理奇数玩家情况

    def match_opponents(self):
        self.update_tiebreakers()
        sorted_players = sorted(self.players, key=lambda x: (x['wins'], x['tiebreakers']), reverse=True)
        matched = set()
        for player in sorted_players:
            if player['id'] not in matched:
                for opponent in sorted_players:
                    if opponent['id'] not in matched and opponent['id'] != player['id']:
                        if player['id'] == self.user_id:
                            print(f"Opponent deck: {opponent['deck']}")
                            user_won = self.get_user_result()
                            winner_id = self.user_id if user_won else opponent['id']
                        elif opponent['id'] == self.user_id:
                            print(f"Opponent deck: {player['deck']}")
                            user_won = self.get_user_result()
                            winner_id = self.user_id if user_won else player['id']
                        else:
                            winner_id = self.determine_winner(player['id'], opponent['id'])
                        self.update_records(player, opponent, winner_id)
                        matched.update([player['id'], opponent['id']])
                        break

    def handle_bye_round(self):
        if len(self.players) % 2 != 0:
            lowest_ranked_player = sorted(self.players, key=lambda x: (x['wins'], x['tiebreakers']))[-1]
            lowest_ranked_player['wins'] += 1  # 获得胜利但小分不变

    def get_user_result(self):
        # 模拟用户胜负情况，实际应用中应由用户输入
        while True:
            result = input("input 1 for win, 0 for lose")
            # return random.choice([True, False])
            if result == '1':
                return True
            elif result == '0':
                return False
            else:
                print("please re-enter your input")

    def update_tiebreakers(self):
        for player in self.players:
            player['tiebreakers'] = sum(self.players[opponent]['wins'] for opponent in player['opponents'])

    def determine_winner(self, deck1, deck2):
        if (deck1, deck2) in self.win_rate:
            win_chance = self.win_rate[(deck1, deck2)]
        elif (deck2, deck1) in self.win_rate:
            win_chance = 1 - self.win_rate[(deck2, deck1)]
        else:
            win_chance = 0.5
        return deck1 if random.random() < win_chance else deck2

    def update_records(self, player1, player2, winner_id):
        if winner_id == player1['id']:
            self.players[player1['id']]['wins'] += 1
            self.players[player2['id']]['losses'] += 1
        else:
            self.players[player1['id']]['losses'] += 1
            self.players[player2['id']]['wins'] += 1
        player1['opponents'].append(player2['id'])
        player2['opponents'].append(player1['id'])

    def print_final_rankings(self):
        self.update_tiebreakers()
        sorted_players = sorted(self.players, key=lambda x: (x['wins'], x['tiebreakers']), reverse=True)
        for rank, player in enumerate(sorted_players, start=1):
            print(
                f"名次：{rank}\t ID:{player['id']}\t 卡组：{player['deck']}\t 大分：{player['wins']}"
                f"\t小分：{player['tiebreakers']}\t对手ID：{player['opponents']}")


# 使用更新后的模拟器进行测试
simulator = SwissRoundSimulatorFinal(decks, win_rate)

# 模拟两轮
for _ in range(num_rounds):
    simulator.simulate_round()
    simulator.print_final_rankings()
# 输出最终排名
