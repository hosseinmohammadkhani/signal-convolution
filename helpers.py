import math
from PIL import Image

def convolve(x , h):

    # Signal starts from 0 and ends in (x.length + h.length – 2)
    output_signal = []

    N = len(x)
    M = len(h)

    for e in range(0 , N + M - 1):
        output_signal.append(0)

    for n in range(0 , N + M - 1):
        acc = 0
        for k in range(0 , N):
            if n - k < 0 or n - k >= M:
                continue
            acc += x[k] * h[n - k]
        output_signal[n] = acc

    return output_signal

def apply_1d_gaussian_filter(signal , sigma):

    # Radius determines how far from the center Gaussian samples are kept
    # Keeping values within ±3σ keeps 99.7% of the Gaussian’s total energy(mass)
    radius = int(3 * sigma)

    gaussian_signal_kernel = []
    for i in range(-radius, radius + 1):
        value = math.exp(-(i ** 2) / (2 * (sigma ** 2)))
        gaussian_signal_kernel.append(value)

    # Normalization
    s = sum(gaussian_signal_kernel)
    gaussian_signal_kernel = [round(v / s , 3) for v in gaussian_signal_kernel]

    return convolve(signal, gaussian_signal_kernel)

def parse_signal(input_signal):
    try:
        return [float(x.strip()) for x in input_signal.split(',')]
    except:
        return None

def convolve2d(input_signal, kernel):
    H = len(input_signal)
    W = len(input_signal[0])

    Kh = len(kernel)
    Kw = len(kernel[0])

    # Output size of full convolution
    y_h = H + Kh - 1
    y_w = W + Kw - 1

    # Initialize output with zeros
    y = [
        [0.0 for _ in range(y_w)]
        for _ in range(y_h)
    ]

    for p in range(y_h):
        for q in range(y_w):
            acc = 0.0

            for i in range(Kh):
                for j in range(Kw):
                    x_row = p - i
                    x_col = q - j

                    if 0 <= x_row < H and 0 <= x_col < W:
                        acc += input_signal[x_row][x_col] * kernel[i][j]

            y[p][q] = acc

    return y

def convert_image_to_matrix(path):

    # Load image
    img = Image.open(path)

    # Grayscale
    gray_img = img.convert("L")

    # Resize to 512x512
    resized_img = gray_img.resize((512, 512))

    # Convert to 2D matrix
    image_matrix_list = list(resized_img.getdata())
    image_matrix = [
        image_matrix_list[i * 512:(i + 1) * 512]
        for i in range(512)
    ]

    return image_matrix


def apply_gaussian_filter_on_image(input_signal , sigma=1.0):
    radius = 2
    kernel = []
    total = 0.0

    for i in range(-radius, radius + 1):
        row = []
        for j in range(-radius, radius + 1):
            value = math.exp(-(pow(i , 2) + pow(j , 2)) / (2 * pow(sigma , 2)))
            row.append(value)
            total += value
        kernel.append(row)

    # Normalization
    for i in range(5):
        for j in range(5):
            kernel[i][j] /= total

    return convolve2d(input_signal, kernel)

def matrix_to_image(matrix, path):
    h = len(matrix)
    w = len(matrix[0])

    img = Image.new("L", (w, h))
    pixels = []

    for row in matrix:
        for v in row:
            v = int(round(v))
            v = max(0, min(255, v))
            pixels.append(v)

    img.putdata(pixels)
    img.save(path , format="PNG")