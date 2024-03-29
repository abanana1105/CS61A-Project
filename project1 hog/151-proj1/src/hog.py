"""The Game of Hog"""

from dice import six_sided, four_sided, make_test_dice

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(current_score, num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. Besides that, for each dice
    whose outcome has same parity with player's current score, add 1 extra point.

    current_score:  The total score of the current player.
    num_rolls:      The number of dice rolls that will be made.
    dice:           A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that current_score and num_rolls is valid.
    assert type(current_score) == int, 'current_score must be an integer.'
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    flag = 0
    count = 0
    count2 = 0
    for i in range(num_rolls):
        a=dice()
        count+=a
        if a==1 :
            flag =1
        if a%2==current_score%2 :
            count2 += 1
    if flag == 1 :
        count =1
    count +=count2
    return count
    # END PROBLEM 1

def picky_piggy(score):
    """Return the points scored from rolling 0 dice.

    score:  The opponent's current score.
    """
    # BEGIN PROBLEM 2 047619
    if score == 0 :
        return 1
    def cycle(a) :
        if a==0:
            return 9
        if a==1:
            return 0
        if a==2:
            return 4
        if a==3:
            return 7
        if a==4:
            return 6
        if a==5:
            return 1
    return cycle(score%6)
    # END PROBLEM 2

def take_turn(num_rolls, current_score, opponent_score, dice=six_sided, goal=GOAL_SCORE):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 in the case
    of a player using Picky Piggy.
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    current_score:   The total score of the current player.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    goal:            The goal score of the game.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert current_score < goal, 'The game should be over.'
    assert opponent_score < goal, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls== 0 :
        return picky_piggy(opponent_score)
    else :
        return roll_dice(current_score, num_rolls,dice)
    # END PROBLEM 3

def swine_swap(player_score, opponent_score):
    """Return whether the players' scores will be swapped due to Swine Swap.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.
    """
    # BEGIN PROBLEM 4
    swine =str(pow(3,player_score+opponent_score))
    if swine[0]==swine[-1] :
        return True
    else :
        return False   
    # END PROBLEM 4

def next_player(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> next_player(0)
    1
    >>> next_player(1)
    0
    """
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5 take_turn(num_rolls, current_score, opponent_score, dice=six_sided, goal=GOAL_SCORE)
    # END PROBLEM 5
    # (note that the indentation for the problem 6 prompt (***YOUR CODE HERE***) might be misleading)
    # BEGIN PROBLEM 6
    while score0<goal and score1<goal :
        if who == 0 :
            score0 += take_turn(strategy0(score0,score1),score0,score1,dice,goal)
        else :
            score1 += take_turn(strategy1(score1,score0),score1,score0,dice,goal)
        if swine_swap(score0,score1) :
            score0,score1 = score1,score0
        say = say(score0,score1)
        who = next_player(who)
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores


def announce_lead_changes(last_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != last_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say


def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 8)
    Player 0 now has 10 and Player 1 now has 8
    >>> h3 = h2(10, 17)
    Player 0 now has 10 and Player 1 now has 17
    Player 1 takes the lead by 7
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, last_score=0, running_high=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 9)
    9 point(s)! That's a record gain for Player 1!
    >>> f3 = f2(20, 9)
    >>> f4 = f3(20, 30)
    21 point(s)! That's a record gain for Player 1!
    >>> f5 = f4(20, 47) # Player 1 gets 17 points; not enough for a new high
    >>> f6 = f5(21, 47)
    >>> f7 = f6(21, 77)
    30 point(s)! That's a record gain for Player 1!
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    def say(score0, score1):
        if who == 0 :
            a=score0 -last_score
            if a > running_high :
                #running_high = a
                print("%d point(s)! That's a record gain for Player %d!" %(a,who))
                return announce_highest(who, score0, a)
            else :
                return announce_highest(who, score0, running_high)
        if who == 1 :
            a=score1 -last_score
            if a > running_high :
                #running_high = a
                print("%d point(s)! That's a record gain for Player %d!" %(a,who))
                return announce_highest(who, score1, a)
            else :
                return announce_highest(who, score1, running_high)
    return say
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(original_function, trials_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TRIALS_COUNT times.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.
    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 1000)
    >>> averaged_dice(0, 1, dice)
    3.5
    """
    # BEGIN PROBLEM 8
    def averaged(*args) :
        count = 0
        for i in range(trials_count) :
            count +=original_function(*args)
        return count/trials_count
    return averaged
    # END PROBLEM 8

def max_scoring_num_rolls(current_score=0, dice=six_sided, trials_count=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn score
    by calling roll_dice with the provided DICE a total of TRIALS_COUNT times.
    Assume that the dice always return positive outcomes.
    def roll_dice(current_score, num_rolls, dice=six_sided):
    >>> dice = make_test_dice(1, 3)
    >>> max_scoring_num_rolls(0, dice)
    1
    """
    # BEGIN PROBLEM 9
    max_=0
    flag = 0
    for i in range(1,11) :
        f=make_averaged(roll_dice, trials_count)
        a=f(current_score,i,dice)
        if a > max_ :
            max_=a
            flag = i
    return flag
    # END PROBLEM 9

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)
    print('always_roll(6) win rate:', average_win_rate(always_roll(6)))
    "*** You may add additional experiments as you wish ***"


def picky_piggy_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy returns 0 dice if that gives at least CUTOFF points, and
    returns NUM_ROLLS otherwise.
    def picky_piggy(score):
    Return the points scored from rolling 0 dice.
    """
    # BEGIN PROBLEM 10
    if picky_piggy(opponent_score) >= cutoff :
        return 0
    else :
        return num_rolls
    # END PROBLEM 10


def swine_swap_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy returns 0 dice when this would result in Swine Swap taking
    effect and gains at least CUTOFF points. Otherwise, it returns NUM_ROLLS.
    A strategy can also take advantage of the Swine Swap rules. 
    The Swine Swap strategy always rolls 0 if doing so **triggers the rule and the player's gain in this turn is at least `cutoff` points**. 
    In other cases, the strategy rolls `num_rolls`.
    """
    if swine_swap(opponent_score,score) and opponent_score > score and picky_piggy(opponent_score) >= cutoff :
        return 0
    else :
        return num_rolls


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    return 6   # Replace this statement
    # END PROBLEM 12

##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


if __name__ == '__main__':
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()