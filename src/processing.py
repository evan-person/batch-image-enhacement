# image enhancement for USGS project
# evan lucas, August 28, 2023

#imports
import cv2
import numpy as np
import os


#define operations



def clahe(image,**kwargs):
    tile_size = kwargs.get('tile_size',20)
    clip_limit = kwargs.get('clip_limit',2.0)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size,tile_size))
    lab[:,:,0] = clahe.apply(lab[:,:,0])
    clahe_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return clahe_img

def rgb_eq(image):
    B, G, R = cv2.split(image)
    B = cv2.equalizeHist(B)
    G = cv2.equalizeHist(G)
    R = cv2.equalizeHist(R)
    histogram_equalized_img = cv2.merge((B,G,R))
    return histogram_equalized_img


def gamma_corr(image, **kwargs):
    minimum_brightness = kwargs.get('minimum_brightness', 0.3)
    cols, rows, _ = image.shape
    brightness = np.sum(image) / (3 * 255 * cols * rows)
    ratio = brightness / minimum_brightness
    if ratio >= 1:
        ratio = 1.0
    alpha = 1 / ratio
    beta = 0
    gamma_corrected_img = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return gamma_corrected_img

def unsharp_mask(image,**kwargs):
    sigma = kwargs.get('sigma',2.0)
    amount = kwargs.get('amount',2.0)
    threshold = kwargs.get('threshold',0)
    kernel_size = kwargs.get('kernel_size',5)
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened


def median_blur(image,**kwargs):
    kernel_size = kwargs.get('kernel_size',7)
    median_blurred_img = cv2.medianBlur(image, kernel_size)
    return median_blurred_img

def gaussian_blur(image,**kwargs):
    kernel_size = kwargs.get('kernel_size',9)
    sigma = kwargs.get('sigma',0)
    gaussian_blurred_img = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    return gaussian_blurred_img

def bilateral_filter(image,**kwargs):
    diameter = kwargs.get('diameter',9)
    sigma_color = kwargs.get('sigma_color',100)
    sigma_space = kwargs.get('sigma_space',100)
    bilateral_filtered_img = cv2.bilateralFilter(image, diameter, sigma_color, sigma_space)
    return bilateral_filtered_img


