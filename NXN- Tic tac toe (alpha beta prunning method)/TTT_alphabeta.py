from pade.behaviours.protocols import Behaviour
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.misc.utility import start_loop
import numpy as np
import time


class Board():
    pos = {}

    def __init__(self,n):
        self.size = n
        self.ttt_mat = np.full((n, n), 0)
        for i in range(n):
            for j in range(n):
                self.pos[n*i+j+1] = [i,j]

    def isempty(self, board_pos):
        if self.ttt_mat[self.pos[board_pos][0]][self.pos[board_pos][1]] == 0:
            return True
        return False

    def go(self, i, val):
        self.ttt_mat[self.pos[i][0]][self.pos[i][1]] = val

    def terminal_test(self):
        #print(self.ttt_mat)
        # Vertical win
        for i in range(0, self.size):
            if self.ttt_mat[0][i] != 0:
                flag = True
                for j in range(1, self.size):
                    if self.ttt_mat[j][i] != self.ttt_mat[j-1][i]:
                        flag = False
                        break
                if flag is True:
                    return self.ttt_mat[0][i]

        # Horizontal win
        for i in range(0, self.size):
            if self.ttt_mat[i][0] != 0:
                flag = True
                for j in range(1, self.size):
                    if self.ttt_mat[i][j] != self.ttt_mat[i][j-1]:
                        flag = False
                        break
                if flag is True:
                    return self.ttt_mat[i][0]

        # Main diagonal win
        if self.ttt_mat[0][0] != 0:
            flag = True
            for i in range(1, self.size):
                if self.ttt_mat[i][i] != self.ttt_mat[i - 1][i - 1]:
                    flag = False
                    break
            if flag is True:
                return self.ttt_mat[0][0]

        # Second diagonal win
        if self.ttt_mat[0][self.size-1] != 0:
            flag = True
            for i in range(1,self.size):
                j = self.size - 1 -i
                if self.ttt_mat[i][j] != self.ttt_mat[i - 1][j + 1]:
                    flag = False
                    break
            if flag is True:
                return self.ttt_mat[0][self.size-1]

        # Is whole board full?
        for i in range(1, self.size * self.size + 1):
            if self.isempty(i):
                return None

        # It's a tie!
        return 0


class Player():
    def __init__(self,sym):
        self.row = [0, 0, 0]
        self.col = [0, 0, 0]
        self.dnal = [0, 0]
        self.symbol= sym;

    def make_move(self, board, position):
        val = self.symbol
        if board.isempty(position):
            board.go(position, val)
            return 0
        print("Sorry....... The position entered is already occupied...... ")
        return -1

    def alpha_beta_search(self,board,opponent):
        # heuristic:
        # -1 - loss
        # 0  - a tie
        # 1  - win
        val,pos = self.max(-20,20,board,opponent,0)
        return pos

    def max(self, alpha, beta, board, opponent,depth):
        maxv = -20
        opt = 0

        result = board.terminal_test()

        if result == opponent.symbol:
            return -10-depth, 1
        elif result == self.symbol:
            return 0-depth, 1
        elif result == 0:
            return 10-depth, 1

        for i in range(1, board.size*board.size+1):
            if board.isempty(i):
                board.go(i,self.symbol)
                (node_val, min_pos) = self.min(alpha, beta, board, opponent,depth+1)
                # Out of all the child node's  value select the maximum one
                if node_val > maxv:
                    maxv = node_val
                # Setting back the field to empty
                board.go(i, 0)

                # if the maximum value is greater than beta (parent (min) node) : range does not exist hence prune
                if maxv >= beta:
                    #print("Max node Pruned at alpha beta position",alpha,beta,opt)
                    return (maxv, opt)

                if maxv > alpha:
                    alpha = maxv
                    # update optimal position from where this maximum value is reached
                    opt = i
        #print("Max node: maxv, alpha,beta,opt", maxv, alpha, beta, opt)
        return maxv, opt

    def min(self, alpha, beta, board, opponent,depth):
        minv = 20
        opt = 0

        result = board.terminal_test()

        if result == opponent.symbol:
            return -10-depth, 1
        elif result == self.symbol:
            return 0-depth, 1
        elif result == 0:
            return 10-depth, 1

        for i in range(1, board.size*board.size+1):
            if board.isempty(i):
                board.go(i,opponent.symbol)
                (node_val, max_pos) = self.max(alpha, beta, board, opponent,depth+1)
                # Out of all the child node's  value select the maximum one
                if node_val < minv:
                    minv = node_val
                # Setting back the field to empty
                board.go(i, 0)
                # if the minimum value is smaller than alpha (parent (max) node) : range does not exist hence prune
                if minv <= alpha:
                    #print("Min node Pruned at alpha beta position", alpha, beta, opt)
                    return (minv, opt)
                # if the minimum value is smaller than beta update beta
                if minv < beta:
                    beta = minv
                    # update optimal position from where this minimum value is reached
                    opt = i
        #print("Min node: minv, alpha,beta,opt", minv, alpha, beta, opt)
        return minv, opt


class PlayBehaviour(Behaviour):
    def __init__(self, agent):
        super().__init__(agent)

    def on_start(self):
        super().on_start()
        size = int(input("Input board size: "))
        board = Board(size)
        computer = Player(1)
        human = Player(2)
        num_turns = 1
        print("MODES: \n 1. Human makes first move\n 2. Computer makes first move\n Enter mode: ")
        b = input()
        b = int(b)
        b -= 1
        print("BOARD: ")
        print(board.ttt_mat)
        print("Human's symbol -> 2\nComputer's symbol -> 1\nBlank symbol -> 0")
        while True:
            result = board.terminal_test()

            # Printing the appropriate message if the game has ended
            if result is not None:
                if result == 1:
                    print("COMPUTER Won The Match !!!!!!!!!!")
                elif result == 2:
                    print("HUMAN Won The Match !!!!!!!!!")
                elif result == 0:
                    print("MATCH DRAW!!!!!!!!!!!!")
                break

            print("\nTurn ", num_turns, " : ")
            if (num_turns+b) % 2 != 0:
                position = input("Enter Position [1 to 9]: ")
                try:
                    position = int(position)
                except ValueError:
                    print("Please enter valid board position")
                    continue
                chk = human.make_move(board, position)
                if chk == -1:                               # Checking for occupied space
                    continue
                print(board.ttt_mat)

            else:
                print("Computer's Move: ")
                t1 = time.time()
                pos = computer.alpha_beta_search(board, human)
                t2 = time.time()
                print("Time taken for the move: ",t2 - t1)
                board.go(pos,computer.symbol)
                print(board.ttt_mat)
            num_turns += 1


class TicTacToeAgent(Agent):
    def __init__(self, aid):
        super().__init__(aid=aid)
        agent_behaviour = PlayBehaviour(self)
        self.behaviours.append(agent_behaviour)


if __name__ == '__main__':
    agents = list()
    agent_name = 'Tic_Tac_Toe_agent_{}@localhost:{}'.format(20000, 20000)
    agent_TTT = TicTacToeAgent(AID(name=agent_name))
    agents.append(agent_TTT)

    start_loop(agents)