import numpy as np
import matplotlib.pyplot as plt
import math

DURATION = 0.05 # 그래프를 업데이트할 시간 간격 (초)
CHUNK = 10

#=======matplotlib 그래프 설정=======
fig, ax = plt.subplots(1, figsize=(10, 4)) # Axis(단수형) or Axes(복수형) matplotlib 자주 쓰이는 변수명
x = np.arange(0, CHUNK) # X축 데이터(시간 도메인)
line, = ax.plot(x, np.random.rand(10), '-', lw=2) #lw = line Weight

# 축 범위 설정

y_max = 100
x_max = math.pi * 2
ax.set_ylim(-1*y_max, y_max) # 2**15 = 16비트 정수의 범위 (-32768 ~ 32767)
ax.set_xlim(CHUNK*-1, CHUNK)
ax.set_xticks([x_max*-1, 0, x_max]) # X축  눈금 제거
ax.set_yticks([-1*y_max, 0, y_max])
ax.set_ylabel("amplitude")
# ax.set_xlabel("-x", ha="left", x=0)
ax.grid()

def update_plot(frame):
    """그래프 업데이트"""
    
    # 16비트 정수형 데이터로 변환
    # data_int = np.frombuffer(data, dtype=np.int16)

    # # 그래프 데이터 업데이트
    # line.set_ydata(data_int)
    return
    # return line,

# --- 5. 애니메이션 시작 및 실행 ---
from matplotlib.animation import FuncAnimation

# FuncAnimation을 사용하여 지정된 간격으로 update_plot 함수 호출
ani = FuncAnimation(fig, update_plot, interval=DURATION * 1000)

try:
    plt.show() # 그래프 창 표시
except KeyboardInterrupt:
    pass # Ctrl+C 입력 시 종료

# --- 6. 정리 ---

print("\n스트림 종료 및 리소스 해제 완료.")