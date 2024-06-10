"""Functions for loading and handling batches of binarized imaging."""
import json
from pathlib import Path
from typing import Dict

import numpy as np
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QApplication

from src.binarization import binarize_ct_scan
from src.image_loading import load_image_for_matplotlib


class NoMoreBatchException(Exception):
    """Raised when there are no more batches left to process."""
    pass


def load_batch_information(
        file_list_json: Path,
        batch_number: int,
        batch_size: int
) -> Dict[str, np.array]:
    """
    Loads information for a single batch of images.

    Args:
        file_list_json (Path): Path to the json file containing paths to the imaging.
        batch_number (int): Batch number.
        batch_size (int): Batch size.
    """
    with open(file_list_json, 'r') as file:
        batch_scan_paths = json.load(file)

    batch_start_index = batch_number * batch_size
    batch_end_index = min((batch_number + 1) * batch_size, len(batch_scan_paths))

    if len(batch_scan_paths) - 1 < batch_start_index:
        raise NoMoreBatchException()

    batch_scan_paths = batch_scan_paths[batch_start_index:batch_end_index]
    batch_information = {}

    for batch_scan_path in batch_scan_paths:
        img = load_image_for_matplotlib(batch_scan_path)
        img = binarize_ct_scan(img, 100)
        batch_information[batch_scan_path] = img
    print(f'loaded {batch_number} batch information')

    if len(batch_information) != batch_size:
        print(batch_information.keys())

    return batch_information


def show_no_more_batch_dialog():
    """Displays a dialog to inform the user about no more batches being left."""
    add_to_blacklist_dialog = QDialog()
    add_to_blacklist_dialog.setWindowTitle('No more batch')

    add_to_blacklist_dialog.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
    add_to_blacklist_dialog.buttonBox.accepted.connect(add_to_blacklist_dialog.accept)

    add_to_blacklist_dialog.layout = QVBoxLayout()
    message = QLabel(f'There is no more batch to process. Closing application.')

    add_to_blacklist_dialog.layout.addWidget(message)
    add_to_blacklist_dialog.layout.addWidget(add_to_blacklist_dialog.buttonBox)
    add_to_blacklist_dialog.setLayout(add_to_blacklist_dialog.layout)

    if add_to_blacklist_dialog.exec():
        QCoreApplication.quit()
