from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# 이미지 불러오기
image_path = 'samgakee.jpg'
image = Image.open(image_path).convert("L")  # Grayscale로 변환
image_array = np.array(image)

# 2D FFT 적용
fft2d = np.fft.fft2(image_array)
fft_shifted = np.fft.fftshift(fft2d)  # FFT 결과를 중앙으로 이동


# 로그 스케일로 변환
magnitude_spectrum = 20 * np.log(np.abs(fft_shifted))


# 이미지로 표현
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(image_array, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('FFT Magnitude Spectrum')
plt.axis('off')

plt.tight_layout()
plt.show()


# 중앙 n%만 남기기
n = 10
rows, cols = image_array.shape
crow, ccol = rows // 2, cols // 2
mask = np.zeros((rows, cols), np.uint8)
mask[crow - int(crow * n / 100): crow + int(crow * n / 100), ccol - int(ccol * n / 100): ccol + int(ccol * n / 100)] = 1

fft_shifted_masked = fft_shifted * mask

# 역 FFT 적용
ifft_result = np.fft.ifft2(np.fft.ifftshift(fft_shifted_masked))
ifft_image = np.abs(ifft_result)

# 이미지로 표현
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(image_array, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(ifft_image, cmap='gray')
plt.title(f'After Removing {n}% of FFT Edges')
plt.axis('off')

plt.tight_layout()
plt.show()
