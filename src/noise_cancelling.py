import numpy as np

def fft_denoise_simple(signal, threshold_ratio=0.1):
    """
    NumPy FFT를 사용한 간단한 주파수 기반 노이즈 캔슬링.

    :param signal: 1D NumPy 배열 형태의 입력 신호 (시간 영역).
    :param threshold_ratio: 최대 진폭 대비 노이즈를 제거할 임계값 비율 (0.0 ~ 1.0).
    :return: 노이즈가 제거된 1D NumPy 배열 신호 (시간 영역).
    """

    # 1. FFT 수행: 시간 영역 -> 주파수 영역 (복소수 스펙트럼)
    # F(w) = Fourier Transform of signal(t)
    signal_fft = np.fft.fft(signal)

    # 2. 노이즈 필터링을 위한 임계값 설정
    # 주파수 성분의 진폭(|F(w)|)을 계산합니다.
    amplitude_spectrum = np.abs(signal_fft)

    # 최대 진폭을 찾아 임계값을 설정합니다.
    max_amplitude = np.max(amplitude_spectrum)
    threshold = max_amplitude * threshold_ratio

    # 3. 임계값보다 작은 성분 제거 (필터링)
    # 임계값보다 작은 진폭을 갖는 주파수 성분의 위치를 찾습니다.
    # $S_{filtered}(\omega) = 0$ if $|S(\omega)| < T$
    
    # 임계값보다 크거나 같은 성분만 남기고 나머지는 0으로 만듭니다.
    filtered_fft = np.where(amplitude_spectrum >= threshold, signal_fft, 0)

    # 4. IFFT 수행: 주파수 영역 -> 시간 영역
    # 역변환 후, 신호는 실수이므로 실수부(.real)만 취합니다.
    denoised_signal = np.fft.ifft(filtered_fft).real

    return denoised_signal

# --- 예시 데이터 생성 및 실행 ---

# 1. 신호 설정
SAMPLING_RATE = 1000  # 샘플링 주파수 (Hz)
DURATION = 1.0        # 신호 지속 시간 (초)
time = np.linspace(0, DURATION, SAMPLING_RATE, endpoint=False)

# 2. 순수 신호 (10Hz)
pure_signal = 1.0 * np.sin(2 * np.pi * 10 * time)

# 3. 노이즈 (랜덤 노이즈)
# 순수 신호보다 진폭은 작지만 넓게 퍼진 잡음
noise = 0.3 * np.random.randn(SAMPLING_RATE)

# 4. 잡음이 포함된 신호
mixed_signal = pure_signal + noise

# 5. 노이즈 캔슬링 적용
# 최대 진폭의 10% 미만을 노이즈로 간주하고 제거
denoised = fft_denoise_simple(mixed_signal, threshold_ratio=0.1)

# print("노이즈 제거 완료. (결과 신호 길이:", len(denoised), ")")