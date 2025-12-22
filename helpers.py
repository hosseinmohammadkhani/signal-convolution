import math

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

def apply_gaussian_filter(signal , sigma):

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