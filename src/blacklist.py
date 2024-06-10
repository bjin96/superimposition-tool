import json

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QVBoxLayout, QLabel


class Blacklist:
    """Class for managing the blacklist."""

    def __init__(self, blacklist_json_path):
        self.blacklist_json_path = blacklist_json_path
        self.blacklist = self.read_blacklist()

    def read_blacklist(self):
        try:
            with open(self.blacklist_json_path, 'r') as file:
                blacklist_information = json.load(file)
            return blacklist_information
        except FileNotFoundError:
            print("File not found, creating new blacklist.json.")
            self.blacklist = []
            self.write_blacklist_to_file()

    def filter_blacklisted_paths(self, batch_information):
        blacklist_paths = [item['file'] for item in self.blacklist]
        return {
            path: binarized_data
            for path, binarized_data in batch_information.items()
            if path not in blacklist_paths
        }

    def write_blacklist_to_file(self):
        with open(self.blacklist_json_path, 'w') as file:
            json.dump(self.blacklist, file)

    def add(self, file, reason):
        try:
            self.blacklist.append({
                'file': file,
                'reason': reason
            })
            self.write_blacklist_to_file()
        except Exception as e:
            print(f'Failed updating blacklist.json with {e}')

    def show_add_dialog(self, selected_scan_path):
        add_to_blacklist_dialog = QDialog()
        add_to_blacklist_dialog.setWindowTitle('Add scan to blacklist')

        add_to_blacklist_dialog.text_input = QLineEdit()
        add_to_blacklist_dialog.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        add_to_blacklist_dialog.buttonBox.accepted.connect(add_to_blacklist_dialog.accept)
        add_to_blacklist_dialog.buttonBox.rejected.connect(add_to_blacklist_dialog.reject)
        add_to_blacklist_dialog.layout = QVBoxLayout()
        message = QLabel(f'Add scan to blacklist: {selected_scan_path}')

        add_to_blacklist_dialog.layout.addWidget(message)
        add_to_blacklist_dialog.layout.addWidget(add_to_blacklist_dialog.text_input)
        add_to_blacklist_dialog.layout.addWidget(add_to_blacklist_dialog.buttonBox)
        add_to_blacklist_dialog.setLayout(add_to_blacklist_dialog.layout)

        if add_to_blacklist_dialog.exec():
            self.add(selected_scan_path, add_to_blacklist_dialog.text_input.text())
