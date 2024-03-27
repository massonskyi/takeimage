import sys
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

import base64

from t2image.Text2Image import text2image, get_all_style
import os

qt_plugin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib', 'python3.11', 'site-packages',
                              'PySide6', 'Qt', 'plugins')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path


class ImageConverter(QObject):
    def __init__(self):
        QObject.__init__(self)

    @Slot(str, str, str, int, result=str)
    def convertTextToImage(self, text, style, count_request):
        images_data = text2image(text, negative=None, style=style, count_request=count_request, images=1, width=1024,
                                 height=1024)
        images_base64 = [base64.b64encode(image_data).decode() for image_data in images_data]
        return images_base64

    @Slot(result=list)
    def getStyles(self):
        return get_all_style()


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Expose Python backend to QML
    converter = ImageConverter()
    engine.rootContext().setContextProperty("imageConverter", converter)

    # Load main QML file
    engine.load("gui.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
