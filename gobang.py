#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import time


#----------------------------------------------------------------------
# chessboard: �����࣬�򵥴��ַ���������ֻ��ߵ����ַ������ж���Ӯ��
#----------------------------------------------------------------------
class chessboard (object):

    def __init__ (self, forbidden = 0):
        self.__board = [ [ 0 for n in range(15) ] for m in range(15) ]
        self.__forbidden = forbidden
        self.__dirs = ( (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), \
            (1, -1), (0, -1), (-1, -1) )
        self.DIRS = self.__dirs
        self.won = {}
    
    # �������
    def reset (self):
        for j in range(15):
            for i in range(15):
                self.__board[i][j] = 0
        return 0
    
    # ������
    def __getitem__ (self, row):
        return self.__board[row]

    # ������ת�����ַ���
    def __str__ (self):
        text = '  A B C D E F G H I J K L M N O\n'
        mark = ('. ', 'O ', 'X ')
        nrow = 0
        for row in self.__board:
            line = ''.join([ mark[n] for n in row ])
            text += chr(ord('A') + nrow) + ' ' + line
            nrow += 1
            if nrow < 15: text += '\n'
        return text
    
    # ת���ַ���
    def __repr__ (self):
        return self.__str__()

    def get (self, row, col):
        if row < 0 or row >= 15 or col < 0 or col >= 15:
            return 0
        return self.__board[row][col]

    def put (self, row, col, x):
        if row >= 0 and row < 15 and col >= 0 and col < 15:
            self.__board[row][col] = x
        return 0
    
    # �ж���Ӯ������0������Ӯ����1������Ӯ����2������Ӯ��
    def check (self):
        board = self.__board
        dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
        for i in range(15):
            for j in range(15):
                if board[i][j] == 0: continue
                id = board[i][j]
                for d in dirs:
                    x, y = j, i
                    count = 0
                    for k in range(5):
                        if self.get(y, x) != id: break
                        y += d[0]
                        x += d[1]
                        count += 1
                    if count == 5:
                        self.won = {}
                        r, c = i, j
                        for z in range(5):
                            self.won[(r, c)] = 1
                            r += d[0]
                            c += d[1]
                        return id
        return 0
    
    # �����������
    def board (self):
        return self.__board
    
    # ������ֵ��ַ���
    def dumps (self):
        import io
        sio = io.StringIO()
        board = self.__board
        for i in range(15):
            for j in range(15):
                stone = board[i][j]
                if stone != 0:
                    ti = chr(ord('A') + i)
                    tj = chr(ord('A') + j)
                    sio.write('%d:%s%s '%(stone, ti, tj))
        return sio.getvalue()
    
    # ���ַ����������
    def loads (self, text):
        self.reset()
        board = self.__board
        for item in text.strip('\r\n\t ').replace(',', ' ').split(' '):
            n = item.strip('\r\n\t ')
            if not n: continue
            n = n.split(':')
            stone = int(n[0])
            i = ord(n[1][0].upper()) - ord('A')
            j = ord(n[1][1].upper()) - ord('A')
            board[i][j] = stone
        return 0

    # �����ն���ɫ
    def console (self, color):
        if sys.platform[:3] == 'win':
            try: import ctypes
            except: return 0
            kernel32 = ctypes.windll.LoadLibrary('kernel32.dll')
            GetStdHandle = kernel32.GetStdHandle
            SetConsoleTextAttribute = kernel32.SetConsoleTextAttribute
            GetStdHandle.argtypes = [ ctypes.c_uint32 ]
            GetStdHandle.restype = ctypes.c_size_t
            SetConsoleTextAttribute.argtypes = [ ctypes.c_size_t, ctypes.c_uint16 ]
            SetConsoleTextAttribute.restype = ctypes.c_long
            handle = GetStdHandle(0xfffffff5)
            if color < 0: color = 7
            result = 0
            if (color & 1): result |= 4
            if (color & 2): result |= 2
            if (color & 4): result |= 1
            if (color & 8): result |= 8
            if (color & 16): result |= 64
            if (color & 32): result |= 32
            if (color & 64): result |= 16
            if (color & 128): result |= 128
            SetConsoleTextAttribute(handle, result)
        else:
            if color >= 0:
                foreground = color & 7
                background = (color >> 4) & 7
                bold = color & 8
                sys.stdout.write(" \033[%s3%d;4%dm"%(bold and "01;" or "", foreground, background))
                sys.stdout.flush()
            else:
                sys.stdout.write(" \033[0m")
                sys.stdout.flush()
        return 0
    
    # ��ɫ���
    def show (self):
        print('  A B C D E F G H I J K L M N O')
        mark = ('. ', 'O ', 'X ')
        nrow = 0
        self.check()
        color1 = 10
        color2 = 13
        for row in range(15):
            print(chr(ord('A') + row), end='')
            for col in range(15):
                ch = self.__board[row][col]
                if ch == 0: 
                    self.console(-1)
                    print('.', end='')
                elif ch == 1:
                    if (row, col) in self.won:
                        self.console(9)
                    else:
                        self.console(10)
                    print('O', end='')
                    #self.console(-1)
                elif ch == 2:
                    if (row, col) in self.won:
                        self.console(9)
                    else:
                        self.console(13)
                    print('X', end='')
                    #self.console(-1)
            self.console(-1)
            print('')
        return 0


