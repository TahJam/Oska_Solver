from moveGen import moveGen
from oskaPlayer import *


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """Compare evaluators"""
    # get the potential moves
    state = convert2D(['---w', 'w-w', 'bb', 'b-w', '---b'])
    curr_player = 'w'
    myMoveGen = moveGen(state, curr_player)
    
    # compare moveGen lists
    print(f'initial state = {convertList(state)}')
    print(f'{len(myMoveGen)=}')
    
    # # compare evaluators
    # for myMove in myMoveGen:
    #     print(f'myMove = {convertList(myMove)}')
    #     print(f'{evaluator(myMove,curr_player)=}')
    #     print(f'{git.board_evaluator(myMove,curr_player)=}')
    #     print('\n') # newline
    """
    My game--------------
    first turn	white=['-www', 'w--', '--', '---', 'bbbb']	
                black=['-www', 'w--', '--', 'b--', '-bbb']
    turn=0	white=['--ww', 'ww-', '--', 'b--', '-bbb']
    turn=1	black=['--ww', 'ww-', 'b-', '---', '-bbb']
    turn=2	white=['---w', 'www', 'b-', '---', '-bbb']
    turn=3	black=['---w', 'www', 'b-', 'b--', '--bb']
    turn=4	white=['---w', 'w-w', 'bw', 'b--', '--bb']
    turn=5	black=['---w', 'w-w', 'bw', 'bb-', '---b']
    turn=6	white=['---w', 'w-w', 'b-', 'bbw', '---b']
    turn=7	black=['---w', 'w-w', 'bb', 'b-w', '---b']
    turn=8	white=['---w', 'w--', 'b-', 'bww', '---b']
    turn=9	black=['---w', 'wb-', '--', 'bww', '---b']
    turn=10	white=['----', 'wbw', '--', 'bww', '---b']
    turn=11	black=['-b--', 'w-w', '--', 'bww', '---b']
    turn=12	white=['-b--', '--w', 'w-', 'bww', '---b']
    turn=13	black=['-b--', '--w', 'wb', 'bw-', '----']
    turn=14	white=['-b--', '--w', '-b', '-w-', 'w---']
    turn=15	black=['-b--', '-bw', '--', '-w-', 'w---']
    turn=16	white=['-b--', '-b-', '-w', '-w-', 'w---']
    turn=17	black=['-bb-', '---', '-w', '-w-', 'w---']
    turn=18	white=['-bb-', '---', '--', '-ww', 'w---']
    turn=19	black=['-bb-', '---', '--', '-ww', 'w---']
    turn=20	white=['-bb-', '---', '--', '--w', 'ww--']
    turn=21	black=['-bb-', '---', '--', '--w', 'ww--']
    turn=22	white=['-bb-', '---', '--', '---', 'www-']
    turn=23	black=None
    Black Won :)
    """

    # next_stateW = [['-----', '----', '---', 'b-', '-ww', 'b-bb', '-ww--'],
    #                  ['-----', '----', '---', 'b-', '-ww', '-bbb', 'ww---'],
    #                  ['-----', '----', '---', 'b-', 'w-w', 'bb-b', '-w-w-'],
    #                  ['-----', '----', '---', 'b-', 'ww-', 'bbb-', '-w--w'],
    #                  ['-----', '----', '---', 'b-', 'ww-', 'bb-b', '-ww--']]
    # next_stateB = [['-----', '----', '-b-', '--', 'www', 'bbbb', '-w---'],
    #                  ['-----', '----', 'b--', '--', 'www', 'bbbb', '-w---'],
    #                  ['-----', '----', '---', 'bb', 'w-w', 'b-bb', '-w---'],
    #                  ['-----', '----', '---', 'bb', 'ww-', 'bbb-', '-w---']]
    # statesW = moveGen(state, 'w')
    # statesB = moveGen(state, 'b')
    #
    # for state in statesW:
    #     if state not in next_stateW:
    #         print('Error in white moves')
    # print(f'{len(statesW)=} and {len(next_stateW)=}')
    # print(f'{len(statesB)=} and {len(next_stateB)=}')
    #
    # for state in statesB:
    #     if state not in next_stateB:
    #         print('error in black moves')

    depth = 5
    print('My game--------------')
    white = oskaplayer(['wwww', '---', '--', '---', 'bbbb'], 'w', depth)
    black = oskaplayer(white, 'b', depth)
    turn = 0
    print(f'first turn\t{white=}\t{black=}')
    while white and black:
        if turn % 2 == 1:  # black turn
            black = oskaplayer(white, 'b', depth)
            print(f'{turn=}\t{black=}')
        else:  # white turn
            white = oskaplayer(black, 'w', depth)
            print(f'{turn=}\t{white=}')
        # determine the winner (whichever is None won)
        if white is None:
            print(f'White Won :)')
        elif black is None:
            print(f'Black Won :)')
        turn += 1
