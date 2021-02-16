"""Black Jack"""
#Automated One Player Game
#Based almost identically off of instructions from: https://bicyclecards.com/how-to-play/blackjack/ 

#House Clarifications:
#1. We do not allow insurance while splitting pairs.
#2. Insurance bet is placed after you complete your hand.

import random
from random import shuffle
import sys

card_list = {'2':['2',2],'3':['3',3],'4':['4',4],'5':['5',5],'6':['6',6],'7':['7',7],'8':['8',8],'9':['9',9],'10':['10',10],'Jack':['Jack',10],'Queen':['Queen',10],'King':['King',10],'Ace':['Ace',1]}

class Deck:
    def __init__(self): 
        self.cards = []
        for i in range(6): #decks
            for i in range(4): #suits
                for i in card_list.values(): #cards
                    self.cards.append(i)
        shuffle(self.cards)
    
    def hit(self, who):
        who.card.append(self.cards.pop())
    def hit_split_pairs(self, who):
        who.second_card.append(self.cards.pop())

class Dealer:
    def __init__(self):
        self.card = []

class Player:
    def __init__(self, name):
        self.name = name
        self.card = []
        self.money = 1000
        self.bet = 0
        self.insurance = False
        self.insurance_bet = 0
        self.double_down = False
        self.doubling_down_hand = []
        self.splitting_pairs_bool = False
        self.splitting_pairs_counter = 0
        self.second_card = []
        self.storage_card = []
        self.reshuffle = False
           