#----------------------------------------------------------------------
# evaluation: ���������࣬����ǰ���̴����
#----------------------------------------------------------------------
class evaluation (object):

    def __init__ (self):
        self.POS = []
        for i in range(15):
            row = [ (7 - max(abs(i - 7), abs(j - 7))) for j in range(15) ]
            self.POS.append(tuple(row))
        self.POS = tuple(self.POS)
        self.STWO = 1       # ���
        self.STHREE = 2     # ����
        self.SFOUR = 3      # ����
        self.TWO = 4        # ���
        self.THREE = 5      # ����
        self.FOUR = 6       # ����
        self.FIVE = 7       # ����
        self.DFOUR = 8      # ˫��
        self.FOURT = 9      # ����
        self.DTHREE = 10    # ˫��
        self.NOTYPE = 11    
        self.ANALYSED = 255     # �Ѿ�������
        self.TODO = 0           # û�з�����
        self.result = [ 0 for i in range(30) ]     # ���浱ǰֱ�߷���ֵ
        self.line = [ 0 for i in range(30) ]       # ��ǰֱ������
        self.record = []            # ȫ�̷������ [row][col][����]
        for i in range(15):
            self.record.append([])
            self.record[i] = []
            for j in range(15):
                self.record[i].append([ 0, 0, 0, 0])
        self.count = []             # ÿ����ֵĸ�����count[����/����][ģʽ]
        for i in range(3):
            data = [ 0 for i in range(20) ]
            self.count.append(data)
        self.reset()

    # ��λ����
    def reset (self):
        TODO = self.TODO
        count = self.count
        for i in range(15):
            line = self.record[i]
            for j in range(15):
                line[j][0] = TODO
                line[j][1] = TODO
                line[j][2] = TODO
                line[j][3] = TODO
        for i in range(20):
            count[0][i] = 0
            count[1][i] = 0
            count[2][i] = 0
        return 0

    # �ĸ�����ˮƽ����ֱ����б����б�������������̣�Ȼ����ݷ���������
    def evaluate (self, board, turn):
        score = self.__evaluate(board, turn)
        count = self.count
        if score < -9000:
            stone = turn == 1 and 2 or 1
            for i in range(20):
                if count[stone][i] > 0:
                    score -= i
        elif score > 9000:
            stone = turn == 1 and 2 or 1
            for i in range(20):
                if count[turn][i] > 0:
                    score += i
        return score
    
    # �ĸ�����ˮƽ����ֱ����б����б�������������̣�Ȼ����ݷ���������
    def __evaluate (self, board, turn):
        record, count = self.record, self.count
        TODO, ANALYSED = self.TODO, self.ANALYSED
        self.reset()
        # �ĸ��������
        for i in range(15):
            boardrow = board[i]
            recordrow = record[i]
            for j in range(15):
                if boardrow[j] != 0:
                    if recordrow[j][0] == TODO:     # ˮƽû�з�������
                        self.__analysis_horizon(board, i, j)
                    if recordrow[j][1] == TODO:     # ��ֱû�з�������
                        self.__analysis_vertical(board, i, j)
                    if recordrow[j][2] == TODO:     # ��бû�з�������
                        self.__analysis_left(board, i, j)
                    if recordrow[j][3] == TODO:     # ��бû�з�����
                        self.__analysis_right(board, i, j)

        FIVE, FOUR, THREE, TWO = self.FIVE, self.FOUR, self.THREE, self.TWO
        SFOUR, STHREE, STWO = self.SFOUR, self.STHREE, self.STWO
        check = {}

        # �ֱ�԰��������㣺FIVE, FOUR, THREE, TWO�ȳ��ֵĴ���
        for c in (FIVE, FOUR, SFOUR, THREE, STHREE, TWO, STWO):
            check[c] = 1
        for i in range(15):
            for j in range(15):
                stone = board[i][j]
                if stone != 0:
                    for k in range(4):
                        ch = record[i][j][k]
                        if ch in check:
                            count[stone][ch] += 1
        
        # ��������������Ϸ��ط���
        BLACK, WHITE = 1, 2
        if turn == WHITE:           # ��ǰ�ǰ���
            if count[BLACK][FIVE]:
                return -9999
            if count[WHITE][FIVE]:
                return 9999
        else:                       # ��ǰ�Ǻ���
            if count[WHITE][FIVE]:
                return -9999
            if count[BLACK][FIVE]:
                return 9999
        
        # ��������������ģ����൱����һ������
        if count[WHITE][SFOUR] >= 2:
            count[WHITE][FOUR] += 1
        if count[BLACK][SFOUR] >= 2:
            count[BLACK][FOUR] += 1

        # ������
        wvalue, bvalue, win = 0, 0, 0
        if turn == WHITE:
            if count[WHITE][FOUR] > 0: return 9990
            if count[WHITE][SFOUR] > 0: return 9980
            if count[BLACK][FOUR] > 0: return -9970
            if count[BLACK][SFOUR] and count[BLACK][THREE]: 
                return -9960
            if count[WHITE][THREE] and count[BLACK][SFOUR] == 0:
                return 9950
            if  count[BLACK][THREE] > 1 and \
                count[WHITE][SFOUR] == 0 and \
                count[WHITE][THREE] == 0 and \
                count[WHITE][STHREE] == 0:
                    return -9940
            if count[WHITE][THREE] > 1:
                wvalue += 2000
            elif count[WHITE][THREE]:
                wvalue += 200
            if count[BLACK][THREE] > 1:
                bvalue += 500
            elif count[BLACK][THREE]:
                bvalue += 100
            if count[WHITE][STHREE]:
                wvalue += count[WHITE][STHREE] * 10
            if count[BLACK][STHREE]:
                bvalue += count[BLACK][STHREE] * 10
            if count[WHITE][TWO]:
                wvalue += count[WHITE][TWO] * 4
            if count[BLACK][TWO]:
                bvalue += count[BLACK][TWO] * 4
            if count[WHITE][STWO]:
                wvalue += count[WHITE][STWO]
            if count[BLACK][STWO]:
                bvalue += count[BLACK][STWO]
        else:
            if count[BLACK][FOUR] > 0: return 9990
            if count[BLACK][SFOUR] > 0: return 9980
            if count[WHITE][FOUR] > 0: return -9970
            if count[WHITE][SFOUR] and count[WHITE][THREE]:
                return -9960
            if count[BLACK][THREE] and count[WHITE][SFOUR] == 0:
                return 9950
            if  count[WHITE][THREE] > 1 and \
                count[BLACK][SFOUR] == 0 and \
                count[BLACK][THREE] == 0 and \
                count[BLACK][STHREE] == 0:
                    return -9940
            if count[BLACK][THREE] > 1:
                bvalue += 2000
            elif count[BLACK][THREE]:
                bvalue += 200
            if count[WHITE][THREE] > 1:
                wvalue += 500
            elif count[WHITE][THREE]:
                wvalue += 100
            if count[BLACK][STHREE]:
                bvalue += count[BLACK][STHREE] * 10
            if count[WHITE][STHREE]:
                wvalue += count[WHITE][STHREE] * 10
            if count[BLACK][TWO]:
                bvalue += count[BLACK][TWO] * 4
            if count[WHITE][TWO]:
                wvalue += count[WHITE][TWO] * 4
            if count[BLACK][STWO]:
                bvalue += count[BLACK][STWO]
            if count[WHITE][STWO]:
                wvalue += count[WHITE][STWO]
        
        # ����λ��Ȩֵ�����������ĵ�Ȩֵ��7������һ��-1������Ȧ��0
        wc, bc = 0, 0
        for i in range(15):
            for j in range(15):
                stone = board[i][j]
                if stone != 0:
                    if stone == WHITE:
                        wc += self.POS[i][j]
                    else:
                        bc += self.POS[i][j]
        wvalue += wc
        bvalue += bc
        
        if turn == WHITE:
            return wvalue - bvalue

        return bvalue - wvalue
    
    # ��������
    def __analysis_horizon (self, board, i, j):
        line, result, record = self.line, self.result, self.record
        TODO = self.TODO
        for x in range(15):
            line[x] = board[i][x]
        self.analysis_line(line, result, 15, j)
        for x in range(15):
            if result[x] != TODO:
                record[i][x][0] = result[x]
        return record[i][j][0]
    
    # ��������
    def __analysis_vertical (self, board, i, j):
        line, result, record = self.line, self.result, self.record
        TODO = self.TODO
        for x in range(15):
            line[x] = board[x][j]
        self.analysis_line(line, result, 15, i)
        for x in range(15):
            if result[x] != TODO:
                record[x][j][1] = result[x]
        return record[i][j][1]
    
    # ������б
    def __analysis_left (self, board, i, j):
        line, result, record = self.line, self.result, self.record
        TODO = self.TODO
        if i < j: x, y = j - i, 0
        else: x, y = 0, i - j
        k = 0
        while k < 15:
            if x + k > 14 or y + k > 14:
                break
            line[k] = board[y + k][x + k]
            k += 1
        self.analysis_line(line, result, k, j - x)
        for s in range(k):
            if result[s] != TODO:
                record[y + s][x + s][2] = result[s]
        return record[i][j][2]

    # ������б
    def __analysis_right (self, board, i, j):
        line, result, record = self.line, self.result, self.record
        TODO = self.TODO
        if 14 - i < j: x, y, realnum = j - 14 + i, 14, 14 - i
        else: x, y, realnum = 0, i + j, j
        k = 0
        while k < 15:
            if x + k > 14 or y - k < 0:
                break
            line[k] = board[y - k][x + k]
            k += 1
        self.analysis_line(line, result, k, j - x)
        for s in range(k):
            if result[s] != TODO:
                record[y - s][x + s][3] = result[s]
        return record[i][j][3]
    
    def test (self, board):
        self.reset()
        record = self.record
        TODO = self.TODO
        for i in range(15):
            for j in range(15):
                if board[i][j] != 0 and 1:
                    if self.record[i][j][0] == TODO:
                        self.__analysis_horizon(board, i, j)
                        pass
                    if self.record[i][j][1] == TODO:
                        self.__analysis_vertical(board, i, j)
                        pass
                    if self.record[i][j][2] == TODO:
                        self.__analysis_left(board, i, j)
                        pass
                    if self.record[i][j][3] == TODO:
                        self.__analysis_right(board, i, j)
                        pass
        return 0
    
    # ����һ���ߣ���������������
    def analysis_line (self, line, record, num, pos):
        TODO, ANALYSED = self.TODO, self.ANALYSED
        THREE, STHREE = self.THREE, self.STHREE
        FOUR, SFOUR = self.FOUR, self.SFOUR
        while len(line) < 30: line.append(0xf)
        while len(record) < 30: record.append(TODO)
        for i in range(num, 30):
            line[i] = 0xf
        for i in range(num):
            record[i] = TODO
        if num < 5:
            for i in range(num): 
                record[i] = ANALYSED
            return 0
        stone = line[pos]
        inverse = (0, 2, 1)[stone]
        num -= 1
        xl = pos
        xr = pos
        while xl > 0:       # ̽����߽�
            if line[xl - 1] != stone: break
            xl -= 1
        while xr < num:     # ̽���ұ߽�
            if line[xr + 1] != stone: break
            xr += 1
        left_range = xl
        right_range = xr
        while left_range > 0:       # ̽����߷�Χ���ǶԷ����ӵĸ������꣩
            if line[left_range - 1] == inverse: break
            left_range -= 1
        while right_range < num:    # ̽���ұ߷�Χ���ǶԷ����ӵĸ������꣩
            if line[right_range + 1] == inverse: break
            right_range += 1
        
        # �����ֱ�߷�ΧС�� 5����ֱ�ӷ���
        if right_range - left_range < 4:
            for k in range(left_range, right_range + 1):
                record[k] = ANALYSED
            return 0
        
        # �����Ѿ�������
        for k in range(xl, xr + 1):
            record[k] = ANALYSED
        
        srange = xr - xl

        # ����� 5��
        if srange >= 4: 
            record[pos] = self.FIVE
            return self.FIVE
        
        # ����� 4��
        if srange == 3: 
            leftfour = False    # �Ƿ�����ǿո�
            if xl > 0:
                if line[xl - 1] == 0:       # ����
                    leftfour = True
            if xr < num:
                if line[xr + 1] == 0:
                    if leftfour:
                        record[pos] = self.FOUR     # ����
                    else:
                        record[pos] = self.SFOUR    # ����
                else:
                    if leftfour:
                        record[pos] = self.SFOUR    # ����
            else:
                if leftfour:
                    record[pos] = self.SFOUR        # ����
            return record[pos]
        
        # ����� 3��
        if srange == 2:     # ����
            left3 = False   # �Ƿ�����ǿո�
            if xl > 0:
                if line[xl - 1] == 0:   # �������
                    if xl > 1 and line[xl - 2] == stone:
                        record[xl] = SFOUR
                        record[xl - 2] = ANALYSED
                    else:
                        left3 = True
                elif xr == num or line[xr + 1] != 0:
                    return 0
            if xr < num:
                if line[xr + 1] == 0:   # �ұ�����
                    if xr < num - 1 and line[xr + 2] == stone:
                        record[xr] = SFOUR  # XXX-X �൱�ڳ���
                        record[xr + 2] = ANALYSED
                    elif left3:
                        record[xr] = THREE
                    else:
                        record[xr] = STHREE
                elif record[xl] == SFOUR:
                    return record[xl]
                elif left3:
                    record[pos] = STHREE
            else:
                if record[xl] == SFOUR:
                    return record[xl]
                if left3:
                    record[pos] = STHREE
            return record[pos]
        
        # ����� 2��
        if srange == 1:     # ����
            left2 = False
            if xl > 2:
                if line[xl - 1] == 0:       # �������
                    if line[xl - 2] == stone:
                        if line[xl - 3] == stone:
                            record[xl - 3] = ANALYSED
                            record[xl - 2] = ANALYSED
                            record[xl] = SFOUR
                        elif line[xl - 3] == 0:
                            record[xl - 2] = ANALYSED
                            record[xl] = STHREE
                    else:
                        left2 = True
            if xr < num:
                if line[xr + 1] == 0:   # �������
                    if xr < num - 2 and line[xr + 2] == stone:
                        if line[xr + 3] == stone:
                            record[xr + 3] = ANALYSED
                            record[xr + 2] = ANALYSED
                            record[xr] = SFOUR
                        elif line[xr + 3] == 0:
                            record[xr + 2] = ANALYSED
                            record[xr] = left2 and THREE or STHREE
                    else:
                        if record[xl] == SFOUR:
                            return record[xl]
                        if record[xl] == STHREE:
                            record[xl] = THREE
                            return record[xl]
                        if left2:
                            record[pos] = self.TWO
                        else:
                            record[pos] = self.STWO
                else:
                    if record[xl] == SFOUR:
                        return record[xl]
                    if left2:
                        record[pos] = self.STWO
            return record[pos]
        return 0
    def textrec (self, direction = 0):
        text = []
        for i in range(15):
            line = ''
            for j in range(15):
                line += '%x '%(self.record[i][j][direction] & 0xf)
            text.append(line)
        return '\n'.join(text)


