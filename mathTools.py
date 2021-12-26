# using fft for 2d convolutions due to speed increase
from numpy.fft import fft2, ifft2
import numpy as np
from numba import njit
from PIL import Image


# normalize 0 to 1
def normalize(arr):
    return (arr - np.min(arr)) / np.ptp(arr)


@njit
def dnorm(x, mu, sd):
    """
    :param x: the variable of the density function
    :param mu: the mu parameter
    :param sd: sigma/ standard deviation
    :return: result of the unm density function
    """
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)


def fft_convolution(f1, f2):
    """

    :param f1: 2d array to be convolved
    :param f2: convolution kernel
    :return: convolution result
    """
    old_dx, old_dy = f1.shape[0], f1.shape[1]
    new_dx, new_dy = old_dx * 2, old_dy * 2
    f1 = padding(f1, new_dx, new_dy)
    f2 = padding(f2, new_dx, new_dy)
    f1 = fft2(f1)
    f2 = fft2(np.flipud(np.fliplr(f2)))
    i, j = f1.shape
    cc = np.real(ifft2(f1 * f2))
    cc = np.roll(cc, -i // 2 + 1, axis=0)
    cc = np.roll(cc, -j // 2 + 1, axis=1)
    cc = cc[old_dx // 2:new_dx - old_dx // 2, old_dy // 2:new_dy - old_dy // 2]
    return cc


def padding(arr, xd, yd):
    """
    :param arr: The array to be zero padded
    :param xd: The desired x dimension
    :param yd: the desired y dimension
    :return: A zero padded array with original content in the middle and of size == (xd,yd)
    """
    h = arr.shape[0]
    w = arr.shape[1]
    a = (xd - h) // 2
    aa = xd - a - h
    b = (yd - w) // 2
    bb = yd - b - w
    return np.pad(arr, pad_width=((a, aa), (b, bb)), mode='constant')


def arr_to_img(arr):
    """
    :param arr: 0-1 scaled array
    :return:
    """
    return Image.fromarray((arr * 255).astype(np.uint8))
