from ProbNStack import ProbNStack

p = 0.006
q = 0.3235613866818617

DOL_SIZE = 14
GACHA_SIZE = 90
WANT = 1
NOWANT = 0
MAX_GACHA = 1260
AMPLIFY = 74

def pic5Nth(p_, q_, nth):
    pk = 0.0
    if nth < AMPLIFY:
        pk = pow(1-p, nth - 1) * p_

    elif nth < GACHA_SIZE:
        pk = pow(1-p, AMPLIFY - 1) * pow(1-q, nth - AMPLIFY) * q_
    
    elif nth >= GACHA_SIZE:
        pk = pow(1-p, AMPLIFY - 1) * pow(1-q, GACHA_SIZE - AMPLIFY)

    return pk

def calCondP(p_, q_, stack_):
    condp = pic5Nth(p_, q_, stack_)
    if stack_ >= AMPLIFY and stack_ < GACHA_SIZE:
        condp /= q_
    elif stack_ < AMPLIFY:
        condp /= p_
    return condp

def DoubleMax(a, b):
    if a > b:
        return a
    return b

def GetBasicP():
    return p

def GetBasicQ():
    return q
 
class CalProb:
    def __init__(self, stack_, getPic):
        #self.p = 0.006
        #self.q = 0.3235613866818617

        #ProbNStack objects
        self.want = list()
        self.nowant = list()
        
        #double list
        self.prob = list()

        for i in range(3):
            self.want.append(list())
            self.nowant.append(list())
            for j in range(GACHA_SIZE + 1):
                self.want[i].append(ProbNStack())
                self.nowant[i].append(ProbNStack())
        
        self.dp = list()
        for i in range(DOL_SIZE + 1):
            self.dp.append(list())
            for j in range(MAX_GACHA + 1):
                self.dp[i].append(ProbNStack())
                self.prob.append(pic5Nth(p, q, j))

    def InitializeBasicProb(self, stack_, getPic):
        j = 1
        self.want[1][0].SetStack(stack_)
        self.nowant[1][0].SetStack(stack_)

        while j <= stack_:
            self.want[1][j].SetStack(j)
            self.nowant[1][j].SetStack(j)
            j += 1
        while j <= GACHA_SIZE:
            self.want[1][j].SetProb(self.picWhatIwantInN(stack_, j - stack_, getPic))
            self.nowant[1][j].SetProb(self.picWhatIdonWantInN(stack_, j - stack_, getPic))
            j += 1

        for j in range(1, GACHA_SIZE + 1):
            self.want[2][j].SetProb(self.picWhatIwantInN(0, j, True))
            self.nowant[2][j].SetProb(self.picWhatIdonWantInN(0, j, True))
                
        for j in range(1, GACHA_SIZE + 1):
            self.want[0][j].SetProb(self.picWhatIwantInN(0, j, False))

    def first_pic(self, gacha, cond):
        if gacha >= GACHA_SIZE:
            gacha = GACHA_SIZE
        elif gacha <= 0:
            return 0.0
        """
            w_i = 2/3*prob^T * w_(i-1) + prob^T * n_(i-1)
            *   n_i = 1/3*prob^T * w_(i-1)
            *   i?????? stage?????? j?????? ????????? ????????? 5?????? ????????? ??????
            *   ????????? ????????? ?????? ????????? ???(want)??? ????????? ?????? ???(nowant)??? ?????? ??????
            *   i-1???????????? ?????? k?????? ???????????? ?????? ????????? j?????? ????????? ????????? 5?????? ????????? w_ijk
            *   3????????? ?????? ??????, ????????? ????????? ??????
        """
        if cond == WANT:
            return self.want[1][gacha].GetProb()
        elif cond == NOWANT:
            return self.nowant[1][gacha].GetProb()
            
        return 0.0

    def prob_on_pic(self, gacha, cond):
        if cond == WANT:
            return self.want[2][gacha].GetProb()
        elif cond == NOWANT:
            return self.nowant[2][gacha].GetProb()
        return 0.0

    def prob_on_nopic(self, gacha):
        return self.want[0][gacha].getProb()
    
    def gen_dp(self, stack_, getPic):
        for j in range(MAX_GACHA + 1):
            self.dp[1][j].SetProb(self.first_pic(j, WANT))    # ?????? ??? ????????????
            self.dp[1][j].SetStack(j)
            
            if j > GACHA_SIZE and getPic:
                k = 1
                while k < j and k <= GACHA_SIZE:
                    dp1j = self.dp[1][j].GetProb()
                    np = self.picWhatIdonWantInN(stack_, j-k, getPic) * self.picWhatIwantInN(0, k, False)
                    dn = self.dp[1][j-k].GetProb() + np
                    
                    if dp1j < dn:
                        self.dp[1][j].SetProb(dn)
                        self.dp[1][j].SetStack(k)

                    k += 1

                if self.dp[1][j].GetProb() >= 1.0:
                    self.dp[1][j].SetProb(1.0)

        for n in range(DOL_SIZE + 1):
            for j in range(MAX_GACHA + 1): # ?????? ?????? ?????????????????? ???????????? ????????? j???
                k = 1
                while k < j and k <= GACHA_SIZE:   # ?????? ?????? ?????????????????? ???????????? ????????? k???
                    dpnj, pp = 0.0, 0.0
                    if n % 2 == 0:  # ?????? ?????? (????????? ??? ?????? ???)
                        dpnj = self.dp[n][j].GetProb()
                        pp = self.dp[n-1][j - k].GetProb() * self.prob_on_pic(k, NOWANT)
                        if dpnj < pp:
                            self.dp[n][j].SetProb(pp)
                            self.dp[n][j].SetStack(k)

                    else:    # ??????-?????? ?????? ??????-?????? (????????? ?????? ???)
                        pp = self.dp[n-2][j-k].GetProb() * self.prob_on_pic(k, WANT)
                        np = self.dp[n-1][j-k].GetProb() * self.prob_on_nopic(k)
                        dpnj = self.dp[n][j].GetProb()
                        if dpnj < pp + np:
                            self.dp[n][j].SetProb(pp + np)
                            self.dp[n][j].SetStack(k)

                    if self.dp[n][j].GetProb() >= 1.0:
                        self.dp[n][j].SetProb(1.0)

                    self.dp[n][j].SetStack(k)
                # while end
            # for j end
        # for n end
    # def gen_dp end

    
    
    def GetDP(self, ndol, gacha):
        return self.dp[ndol * 2 - 1][gacha].GetProb()

    def picWhatIdonWantInN(self, stack_, nyeoncha, getPic):
        if nyeoncha <= 0:
            return 0.0

        if not getPic:
            return 0.0

        elif stack_ + nyeoncha >= GACHA_SIZE:
            return 0.5

        prob = 0.0
        p_ = p / 2
        q_ = q / 2

        i = stack_ + 1
        while i <= stack_ + nyeoncha and i <= GACHA_SIZE:
            prob += pic5Nth(p_, q_, i)
            i += 1

        return prob

    def picWhatIwantInN(self, stack_, nyeoncha, getPic):
        if nyeoncha <= 0:
            return 0.0
        
        prob = 0.0
        p_, q_ = 0.0, 0.0

        if getPic:
            p_ = p / 2
            q_ = q / 2
        else:
            p_ = p
            q_ = q

        condp = calCondP(p_, q_, stack_)
        
        i = stack_ + 1
        while i <= stack_ + nyeoncha and i <= GACHA_SIZE:
            prob += pic5Nth(p_, q_, i)
            i += 1

        return prob / condp

 