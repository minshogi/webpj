class ProbNStack:
    def __init__(self, _p_ = 0.0, _s_ = 0):
        self.probability_ = _p_
        self.stack_ = _s_
    
    def GetProb(self):
        return self.probability_

    def GetStack(self):
        return self.stack_

    def SetProb(self, prob):
        res = self.probability_ != prob
        self.probability_ = prob
        return res

    def SetStack(self, stack):
        res = self.stack_ != stack
        self.stack_ = stack
        return res