class Game:
    def __init__(self):
        player = input('Enter Your Name: ')
        self.quit_anytime(player)
        self.player = Player(player.title())
        self.deck = Deck()
        self.dealer = Dealer()
        self.skip_over = False

    def quit_anytime(self, response):
        quit_list = ['q','Q']
        if response in quit_list:
            sys.exit()
        else:
            return
    def response_handler(self, response, possible_values, int_tag = False):
        if int_tag == True:
            while True:
                try:
                    response_checker = int(input(response))
                    self.quit_anytime(response_checker)
                    break
                except ValueError:
                    print("*Error: Please enter a valid number...")
        else:
            response_checker = input(response)
            self.quit_anytime(response_checker)
            #quit_anytime(response_checker)
        
        x = False
        if int_tag == True:
            x = True
        
        def response_handler_2(checker, possible_values):
            assert(checker in possible_values), "Enter a Valid Response!"
        while True:
            try:
                response_handler_2(response_checker, possible_values)
                break
            except AssertionError:
                return self.response_handler("*Error: Please enter a valid response: \n", possible_values, int_tag = x)
        return response_checker
    
    def two_card_player_totals(self):
        player_total_low = self.player.card[0][1] + self.player.card[1][1]
        player_total_high = False
        for i in self.player.card:
            for x in i:
                if x == 'Ace':
                    player_total_high = (player_total_low + 10)
        if player_total_high:
            if player_total_high > 21:
                player_total_high = False
        return player_total_low, player_total_high
    def two_card_dealer_totals(self):
        dealer_total_low = self.dealer.card[0][1] + self.dealer.card[1][1]
        dealer_total_high = False
        for i in self.dealer.card:
            for x in i:
                if x == 'Ace':
                    dealer_total_high = (dealer_total_low + 10)
        if dealer_total_high:
            if dealer_total_high > 21:
                dealer_total_high = False
        return dealer_total_low, dealer_total_high

    def deal_cards(self):
        for i in range(2):
            self.player.card.append(self.deck.cards.pop())
        for i in range(2):
            self.dealer.card.append(self.deck.cards.pop())
    def clear_table(self):
        if self.player.splitting_pairs_counter == 0:
            self.player.card.clear()
            self.dealer.card.clear()
            self.player.bet = 0
            self.player.insurance = False
            self.player.insurance_bet = 0
            self.player.double_down = False
            self.player.doubling_down_hand.clear()
            self.skip_over = False
            self.player.reshuffle = False
        elif self.player.splitting_pairs_counter == 1:
            self.player.double_down = False
            self.skip_over = False
            self.player.reshuffle = False
        else:
            self.player.card.clear()
            self.dealer.card.clear()
            self.player.bet = 0
            self.player.double_down = False
            self.player.doubling_down_hand.clear()
            self.player.splitting_pairs_bool = False
            self.player.splitting_pairs_counter = 0
            self.player.second_card.clear()
            self.player.storage_card.clear()
            self.skip_over = False
            self.player.reshuffle = False

    def insurance(self):
        self.player.insurance = True
        print("Insurance will be handled when you complete your hand...\n")
        return
    def splitting_pairs(self):
        double_aces = False
        if self.player.card[0][1] == 'Ace' and self.player.card[1][1] == 'Ace':
            print(f"Your first hand is {self.player.card[0][1]}, {self.player.card[1][1]}")
            print("You have drawn two aces, each hand gets is hit only once...")
            double_aces = True
        """First Hand"""
        self.splitting_pairs_bool = True
        self.player.second_card.append(self.player.card.pop())
        self.deck.hit(self.player)
        self.deck.hit_split_pairs(self.player)
        self.player.splitting_pairs_counter += 1
        player_total_low, player_total_high = self.two_card_player_totals()
        print(f"\nYour first hand is {self.player.card[0][1]}, {self.player.card[1][1]}")
        if player_total_high:
            print(f"Your low total: {player_total_low}\n|\nYour high total: {player_total_high}\n")
        else:
            print(f"Your total: {player_total_low}\n")
        skipper = False
        if player_total_high in range(9,11) or player_total_low in range(9,11):
            response = self.response_handler("Would you like to double down? Enter Y or N", "yYnN",int_tag = False)
            if response in "yY":
                print("Doubling down will commense after you complete your second hand")
                self.player.doubling_down_hand.append("Hand 1")
                skipper = True
        if double_aces == False:
            if skipper == False:
                self.normal_round_mod_s()
        self.clear_table()
        print("\nFinished first hand, moving on...")
        """Second Hand"""
        print("___________\nBeginning second hand\n")
        self.player.storage_card = self.player.card
        self.player.card = self.player.second_card
        player_total_low, player_total_high = self.two_card_player_totals()
        print(f"Your second hand is: {self.player.card[0][1]}, {self.player.card[1][1]}\n")
        if player_total_high:
            print(f"Your low total: {player_total_low}\n|\nYour high total: {player_total_high}\n")
        else:
            print(f"Your total: {player_total_low}\n")
        if player_total_high in range(9,11) or player_total_low in range(9,11):
            response = self.response_handler("\nWould you like to double down? Enter Y or N", "yYnN",int_tag = False)
            skipper = False
            if response in "yY":
                print("Doubling down will commense after you complete your second hand")
                self.player.doubling_down_hand.append("Hand 2")
                skipper = True
        if double_aces == False:
            if skipper == False:
                self.normal_round_mod_s()
        print("Finished second hand, moving on...")
        print("Now completing first hand")
        self.player.splitting_pairs_counter += 1
        self.player.storage_card = self.player.card
        #got your card transfers mixed up
        if "Hand 1" in self.player.doubling_down_hand:
            self.doubling_down()
        self.normal_round_complete()
        self.complete_hand()
        print("Now completing Second Hand")
        self.skip_over = False
        self.player.card = self.player.second_card
        if "Hand 2" in self.player.doubling_down_hand:
            self.doubling_down()
        self.complete_hand()
        self.clear_table()
        self.skip_over = True
        return
    def doubling_down(self):
        if self.dealer.card[1][0] == "Ace":
            print("*Insurance Available...")
            response = self.response_handler("Would you like to purchase insurance? Enter Y or N\n", "yYnN",int_tag = False)
            if response in "yY":
                self.insurance()
        self.player.double_down = True
        print("|\nYour bet has been doubled, and final card dealed\n")
        self.player.money = self.player.money - self.player.bet
        self.player.bet = self.player.bet * 2
        self.deck.hit(self.player)
        inputz = input("Press enter to reveal your hand\n")
        self.quit_anytime(inputz)
        print(f"Your hand is now: {self.player.card[0][0]}, {self.player.card[1][0]}, {self.player.card[2][0]}\n")
        player_card_count_int = [i[1] for i in self.player.card]
        if sum(player_card_count_int) > 21:
            print("You bust... ")
            self.skip_over = True
            return
            reveal = input("Press enter to turn in chips...\n")
            self.quit_anytime(reveal)
        if self.player.insurance == True:
            y = range(0,((self.player.money/2)+1))
            x = int(self.player.money/2)
            responz = self.response_handler(f"Enter an insurance amount between $0-{x}: ", y, int_tag = True)
            self.quit_anytime(responz)
            self.player.insurance_bet = responz
        
        reveal = input("Press enter to reveal dealer hand:\n")
        self.quit_anytime(reveal)
        dealer_card_count_str = [i[0] for i in self.dealer.card]
        dealer_card_count_int = [i[1] for i in self.dealer.card]
        print(f"Dealer Cards: {', '.join(map(str, dealer_card_count_str))}")
        if self.player.insurance == True:
            if self.dealer.card[1][0] == 10:
                y = range(0,((self.player.money/2)+1))
                x = int(self.player.money/2)
                responz = self.response_handler(f"Enter an insurance amount between $0-{x}: ", y, int_tag = True)
                print("Insurance payed out...")
                print(f"Current Balance: {self.player.money}")
            else:
                print("Insurance lost...")
                self.player.money = self.player.money - self.player.insurance_bet
        dealer_total_high = False
        for i in self.dealer.card:
            for x in i:
                if x == 'Ace':
                    dealer_total_high = (sum(dealer_card_count_int) + 10)
        if dealer_total_high:
            if dealer_total_high > 21:
                dealer_total_high = False
        if dealer_total_high:
            print(f"Dealer low total: {sum(dealer_card_count_int)}\n|\nDealer high total: {dealer_total_high}\n")
        else:
            print(f"Dealer total: {sum(dealer_card_count_int)}\n")
        self.complete_hand()
        self.skip_over = True
       
    def welcome(self):
        #random_num = random.randint(60,76)
        self.deck.cards = self.deck.cards #[random_num:]
        print(f"Welcome to Black Jack {self.player.name}!\nPlease refer to the rules on bicyclecards.com.")
        print("Press the enter key after command keys to complete chosen command...")
        print("Press 'Q' any time to quit.\n ")
        self.play_game()
    
    def response_checker_card_start(self):
            assert(len(self.deck.cards) > 19), "Deck has run out of cards. bet returned, and deck shuffled..."

    def play_game(self):
        try:
            print("________________________________________")
            print(f"Your current balance is: ${self.player.money}")
            reveal = input("Press enter to start round: ")
            self.quit_anytime(reveal)
            if self.player.money >= 500:
                bet_range = range(2, 501)
                enter_bet = "\nPlease enter a bet between $2-500: "
            else:
                bet_range = range(2,(self.player.money+1))
                enter_bet = f"\nPlease enter a bet between $2-{(self.player.money)}: "
            response_checker = self.response_handler(enter_bet,bet_range, int_tag = True)
            self.quit_anytime(response_checker)
            self.player.bet = response_checker
            self.player.money = (self.player.money - self.player.bet)
            self.response_checker_card_start()
            self.deal_cards()
            print(f"\nAvailable Funds: {self.player.money}\n")
            #change dealer card back to hidden
            print(f"Dealer Cards: {'Hidden'}, {self.dealer.card[1][0]}")
            print(f"Your Cards: {self.player.card[0][0]}, {self.player.card[1][0]}\n|")
            self.initial_plays_possible()
            if self.skip_over == True:
                if self.player.money <= 0:
                    print("You have run out of money, have a good night...")
                    sys.exit()
                else:
                    self.clear_table()
                    self.play_game()
            self.check_special_plays()
            if self.skip_over == True:
                if self.player.money <= 0:
                    print("You have run out of money, have a good night...")
                    sys.exit()
                else:
                    self.clear_table()
                    self.play_game()
            self.normal_round()
            if self.skip_over == True:
                if self.player.money <= 0:
                    print("You have run out of money, have a good night...")
                    sys.exit()
                else:
                    self.clear_table()
                    self.play_game()
            self.complete_hand()
            self.clear_table()
            if self.player.money <= 0:
                print("You have run out of money, have a good night...")
                sys.exit()
            else:
                self.clear_table()
                self.play_game()
        except AssertionError:
            print("Deck has run out of cards. Bet returned, and deck re_shuffled...")
            self.player.splitting_pairs_counter = 0
            self.money = self.player.money + self.player.bet
            self.clear_table()
            self.deck
            self.welcome()
    def initial_plays_possible(self): 
        dealer_total_low, dealer_total_high = self.two_card_dealer_totals()
        player_total_low, player_total_high = self.two_card_player_totals()

        if player_total_high:
            print(f"Your low total: {player_total_low}\n|\nYour high total: {player_total_high}\n")
        else:
            print(f"Your total: {player_total_low}\n")
        #potential initial play instances begin here
       
        if player_total_high == 21 or player_total_low == 21:
            if dealer_total_high == 21 or dealer_total_low == 21:
                print("You got a natural!")
                reveal = input("Press enter to reveal dealer cards...\n")
                self.quit_anytime(reveal)
                print(f"Dealer cards: {self.dealer.card[0][0]}, {self.dealer.card[1][0]}\n")
                print("Player and dealer drew naturals. This round is a draw.")
                self.player.money = self.player.money + self.player.bet
                print("(Your bet has been returned)\n")
                print(f"Your balance is now {self.player.money}\n")
                responz = input("press enter for new round...")
                self.quit_anytime(responz)
                self.skip_over = True
                return
            #player natural
            else:
                print("You got a natural")
                reveal = input("Press enter to reveal dealer cards...\n")
                self.quit_anytime(reveal)
                print(f"Dealer cards: {self.dealer.card[0][0]}, {self.dealer.card[1][0]}\n")
                if self.player.splitting_pairs_counter > 0:
                    print("You have been given your bet...\n")
                    self.player.money = self.player.money + int((self.player.bet * 2))
                    responz = input("Press enter for new round...")
                    self.quit_anytime(responz)
                    self.skip_over = True
                    return
                else:
                    print("You have been given half your bet for a natural hand...\n")
                    self.player.money = self.player.money + int((self.player.bet * 1.5))
                    responz = input("Press enter for new round...")
                    self.quit_anytime(responz)
                    self.skip_over = True
                    return
    def check_special_plays(self):
        player_total_low, player_total_high = self.two_card_player_totals()
        #splitting pairs or doubling down option
        if self.player.card[0][0] == self.player.card[1][0]:
            if player_total_high in range(9,11) or player_total_low in range(9,11):
                print("Splitting pairs and doubling down available")
                response = self.response_handler("Would you like to use one of these special plays?", "yYnN", int_tag = False)
                if response in 'yY':
                    response = self.response_handler("Enter 'D' for doubling down or 'S' for splitting pairs", "dDsS", int_tag = False)
                    if response in "dD":
                        self.doubling_down()
                    else:
                        self.splitting_pairs()
            else:
                response = self.response_handler("Would you like to split pairs? Enter Y or N", "yYnN", int_tag = False)
                if response  in "yY":
                    self.splitting_pairs()
        #doubling down
        elif player_total_high in range(9,11) or player_total_low in range(9,11):
            response = self.response_handler("Would you like to double down? Enter Y or N", "yYnN",int_tag = False)
            if response in "yY":
                self.doubling_down()
        
        elif self.dealer.card[1][0] == "Ace":
            print("*Insurance Available...")
            response = self.response_handler("Would you like to purchase insurance? Enter Y or N", "yYnN",int_tag = False)
            if response in "yY":
                self.insurance()
        else:
            return    

    def normal_round_mod_s(self):
        response = self.response_handler("Press 'H' to hit\nPress 'C' to complete your hand: ", "cChH\n", int_tag = False)
        if response in "hH":
            self.normal_round_hit()
            self.normal_round_mod_s()
        if self.skip_over == True:
            if self.player.money <= 0:
                print("You have run out of money, have a good night...")
                sys.exit()
            else:
                return
        if response in "cC":
            return
    def normal_round_hit(self):
        self.deck.hit(self.player)
        player_card_count_str = [i[0] for i in self.player.card]
        player_card_count_int = [i[1] for i in self.player.card]
        x = ', '.join(map(str, player_card_count_str))
        print(f"\nYour Cards: {', '.join(map(str, player_card_count_str))}")
        player_total_high = False
        for i in self.player.card:
            for x in i:
                if x == 'Ace':
                    player_total_high = (sum(player_card_count_int) + 10)
        if player_total_high:
            if player_total_high > 21:
                player_total_high = False
        if player_total_high:
            print(f"Your low total: {sum(player_card_count_int)}\n|\nYour high total: {player_total_high}\n__________")
        else:
            print(f"Your total: {sum(player_card_count_int)}\n__________")
        if sum(player_card_count_int) > 21:
            print("You bust... ")
            reveal = input("Press enter to turn in chips...\n")
            self.quit_anytime(reveal)
            if self.player.splitting_pairs_bool == True:
                return 
            self.skip_over = True
            return
        else:
            if self.player.splitting_pairs_counter == 0:
                self.normal_round()
            else:
                return
    def normal_round_complete(self):
        print("\nHand Completed")
        if self.player.insurance == True:
            y = range(0,((self.player.money/2)+1))
            x = int(self.player.money/2)
            responz = self.response_handler(f"Enter an insurance amount between $0-{x}: ", y, int_tag = True)
            self.quit_anytime(responz)
            self.player.insurance_bet = responz
        reveal = input("Press enter to reveal dealer hand:\n__________")
        self.quit_anytime(reveal)
        dealer_card_count_str = [i[0] for i in self.dealer.card]
        dealer_card_count_int = [i[1] for i in self.dealer.card]
        print(f"Dealer Cards: {', '.join(map(str, dealer_card_count_str))}")
        if self.player.insurance == True:
            if self.dealer.card[1][0] == 10:
                self.player.money = self.player.money + (int(self.player.insurance_bet * 2))
                print("Insurance payed out...")
                print(f"Current Balance: {self.player.money}")
            else:
                print("Insurance lost...")
                self.player.money = self.player.money - self.player.insurance_bet
        dealer_total_high = False
        for i in self.dealer.card:
            for x in i:
                if x == 'Ace':
                    dealer_total_high = (sum(dealer_card_count_int) + 10)
        if dealer_total_high:
            if dealer_total_high > 21:
                dealer_total_high = False
        if dealer_total_high:
            print(f"Dealer low total: {sum(dealer_card_count_int)}\n|\nDealer high total: {dealer_total_high}\n")
        else:
            print(f"Dealer total: {sum(dealer_card_count_int)}\n")
        return
    def normal_round(self):
        response = self.response_handler("Press 'H' to hit\nPress 'C' to complete your hand: ", "cChH\n", int_tag = False)
        if response in "hH":
            self.normal_round_hit()
        if self.skip_over == True:
            if self.player.money <= 0:
                print("You have run out of money, have a good night...")
                sys.exit()
            else:
                return
        if response in "cC":
            self.normal_round_complete()
        if self.skip_over == True:
            if self.player.money <= 0:
                print("You have run out of money, have a good night...")
                sys.exit()
            else:
                return
            
    def complete_hand(self):
        if self.skip_over == True:
            if self.player.money <= 0:
                print("You have run out of money, have a good night...")
                sys.exit()
        #re-create player, dealer / high, low, variables to auto update
        temp_dealer_total_low = [i[1] for i in self.dealer.card]
        dealer_total_low = sum(temp_dealer_total_low)            
        
        dealer_total_high = False
        dealer_total_high = any("Ace" in list for list in self.dealer.card)  
        if dealer_total_high:
            dealer_total_high = dealer_total_low + 10
            if dealer_total_high > 21:
                dealer_total_high = False
                
        #auto updating player card total per hand
        temp_player_total_low = [i[1] for i in self.player.card]
        player_total_low = sum(temp_player_total_low)
        
        player_total_high = False
        player_total_high = any("Ace" in list for list in self.player.card)
        if player_total_high:
            player_total_high = player_total_low + 10
            if player_total_high > 21:
                player_total_high = False
        
        #if dealer busts, new round
        if dealer_total_low > 21:
            print("Dealer busts hand...\nYour bet is payed!")
            self.player.money = self.player.money + (self.player.bet * 2)
            if self.player.splitting_pairs_counter == 1:
                return
            reveal = input("Press enter for a new round...\n-----\n")
            self.quit_anytime(reveal)
            return
        if dealer_total_high:
            if dealer_total_high in range(17,22):
                if player_total_high:
                    if dealer_total_high > player_total_high:
                        print("Dealer wins this hand.\n")
                        reveal = input("Press enter to turn in chips...")
                        self.quit_anytime(reveal)
                        if reveal != '':
                            print("Well we will just take them anyway, or..... we can break your jaw for you?...\n")
                        if self.player.splitting_pairs_counter == 1:
                            return
                        new_hand = input("Press enter for a new round...\n-----\n")
                        self.quit_anytime(new_hand)
                        return
                    elif dealer_total_high < player_total_high:
                        print("Player wins hand!\n")
                        self.player.money = self.player.money + (self.player.bet*2) 
                        if self.player.splitting_pairs_counter == 1:
                            return 
                        reveal = input("Press enter for a new round...\n-----\n")
                        self.quit_anytime(reveal)
                        return
                    else:
                        print("Player and dealer tie... No bets payed\n")
                        self.player.money = self.player.money + self.player.bet
                        if self.player.splitting_pairs_counter == 1:
                            return
                        reveal = input("Press enter for a new round...\n-----\n")
                        self.quit_anytime(reveal)
                        return
                elif dealer_total_high > player_total_low:
                    print("Dealer wins this hand.\n")
                    reveal = input("Press enter to turn in chips...")
                    self.quit_anytime(reveal)
                    if reveal != '':
                        print("Well we will just take them anyway, or..... we can break your jaw for you?...\n")
                    if self.player.splitting_pairs_counter == 1:
                        return
                    new_hand = input("Press enter for a new round...\n-----\n")
                    self.quit_anytime(new_hand)
                    return
                elif dealer_total_high < player_total_low:
                    print("Player wins hand!\n")
                    self.player.money = self.player.money + (self.player.bet*2) 
                    if self.player.splitting_pairs_counter == 1:
                        return 
                    reveal = input("Press enter for a new round...\n-----\n")
                    self.quit_anytime(reveal)
                    return
                else:
                    print("Player and dealer tie... No bets payed\n")
                    self.player.money = self.player.money + self.player.bet
                    if self.player.splitting_pairs_counter == 1:
                        return
                    reveal = input("Press enter for a new round...\n-----\n")
                    self.quit_anytime(reveal)
                    return
            else:
                self.deck.hit(self.dealer)
                print("Dealer delt new card...\n")
                dealer_card_count_str = [i[0] for i in self.dealer.card]
                dealer_card_count_int = [i[1] for i in self.dealer.card]
                print(f"Dealers Hand: {', '.join(map(str, dealer_card_count_str))}")
                dealer_total_high = False
                for i in self.dealer.card:
                    for x in i:
                        if x == 'Ace':
                            dealer_total_high = (sum(dealer_card_count_int) + 10)
                if dealer_total_high:
                    if dealer_total_high > 21:
                        dealer_total_high = False
                if dealer_total_high:
                    print(f"Dealer low total: {sum(dealer_card_count_int)}\n|\nDealer high total: {dealer_total_high}\n")
                else:
                    print(f"Dealer total: {sum(dealer_card_count_int)}\n")
                reveal = input("Press enter to continue...\n")
                self.quit_anytime(reveal)
                self.complete_hand()
        elif dealer_total_low in range(17,22):
            if player_total_high:
                if dealer_total_low > player_total_high:
                    print("Dealer wins this hand!\n")
                    if self.player.splitting_pairs_counter == 1:
                        return
                    reveal = input("Press enter for a new round...\n-----\n")
                    self.quit_anytime(reveal)
                    return
                elif dealer_total_low < player_total_high:
                    print("You won this hand!\n")
                    self.player.money = self.player.money + (self.player.bet * 2)
                    if self.player.splitting_pairs_counter == 1:
                        return
                    reveal = input("Press enter for a new round...\n-----\n")
                    self.quit_anytime(reveal)
                    return
                else:
                    print("Player and dealer tie... No bets payed\n")
                    self.player.money = self.player.money + self.player.bet
                    if self.player.splitting_pairs_counter == 1:
                        return
                    reveal = input("Press enter for a new round...\n-----\n")
                    self.quit_anytime(reveal)
                    return
            elif dealer_total_low > player_total_low:
                print("Dealer wins this hand!\n")
                if self.player.splitting_pairs_counter == 1:
                    return
                reveal = input("Press enter for a new round...\n-----\n")
                self.quit_anytime(reveal)
                return
            elif dealer_total_low < player_total_low:
                print("You won this hand!\n")
                self.player.money = self.player.money + (self.player.bet * 2)
                if self.player.splitting_pairs_counter == 1:
                    return
                reveal = input("Press enter for a new round...\n-----\n")
                self.quit_anytime(reveal)
                return
            else:
                print("Player and dealer tie... No bets payed\n")
                self.player.money = self.player.money + self.player.bet
                if self.player.splitting_pairs_counter == 1:
                    return
                reveal = input("Press enter for a new round...\n-----\n")
                self.quit_anytime(reveal)
                return
        else:
            self.deck.hit(self.dealer)
            print("Dealer delt new card...\n")
            dealer_card_count_str = [i[0] for i in self.dealer.card]
            dealer_card_count_int = [i[1] for i in self.dealer.card]
            print(f"Dealers Hand: {', '.join(map(str, dealer_card_count_str))}")
            dealer_total_high = False
            for i in self.dealer.card:
                for x in i:
                    if x == 'Ace':
                        dealer_total_high = (sum(dealer_card_count_int) + 10)
            if dealer_total_high:
                if dealer_total_high > 21:
                    dealer_total_high = False
            if dealer_total_high:
                print(f"Dealer low total: {sum(dealer_card_count_int)}\n|\nDealer high total: {dealer_total_high}\n")
            else:
                print(f"Dealer total: {sum(dealer_card_count_int)}\n")
            reveal = input("Press enter to continue...\n")
            self.quit_anytime(reveal)
            self.complete_hand()
             
game = Game()
game.welcome()










        


        

