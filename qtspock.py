# Adapted from https://github.com/jupyter/qtconsole/tree/master/examples

"""A RichJupyterWidget embedded in a PyQT Application using a Spock profile
To run:
    python3 qtspock
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from builtins import (bytes, str, open, super, range,  # noqa
                      zip, round, input, int, pow, object)

import sys
from PyQt5 import QtWidgets

from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.manager import QtKernelManager

# The ID of an installed kernel, e.g. 'bash' or 'ir'.
USE_KERNEL = 'python2'


def make_jupyter_widget_with_kernel():
    """Start a kernel, connect to it, and create a RichJupyterWidget to use it
    """
    kernel_manager = QtKernelManager(kernel_name=USE_KERNEL)
    kernel_manager.start_kernel(extra_arguments=["--profile", "spockdoor"])

    kernel_client = kernel_manager.client()
    kernel_client.start_channels()

    jupyter_widget = RichJupyterWidget()
    jupyter_widget.kernel_manager = kernel_manager
    jupyter_widget.kernel_client = kernel_client
    return jupyter_widget


class MainWindow(QtWidgets.QWidget):
    """A window that contains a single Qt console."""
    def __init__(self):
        super().__init__()

        self.lineEdit = QtWidgets.QLineEdit()
        self.pushButton = QtWidgets.QPushButton("submit")

        self.pushButton.clicked.connect(self.submit)
        self.lineEdit.returnPressed.connect(self.submit)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.pushButton)
        self.jupyter_widget = make_jupyter_widget_with_kernel()

        mainlayout = QtWidgets.QVBoxLayout()

        mainlayout.addWidget(self.jupyter_widget)
        mainlayout.addLayout(layout)
        self.setLayout(mainlayout)

    def submit(self):
        self.jupyter_widget.execute(self.lineEdit.text())
        self.lineEdit.setText("")

    def shutdown_kernel(self):
        print('Shutting down kernel...')
        self.jupyter_widget.kernel_client.stop_channels()
        self.jupyter_widget.kernel_manager.shutdown_kernel()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.aboutToQuit.connect(window.shutdown_kernel)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
