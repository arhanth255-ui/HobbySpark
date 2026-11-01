
import sys
import subprocess

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QPlainTextEdit
)

from PySide6.QtCore import Qt, QProcess


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"


def error(message):
    print(f"{RED}✖{RESET}  {BOLD}{message}{RESET}", file=sys.stderr)


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HobbySpark Utility")

        layout = QVBoxLayout()

        self.main_console = QPlainTextEdit()
        self.main_console.setReadOnly(True)
        self.main_console.setPlaceholderText(
            "Your python output will appear here..."
        )
        self.main_console.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.NoWrap
        )

        # Smart auto-scrolling
        self.auto_scroll = True

        self.main_console.verticalScrollBar().valueChanged.connect(
            self.scroll_changed
        )

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(lambda: self.close())

        layout.addWidget(self.main_console)

        layout.addWidget(
            self.ok_button,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        self.setLayout(layout)

        self.success = None
        self.process = None
        self.file = None

    def run(self, file, python):
        self.file = file
        self.success = None
        self.auto_scroll = True

        self.main_console.clear()

        self.process = QProcess(self)

        self.process.setProgram(python)
        self.process.setArguments([file])

        self.process.readyReadStandardOutput.connect(
            self.read_output
        )

        self.process.readyReadStandardError.connect(
            self.read_error
        )

        self.process.finished.connect(
            self.process_finished
        )

        self.process.errorOccurred.connect(
            self.process_error
        )

        self.process.start()

        self.exec()

        return self.success

    def scroll_changed(self, value):
        scrollbar = self.main_console.verticalScrollBar()

        self.auto_scroll = (
            value >= scrollbar.maximum()
        )

    def read_output(self):
        new_output = bytes(
            self.process.readAllStandardOutput()
        )

        should_scroll = self.auto_scroll

        self.main_console.insertPlainText(
            new_output.decode("utf-8", errors="replace")
        )

        if should_scroll:
            scrollbar = self.main_console.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def read_error(self):
        new_error = bytes(
            self.process.readAllStandardError()
        )

        error(
            new_error.decode("utf-8", errors="replace").rstrip()
        )

    def process_error(self, process_err):
        if process_err == QProcess.ProcessError.FailedToStart:
            error(
                f"Could not start {self.file}: "
                f"{self.process.errorString()}"
            )

            self.success = False
            self.close()

    
    def process_finished(self, process_code, stat):
        # Read any remaining stderr before reporting failure
        stderr_output = bytes(
            self.process.readAllStandardError()
        ).decode("utf-8", errors="replace")
        if (
            process_code == 0
            and stat == QProcess.ExitStatus.NormalExit
        ):
            self.success = True

        elif (
            process_code==9 
            and stat==QProcess.ExitStatus.CrashExit
        ):  
            ans = QMessageBox.question(self, "Cancellation", "You seem to have cancelled the program before it finished running. Do you want to continue? [Note that selecting no will stop the execution of whatever process you have started using the hobbyspark cli] ", QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
            if ans==QMessageBox.StandardButton.Yes:
                self.success=True
            else:
                self.success=None


        else:
            error(f"Running of the file {self.file} failed: {stderr_output}")

            self.success = False


    def closeEvent(self, event):

        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())
