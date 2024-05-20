import numpy as np

def circle_map(x, omega, K):
    """Implements the circle map function."""
    return (x + omega - (K / (2 * np.pi)) * np.sin(2 * np.pi * x)) % 1

def gauss_map(x, alpha, beta):
    """Implements the Gaussian map function."""
    return np.exp(-alpha * x**2) + beta

def composed_map(x, alpha, beta, omega, K):
    """Implements the composed map function."""
    return gauss_map(circle_map(x, omega, K), alpha, beta)

def int_to_bin_array(num):
    """Converts an integer to a binary array."""
    return np.array(list(np.binary_repr(num, width=8))).astype(np.uint8)

def bin_array_to_int(bin_array):
    """Converts a binary array to an integer."""
    return int("".join(bin_array.astype(str)), 2)

def generate_keystream(func, size, *args):
    """Generates a keystream """
    length = np.prod(size)
    keystream = []

    x, alpha, beta, omega, K = args

    for _ in range(length):
        if func == 'circle-map':
            x = circle_map(x, omega, K)
        elif func == 'gauss-map':
            x = gauss_map(x, alpha, beta)
        else:
        # elif func == 'circle-gauss-com':
            x = composed_map(x, alpha, beta, omega, K)

        keystream.append(int(x * 1000) % 256)

    return np.array(keystream, dtype=np.uint8).reshape(size)

