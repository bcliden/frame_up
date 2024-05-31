import sys
from signal import SIG_DFL, SIGINT, signal

from frame_up_gui.App import FrameUpApp
from frame_up_gui.widgets.MainWindow import MainWindow

if __name__ == "__main__":
    # close if anyone asks us to
    signal(SIGINT, SIG_DFL)

    app = FrameUpApp(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
