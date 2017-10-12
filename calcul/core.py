"""
#_____wuziqi core____
#
#这一部分包含所有五子棋内核的计算
#
#包含
#    五子棋树的结构和相关操作方法
#    走棋顺序控制
#    价值判断方法等

"""

__author__ = "caoliang"

import time
from random import randint
from threading import Thread
from time import sleep
from copy import deepcopy


class Tree():
    def __init__(self, score = 0, pos = (-1,-1), ly = 0):
        self.score = score
        self.pos = pos
        self.ptr_sum = 0
        self.ptr = []
        self.layer = ly

    def add(self,pointer):
        self.ptr_sum = self.ptr_sum + 1
        pointer.layer = self.layer + 1
        self.ptr.append(pointer)

    def show(self):
        print("当前有：",self.ptr_sum,"个子节点")

    def find_ele(self,pos):
        for i in self.ptr:
            if pos == i.pos:
                return 1
        return 0

    def delete(self,ele):
        self.ptr_sum = self.ptr_sum - 1
        self.ptr.remove(ele)

def show_all(tr):
    print("layer: ",tr.layer,"score: ",tr.score,"pos: ",tr.pos)
    if tr.ptr_sum != 0:
        print('\n')
        for i in tr.ptr:
            show_all(i)

def show_layer(tr,ly):
    if tr.layer == ly:
        print("layer: ",tr.layer,"score: ",tr.score,"pos: ",tr.pos)
    if tr.ptr_sum != 0:
        for i in tr.ptr:
            show_layer(i,ly)

def copy_tree(new_tr,tr):
    for i in tr.ptr:
        new_tr.add(i)

def cut_branch_pl(tr):
    li = []

    for i in tr.ptr:
        li = li + [i.score]
    li.sort()

    best_level = li[0]

    for i in tr.ptr:
        if i.score > best_level:
            tr.delete(i)

def cut_branch_pc(new_tr,tr):
    li = []

    for i in tr.ptr:
        li = li + [i.score]

    li.sort()
    li.reverse()

    valid_step = len(li) - 1
    if valid_step > 8:
        valid_step = 8

    best_level = li[valid_step]
    for i in tr.ptr:
        if i.score >= best_level:
            new_tr.add(i)

def cut_branch(tr):
    li = []

    for i in tr.ptr:
        li = li + [i.score]

    li.sort()
    li.reverse()

    valid_step = len(li) - 1
    if valid_step > 8:
        valid_step = 8

    best_level = li[valid_step]
    for i in tr.ptr:
        if i.score >= best_level:
            new_tr.add(i)
            #计算每一个子树的分值
def cal_sub(tr):
    if tr.ptr_sum == 0 :
        return tr.score
    else:
        score = tr.score
        for i in tr.ptr:
            score = score + cal_sub(i)
        return score

        #寻找tr 所有子树中最大的一支,并弹出该子树
def cal_max_branch(tr):
    if tr.ptr_sum == 0:
        return tr
    else:
        max_score = -9000000

        for i in tr.ptr:
            new_score = cal_sub(i)

            #统计最大值
            if new_score > max_score:
                max_score = new_score
                best_ptr = i

        return best_ptr

