import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QThread, Signal
from text_reader import pdfs_to_text


class WorkerThread(QThread):
    status_signal = Signal(str)

    def __init__(self, folder_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.folder_path = folder_path

    def run(self):
        self.status_signal.emit("Working...")
        # Process PDFs in the provided folder path
        pdfs_to_text(self.folder_path)
        self.status_signal.emit("Done")


class PdfToTxtApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF2TXT")
        self.setGeometry(100, 100, 400, 300)  # Increased size for better visibility

        # Layout
        layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("PDF to TXT")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Instructions
        self.instructions_label = QLabel(
            "Enter a folder containing PDFs. The converted text files will be exported to the same folder with the .txt extension."
        )
        self.instructions_label.setWordWrap(True)  # Enable text wrapping
        layout.addWidget(self.instructions_label)

        # Folder Selection
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Select folder...")
        layout.addWidget(self.folder_input)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_folder)
        self.browse_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        layout.addWidget(self.browse_button)

        # Go Button
        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.start_processing)
        self.go_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        layout.addWidget(self.go_button)

        # Status Indicator
        self.status_indicator = QLabel("Ready")
        self.status_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_indicator)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def start_processing(self):
        folder_path = self.folder_input.text()
        if not folder_path:
            self.status_indicator.setText("Please select a folder.")
            return

        self.status_indicator.setText("Starting...")
        self.worker_thread = WorkerThread(folder_path)
        self.worker_thread.status_signal.connect(self.update_status)
        self.worker_thread.start()

    def update_status(self, status):
        self.status_indicator.setText(status)


if __name__ == "__main__":
    print('\n'*50)
    app = QApplication(sys.argv)
    window = PdfToTxtApp()
    window.show()
    sys.exit(app.exec())
