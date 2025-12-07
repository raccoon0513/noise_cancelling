import math
def integral (f,a,b,n):
    """f=함수
    a=시작점
    b=도착점
    n=알고리즘 시도할 횟수"""
    h=(b-a)/n 
    result=(f(a)+f(b))/2
    for i in range(1,n):
        result += (f(a+(i*h)))
    return result*h

def compare(return_value, answers):
    """approximation(근사값)"""
    approximation = min(answers,key=lambda x: abs(x-return_value))
    answer_index = answers.index(approximation)
    return answer_index
# ===============================================================
#문제 : \int_{1}^{2}\frac{\sqrt{4}}{3}\left(x+x\ln x\right)dx
quiz = lambda x : ((math.sqrt(3)/4)*(x+(x*math.log(x))))
answers = [
    (math.sqrt(3) * (3 + (8 * math.log(2)))) / 16,
    (math.sqrt(3) * (5 + (12 * math.log(2)))) / 24,
    (math.sqrt(3) * (1 + (12 * math.log(2)))) / 16,
    (math.sqrt(3) * (1 + (2 * math.log(2)))) / 4,
    (math.sqrt(3) * (1 + (9 * math.log(2)))) / 12
]

return_value = integral(f=quiz, a=1, b=2, n=10000)
answer_index = compare(return_value=return_value, answers=answers)
print(f"구한 근사치는 {return_value}")
print(f"답은 {answer_index+1}번, {answers[answer_index]}")
# ===============================================================