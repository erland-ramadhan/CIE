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

def calculate_rmse(image1, image2):
    """Calculates the Root Mean Square Error (RMSE) between two images."""
    # return np.sqrt(np.mean((image1 - image2) ** 2))
    return np.sqrt(np.mean(np.subtract(image1, image2) ** 2))

def calculate_psnr(image1, image2):
    """Calculates the Peak Signal-to-Noise Ratio (PSNR) between two images."""
    # mse = np.mean((image1 - image2) ** 2)
    mse = np.mean(np.subtract(image1, image2) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0

    return 20 * np.log10(max_pixel / np.sqrt(mse))

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

        keystream.append(int(x * 1e6) % 256)

    return np.array(keystream, dtype=np.uint8).reshape(size)

def encrypt(image_matrix, func, *args):
    if func == 'circle-gauss-seq':
        image_circle = encrypt(image_matrix, 'circle-map', *args)
        return encrypt(image_circle, 'gauss-map', *args)
    else:
        size = image_matrix.shape
        keystream = generate_keystream(func, size, *args)
        encrypted_mat = np.zeros_like(image_matrix)

        for i in range(size[0]):
            for j in range(size[1]):
                for k in range(size[2]):
                    image_mat_bin = int_to_bin_array(image_matrix[i, j, k])
                    keystream_bin = int_to_bin_array(keystream[i, j, k])
                    encrypted_bin = np.bitwise_xor(image_mat_bin, keystream_bin)
                    encrypted_mat[i, j, k] = bin_array_to_int(encrypted_bin)

        return encrypted_mat

def decrypt(image_matrix, func, *args):
    if func == 'circle-gauss-seq':
        image_gauss = decrypt(image_matrix, 'gauss-map', *args)
        return decrypt(image_gauss, 'circle-map', *args)
    else:
        size = image_matrix.shape
        keystream = generate_keystream(func, size, *args)
        decrypted_mat = np.zeros_like(image_matrix)

        for i in range(size[0]):
            for j in range(size[1]):
                for k in range(size[2]):
                    image_mat_bin = int_to_bin_array(image_matrix[i, j, k])
                    keystream_bin = int_to_bin_array(keystream[i, j, k])
                    decrypted_bin = np.bitwise_xor(image_mat_bin, keystream_bin)
                    decrypted_mat[i, j, k] = bin_array_to_int(decrypted_bin)

        return decrypted_mat
