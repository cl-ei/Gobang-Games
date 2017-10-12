class Tree():
    def __init__(self, score = 0, pos = (-1,-1)):
        self.score = score
        self.pos = pos
        self.ptr_sum = 0
        self.ptr = []
    def add(self,pointer):
        self.ptr_sum = self.ptr_sum + 1
        self.ptr = self.ptr + [pointer]

def cal_sub(tr):
    score = tr.score

    if tr.ptr_sum == 0 :
        return score
    else:
        for i in range(tr.ptr_sum):
            score = score + cal_sub(tr.ptr[i]) 
    return score

def cal_pos(tr):
    if tr.ptr_sum <= 1:
        return tr.ptr[0].pos
    else:
        old_score = tr.ptr[0].score
        best_pos = tr.ptr[0].pos
        for i in range(1,tr.ptr_sum):
            new_score = cal_sub(tr.ptr[i])
            if new_score > old_score:
                best_pos = tr.ptr[i].pos
                old_score = new_score

    return best_pos     

