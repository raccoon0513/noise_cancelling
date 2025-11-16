import numpy as np
import matplotlib.pyplot as plt
import pyaudio

CHUNK = 1024  # 한 번에 처리할 샘플 수
FORMAT = pyaudio.paInt16 # 샘플 형식 (16비트 정수)
CHANNELS = 1 # 모노
RATE = 44100 # 샘플링 레이트 (Hz)
DURATION = 0.05 # 그래프를 업데이트할 시간 간격 (초)

p = pyaudio.PyAudio()

try:
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
except Exception as e:
    print(f"오디오 스트림을 여는 데 실패했습니다. 장치 설정 및 권한을 확인하세요: {e}")
    p.terminate()
    exit()

#=======matplotlib 그래프 설정=======
fig, ax = plt.subplots(1, figsize=(10, 4)) # Axis(단수형) or Axes(복수형) matplotlib 자주 쓰이는 변수명
x = np.arange(0, CHUNK) # X축 데이터(시간 도메인)
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)

# 축 범위 설정
max = 2**12 #기존 2**15
ax.set_ylim(-1*max, max) # 2**15 = 16비트 정수의 범위 (-32768 ~ 32767)
ax.set_xlim(0, CHUNK)
ax.set_xticks([]) # X축  눈금 제거
ax.set_yticks([-1*max, 0, max])
ax.set_ylabel("amplitude")
ax.set_xlabel("(sliced_sample_number)", ha="left", x=0)
ax.grid()

def update_plot(frame):
    """그래프 업데이트"""
    try:
        # 오디오 데이터 읽기
        data = stream.read(CHUNK, exception_on_overflow=False)
    except IOError:
        # 오디오 버퍼 오버플로우 발생 시
        print("IOError: Audio buffer overflow occurred.")
        return line,

    # 16비트 정수형 데이터로 변환
    data_int = np.frombuffer(data, dtype=np.int16)

    # 그래프 데이터 업데이트
    line.set_ydata(data_int)
    
    return line,

# --- 5. 애니메이션 시작 및 실행 ---
from matplotlib.animation import FuncAnimation

# FuncAnimation을 사용하여 지정된 간격으로 update_plot 함수 호출
ani = FuncAnimation(fig, update_plot, interval=DURATION * 1000)

try:
    plt.show() # 그래프 창 표시
except KeyboardInterrupt:
    pass # Ctrl+C 입력 시 종료

# --- 6. 정리 ---
stream.stop_stream()
stream.close()
p.terminate()
print("\n스트림 종료 및 리소스 해제 완료.")