#----------------------------------------------------------------------
# DFS: ����������
#----------------------------------------------------------------------
class searcher (object):

    # ��ʼ��
    def __init__ (self):
        self.evaluator = evaluation()
        self.board = [ [ 0 for n in range(15) ] for i in range(15) ]
        self.gameover = 0
        self.overvalue = 0
        self.maxdepth = 3

    # ������ǰ��ֵ��߷�
    def genmove (self, turn):
        moves = []
        board = self.board
        POSES = self.evaluator.POS
        for i in range(15):
            for j in range(15):
                if board[i][j] == 0:
                    score = POSES[i][j]
                    moves.append((score, i, j))
        moves.sort()
        moves.reverse()
        return moves
    
    # �ݹ�������������ѷ���
    def __search (self, turn, depth, alpha = -0x7fffffff, beta = 0x7fffffff):

        # ���Ϊ�����������̲�����
        if depth <= 0:
            score = self.evaluator.evaluate(self.board, turn)
            return score

        # �����Ϸ������������
        score = self.evaluator.evaluate(self.board, turn)
        if abs(score) >= 9999 and depth < self.maxdepth: 
            return score

        # �����µ��߷�
        moves = self.genmove(turn)
        bestmove = None

        # ö�ٵ�ǰ�����߷�
        for score, row, col in moves:

            # ��ǵ�ǰ�߷�������
            self.board[row][col] = turn
            
            # ������һ�غϸ�˭��
            nturn = turn == 1 and 2 or 1

            # ��������������������֣��ߵ��к��ߵ���
            score = - self.__search(nturn, depth - 1, -beta, -alpha)

            # �����������ǰ�߷�
            self.board[row][col] = 0

            # ������÷�ֵ���߷�
            # alpha/beta ��֦
            if score > alpha:
                alpha = score
                bestmove = (row, col)
                if alpha >= beta:
                    break
        
        # ����ǵ�һ�����¼��õ��߷�
        if depth == self.maxdepth and bestmove:
            self.bestmove = bestmove

        # ���ص�ǰ��õķ������͸÷����Ķ�Ӧ�߷�
        return alpha

    # �������������뵱ǰ�Ǹ�˭��(turn=1/2)���Լ��������(depth)
    def search (self, turn, depth = 3):
        self.maxdepth = depth
        self.bestmove = None
        score = self.__search(turn, depth)
        if abs(score) > 8000:
            self.maxdepth = depth
            score = self.__search(turn, 1)
        row, col = self.bestmove
        return score, row, col


