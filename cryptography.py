import numpy as np
import math

def circle_map(x, omega, K):
    """Implements the circle map function."""
    return (x + omega - (K / (2 * np.pi)) * np.sin(2 * np.pi * x)) % 1

def gauss_map(x, alpha, beta):
    """Implements the Gaussian map function."""
    return np.exp(-alpha * x**2) + beta

def composed_map(x, alpha, beta, omega, K):
    """Implements the composed map function."""
    return gauss_map(circle_map(x, omega, K), alpha, beta)

def calculate_rmse(image1, image2):
    """Calculates the Root Mean Square Error (RMSE) between two images."""
    return np.sqrt(np.mean(np.subtract(image1, image2) ** 2))

def calculate_psnr(image1, image2):
    """Calculates the Peak Signal-to-Noise Ratio (PSNR) between two images."""
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
            x = composed_map(x, alpha, beta, omega, K)

        keystream.append(math.floor(x * 1e6) % 256)

    return np.array(keystream, dtype=np.uint8)

def encrypt(image_matrix, func, *args):
    if func == 'circle-gauss-seq':
        image_circle = encrypt(image_matrix, 'circle-map', *args)
        return encrypt(image_circle, 'gauss-map', *args)
    else:
        size = image_matrix.shape
        length = np.prod(size)

        keystream = generate_keystream(func, size, *args)
        image_flat = image_matrix.flatten()
        encrypted_flat = [np.bitwise_xor(image_flat[0], keystream[0])]

        i = 1
        while i < length:
            result_ = np.bitwise_xor(image_flat[i], keystream[i])
            result = np.bitwise_xor(result_, encrypted_flat[-1])
            encrypted_flat.append(result)
            i += 1

        encrypted_flat = np.array(encrypted_flat)
        encrypted_mat = encrypted_flat.reshape(size)
        return encrypted_mat

def decrypt(image_matrix, func, *args):
    if func == 'circle-gauss-seq':
        image_gauss = decrypt(image_matrix, 'gauss-map', *args)
        return decrypt(image_gauss, 'circle-map', *args)
    else:
        size = image_matrix.shape
        length = np.prod(size)

        keystream = generate_keystream(func, size, *args)
        image_flat = image_matrix.flatten()
        decrypted_flat = [np.bitwise_xor(image_flat[0], keystream[0])]

        i = 1
        while i < length:
            result_ = np.bitwise_xor(image_flat[i], keystream[i])
            result = np.bitwise_xor(result_, image_flat[i-1])
            decrypted_flat.append(result)
            i += 1

        decrypted_flat = np.array(decrypted_flat)
        decrypted_mat = decrypted_flat.reshape(size)

        return decrypted_mat
