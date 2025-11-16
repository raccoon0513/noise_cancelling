import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyaudio

CHUNK = 1024  # 한 번에 처리할 샘플 수
FORMAT = pyaudio.paInt16 # 샘플 형식 (16비트 정수)
CHANNELS = 1 # 모노
RATE = 44100 # 샘플링 레이트 (Hz)
DURATION = 0.05 # 그래프를 업데이트할 시간 간격 (초)

#큐베이스와 비슷하게 가시형 주파수 설정함
CUSTOM_TICKS = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]

# --- 2. PyAudio 초기화 및 기본 입력 장치 사용 ---
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

#===========그래프 설정(주파수 스펙트럼)======
fig, ax = plt.subplots(1, figsize=(10, 4))

# 주파수 축 계산: 0부터 샘플링 레이트의 절반(나이퀴스트 주파수)까지
xf = np.fft.fftfreq(CHUNK, d=1/RATE)[:CHUNK//2] 
line, = ax.plot(xf, np.zeros(CHUNK//2), '-', lw=2)

ax.set_xscale('log') #x축 스케일 로그로 설정
ax.set_xticks(CUSTOM_TICKS)#x축 눈금 CUSTOM_TICKS로
ax.get_xaxis().set_major_formatter(plt.ScalarFormatter()) # 눈금 라벨을 정수로 표시
ax.set_xlim(CUSTOM_TICKS[0], CUSTOM_TICKS[-1]) #x축 표시 범위 20Hz~20kHz

# Y축 범위 설정 (필요에 따라 조정)
ax.set_ylim(0, 100000) 
ax.set_ylabel("magnitude")
ax.grid(True, which="both", ls="-", axis='x') # 로그 스케일에 맞춰 그리드 설정
# ax.set_title("")

def update_plot(frame):
    """그래프 업데이트"""
    try:
        data = stream.read(CHUNK, exception_on_overflow=False)
    except IOError as e:
        print(f"IOError: Audio buffer overflow occurred. ({e})")
        return line,

    data_int = np.frombuffer(data, dtype=np.int16)

    # FFT 계산 및 크기(Magnitude) 추출
    yf = np.fft.fft(data_int)
    magnitude = np.abs(yf[:CHUNK//2])
    
    line.set_ydata(magnitude)
    return line,

# --- 5. 애니메이션 시작 및 실행 ---
ani = FuncAnimation(fig, update_plot, interval=DURATION * 1000, blit=False) 

try:
    plt.show() 
except KeyboardInterrupt:
    pass 
except Exception as e:
    print(f"애니메이션 실행 중 오류 발생: {e}")

# --- 6. 정리 ---
if 'stream' in locals() and stream.is_active():
    stream.stop_stream()
    stream.close()
p.terminate()
print("\n스트림 종료 및 리소스 해제 완료.")