#----------------------------------------------------------------------
# psyco speedup
#----------------------------------------------------------------------
def psyco_speedup ():
    try:
        import psyco
        psyco.bind(chessboard)
        psyco.bind(evaluation)
    except:
        pass
    return 0

psyco_speedup()


#----------------------------------------------------------------------
# main game
#----------------------------------------------------------------------
def gamemain():
    b = chessboard()
    s = searcher()
    s.board = b.board()

    opening = [
        '1:HH 2:II',
        #'2:IG 2:GI 1:HH',
        '1:IH 2:GI',
        '1:HG 2:HI',
        #'2:HG 2:HI 1:HH',
        #'1:HH 2:IH 2:GI',
        #'1:HH 2:IH 2:HI',
        #'1:HH 2:IH 2:HJ',
        #'1:HG 2:HH 2:HI',
        #'1:GH 2:HH 2:HI',
    ]

    import random
    openid = random.randint(0, len(opening) - 1)
    b.loads(opening[openid])
    turn = 2
    history = []
    undo = False

    # �����Ѷ�
    DEPTH = 1

    if len(sys.argv) > 1:
        if sys.argv[1].lower() == 'hard':
            DEPTH = 2

    while 1:
        print('')
        while 1:
            print('<ROUND %d>'%(len(history) + 1))
            b.show()
            print('Your move (u:undo, q:quit):', end='')
            text = input().strip('\r\n\t ')
            if len(text) == 2:
                tr = ord(text[0].upper()) - ord('A')
                tc = ord(text[1].upper()) - ord('A')
                if tr >= 0 and tc >= 0 and tr < 15 and tc < 15:
                    if b[tr][tc] == 0:
                        row, col = tr, tc
                        break
                    else:
                        print('can not move there')
                else:
                    print('bad position')
            elif text.upper() == 'U':
                undo = True
                break
            elif text.upper() == 'Q':
                print(b.dumps())
                return 0
        
        if undo == True:
            undo = False
            if len(history) == 0:
                print('no history to undo')
            else:
                print('rollback from history ...')
                move = history.pop()
                b.loads(move)
        else:
            history.append(b.dumps())
            b[row][col] = 1

            if b.check() == 1:
                b.show()
                print(b.dumps())
                print('')
                print('YOU WIN !!')
                return 0

            print('robot is thinking now ...')
            score, row, col = s.search(2, DEPTH)
            cord = '%s%s'%(chr(ord('A') + row), chr(ord('A') + col))
            print('robot move to %s (%d)'%(cord, score))
            b[row][col] = 2

            if b.check() == 2:
                b.show()
                print(b.dumps())
                print('')
                print('YOU LOSE.')
                return 0

    return 0


