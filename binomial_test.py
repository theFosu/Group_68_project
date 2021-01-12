""" Checks the probability that the results of a number of games happened by pure luck,
    while the winning rate in an ideal world would be .5"""


import scipy.stats as s

number_of_games = int(input('insert the total number of games: '))
games_won = int(input('Insert the number of games won by the evaluated player: '))

print('The probability that the result happened by chance is: %s' % str(s.binom_test(games_won, number_of_games, 1.0/2, alternative='greater')))