class Core():
    def __init__(self):

        #棋盘：0为空位，1为玩家落子，2为电脑落子
        self.table   = [([0] * 15) for i in range(15)]

        self.busy        = 0
        self.who_win     = 0

        #行棋的记录
        self.index   = 0
        self.step    = [([0] * 2) for i in range(226)]

        #上一步行棋在4个方向上的其他棋子数
        self.last_pcs_dirction   = [0,0,0,0]

        #评分表
        self.table_type =['aaaaa',
                          '?aaaa?',

                          'aaaa?','?aaaa',
                          'aaa?a','a?aaa',

                          'aa?aa',
                          '??aaa??',

                          'aaa??','??aaa',
                          '?a?aa?','?aa?a?',
                          'a??aa','aa??a',

                          'a?a?a',
                          '???aa???',

                          'aa???','???aa',

                          '??a?a??',
                          '?a??a?']
        self.table_score=[8000000,
                          300000,

                          2500,2500,
                          3000,3000,

                          2600,
                          3000,

                          500,500,
                          800,800,
                          600,600,

                          550,
                          650,

                          150,150,

                          250,
                          200]

        #玩家走一步棋
    def player_take(self,pos = (0,0)):

        if self.table[pos[0]][pos[1]] == 0:
            self.table[pos[0]][pos[1]] = 1

            self.index = self.index + 1
            self.step[self.index] = pos

            self.test_player()
            if self.who_win == 0:
                self.computer_ctl()

                #电脑走棋控制函数
    def computer_ctl(self):
        if self.busy == 0 :
            self.busy = 1
            if self.index<2:
                task = Thread(target=self.computer_take_first,args=(0,))
            else:
                task = Thread(target=self.computer_take,args=(0,))
            task.start()
            return 1
        return 0

    #电脑走第一步
    def computer_take_first(self,tmp):
        sleep(0.6)
        if self.index == 0:
            self.table[7][7] == 2
            self.index = self.index + 1
            self.step[self.index] = (7,7)

        elif self.index == 1:
            tab_map = [[0,-1],[0,1],[-1,0],[1,0],
                       [1,-1],[1,1],[-1,-1],[-1,1]]

            if self.step[1] == (7,7):
                x,y = tab_map[randint(0,7)]
                self.table[7+x][7+y] = 2
                self.index = self.index + 1
                self.step[self.index] = (7+x,7+y)

            else:
                x , y = self.step[self.index]
                x = x - 7
                y = y - 7
                if x > 0:
                    x = 1
                if x < 0:
                    x = -1
                if y > 0:
                    y = 1
                if y < 0:
                    y = -1

                x = self.step[self.index][0]-x
                y = self.step[self.index][1]-y

                self.table[x][y] = 2
                self.index = self.index + 1
                self.step[self.index] = (x,y)

        else:
            print("Error! self.index out of range !")

        self.busy = 0

    #电脑走第二步以后
    def computer_take(self,tmp):

        top_map = Tree()
        self.fill_tree_computer_layer(self.table,top_map,depth = 2)

        #计算最大的子树，并弹出该坐标
        x,y = cal_max_branch(top_map).pos

        self.table[x][y] = 2
        self.index = self.index + 1
        self.step[self.index] = [x,y]

        self.test_computer()
        self.busy = 0

    #迭代：玩家走下一步
    def fill_tree_player_layer(self,table,top_map,depth):

        for j in range(15):
            for i in range(15):
                if table[i][j] == 0:
                    score = self.cal_single_pcs_value(table,[i,j],1)
                    if score != 0:
                        node = Tree(0-score,(i,j))
                        top_map.add(node)


        dep = depth - 1

        #深度大于0，需要迭代下一次
        if dep > 0:

            #接下来把对对方有利的落子点，也添加到这里        
            for j in range(15):
                for i in range(15):
                    if table[i][j] == 0:
                        score = self.cal_single_pcs_value(table,[i,j],2)
                        if score != 0 and top_map.find_ele((i,j))==0:
                            node = Tree(0,(i,j))
                            top_map.add(node)

            #下一次迭代
            for i in top_map.ptr:
                if i.score > -8000000:
                    tab = deepcopy(table)
                    x,y = i.pos
                    tab[x][y] = 1
                    self.fill_tree_computer_layer(tab,i,dep)

        #深度到底，不进行下一次，剪掉不值得的走棋点
        else:
            cut_branch_pl(top_map)

    #迭代：假设电脑走下一步
    def fill_tree_computer_layer(self,table,top_map,depth):

        for j in range(15):
            for i in range(15):
                if table[i][j] == 0:
                    score = self.cal_single_pcs_value(table,[i,j],2)
                    if score != 0:
                        node = Tree(score,(i,j))
                        top_map.add(node)

        #剪枝完毕，确认是否要进行下一次迭代
        dep = depth - 1
        if dep > 0:
            #接下来把对对方有利的落子点，也添加到这里        
            for j in range(15):
                for i in range(15):
                    if table[i][j] == 0:
                        score = self.cal_single_pcs_value(table,[i,j],1)
                        if score != 0 and top_map.find_ele((i,j))==0:
                            node = Tree(0,(i,j))
                            top_map.add(node)

            for i in top_map.ptr:
                if i.score < 8000000:
                    tab = deepcopy(table)
                    x,y = i.pos
                    tab[x][y] = 2
                    self.fill_tree_player_layer(tab,i,dep)

    #判断落子点周围四个方向上，连成最长一串的棋子的个数       
    def cal_sum_arround(self,table=[],pos = (0,0),key = 1):

        x,y = pos
        five_p = [0,0,0,0, 0,0,0,0]

        #判断 8个方向上的棋子数

        for i in range(1,5):
            if (x-i)> -1 and table[x-i][y] == key:
                five_p[0] = five_p[0] + 1
            else:
                break

        for i in range(1,5):
            if (x-i)>-1 and (y-i)>-1 and table[x-i][y-i] == key:
                five_p[1] = five_p[1] + 1
            else:
                break

        for i in range(1,5):
            if (y-i)>-1 and table[x][y-i] == key:
                five_p[2] = five_p[2] + 1
            else:
                break

        for i in range(1,5):
            if (x+i)<15 and (y-i)>-1 and table[x+i][y-i] == key:
                five_p[3] = five_p[3] + 1
            else:
                break

        for i in range(1,5):
            if (x+i)<15 and table[x+i][y] == key:
                five_p[4] = five_p[4] + 1
            else:
                break

        for i in range(1,5):
            if (x+i)<15 and (y+i)<15 and table[x+i][y+i] == key:
                five_p[5] = five_p[5] + 1
            else:
                break

        for i in range(1,5):
            if (y+i)<15 and table[x][y+i] == key:
                five_p[6] = five_p[6] + 1
            else:
                break
        for i in range(1,5):
            if (x-i)>-1 and (y+i)<15 and table[x-i][y+i] == key:
                five_p[7] = five_p[7] + 1
            else:
                break
        #--------------------------------------#
        dir=[0,0,0,0]
        for i in range(4):
            dir[i] = five_p[i] + five_p[i+4]
        return dir

    #检测玩家是否胜利
    def test_player(self):
        self.last_pcs_dirction = self.cal_sum_arround(self.table,self.step[self.index])
        for i in range(4):
            if self.last_pcs_dirction[i] >=4:
                self.who_win = 1
                break

    def test_computer(self):
        self.last_pcs_dirction = self.cal_sum_arround(self.table,self.step[self.index],2)
        for i in range(4):
            if self.last_pcs_dirction[i] >=4:
                self.who_win = 2
                break

    #获取落子点周围四个方向上的棋型
    def get_chess_type(self,table=[],pos = (0,0),key = 1):
        x,y = pos
        chess_type = ['' for i in range(8)]

        #判断 8个方向上的棋子数
        for i in range(1,5):
            if (x-i) < 0:
                break
            elif table[x-i][y] == key :
                chess_type[0] = chess_type[0] + 'a'
            elif table[x-i][y] == 0 :
                chess_type[0] = chess_type[0] + '?'
            else:
                break

        for i in range(1,5):
            if (x-i) < 0 or  (y-i) < 0:
                break
            elif table[x-i][y-i] == key :
                chess_type[1] = chess_type[1] + 'a'
            elif table[x-i][y-i] == 0 :
                chess_type[1] = chess_type[1] + '?'
            else:
                break

        for i in range(1,5):
            if (y-i) < 0 :
                break
            elif table[x][y-i] == key :
                chess_type[2] = chess_type[2] + 'a'
            elif table[x][y-i] == 0 :
                chess_type[2] = chess_type[2] + '?'
            else:
                break

        for i in range(1,5):
            if (x+i)>14 or (y-i) < 0 :
                break
            elif table[x+i][y-i] == key :
                chess_type[3] = chess_type[3] + 'a'
            elif table[x+i][y-i]  == 0 :
                chess_type[3] = chess_type[3] + '?'
            else:
                break
        # 后4个方向

        for i in range(1,5):
            if (x+i)>14:
                break
            elif table[x+i][y] == key :
                chess_type[4] = chess_type[4] + 'a'
            elif table[x+i][y] == 0 :
                chess_type[4] = chess_type[4] + '?'
            else:
                break

        for i in range(1,5):
            if (x+i)>14 or (y+i)>14:
                break
            elif table[x+i][y+i] == key:
                chess_type[5] = chess_type[5] + 'a'
            elif table[x+i][y+i] == 0:
                chess_type[5] = chess_type[5] + '?'
            else:
                break

        for i in range(1,5):
            if (y+i)>14:
                break
            elif table[x][y+i] == key:
                chess_type[6] = chess_type[6] + 'a'
            elif table[x][y+i] == 0:
                chess_type[6] = chess_type[6] + '?'
            else:
                break
        for i in range(1,5):
            if (x-i)<0 or (y+i)>14:
                break
            elif table[x-i][y+i] == key:
                chess_type[7] = chess_type[7] + 'a'
            elif table[x-i][y+i] == 0:
                chess_type[7] = chess_type[7] + '?'
            else:
                break
        #--------------------------------------#
        chess_type_4_dir = ['' for i in range(4)]

        for i in range(4):
            chess_type_4_dir[i] = chess_type[i][::-1] + 'a' + chess_type[i+4]
        return chess_type_4_dir

    def cal_single_pcs_value(self,table=[],pos = (0,0),key = 1):
        pcs_type = self.get_chess_type(table,pos,key)
        score = 0
        for i in range(4):
            for j in range(20):
                if pcs_type[i].find(self.table_type[j]) > -1:
                    score = score + self.table_score[j]
        return score

    #回退一步，悔棋函数
    def go_back(self):
        if self.index>=2:
            if self.who_win == 1:
                self.who_win = 0
                #将棋盘最后1步归0                       
                x,y=self.step[self.index]
                self.table[x][y] = 0

                print("tuihui:",x,y)
                self.index -= 1
                return 1
            else:
                self.who_win = 0
                #将棋盘最后2步归0
                for i in range(2):
                    x,y=self.step[self.index]
                    self.table[x][y] = 0

                    print("tuihui:",x,y)
                    self.index -= 1
                return 1
        else:
            return 0

    #提示函数
    def go_ahead(self):
        top_map = Tree()
        self.fill_tree_player_layer(self.table,top_map,1)
        self.player_take(cal_max_branch(top_map).pos)


def test():
    print("core is running !")

if __name__=='__main__':
    test()
