# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DetectionWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DetectionWindow(object):
    def setupUi(self, DetectionWindow):
        DetectionWindow.setObjectName("DetectionWindow")
        DetectionWindow.resize(996, 592)
        DetectionWindow.setMinimumSize(QtCore.QSize(996, 592))
        DetectionWindow.setMaximumSize(QtCore.QSize(996, 592))
        DetectionWindow.setStyleSheet(
            "QDialog {\n"
            "background-color:  #2a292e;\n"
            "}\n"
            "\n"
            "QLabel {\n"
            "color: white;\n"
            "font-size: 18px;\n"
            "font-weight: bold;\n"
            "}\n"
            "\n"
            "QPushButton{\n"
            "font-size: 18px;\n"
            "font-weight: bold;\n"
            "color: #1db954;\n"
            "border: 2px solid #1db954;\n"
            "border-radius: 14px;\n"
            "letter-spacing: 1px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "color: #121212;\n"
            "background-color:     #1db954;\n"
            "border: 2px solid #121212;\n"
            "}\n"
            "\n"
            "QHBoxLayout {\n"
            "border: 2px solid green;\n"
            "}"
        )
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(DetectionWindow)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 25, 25, 25)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.information = QtWidgets.QHBoxLayout()
        self.information.setObjectName("information")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(10, 0, 10, 20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_4.addItem(spacerItem)
        self.label_3 = QtWidgets.QLabel(DetectionWindow)
        self.label_3.setMinimumSize(QtCore.QSize(0, 50))
        self.label_3.setStyleSheet(
            "color: white;\n"
            "border: 2px solid #535353;\n"
            "border-radius: 14px;\n"
            "margin-bottom: 10px;\n"
            "padding: 10px;\n"
            ""
        )
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.verticalWidget = QtWidgets.QWidget(DetectionWindow)
        self.verticalWidget.setStyleSheet(
            "border: 2px solid #535353;\n" "border-radius: 14px;"
        )
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalWidget)
        self.label.setStyleSheet(
            "color: white;\n"
            "border: 2px solid #535353;\n"
            "border-radius: 14px;\n"
            "padding: 10px;\n"
            "margin: 10px;\n"
            ""
        )
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.detected_gesture_name = QtWidgets.QLabel(self.verticalWidget)
        self.detected_gesture_name.setStyleSheet("color: #1db954;\n" "border: none;")
        self.detected_gesture_name.setObjectName("detected_gesture_name")
        self.verticalLayout.addWidget(self.detected_gesture_name)
        self.label_2 = QtWidgets.QLabel(self.verticalWidget)
        self.label_2.setStyleSheet(
            "color: white;\n"
            "border: 2px solid #535353;\n"
            "border-radius: 14px;\n"
            "padding: 10px;\n"
            "margin: 10px;\n"
            ""
        )
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.detection_confidence = QtWidgets.QLabel(self.verticalWidget)
        self.detection_confidence.setStyleSheet("color: #1db954;\n" "border: none;")
        self.detection_confidence.setObjectName("detection_confidence")
        self.verticalLayout.addWidget(self.detection_confidence)
        self.verticalLayout_4.addWidget(self.verticalWidget)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_4.addItem(spacerItem1)
        self.information.addLayout(self.verticalLayout_4)
        self.horizontalLayout.addLayout(self.information)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.detection_camera = QtWidgets.QLabel(DetectionWindow)
        self.detection_camera.setMinimumSize(QtCore.QSize(600, 400))
        self.detection_camera.setStyleSheet(
            "QLabel {\n" "border-radius: 14px;\n" "border: 2px solid #535353;\n" "}"
        )
        self.detection_camera.setObjectName("detection_camera")
        self.verticalLayout_3.addWidget(self.detection_camera)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setContentsMargins(-1, 20, -1, 20)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.pushButton_2 = QtWidgets.QPushButton(DetectionWindow)
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 56))
        self.pushButton_2.setMaximumSize(QtCore.QSize(150, 56))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_10.addWidget(self.pushButton_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_8.addLayout(self.verticalLayout_3)
        self.horizontalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(DetectionWindow)
        QtCore.QMetaObject.connectSlotsByName(DetectionWindow)

    def retranslateUi(self, DetectionWindow):
        _translate = QtCore.QCoreApplication.translate
        DetectionWindow.setWindowTitle(_translate("DetectionWindow", "Detection"))
        self.label_3.setText(
            _translate(
                "DetectionWindow",
                '<html><head/><body><p align="center"><span style=" font-size:14pt;">INFORMATION</span></p></body></html>',
            )
        )
        self.label.setText(
            _translate(
                "DetectionWindow",
                '<html><head/><body><p align="center"><span style=" font-size:14pt;">DETECTED GESTURE</span></p></body></html>',
            )
        )
        self.detected_gesture_name.setText(
            _translate(
                "DetectionWindow",
                '<html><head/><body><p align="center"><br/></p></body></html>',
            )
        )
        self.label_2.setText(
            _translate(
                "DetectionWindow",
                '<html><head/><body><p align="center"><span style=" font-size:14pt;">CONFIDENCE</span></p></body></html>',
            )
        )
        self.detection_confidence.setText(
            _translate(
                "DetectionWindow",
                '<html><head/><body><p align="center"><br/></p></body></html>',
            )
        )
        self.detection_camera.setText(
            _translate(
                "DetectionWindow",
                '<html><head/><body><p align="center"><span style=" font-size:14pt;">CLICK START, OPEN SPOTIFY AND START PLAY MUSIC </span></p></body></html>',
            )
        )
        self.pushButton_2.setText(_translate("DetectionWindow", "START"))
