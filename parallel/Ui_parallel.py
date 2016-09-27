# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Python\parallal\parallal.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog

class Ui_Form(QMainWindow):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(820, 585)
        Form.setWindowTitle( "Bilingual Editor")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(40, 80, 760, 500))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        
        self.imbtn = QtWidgets.QPushButton(Form)
        self.imbtn.setGeometry(QtCore.QRect(40, 20, 101, 31))
        self.imbtn.setObjectName("imbtn")
        self.imbtn.setText("Import")
        self.imbtn.clicked.connect(self.on_imbtn_clicked)
        
        self.exbtn = QtWidgets.QPushButton(Form)
        self.exbtn.setGeometry(QtCore.QRect(700, 20, 101, 31))
        self.exbtn.setObjectName("exbtn")
        self.exbtn.setText("Export")
        self.exbtn.clicked.connect(self.on_exbtn_clicked)
        
        self.font = QtGui.QFont()
        self.font.setFamily("ADMUI3Lg")
        self.font.setPointSize(12)
        
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 760, 500))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 20, 54, 12))
        self.label.setObjectName("label")
        
        self.scrollArea.setWidget(self.verticalLayoutWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.finish=1
        self.selected=''
        self.cut=0
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def on_imbtn_clicked(self):
        directoryUri = QFileDialog.getOpenFileName(self,  'Select a file', 'C:\\Users\\hp\\Desktop', 'Text Files (*.txt)')
        print(directoryUri)
        bifile=open(directoryUri[0],'r+', encoding='utf-8')
        n=0
        string=''
        self.lineEdit=[]
        for word in bifile.read():
            string+=word
            if re.match(r'\n', word):
                self.lineEdit.append(QtWidgets.QLineEdit(self.verticalLayoutWidget))
                self.verticalLayout.addWidget(self.lineEdit[n])
                self.lineEdit[n].setText(string)
                self.lineEdit[n].setGeometry(QtCore.QRect(170, 90, 161, 31))
                self.lineEdit[n].setFont(self.font)
                #self.lineEdit[n].setObjectName('lineEdit_'+str(n))
                self.lineEdit[n].cursorPositionChanged['int', 'int'].connect(self.cursorEvent)
                #print(lineEdit[n].cursorPosition())
                if n%2==0:
                    self.lineEdit[n].setStyleSheet("background-color: rgb(215, 255, 205);")
                
                string=''
                n+=1
        bifile.close()
    
    def on_exbtn_clicked(self):
        directoryUri = QFileDialog.getSaveFileName(self,  'Select a file', 'C:\\Users\\hp\\Desktop', 'Text Files (*.txt)')
        if directoryUri[0]:
            exfile=open(directoryUri[0], 'w+', encoding='utf-8')
            for i in range(len(self.lineEdit)):
                exfile.write(self.lineEdit[i].text())
        exfile.close()
        
    def mousePressEvent(self, event):
        print('asd')
        self.parent().setStyleSheet("background-color: rgb(0, 0, 0);")
        
        
    def cursorEvent(self):
        if self.finish==1:
            self.finish=0
            sender=self.sender()
            pattern='[\x21-\x2f\x3a-\x3e\x5b-\x60\x7b-\x7e\uff0c\uff0c\uff1a\uff1b\uff01\uff1f\u3002\u201c\u201d\u300a\u300b\u2026\uff08\uff09]'
            s=''

            if self.cut==1 :

                while 1:
                    sender.cursorBackward(1, 1)
                    if  s==sender.selectedText() or sender.selectedText()=='':
                        break
                    if re.search(pattern,sender.selectedText()):
                        sender.cursorForward(1, 1)
                        break
                    else:
                        s=sender.selectedText()
                sender.deselect()
                sender.paste()
                self.cut=0
                self.finish=1
            else:
                
                len=0
                pos=sender.cursorPosition()
                while 1:
                    sender.cursorForward(1, 1)
                    if  s==sender.selectedText() or sender.selectedText()=='':
                        break
                    if re.search(pattern,sender.selectedText()):
                        break
                    else:
                        s=sender.selectedText()
                        len+=1
                sender.setCursorPosition(pos)
                while 1:
                    sender.cursorBackward(1, 1)
                    if  s==sender.selectedText() or sender.selectedText()=='':
                        pos=sender.cursorPosition()
                        break
                    if re.search(pattern,sender.selectedText()):
                        pos=sender.cursorPosition()+1
                        break
                    else:
                        s=sender.selectedText()
                        len+=1

                sender.setSelection(pos, len+1)
                if self.selected==sender.selectedText() and self.cut==0:
                    self.cut=1
                    sender.cut()
                    self.selected=''
                    
                else:
                    self.selected=sender.selectedText()
                self.finish=1
                

            
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

