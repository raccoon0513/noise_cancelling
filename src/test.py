import math
#quiz : int 1 to 3  x^3 dx 
# result = n^4/4 + C,81/4-1/4  = 20
# h/2 ( f(a) + f(b))+ (h * sigma {i=1}{n-1}{f(a+(i*h))})

def f(x):
    """적분할 함수"""
    return math.sqrt(math.sin(x)-(math.sin(x)**3))
    # return x**2

def integral (f,a,b,n):
    """f=함수
    a=시작점
    b=도착점
    n=알고리즘 시도할 횟수"""
    h=(b-a)/n #h=func{a}{b}
    result=(f(a)+f(b))/2
    for i in range(1,n):
        result += (f(a+(i*h)))
    return result*h

def floor_n(num, n):
    """인수, n번째 자리까지 표시"""
    return math.floor(num * (10**n) ) / (10**n)

round = 4 #몇번째 자리까지 비교할 것인가
answer = floor_n(2/3, round)
a=0
b=(math.pi/2)

# answer = floor_n(2+(1/3), round)
# a=1
# b=2
# ===============================================================
upper = 10000 #더하는 수
def answer_check(n):
    submit = integral(f, a,b, n)
    if(answer==floor_n(submit, round)):
        return True
    return False
def find_count(count, upper):
    """몇번째 회차인지"""
    # print(f"No.{count}, trying...")
    div_upper = math.floor(upper/10)
    if(div_upper<1):
        return count, div_upper
    if(answer_check(count)):
        return find_count(count-upper, div_upper)
    if(not answer_check(count)):
        return find_count(count+upper, upper)
    return count
best_count = find_count(1, upper)[0]
print(best_count)
print(integral(f, a, b, best_count))    
print(f"정답은 {answer}\n근사치는 {integral(f, a, b, best_count)}\n시도 횟수 {best_count}")
# ===============================================================
