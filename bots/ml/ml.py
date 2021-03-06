#!/usr/bin/env python
"""
A basic adaptive bot. This is part of the third worksheet.

"""

from api import State, util
import random, os
from itertools import chain

import joblib

model_names = ['model','model1','model2','model3','model4','model5','model6','model7','model8','model9','model10','model11','model12'\
               ,'model13','model14','model15','model16','model17','model18','model19','model20','model21','model22','model23']
model_name = model_names[22]

classification = True

# Path of the model we will use. If you make a model
# with a different name, point this line to its path.
DEFAULT_MODEL = os.path.dirname(os.path.realpath(__file__)) + '/models/{}.pkl'.format(model_name)

class Bot:

    __randomize = True

    __model = None

    def __init__(self, randomize=True, model_file=DEFAULT_MODEL):
        print(model_file)

        self.__randomize = randomize

        # Load the model
        self.__model = joblib.load(model_file)

    def get_move(self, state):

        val, move = self.value(state)

        return move

    def value(self, state):
        """
        Return the value of this state and the associated move
        :param state:
        :return: val, move: the value of the state, and the best move.
        """

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        for move in moves:

            next_state = state.next(move)

            # IMPLEMENT: Add a function call so that 'value' will
            # contain the predicted value of 'next_state'
            # NOTE: This is different from the line in the minimax/alphabeta bot
            value = self.heuristic(next_state)

            if maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move

        return best_value, best_move

    def heuristic(self, state):

        # Convert the state to a feature vector
        feature_vector = [features(state,model_name)]

        # These are the classes: ('won', 'lost')
        classes = list(self.__model.classes_)

        # Ask the model for a prediction
        # This returns a probability for each class
        prob = self.__model.predict_proba(feature_vector)[0]

        # Weigh the win/loss outcomes (-1 and 1) by their probabilities

        if not classification:
            res = -1.0 * prob[classes.index('lost')] + 1.0 * prob[classes.index('won')]
        else:
            res = -1.0 * prob[classes.index('lost1')] + 1.0 * prob[classes.index('won1')] + -2.0 * prob[classes.index('lost2')]\
        + 2.0 * prob[classes.index('won2')] + -3.0 * prob[classes.index('lost3')] + 3.0 * prob[classes.index('won3')]

        return res

def maximizing(state):
    """
    Whether we're the maximizing player (1) or the minimizing player (2).
    :param state:
    :return:
    """
    return state.whose_turn() == 1