#----------------------------------------------------------------------
# testing case
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        b = chessboard()
        b[10][10] = 1
        b[11][11] = 2
        for i in range(4):
            b[5 + i][2 + i] = 2
        for i in range(4):
            b[7 - 0][3 + i] = 2
        print(b)
        print('check', b.check())
        return 0
    def test2():
        b = chessboard()
        b[7][7] = 1
        b[8][8] = 2
        b[7][9] = 1
        eva = evaluation()
        for l in eva.POS: 
            print(l)
        return 0
    def test3():
        e = evaluation()
        line = [ 0, 0, 1, 0, 1, 1, 1, 0, 0, 0]
        record = []
        e.analysis_line(line, record, len(line), 6)
        print(record[:10])
        return 0
    def test4():
        b = chessboard()
        b.loads('2:DF 1:EG 2:FG 1:FH 2:FJ 2:GG 1:GH 1:GI 2:HG 1:HH 1:IG 2:IH 1:JF 2:JI 1:KE')
        b.loads('2:CE 2:CK 1:DF 1:DK 2:DL 1:EG 1:EI 1:EK 2:FG 1:FH 1:FI 1:FJ 1:FK 2:FL 1:GD 2:GE 2:GF 2:GG 2:GH 1:GI 1:GK 2:HG 1:HH 2:HJ 2:HK 2:IG 1:JG 2:AA')
        eva = evaluation()
        print(b)
        score = 0
        t = time.time()
        for i in range(10000):
            score = eva.evaluate(b.board(), 2)
        #eva.test(b.board())
        t = time.time() - t
        print(score, t)
        print(eva.textrec(3))
        return 0
    def test5():
        import profile
        profile.run("test4()", "prof.txt")
        import pstats
        p = pstats.Stats("prof.txt")
        p.sort_stats("time").print_stats()
    def test6():
        b = chessboard()
        b.loads('1:CJ 2:DJ 1:dk 1:DL 1:EH 1:EI 2:EJ 2:EK 2:FH 2:FI 2:FJ 1:FK 2:FL 1:FM 2:GF 1:GG 2:GH 2:GI 2:GJ 1:GK 1:GL 2:GM 1:HE 2:HF 2:HG 2:HH 2:HI 1:HJ 2:HK 2:HL 1:IF 1:IG 1:IH 2:II 1:IJ 2:IL 2:JG 1:JH 1:JI 1:JJ 1:JK 2:JL 1:JM 1:KI 2:KJ 1:KL 1:LJ 2:MK')
        #b.loads('1:HH,1:HI,1:HJ,1:HK')
        s = searcher()
        s.board = b.board()
        t = time.time()
        score, row, col = s.search(2, 3)
        t = time.time() - t
        b[row][col] = 2
        print(b)
        print(score, t)
        print(chr(ord('A') + row) + chr(ord('A') + col))
    def test7():
        b = chessboard()
        s = searcher()
        s.board = b.board()
        b.loads('2:HH 1:JF')
        turn = 2
        while 1:
            score, row, col = s.search(2, 2)
            print('robot move %s%s (%d)'%(chr(ord('A') + row), chr(ord('A') + col), score))
            b[row][col] = 2
            if b.check() == 2:
                print(b)
                print(b.dumps())
                print('you lose !!')
                return 0
            while 1:
                print(b)
                print('your move (pos):',)
                text = raw_input().strip('\r\n\t ')
                if len(text) == 2:
                    tr = ord(text[0].upper()) - ord('A')
                    tc = ord(text[1].upper()) - ord('A')
                    if tr >= 0 and tc >= 0 and tr < 15 and tc < 15:
                        if b[tr][tc] == 0:
                            row, col = tr, tc
                            break
                        else:
                            print('can not move there')
                    else:
                        print('bad position')
                elif text.upper() == 'Q':
                    print(b.dumps())
                    return 0
            b[row][col] = 1
            if b.check() == 1:
                print(b)
                print(b.dumps())
                print('you win !!')
                return 0
        return 0
    #test6()
    gamemain()



