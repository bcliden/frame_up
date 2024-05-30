import sys

from frame_up_gui.App import FrameUpApp
from frame_up_gui.widgets.MainWindow import MainWindow

if __name__ == "__main__":
    app = FrameUpApp(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
