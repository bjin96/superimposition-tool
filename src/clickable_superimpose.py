"""Superimposition tool frontend"""
from copy import copy
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QListWidget, QPushButton
from matplotlib import patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from src.batch_information import load_batch_information
from src.blacklist import Blacklist
from src.image_loading import load_image_for_matplotlib
from src.threading import BatchFetcher


class SuperimpositionTool(QtWidgets.QWidget):
    def __init__(self, batch_size, template_path, blacklist_path, input_file_list_path):
        super().__init__()

        self.current_slice = 0
        self.current_single_image_slice = 0
        self.template_path = template_path

        self.is_batch_image_view = True

        self.current_batch_number = 0

        self.selected = {}
        self.selected_pixel = None

        self.selected_scan_path = None
        self.blacklist = Blacklist(blacklist_path)

        self.batch_information = load_batch_information(input_file_list_path, self.current_batch_number, batch_size)

        self.scans_with_data_at_selected_location = QListWidget()
        self.scans_with_data_at_selected_location.setMinimumWidth(400)
        self.scans_with_data_at_selected_location.setMaximumWidth(400)
        self.scans_with_data_at_selected_location.itemDoubleClicked.connect(self.on_select)

        self.go_back_superimpose_button = QPushButton('Go back to superimposed scan')
        self.go_back_superimpose_button.setMaximumWidth(250)
        self.go_back_superimpose_button.clicked.connect(self.show_superimpose)

        self.add_to_blacklist_button = QPushButton('Add to blacklist')
        self.add_to_blacklist_button.setMaximumWidth(150)
        self.add_to_blacklist_button.clicked.connect(self.show_add_to_blacklist_dialog)
        self.add_to_blacklist_button.setEnabled(False)

        self.next_batch_button = QPushButton('Next batch')
        self.next_batch_button.setMaximumWidth(150)
        self.next_batch_button.clicked.connect(self.show_next_batch)
        self.next_batch_button.setEnabled(False)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.figure.clear()
        self.ax = None
        self.ax1 = None
        self.ax2 = None
        self.image = None
        self.image1 = None
        self.image2 = None

        self.figure.canvas.mpl_connect('scroll_event', self.on_scroll())
        self.figure.canvas.mpl_connect('button_press_event', self.on_click())

        self.show_superimpose()

        layout = QVBoxLayout()

        row0 = QHBoxLayout()
        self.batch_number_display = QLabel(f'Batch: {self.current_batch_number}')
        row0.addWidget(self.batch_number_display)
        row0.addWidget(self.next_batch_button)
        layout.addLayout(row0)

        row1 = QHBoxLayout()
        row1.addWidget(self.canvas)

        boxes_list_layout = QVBoxLayout()
        boxes_list_layout.addWidget(QLabel('Scans with bright pixel at location:'))
        boxes_list_layout.addWidget(self.scans_with_data_at_selected_location)

        button_row = QHBoxLayout()
        button_row.addWidget(self.go_back_superimpose_button)
        button_row.addWidget(self.add_to_blacklist_button)
        boxes_list_layout.addLayout(button_row)

        row1.addLayout(boxes_list_layout)

        layout.addLayout(row1)

        self.setLayout(layout)

        self.thread = BatchFetcher(
            load_batch_information,
            self.on_load_batch_information_finished,
            INPUT_FILE_LIST_PATH,
            self.current_batch_number + 1,
            BATCH_SIZE
        )

    def show_add_to_blacklist_dialog(self):
        self.blacklist.show_add_dialog(str(self.selected_scan_path))
        self.add_to_blacklist_button.setEnabled(False)

    def on_load_batch_information_finished(self, batch_information):
        self.next_batch_information = batch_information
        self.next_batch_button.setEnabled(True)

    def show_next_batch(self):
        self.next_batch_button.setEnabled(False)
        self.current_batch_number += 1

        self.current_slice = 0
        self.current_single_image_slice = 0

        self.is_batch_image_view = True
        self.selected = {}
        self.selected_pixel = None

        self.selected_scan_path = None
        self.scans_with_data_at_selected_location.clear()

        self.batch_information = copy(self.next_batch_information)
        self.show_superimpose()
        self.thread = BatchFetcher(
            load_batch_information,
            self.on_load_batch_information_finished,
            INPUT_FILE_LIST_PATH,
            self.current_batch_number + 1,
            BATCH_SIZE
        )

        self.batch_number_display.setText(f'Batch: {self.current_batch_number}')

    def on_toggle_selector(self):
        def _on_toggle_selector(event):
            print('toggle_selector')
            if event.key in ['escape']:
                self.show_superimpose()

        return _on_toggle_selector

    def show_superimpose(self):
        self.current_single_image_slice = self.current_slice
        self.add_to_blacklist_button.setEnabled(False)
        self.go_back_superimpose_button.setEnabled(False)
        self.batch_information = self.blacklist.filter_blacklisted_paths(self.batch_information)
        self.create_superimposed_image()

        self.is_batch_image_view = True
        self.current_image_data = self.superimpose

        self.figure.clear()
        self.figure.subplots_adjust(bottom=0, top=1, left=0, right=1)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.image = self.ax.imshow(self.current_image_data[:, :, self.current_slice], vmin=0, vmax=2)

        if self.selected_pixel is not None:
            rectangle1 = patches.Rectangle(
                self.selected_pixel.xy,
                1,
                1,
                linewidth=1,
                edgecolor='red',
                facecolor='none'
            )
            self.selected_pixel = self.ax.add_patch(rectangle1)

        self.figure.canvas.draw_idle()

    def show_selected_image(self, path):
        self.add_to_blacklist_button.setEnabled(True)
        self.go_back_superimpose_button.setEnabled(True)
        self.current_single_image_slice = self.current_slice

        registered_scan_path = Path(path)
        relative_path = registered_scan_path.relative_to(registered_scan_path.parents[3])

        self.selected_scan_path = registered_scan_path

        registered_scan = load_image_for_matplotlib(registered_scan_path)
        registered_scan = np.clip(registered_scan, 0, 100)

        template_scan = load_image_for_matplotlib(self.template_path)

        self.current_image_data1_mask = copy(self.batch_information[path])
        self.current_image_data1_template = template_scan
        self.current_image_data2 = registered_scan

        self.figure.clear()
        self.figure.subplots_adjust(bottom=0, top=1, left=0, right=1)

        self.ax1 = self.figure.add_subplot(121)
        self.ax1.set_xticks([])
        self.ax1.set_yticks([])
        self.ax1.set_title('High-attenuation values mask')
        self.image1_template = self.ax1.imshow(template_scan[:, :, self.current_slice], cmap='gray')

        binary_mask1 = copy(self.batch_information[path][:, :, self.current_slice])
        binary_mask1[binary_mask1 == 0] = np.nan
        self.image1_mask = self.ax1.imshow(binary_mask1, cmap='prism',
                                           alpha=0.4)
        rectangle1 = patches.Rectangle(
            self.selected_pixel.xy,
            1,
            1,
            linewidth=1,
            edgecolor='red',
            facecolor='none'
        )
        self.selected_pixel1 = self.ax1.add_patch(rectangle1)

        self.ax2 = self.figure.add_subplot(122)
        self.ax2.set_xticks([])
        self.ax2.set_yticks([])
        self.ax2.set_title('Registered source scan\n' + str(relative_path.parent))

        self.image2 = self.ax2.imshow(registered_scan[:, :, self.current_slice], cmap='gray')
        rectangle2 = patches.Rectangle(
            self.selected_pixel.xy,
            1,
            1,
            linewidth=1,
            edgecolor='red',
            facecolor='none'
        )
        self.selected_pixel2 = self.ax2.add_patch(rectangle2)

        self.figure.canvas.draw_idle()

    def create_superimposed_image(self):
        superimpose = sum(list(self.batch_information.values()))
        self.superimpose = np.log2(superimpose)

    def on_select(self):
        selected_paths = [item.text() for item in self.scans_with_data_at_selected_location.selectedItems()]
        self.is_batch_image_view = False
        for path in selected_paths:
            self.show_selected_image(path)

    def on_click(self):
        def _on_click(e):
            if not self.is_batch_image_view:
                return

            if e.button == 1:
                self.selected = {}
                for path, data in self.batch_information.items():
                    if data[round(e.ydata), round(e.xdata), self.current_slice] > 0.7:
                        self.selected[path] = data
            self.scans_with_data_at_selected_location.clear()

            self.scans_with_data_at_selected_location.addItems(self.selected.keys())

            if self.selected_pixel is not None:
                try:
                    self.selected_pixel.remove()
                except ValueError:
                    pass
            rectangle = patches.Rectangle(
                (round(e.xdata) - 0.5, round(e.ydata) - 0.5),
                1,
                1,
                linewidth=1,
                edgecolor='red',
                facecolor='none'
            )
            self.selected_pixel = self.ax.add_patch(rectangle)
            self.figure.canvas.draw_idle()

        return _on_click

    def on_scroll(self):
        def _on_scroll(e):
            if not self.is_batch_image_view:
                if e.inaxes == self.ax1 or e.inaxes == self.ax2:
                    if e.button == 'up':
                        self.current_single_image_slice = self.current_single_image_slice + 1 % \
                                                          self.current_image_data.shape[2]
                    elif e.button == 'down':
                        self.current_single_image_slice = self.current_single_image_slice - 1 % \
                                                          self.current_image_data.shape[2]
                    self.image1_template.set_data(
                        self.current_image_data1_template[:, :, self.current_single_image_slice])
                    binary_mask1 = self.current_image_data1_mask[:, :, self.current_single_image_slice]
                    binary_mask1[binary_mask1 == 0] = np.nan
                    self.image1_mask.set_data(binary_mask1)
                    self.image2.set_data(self.current_image_data2[:, :, self.current_single_image_slice])
                    self.figure.canvas.draw_idle()
                return

            if self.selected_pixel is not None:
                try:
                    self.selected_pixel.remove()
                except ValueError:
                    pass
                self.scans_with_data_at_selected_location.clear()
            if e.inaxes == self.ax:
                if e.button == 'up':
                    self.current_slice = self.current_slice + 1 % self.current_image_data.shape[2]
                elif e.button == 'down':
                    self.current_slice = self.current_slice - 1 % self.current_image_data.shape[2]
                self.image.set_data(self.current_image_data[:, :, self.current_slice])
                self.figure.canvas.draw_idle()

        return _on_scroll



