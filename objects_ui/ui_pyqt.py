# Form implementation generated from reading ui file 'ui_pyqt.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(537, 729)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(MainWindow)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_10 = QtWidgets.QLabel(parent=MainWindow)
        self.label_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_8.addWidget(self.label_10)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label = QtWidgets.QLabel(parent=MainWindow)
        self.label.setObjectName("label")
        self.horizontalLayout_7.addWidget(self.label)
        self.InputFilePath = QtWidgets.QLineEdit(parent=MainWindow)
        self.InputFilePath.setObjectName("InputFilePath")
        self.horizontalLayout_7.addWidget(self.InputFilePath)
        self.InputFileButton = QtWidgets.QToolButton(parent=MainWindow)
        self.InputFileButton.setObjectName("InputFileButton")
        self.horizontalLayout_7.addWidget(self.InputFileButton)
        self.verticalLayout_8.addLayout(self.horizontalLayout_7)
        self.AutoDetectButton = QtWidgets.QPushButton(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AutoDetectButton.sizePolicy().hasHeightForWidth())
        self.AutoDetectButton.setSizePolicy(sizePolicy)
        self.AutoDetectButton.setObjectName("AutoDetectButton")
        self.verticalLayout_8.addWidget(self.AutoDetectButton)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.ListWidget_InPlugin = QtWidgets.QListWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ListWidget_InPlugin.sizePolicy().hasHeightForWidth())
        self.ListWidget_InPlugin.setSizePolicy(sizePolicy)
        self.ListWidget_InPlugin.setStyleSheet("font: 15pt \"Ubuntu\";")
        self.ListWidget_InPlugin.setObjectName("ListWidget_InPlugin")
        self.gridLayout.addWidget(self.ListWidget_InPlugin, 2, 1, 1, 1)
        self.ListWidget_InPlugSet = QtWidgets.QListWidget(parent=MainWindow)
        self.ListWidget_InPlugSet.setMaximumSize(QtCore.QSize(100, 10000))
        self.ListWidget_InPlugSet.setObjectName("ListWidget_InPlugSet")
        self.gridLayout.addWidget(self.ListWidget_InPlugSet, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=MainWindow)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=MainWindow)
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)
        self.verticalLayout_8.addLayout(self.gridLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout_8)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_6 = QtWidgets.QLabel(parent=MainWindow)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_9.addWidget(self.label_6)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_5 = QtWidgets.QLabel(parent=MainWindow)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_10.addWidget(self.label_5)
        self.OutputFilePath = QtWidgets.QLineEdit(parent=MainWindow)
        self.OutputFilePath.setObjectName("OutputFilePath")
        self.horizontalLayout_10.addWidget(self.OutputFilePath)
        self.OutputFileButton = QtWidgets.QToolButton(parent=MainWindow)
        self.OutputFileButton.setObjectName("OutputFileButton")
        self.horizontalLayout_10.addWidget(self.OutputFileButton)
        self.verticalLayout_9.addLayout(self.horizontalLayout_10)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.ListWidget_OutPlugSet = QtWidgets.QListWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(9)
        sizePolicy.setHeightForWidth(self.ListWidget_OutPlugSet.sizePolicy().hasHeightForWidth())
        self.ListWidget_OutPlugSet.setSizePolicy(sizePolicy)
        self.ListWidget_OutPlugSet.setMinimumSize(QtCore.QSize(0, 0))
        self.ListWidget_OutPlugSet.setMaximumSize(QtCore.QSize(100, 10000))
        self.ListWidget_OutPlugSet.setObjectName("ListWidget_OutPlugSet")
        self.gridLayout_5.addWidget(self.ListWidget_OutPlugSet, 1, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(parent=MainWindow)
        self.label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 0, 0, 1, 1)
        self.ListWidget_OutPlugin = QtWidgets.QListWidget(parent=MainWindow)
        self.ListWidget_OutPlugin.setStyleSheet("font: 15pt \"Ubuntu\";")
        self.ListWidget_OutPlugin.setObjectName("ListWidget_OutPlugin")
        self.gridLayout_5.addWidget(self.ListWidget_OutPlugin, 1, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(parent=MainWindow)
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 0, 1, 1, 1)
        self.verticalLayout_9.addLayout(self.gridLayout_5)
        self.verticalLayout_2.addLayout(self.verticalLayout_9)
        self.StatusText = QtWidgets.QLabel(parent=MainWindow)
        self.StatusText.setStyleSheet("font: 18pt \"Ubuntu\";")
        self.StatusText.setObjectName("StatusText")
        self.verticalLayout_2.addWidget(self.StatusText)
        self.SubStatusText = QtWidgets.QLabel(parent=MainWindow)
        self.SubStatusText.setObjectName("SubStatusText")
        self.verticalLayout_2.addWidget(self.SubStatusText)
        self.progressBar = QtWidgets.QProgressBar(parent=MainWindow)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.ConvertButton = QtWidgets.QPushButton(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ConvertButton.sizePolicy().hasHeightForWidth())
        self.ConvertButton.setSizePolicy(sizePolicy)
        self.ConvertButton.setMinimumSize(QtCore.QSize(222, 0))
        self.ConvertButton.setStyleSheet("font: 20pt \"Source Sans Pro\";")
        self.ConvertButton.setObjectName("ConvertButton")
        self.verticalLayout_2.addWidget(self.ConvertButton)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Form"))
        self.label_10.setText(_translate("MainWindow", "Input"))
        self.label.setText(_translate("MainWindow", "Input File"))
        self.InputFileButton.setText(_translate("MainWindow", "..."))
        self.AutoDetectButton.setText(_translate("MainWindow", "Auto-Detect"))
        self.label_4.setText(_translate("MainWindow", "Input Plugin"))
        self.label_7.setText(_translate("MainWindow", "Plugin Set"))
        self.label_6.setText(_translate("MainWindow", "Output"))
        self.label_5.setText(_translate("MainWindow", "Output File"))
        self.OutputFileButton.setText(_translate("MainWindow", "..."))
        self.label_8.setText(_translate("MainWindow", "Plugin Set"))
        self.label_9.setText(_translate("MainWindow", "Output Plugin"))
        self.StatusText.setText(_translate("MainWindow", "Status: "))
        self.SubStatusText.setText(_translate("MainWindow", "Status Text"))
        self.ConvertButton.setText(_translate("MainWindow", "Convert"))
