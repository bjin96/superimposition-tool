import json
import sys

from PyQt5.QtWidgets import QApplication

from src.clickable_superimpose import SuperimpositionTool


if __name__ == '__main__':
    with open('config.json', 'r') as file:
        config = json.load(file)

    app = QApplication(sys.argv)
    main = SuperimpositionTool(
        batch_size=config['batch_size'],
        template_path=config['template_path'],
        blacklist_path=config['blacklist_path'],
        input_file_list_path=config['input_file_list_path']
    )
    main.show()
    sys.exit(app.exec())
