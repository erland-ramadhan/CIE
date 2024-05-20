from chaos_utils import *

def decrypt_image(image_matrix, func, *args):
    if func == 'circle-gauss-seq':
        image_gauss = decrypt_image(image_matrix, 'gauss-map', *args)
        return decrypt_image(image_gauss, 'circle-map', *args)
    else:
        size = image_matrix.shape
        keystream = generate_keystream(func, size, *args)
        decrypted_image_mat = np.zeros_like(image_matrix)

        for i in range(size[0]):
            for j in range(size[1]):
                for k in range(size[2]):
                    image_mat_bin = int_to_bin_array(image_matrix[i, j, k])
                    keystream_bin = int_to_bin_array(keystream[i, j, k])
                    decrypted_bin = np.bitwise_xor(image_mat_bin, keystream_bin)
                    decrypted_image_mat[i, j, k] = bin_array_to_int(decrypted_bin)

        return decrypted_image_mat
