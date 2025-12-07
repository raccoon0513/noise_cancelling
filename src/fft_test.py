import numpy as np
import matplotlib.pyplot as plt

# --- 폰 망골트 함수 (Lambda(n))를 계산하는 함수 ---
def von_mangoldt_function(N):
    """N까지의 폰 망골트 함수 값 (Lambda(n))을 계산합니다."""
    # 배열 초기화
    Lambda = np.zeros(N + 1)
    
    # 1. 에라토스테네스의 체를 사용하여 N까지의 소수 구하기
    is_prime = np.ones(N + 1, dtype=bool)
    if N >= 0: is_prime[0] = False
    if N >= 1: is_prime[1] = False
    
    for p in range(2, int(np.sqrt(N)) + 1):
        if is_prime[p]:
            is_prime[p*p : N+1 : p] = False
    
    # 2. 폰 망골트 함수 값 할당 (소수와 소수의 거듭제곱에 ln(p) 값 할당)
    primes = np.where(is_prime)[0]
    
    for p in primes:
        pk = p
        while pk <= N:
            Lambda[pk] = np.log(p)
            pk *= p
            if p == 1: break # 무한 루프 방지

    return Lambda

# --- 분석 파라미터 설정 ---
N = 500000  # 분석할 최대 정수 범위 (샘플 개수)
Lambda_n = von_mangoldt_function(N)
# 0번 인덱스는 무시하고 1부터 N까지의 값만 사용
Lambda_n = Lambda_n[1:]
N_samples = len(Lambda_n) # 실제 샘플 개수 (5000)

# --- X축 (인덱스) 생성 ---
n_axis = np.arange(1, N + 1)# --- 1. FFT 수행 ---
# Lambda_n 배열에 FFT를 적용합니다.
# 샘플링 주파수 fs는 1로 간주합니다. (이산 신호이므로)
X_k = np.fft.fft(Lambda_n)

# --- 2. 주파수 축 생성 ---
# 주파수 축은 f = k / N_samples 입니다. (k는 0부터 N-1)
f_axis = np.fft.fftfreq(N_samples, d=1) # d=1은 샘플링 간격

# --- 3. 진폭 스펙트럼 계산 및 정렬 ---
# 복소수 결과의 크기(절댓값)를 계산합니다.
X_abs = np.abs(X_k)

# FFT 결과는 0을 기준으로 대칭이므로, 시각화를 위해 fftshift로 0을 중앙으로 이동시킵니다.
X_abs_shifted = np.fft.fftshift(X_abs)
f_axis_shifted = np.fft.fftshift(f_axis)

# --- 4. 시각화 ---
plt.figure(figsize=(12, 8))

# 4-1. 시간/인덱스 영역 플롯 (소수의 분포)
plt.subplot(2, 1, 1)
# 폰 망골트 함수는 소수 위치에 ln(p) 값이 찍히는 이산적인 신호입니다.
plt.stem(n_axis[:50000], Lambda_n[:50000], markerfmt='o', basefmt=' ', linefmt='C0-', label=r'$\Lambda(n)$')
plt.title(r'Von Mangoldt Function $\Lambda(n)$ (Prime Locations, First 200 Samples)')
plt.xlabel('Integer $n$')
plt.ylabel(r'$\ln(p)$ or $0$')
plt.grid(True)

# 4-2. 주파수 영역 스펙트럼 플롯 (소수 분포의 진동 성분)
plt.subplot(2, 1, 2)
# 0 근처의 낮은 주파수 성분이 소수 분포의 평균적인 경향을 나타냅니다.
# 0이 아닌 곳의 피크(진동 성분)가 리만 제타 함수의 근과 관련될 수 있습니다.
plt.plot(f_axis_shifted, X_abs_shifted)
plt.title('FFT Spectrum of $\Lambda(n)$ (Frequency Components)')
plt.xlabel('Frequency $\omega$')
plt.ylabel('Magnitude $|X(\omega)|$')
plt.xlim(-0.1, 0.1) # 0 근처의 낮은 주파수 영역을 확대하여 진동 성분 확인
plt.grid(True)

plt.tight_layout()
plt.show()