
## Functions

### convolve(x, h) <br>
This function simply applies discrete convolution formula on x and h signals, if k index is in (0 , N(length of x signal)) range and n - k index is in (0 , M(length of h signal)) range, then x[k] * h[n - k] will be aggregated by the previous value of acc variable. This aggregation will last until N + M - 2 index of the output_signal list.

### apply_gaussian_filter(signal, sigma) <br>
The primary purpose of this function is to smooth a discrete signal. Using kernel of Gaussian formula, radius and sigma determine how far from the center samples are kept. Radius=3σ is being used because keeping values within ±3σ keeps 99.7% of the Gaussian’s total energy(mass).<br>
In the range of (-radius , radius) values are being calculated and stored in gaussian_signal_kernel list using kernel of Gaussian. After normalization, Gaussian filter will be applied to the input signal by convolve function.
