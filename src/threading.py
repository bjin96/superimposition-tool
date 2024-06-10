from PyQt5.QtCore import QThread, pyqtSignal

from src.batch_information import NoMoreBatchException, show_no_more_batch_dialog


class BatchFetcher(QThread):
    finished = pyqtSignal(["QString"], [dict])

    def __init__(self, function, on_finish, *args, **kwargs):
        super(BatchFetcher, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.function = function
        self.finished.connect(on_finish)
        self.finished[dict].connect(on_finish)
        self.start()

    def run(self):
        result = None
        try:
            result = self.function(*self.args, **self.kwargs)
        except NoMoreBatchException:
            show_no_more_batch_dialog()
        except Exception as e:
            print(f'Failed fetching the next batch with: {e}')
        finally:
            if isinstance(result, dict):
                self.finished[dict].emit(result)
            else:
                self.finished.emit(str(result))
