import string
from collections import OrderedDict
from sys import maxsize
from copy import copy

class HungryBoard(object):
    """
    This class represents the board on which the game is being played.
    We are storing the board in an OrderedDict object, which is nothing but a
    normal python dictionary or hashtable, but the order in which we insert
    keys is remembered. All the values of the board are initialized to Zero values
    except the players and maybe their move options.

    The functions and their nature are described below:

    init_board - This function initializes the players in their proper positions.
    get_board_data - This function returns the main OrderedDict variable containing all the board data as well as its size.
    print_board - This function prints the board.
    lmoves - This function returns all the valid moves for larva(without checking for validity)
    bmoves - This function returns all the valid moves for a particular bird(without checking for validity)
    """
    def __init__(self,N):
        self.board = OrderedDict()
        self.weights = OrderedDict()
        
        for char in string.ascii_uppercase[:N]:
            self.board[char] = [0 for i in range(N)]

        for i,char in enumerate(string.ascii_uppercase[:N]):
            self.weights[char] = [i+k for k in range(1,64,N)][::-1]

        self.size = N
        self.bird = {}
        self.mapping = {i:char for i,char in enumerate(self.board.keys())}
        self.rev_mapping = {j:i for i,j in self.mapping.items()}

        self.board['A'][0] = 'B1'
        self.board['C'][0] = 'B2'
        self.board['E'][0] = 'B3'
        self.board['G'][0] = 'B4'
        self.board['D'][1] = 'L'

        self.bird['B1'] = ('A',0)
        self.bird['B2'] = ('C',0)
        self.bird['B3'] = ('E',0)
        self.bird['B4'] = ('G',0)
        
        self.larva = ('D',1)

        self.corner_penf = {
            'A':1.5,
            'B':1.4,
            'C':1.3,
            'D':1.2,
            'E':1.2,
            'F':1.3,
            'G':1.4,
            'H':1.5
        }

        self.height_penf = 1.5


    def get_board_data(self):
        return self.board,self.size,self.bird,self.larva

    def get_board_mapping(self):
        return self.mapping,self.rev_mapping

    def get_coords(self,coords):
        return self.rev_mapping[coords[0]],coords[1]

    def lmoves(self,coords):
        x,y = coords
        x = self.rev_mapping[x]
        choices = [(self.mapping[i],j) for i,j in [(x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1)] if 0<=i<=7 and 0<=j<=7]
        return [x for x in choices if x not in self.bird.values() and x != self.larva]

    def bmoves(self,coords):
        x,y = coords
        x = self.rev_mapping[x]
        choices = [(self.mapping[i],j) for i,j in [(x+1,y+1),(x-1,y+1)] if 0<=i<=7 and 0<=j<=7]
        return [x for x in choices if x not in self.bird.values() and x != self.larva]

    def manhattan_distance(self,x,y):
        return sum(abs(a-b) for a,b in zip(x,y))

    def get_manhattan_distance_sum(self,bird,larva):
        return sum([self.manhattan_distance(self.get_coords(larva),self.get_coords(bird[key])) for key in self.bird.keys()])

    def mmh_val(self,bird,larva):

        b1_pos = bird['B1']
        b2_pos = bird['B2']
        b3_pos = bird['B3']
        b4_pos = bird['B4']

        a1 = 1 - self.corner_penf[larva[0]]
        a1 += 1 - larva[1]

        a2,a3,a4,a5 = -1,-1,-1,-1
        
        if larva in self.bmoves(b1_pos):
            a2 -= 1.25
        if larva in self.bmoves(b2_pos):
            a3 -= 1.25
        if larva in self.bmoves(b3_pos):
            a4 -= 1.25
        if larva in self.bmoves(b4_pos):
            a5 -= 1.25

        if len([(x,y) for x,y in self.lmoves(larva) if y ==0]) > 0:
            a1 += 1.25

        larva_weight = a1 * self.weights[larva[0]][larva[1]]
            
        if b1_pos[1] >= larva[1]:
            a2 += self.height_penf * abs(larva[1] - b1_pos[1])
        b1_weight = a2 * self.weights[b1_pos[0]][b1_pos[1]]
        
        if b2_pos[1] >= larva[1]:
            a3 += self.height_penf * abs(larva[1] - b2_pos[1])
        b2_weight = a3 * self.weights[b2_pos[0]][b2_pos[1]]
        
        if b3_pos[1] >= larva[1]:
            a4 += self.height_penf * abs(larva[1] - b3_pos[1])
        b3_weight = a4 * self.weights[b3_pos[0]][b3_pos[1]]
        
        if b4_pos[1] >= larva[1]:
            a5 += self.height_penf * abs(larva[1] - b4_pos[1])
        b4_weight = a5 * self.weights[b4_pos[0]][b4_pos[1]]

        return larva_weight + b1_weight + b2_weight + b3_weight + b4_weight + self.get_manhattan_distance_sum(bird,larva)

    def minimax(self, node, depth, maximizingPlayer):
        if depth == 0 or node.is_terminal():
            if node.util_value == 0:
                if hasattr(node,'choice'):
                    return 0 if maximizingPlayer else -999**999
                else:
                    return -999**999 if maximizingPlayer else 0
            else:
                return node.util_value
        if maximizingPlayer:
            bestValue = -999**999
            for child in node.children:
                val = self.minimax(child, depth - 1, False)
                child.util_value = val
                bestValue = max(bestValue, val)
            return bestValue
        else:
            bestValue = maxsize
            for child in node.children:
                val = self.minimax(child, depth - 1, True)
                child.util_value = val
                bestValue = min(bestValue, val)
            return bestValue

    def minimax_with_ab_pruning(self, node, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or node.is_terminal():
            if node.util_value == 0:
                if hasattr(node,'choice'):
                    return 0 if maximizingPlayer else -999**999
                else:
                    return -999**999 if maximizingPlayer else 0
            else:
                return node.util_value
        if maximizingPlayer:
            val = -999**999
            for child in node.children:
                val = max(val, self.minimax_with_ab_pruning(child, depth - 1, alpha, beta, False))
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return val
        else:
            val = maxsize
            for child in node.children:
                val = min(val, self.minimax_with_ab_pruning(child, depth - 1, alpha, beta, True))
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return val

    def print_board(self):
        print '\n'
        for row in range(self.size)[::-1]:
            print str(row+1) + '   ' + '  '.join(map(lambda x:'{:<3}'.format(x),[self.board[column][row] for column in self.board.keys()]))
        print ''
        print ' '*4 + '  '.join(map(lambda x:'{:<3}'.format(x),self.board.keys()))
        print '\n'

    def print_weights(self):
        print '\n'
        for row in range(self.size)[::-1]:
            print str(row+1) + '   ' + '  '.join(map(lambda x:'{:<3}'.format(x),[self.weights[column][row] for column in self.weights.keys()]))
        print ''
        print ' '*4 + '  '.join(map(lambda x:'{:<3}'.format(x),self.weights.keys()))
        print '\n'

class BirdNode(object):
    def __init__(self,coords,choice,parent=None):
        self.children = []
        self.parent = parent  
        self.choice = choice      
        self.coords = coords
        self.util_value = 0

    def is_terminal(self):
        return True if not self.children else False

    def __repr__(self):
        return self.choice + ' ' + str(self.coords) + ' = ' + str(self.util_value)
    
class LarvaNode(object):
    def __init__(self,coords,parent=None):
        self.children = []
        self.parent = parent        
        self.coords = coords
        self.util_value = 0

    def is_terminal(self):
        return True if not self.children else False

    def __repr__(self):
        return 'Larva' + ' ' + str(self.coords) + ' = ' + str(self.util_value)             

def parse(coords):
    """
    This method converts real world user inputs about the board
    to a program specific cooradinate value.
    """
    return coords[0].upper(),int(coords[1]) - 1

def revparse(coords):
    """
    This method converts program specific coordinate value to 
    real world user inputs about the board.
    """
    return '{},{}'.format(coords[0].upper(),str(int(coords[1]) + 1))

def pprint(n,statement):
    print ''
    print '*' * n
    print statement
    print '*' * n
    print ''

def print_tree(node):
    nodes = not isinstance(node, (list, tuple)) and [node] or node
    depth = [1]
    def wrapped(node):
        depthStr = '  ' * len(depth)
        print "%s -> %s" % (depthStr, node)
        depth.append(1)
        for child in node.children:
            wrapped(child)
            depth[-1] += 1
        depth.pop()
    for node in nodes:
        wrapped(node)
        depth[0] += 1

def game(choice,mode):
    """
    This function pertains to the human vs human game mode.
    """
    board = HungryBoard(8)

    board_matrix,board_size,bird,larva = board.get_board_data()
    player_move_history = []

    if mode == 'hvai':
        if choice == 'bird':
            ai = 'larva'
        elif choice == 'larva':
            ai = 'bird'
        else:
            ai = None
    else:
        ai = None

    choice = 'larva'

    board.print_board()
    print ''

    while True:

        if choice == 'bird':

            if ai == 'bird':

                bird_options = {bird_choice:[BirdNode(x,bird_choice,board.bird[bird_choice]) for x in board.bmoves(board.bird[bird_choice])] for bird_choice in board.bird.keys()}

                for bird_type,moves in bird_options.items():    
                    for option in moves:
                        
                        board.bird[bird_type],temp = option.coords,board.bird[bird_type]        
                        
                        option.children = [LarvaNode(x,option) for x in board.lmoves(board.larva)]

                        for child in option.children:
                            board.larva,sec_temp = child.coords,board.larva
                            
                            for key in board.bird.keys():
                                for move in board.bmoves(board.bird[key]):

                                    b = BirdNode(move,key,child)                                    
                                    
                                    t_temp,board.bird[key] = board.bird[key],b.coords
                                    
                                    b.util_value = board.mmh_val(board.bird,board.larva) 
                                    
                                    board.bird[key] = t_temp                                  
                                    
                                    child.children.append(b)                                

                            board.larva = sec_temp

                        board.bird[bird_type] = temp 
                
                best_value = maxsize                

                print 'Choices made by AI are:\n'                

                for bird_type,moves in bird_options.items():
                    for move in moves:             
                        val = board.minimax(move,3,True)                           
                        # val = board.minimax_with_ab_pruning(move,3,-999**999,maxsize,False)
                        move.util_value = val
                        print_tree(move)

                        if val < best_value:
                            best_value = val
                            best_choice = move
                
                bird_choice = best_choice.choice
                bird_new_pos = best_choice.coords

                print '\nBest move made by AI is bird {} from {} to {}\n'.format(bird_choice,revparse(board.bird[bird_choice]),revparse(bird_new_pos))

            else:
                while True:
                    pprint(100,'Please select a bird to move - valid choices are "B1","B2","B3","B4"')

                    while True:
                        bird_choice = raw_input().upper()
                        if bird_choice in bird.keys():
                            break
                        else:
                            print 'Please enter a valid choice for bird - choices are "B1","B2","B3","B4"'

                    moves_cnt = 0

                    pprint(100,'valid moves are listed below:')

                    for i,j in board.bmoves(bird[bird_choice]):
                        display_coords = bird[bird_choice][0],bird[bird_choice][1]+1
                        print '{} -> {}'.format(''.join(map(str,display_coords)),i+str(j+1))
                        board_matrix[i][j] = '?'
                        moves_cnt += 1

                    if moves_cnt == 0:
                        print 'no valid moves for bird choice.'
                    else:
                        break

                board.print_board()

                while True:

                    print '*' * 100
                    print 'Please select a move from the above options\nPlease specify the move by entering the column and row like "A,4"'
                    print '*' * 100 + '\n'

                    bird_new_pos = parse(tuple(raw_input().split(',')))

                    if bird_new_pos in board.bmoves(bird[bird_choice]):
                        break
                    else:
                        print 'Invalid move.\n'

            old_column,old_row = bird[bird_choice]
            for i,j in board.bmoves(bird[bird_choice]):
                if (i,j) != larva and (i,j) not in bird.values():
                    board_matrix[i][j] = 0

            board.bird[bird_choice],bird[bird_choice] = bird_new_pos,bird_new_pos
            new_column,new_row = bird[bird_choice]
            board_matrix[old_column][old_row] = 0
            board_matrix[new_column][new_row] = bird_choice

            if larva in board.bmoves(bird[bird_choice]) and len([(x,y) for x,y in board.lmoves(larva) if (x,y) not in bird.values()]) == 0:
                print 'Move successful.\nBird {} can eat larva.\nBirds win.'.format(bird_choice)
                break
            else:
                print 'Move successful.\nNow larva can make a move.'
            board.print_board()
            player_move_history.append((bird_choice,old_column,old_row,new_column,new_row))
            choice = 'larva'

        elif choice == 'larva':
            pprint(100,'please select a valid move - options are listed below:')

            if ai == 'larva':
                larva_options = [LarvaNode(x,board.larva) for x in board.lmoves(board.larva)]

                for option in larva_options:
                    board.larva,temp = option.coords,board.larva  

                    for key in board.bird.keys():
                        for move in board.bmoves(board.bird[key]):
                            option.children.append(BirdNode(move,key,option))

                    for child in option.children:
                        board.bird[child.choice],sec_temp = child.coords,board.bird[child.choice]
                        
                        for move in board.lmoves(board.larva):

                            l = LarvaNode(move,child)

                            board.larva,l_temp = l.coords,board.larva

                            l.util_value = board.mmh_val(board.bird,board.larva)                   

                            board.larva = l_temp

                            child.children.append(l)
                        
                        board.bird[child.choice] = sec_temp

                    board.larva = temp

                best_value = None
                best_choice = None


                print 'Choices made by AI are:\n'
                for option in larva_options:      
                    val = board.minimax(option,3,False)              
                    # val = board.minimax_with_ab_pruning(option,3,-999**999,maxsize,True)
                    # print 'larva > {} > {}'.format(revparse(option.coords),str(val))                
                    option.util_value = val
                    print_tree(option)
                    if val > best_value:
                        best_value = val       
                        best_choice = option   

                if best_choice == None:
                    print 'No more valid moves for larva. Birds win.\n'
                    pprint(100,'Move History:')
                    for move in player_move_history:
                        print 'Player {} moved from {},{} to {},{}'.format(*move)
                    print '*' * 100
                    break

                larva_new_pos = best_choice.coords

                print '\nBest move made by AI is larva from {} to {}\n'.format(revparse(board.larva),revparse(larva_new_pos))

            else:
                moves_cnt = 0
                for i,j in board.lmoves(larva):
                    if (i,j) in [x for sublist in [board.bmoves(board.bird[key]) for key in board.bird.keys()] for x in sublist]:
                        moves_cnt -= 1
                    display_coords = larva[0],larva[1]+1
                    print '{} -> {}'.format(''.join(map(str,display_coords)),i+str(j+1))
                    board_matrix[i][j] = '?'
                    moves_cnt += 1

                if moves_cnt <= 0:
                    print 'No more valid moves for larva. Birds win.\n'
                    pprint(100,'Move History:')
                    for move in player_move_history:
                        print 'Player {} moved from {},{} to {},{}'.format(*move)
                    print '*' * 100
                    break

                board.print_board()

                while True:

                    print '*' * 100
                    print 'Please select a move from the above options\nPlease specify the move by entering the column and row like "A,4"'
                    print '*' * 100 + '\n'

                    larva_new_pos = parse(tuple(raw_input().split(',')))

                    if larva_new_pos in board.lmoves(larva):
                        break
                    else:
                        print 'Invalid move.\n'

            old_column,old_row = larva

            for i,j in board.lmoves(larva):
                if (i,j) not in bird.values():
                    board_matrix[i][j] = 0

            board.larva,larva = larva_new_pos,larva_new_pos
            new_column,new_row = larva

            board_matrix[old_column][old_row] = 0
            board_matrix[new_column][new_row] = 'L'

            print 'Move successful.\nNow bird can make a move.'
            board.print_board()
            player_move_history.append(('L',old_column,old_row,new_column,new_row))
            choice = 'bird'

            if larva in [(x,0) for x in board_matrix.keys()]:
                print 'Larva wins the game.\n'
                print '*' * 100
                print 'Move History:'
                print '*' * 100
                for move in player_move_history:
                    print 'Player {} moved from {},{} to {},{}'.format(*move)
                print '*' * 100
                break

        elif choice.lower() == 'exit':
            break
        else:
            print 'Not a valid option - options are bird,larva and exit'

if __name__ == '__main__':
    pprint(100,'Welcome to Hungry Birds')

    while True:
        print 'Enter mode of playing:'
        print '1.Human vs Human\n2.Human vs A.I\n3.Exit\n'
        print 'Valid options are 1,2 or 3'
        option = raw_input()
        try:
            option = int(option)
        except Exception as e:
            print 'Invalid option - valid options are 1,2 or 3'
            break

        if option == 1:
            while True:

                print 'Please enter the choice for first move - valid options are bird or larva'
                option = raw_input()

                if option == 'bird' or option == 'larva':
                    game(option,'hvh')
                    break
                else:
                    print 'wrong choice.\n'

        elif option == 2:
            while True:

                print 'Choose a player for yourself - valid options are bird or larva'
                print 'Kindly note that the AI will automatically select the other player'
                option = raw_input()

                if option == 'bird' or option == 'larva':
                    game(option,'hvai')
                    break
                else:
                    print 'wrong choice.\n'

        elif option == 3:
            print '\nThanks for playing'
            break
        else:
            print 'Invalid option - valid options are 1,2 or 3'
            break
