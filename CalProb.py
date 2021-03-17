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
    stack_ %= GACHA_SIZE
    condp = pic5Nth(p_, q_, stack_)
    if stack_ >= AMPLIFY and stack_ < GACHA_SIZE:
        condp = condp / q_ * (1-q_)
    elif stack_ < AMPLIFY:
        condp = condp / p_ * (1-p_)
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
    def __init__(self, stack_ = 0, getPic = True):
        #self.p = 0.006
        #self.q = 0.3235613866818617
        self.initializeTable()
        self.InitializeBasicProb(stack_, getPic)
        self.gen_dp(stack_, getPic)

    def initializeTable(self):
        #ProbNStack objects
        self.want = list()
        self.nowant = list()
        
        #double list
        self.prob = list()

        for _ in range(3):
            inner_want = list()
            inner_nowant = list()
            for _ in range(GACHA_SIZE + 1):
                inner_nowant.append(ProbNStack())
                inner_want.append(ProbNStack())
            self.want.append(inner_want)
            self.nowant.append(inner_nowant)
        
        self.dp = list()
        for _ in range(DOL_SIZE + 1):
            inner_pns = list()
            for j in range(MAX_GACHA + 1):
                inner_pns.append(ProbNStack())
            
            self.dp.append(inner_pns)
        
        for j in range(GACHA_SIZE + 1):
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
            *   i번째 stage에서 j개의 가챠를 돌려서 5성을 획득할 확률
            *   그리고 그것은 내가 원하는 것(want)과 원하지 않는 것(nowant)로 따로 분류
            *   i-1번째에서 만약 k개의 가챠만에 나온 확률에 j개의 가챠를 돌려서 5성을 얻으면 w_ijk
            *   3차원을 하지 말고, 데이터 구조를 활용
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
        return self.want[0][gacha].GetProb()
    
    def gen_dp(self, stack_, getPic):
        for j in range(MAX_GACHA + 1):
            self.dp[1][j].SetProb(self.first_pic(j, WANT))    # 기본 첫 스테이지
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
            for j in range(MAX_GACHA + 1): # 전체 가챠 스테이지에서 사용하는 가차권 j개
                k = 1
                while k < j and k <= GACHA_SIZE:   # 이번 가챠 스테이지에서 사용하는 가차권 k개
                    dpnj, pp = 0.0, 0.0
                    if n % 2 == 0:  # 픽뚫 확률 (짝수는 못 뽑는 거)
                        dpnj = self.dp[n][j].GetProb()
                        pp = self.dp[n-1][j - k].GetProb() * self.prob_on_pic(k, NOWANT)
                        if dpnj < pp:
                            self.dp[n][j].SetProb(pp)
                            self.dp[n][j].SetStack(k)

                    else:    # 픽업-픽업 또는 픽뚫-픽업 (홀수는 뽑는 거)
                        pp = self.dp[n-2][j-k].GetProb() * self.prob_on_pic(k, WANT)
                        np = self.dp[n-1][j-k].GetProb() * self.prob_on_nopic(k)
                        dpnj = self.dp[n][j].GetProb()
                        if dpnj < pp + np:
                            self.dp[n][j].SetProb(pp + np)
                            self.dp[n][j].SetStack(k)

                    if self.dp[n][j].GetProb() >= 1.0:
                        self.dp[n][j].SetProb(1.0)

                    self.dp[n][j].SetStack(k)

                    k += 1
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
        p_, q_ = p, q

        if getPic:
            p_ = p / 2
            q_ = q / 2

        condp = calCondP(p_, q_, stack_)
        
        i = stack_ + 1
        while i <= stack_ + nyeoncha and i <= GACHA_SIZE:
            prob += pic5Nth(p_, q_, i)
            i += 1
        if condp != 0.0:
            return prob / condp
        return prob

 