def features(state,model_name):
    # type: (State) -> tuple[float, ...]
    """
    Extract features from this state. Remember that every feature vector returned should have the same length.

    :param state: A state to be converted to a feature vector
    :return: A tuple of floats: a feature vector representing this state.
    """
    feature_set = []

    # Add player 1's points to feature set
    p1_points = state.get_points(1)

    # Add player 2's points to feature set
    p2_points = state.get_points(2)

    # Add player 1's pending points to feature set
    p1_pending_points = state.get_pending_points(1)

    # Add plauer 2's pending points to feature set
    p2_pending_points = state.get_pending_points(2)

    # Get trump suit
    trump_suit = state.get_trump_suit()

    # Add phase to feature set
    phase = state.get_phase()

    # Add stock size to feature set
    stock_size = state.get_stock_size()

    # Add leader to feature set
    leader = state.leader()

    # Add whose turn it is to feature set
    whose_turn = state.whose_turn()

    # Add opponent's played card to feature set
    opponents_played_card = state.get_opponents_played_card()

    #moves = state.moves()



    ################## You do not need to do anything below this line ########################

    perspective = state.get_perspective()

    # Perform one-hot encoding on the perspective.
    # Learn more about one-hot here: https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/
    perspective = [card if card != 'U'   else [1, 0, 0, 0, 0, 0] for card in perspective]
    perspective = [card if card != 'S'   else [0, 1, 0, 0, 0, 0] for card in perspective]
    perspective = [card if card != 'P1H' else [0, 0, 1, 0, 0, 0] for card in perspective]
    perspective = [card if card != 'P2H' else [0, 0, 0, 1, 0, 0] for card in perspective]
    perspective = [card if card != 'P1W' else [0, 0, 0, 0, 1, 0] for card in perspective]
    perspective = [card if card != 'P2W' else [0, 0, 0, 0, 0, 1] for card in perspective]
    # Append one-hot encoded perspective to feature_set
    feature_set += list(chain(*perspective))

    # Append normalized points to feature_set
    total_points = p1_points + p2_points
    feature_set.append(p1_points/total_points if total_points > 0 else 0.)
    feature_set.append(p2_points/total_points if total_points > 0 else 0.)

    # Append normalized pending points to feature_set
    total_pending_points = p1_pending_points + p2_pending_points
    feature_set.append(p1_pending_points/total_pending_points if total_pending_points > 0 else 0.)
    feature_set.append(p2_pending_points/total_pending_points if total_pending_points > 0 else 0.)

    '''
    My features
    '''

    model_additional_features = {
        'model' :  [],
        'model1':  [],
        'model2':  ['point_diff/total'],
        'model3':  ['ace one hot'],
        'model4':  ['point_diff/total', 'ace one hot'],
        'model5':  ['trump one hot'],
        'model6':  ['trump one hot', 'point_diff/total'],
        'model7':  ['trump one hot', 'point_diff/total', 'ace one hot'],
        'model8':  [],
        'model9':  ['point_diff/total'],
        'model10': ['points to win'],
        'model11': ['points in hand/points to win'],
        'model12': ['points to win'],
        'model13': ['point_diff/total','points to win'],
        'model14': ['points squared'],
        'model15': ['points squared','point_diff/total','points to win'],
        'model16': ['point_diff/total','point_diff/total2','points to win', 'points to win2'],
        'model17': ['point_diff/total2'],
        'model18': ['points to win2'],
        'model19': ['point_diff/total','points to win'],
        'model20': ['point_diff'],
        'model21': ['point_diff/total','point_diff/total2','points to win', 'points to win2','point_diff','points in hand/points to win',\
                    'trump one hot','ace one hot','points squared'],
        'model22': ['point_diff/total','points to win', 'point_diff'],
        'model23': ['point_diff/total', 'points to win', 'point_diff']
    }


    #points squared



    if 'points squared' in model_additional_features[model_name]:
        feature_set.append(p1_points*p1_points)
        feature_set.append(p2_points*p2_points)
    #apppend difference between points over total points
    if 'point_diff/total' in model_additional_features[model_name]:
        feature_set.append((p1_points - p2_points)/total_points if total_points> 0 else 0.)
        feature_set.append((p2_points - p1_points)/total_points if total_points>0 else 0.)

    if 'point_diff/total2' in model_additional_features[model_name]:
        feature_set.append(((p1_points - p2_points) / total_points)**2 if total_points > 0 else 0.)
        feature_set.append(((p2_points - p1_points) / total_points)**2 if total_points > 0 else 0.)

    if 'point_diff' in model_additional_features[model_name]:
        feature_set.append(p1_points-p2_points)
        feature_set.append(p2_points-p1_points)


    hand = state.hand()
    #ace in hand [0,0,0,0,0]
    if 'ace one hot' in model_additional_features[model_name]:
        ace = [0,5,10,15]
        ace_in_hand = [0]*5
        index = sum([1 for item in ace if item in hand])
        ace_in_hand[index]=1
        feature_set+=ace_in_hand
    #marriage one hot

    if 'marriage one hot' in model_additional_features[model_name]:
        marriage = False
        for move in state.moves():
            x,y = move
            if type(x) is int and type(y) is int:
                marriage = True
                break
        feature_set+= [1,0] if marriage else [0,1]
    #trump in hand [0,0,0,0,0,0] C - 0,1,2,3,4   D - 5,6,7,8,9  H - 10,11,12,13,14 S - 15,16,17,18,19

    if 'trump one hot' in model_additional_features[model_name]:
        cards = {}
        cards['C'] = [0,1,2,3,4]
        cards['D'] = [5,6,7,8,9]
        cards['H'] = [10,11,12,13,14]
        cards['S'] = [15,16,17,19,19]
        trump_in_hand = [0]*6
        trump_hand = cards[trump_suit]
        index = sum([1 for item in trump_hand if item in hand])
        trump_in_hand[index] = 1
        feature_set+=trump_in_hand

    if 'points to win' in model_additional_features[model_name]:
        feature_set.append(66-p1_points)
        feature_set.append(66-p2_points)

    if 'points to win2' in model_additional_features[model_name]:
        feature_set.append((66-p1_points)**2)
        feature_set.append((66-p2_points)**2)

    if 'points in hand/points to win' in model_additional_features[model_name]:
        score = [11, 10, 4, 3, 2]
        score_sum = 0
        for card in hand:
            score_sum += score[card%5]
        feature_set.append(score_sum/(66.01-state.get_points(state.whose_turn())))


    '''
    end of my features
    '''
    # Convert trump suit to id and add to feature set
    # You don't need to add anything to this part
    suits = ["C", "D", "H", "S"]
    trump_suit_onehot = [0, 0, 0, 0]
    trump_suit_onehot[suits.index(trump_suit)] = 1
    feature_set += trump_suit_onehot

    # Append one-hot encoded phase to feature set
    feature_set += [1, 0] if phase == 1 else [0, 1]

    # Append normalized stock size to feature set
    feature_set.append(stock_size/10)

    # Append one-hot encoded leader to feature set
    feature_set += [1, 0] if leader == 1 else [0, 1]

    # Append one-hot encoded whose_turn to feature set
    feature_set += [1, 0] if whose_turn == 1 else [0, 1]

    # Append one-hot encoded opponent's card to feature set
    opponents_played_card_onehot = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    opponents_played_card_onehot[opponents_played_card if opponents_played_card is not None else 20] = 1
    feature_set += opponents_played_card_onehot


    # Return feature set
    #print(feature_set)
    return feature_set
