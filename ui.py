import sys
import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap, QPainter
from PyQt5.QtWidgets import *
import PyQt5
import predict

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'Qt5', 'plugins')
os.environ['QT_PLUGIN_PATH'] = plugin_path


class Picture(QWidget):
    def __init__(self):
        super(Picture, self).__init__()

        self.resize(1200, 800)
        self.setWindowTitle("植物幼苗分类预测")
        self.setWindowIcon(QIcon('./LOGO.ico'))

        # 显示图片的Pic_label
        self.Pic_label = QLabel(self)
        self.Pic_label.setFixedSize(300, 300)
        self.Pic_label.move(10, 150)
        self.Pic_label.setStyleSheet("QLabel{background:white;}"
                                     "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                     )

        # 显示预测标签的Result_label
        self.Result_label = QLabel(self)
        self.Result_label.setFixedSize(270, 50)
        self.Result_label.move(320, 400)
        self.Result_label.setStyleSheet("QLabel{background:rgb(255,255,255,120);}"
                                        "QLabel{color:rgb(0,0,0,255);font-size:20px;font-weight:bold;font-family:Microsoft YaHei;alignment:AlignHCenter}"
                                        )

        # 打开图片按钮
        btn = QPushButton(self)
        btn.setText("打开图片")
        btn.move(10, 30)
        btn.clicked.connect(self.openimage)

        # 提示
        self.Notice_label = QLabel(self)
        self.Notice_label.setText("图片路径不能有中文！")
        self.Notice_label.setFixedSize(160, 30)
        self.Notice_label.move(12, 70)
        self.Notice_label.setStyleSheet("QLabel{background:white;}"
                                        "QLabel{color:rgb(300,300,300,120);font-size:15px;font-weight:bold;font-family:Microsoft YaHei;}"
                                        )

    # 设置背景图片
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        pixmap = QPixmap("./background.jpg")
        painter.drawPixmap(self.rect(), pixmap)

    # 打开图片
    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(
            self, "打开图片", "", "*.png;;*.jpg;;All Files(*)")
        print(imgName)
        jpg = QtGui.QPixmap(imgName).scaled(
            self.Pic_label.width(), self.Pic_label.height())
        # self.label.setText("123")
        self.Pic_label.setPixmap(jpg)
        result = predict.get_prediction(imgName)
        print(result)
        self.showResult(result)
        # self.Result_label.setText(str(result))

    # 显示预测结果
    def showResult(self, result):
        self.Result_label.setText('预测结果:'+result)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = Picture()
    my.show()
    sys.exit(app.exec_())
