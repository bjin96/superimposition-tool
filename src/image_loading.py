from pathlib import Path

import numpy as np
from nibabel import load


def load_image_for_matplotlib(
        path: Path
) -> np.ndarray:
    """
    Load a .nii.gz image and return as numpy array ready to be displayed in a matplotlib figure.

    Args:
        path (Path): Path to .nii.gz image.

    Returns
        Numpy array that can be displayed in a matplotlib figure.
    """
    return load(path).get_fdata().transpose(1, 0, 2)[::-1, ::-1, :]