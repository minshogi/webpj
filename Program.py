from CalProb import CalProb

stack = int(input('현재 쌓인 스택값 입력: '))
getPic_ = input('전에 픽업캐 뽑았나?(Y/N) ')
getPic = False

if getPic_ == 'Y' or getPic_ == 'y':
    getPic = True

cp= CalProb(stack, getPic)
gacha = int(input('지를 수 있는 가챠 수 > '))

ndol = int(input('뽑고자 하는 픽업캐 돌파 수(명함 = 1) > '))

result = cp.GetDP(ndol, stack + gacha)

print('{}연차 내로 뽑을 확률 = {}%'.format(gacha, result * 100))
