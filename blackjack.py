import tkinter
import random


def load_image(cards_images):
    suits = ['C', 'D', 'H', 'S']
    face_cards = ['J', 'Q', 'K']

    for suit in suits:
        for i in range(1, 11):
            name = 'PNG/{}{}.png'.format(str(i), suit)
            image = tkinter.PhotoImage(file=name).subsample(5)
            cards_images.append((i, image,))
            # print(cards_images)

        for face in face_cards:
            name = 'PNG/{}{}.png'.format(face, suit)
            image = tkinter.PhotoImage(file=name).subsample(5)
            cards_images.append((10, image,))

    print(cards_images)


def deal_action(deal_frame, count):
    action_card = deck.pop(0)
    print(action_card[0], action_card[1])
    tkinter.Label(deal_frame, image=action_card[1]).grid(row=0, column=count, sticky='wn')
    print(locals())
    return action_card


def find_score(find_score_cards):
    k = 0
    ace_exist = False
    for j in find_score_cards:
        if j[0] == 1 and not ace_exist:
            k += 11
            ace_exist = True
        else:
            k += j[0]
        print(k)

    if k > 21 and ace_exist:
        k -= 10

    print(locals())
    return k


def test_results(checker):
    p_score = player_score.get()
    d_score = dealer_score.get()

    is_game_finished = False

    if d_score > 21:
        result_text.set("You Win! Dealer is BUSTED")
        is_game_finished = True
    elif p_score > 21:
        result_text.set("Player is BUSTED!")
        is_game_finished = True
    elif d_score == 21 and d_score == p_score:
        result_text.set("It's a PUSH")
        is_game_finished = True
    elif p_score == 21:
        result_text.set("You Win! you got a blackjack")
        is_game_finished = True
    elif d_score == 21:
        result_text.set("Dealer Wins! Dealer has a blackjack")
        is_game_finished = True
    elif checker == 'dealer' and d_score == p_score:
        result_text.set("It's a PUSH")
        is_game_finished = True
    elif checker == 'dealer' and p_score < d_score:
        result_text.set("Dealer Wins!")
        is_game_finished = True
    elif checker == 'dealer' and p_score > d_score:
        result_text.set("Player Wins!")
        is_game_finished = True

    if is_game_finished:
        game_finished()

    print(locals())


def game_finished():
    dealer_button.configure(state='disabled')
    player_button.configure(state='disabled')
    new_game_button.configure(state='active')


def cmd_player():
    g = deal_action(player_frame, len(player_cards))
    player_cards.append(g)
    p_score1 = find_score(player_cards)
    player_score.set(p_score1)
    test_results('player')


def cmd_dealer():
    p_score2 = player_score.get()
    d_score2 = dealer_score.get()
    while d_score2 < 22:
        h = deal_action(dealer_frame, len(dealer_cards))
        dealer_cards.append(h)
        d_score2 = find_score(dealer_cards)
        dealer_score.set(d_score2)
        if p_score2 < d_score2:
            break
    test_results('Dealer')


def load_game():
    # frame for cards
    global dealer_frame
    global player_frame
    global dealer_cards
    global player_cards
    global deck
    random.shuffle(cards)
    deck = list(cards)
    dealer_cards = []
    player_cards = []
    player_score.set(0)
    dealer_score.set(0)
    dealer_button.configure(state='active')
    player_button.configure(state='active')
    new_game_button.configure(state='disabled')
    dealer_frame = tkinter.Frame(card_frame, bg='green')
    dealer_frame.grid(row=0, column=1, columnspan=3, rowspan=2)
    player_frame = tkinter.Frame(card_frame, bg='brown')
    player_frame.grid(row=2, column=1, columnspan=3, rowspan=2)

    # base play
    dealer_cards.append(deal_action(dealer_frame, len(dealer_cards)))
    dealer_score.set(find_score(dealer_cards))
    cmd_player()
    cmd_player()
    result_text.set("Game in Progress")
    test_results('auto')


def cmd_new_game():
    dealer_frame.destroy()
    player_frame.destroy()
    load_game()


my_window = tkinter.Tk()
my_window.title("BlackJack")
my_window.geometry("640x480")
my_window.configure(bg='green')

result_text = tkinter.StringVar()
my_label1 = tkinter.Label(my_window, textvar=result_text, borderwidth=1, relief='raised', bg='cyan')
my_label1.grid(row=0, column=0, columnspan=3, sticky='ew')
card_frame = tkinter.Frame(my_window, bg='blue', relief='sunken')
card_frame.grid(row=1, column=0, columnspan=4)
button_frame = tkinter.Frame(my_window, bg='Yellow')
button_frame.grid(row=2, column=0)

# dealer label and dealer score label
dealer_label = tkinter.Label(card_frame, text='Dealer', bg='pink')
dealer_label.grid(row=0, column=0)
dealer_score = tkinter.IntVar()
dealer_score_label = tkinter.Label(card_frame, text="Dealer Score", textvariable=dealer_score)
dealer_score_label.grid(row=1, column=0)

# player label and player score label
player_label = tkinter.Label(card_frame, text='Player', bg='purple')
player_label.grid(row=2, column=0)
player_score = tkinter.IntVar()
player_score_label = tkinter.Label(card_frame, text="Player Score ", textvariable=player_score)
player_score_label.grid(row=3, column=0)

# frame for cards
dealer_frame = tkinter.Frame(card_frame, bg='green')
dealer_frame.grid(row=0, column=1, columnspan=3, rowspan=2)
player_frame = tkinter.Frame(card_frame, bg='brown')
player_frame.grid(row=2, column=1, columnspan=3, rowspan=2)

# setup buttons
dealer_button = tkinter.Button(button_frame, text="Dealer", command=cmd_dealer)
dealer_button.grid(row=0, column=0)
player_button = tkinter.Button(button_frame, text="Player", command=cmd_player)
player_button.grid(row=0, column=1)
new_game_button = tkinter.Button(button_frame, text="New Game", command=cmd_new_game)
new_game_button.grid(row=0, column=2)
new_game_button.configure(state='disabled')

cards = []
load_image(cards)
random.shuffle(cards)
deck = list(cards)

dealer_cards = []
player_cards = []

load_game()

my_window.mainloop()
