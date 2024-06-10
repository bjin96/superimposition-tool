import numpy as np


def binarize_ct_scan(
        image_data: np.array,
        threshold: float
) -> np.array:
    """
    Binarizes the imaging data according to a threshold value.

    Args:
        image_data (np.array): Image to be binarized.
        threshold (float): Threshold for binarization.

    Returns:
        Binarized image.
    """
    image_data[image_data < threshold] = 0
    image_data[image_data >= threshold] = 1
    return image_data
