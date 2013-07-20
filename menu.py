
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from taalum import *

class Menu(QWidget):
	
	def __init__(self):
		super(Menu, self).__init__()
		self.mode= 'Belajar'
		self.level = 'Dasar'
		self.pakeBaju()
		self.gaya()
		self.pasangSlot()
		self.listRecentSessions()
		self.senter()
		self.show()
		
	def pakeBaju(self):
		self.belajar = QRadioButton('Belajar')
		self.belajar.setChecked(True)
		self.latihan = QRadioButton('Latihan')
		
		
		self.Hdasar = QRadioButton('Dasar')
		self.Hdasar.setChecked(True)
		self.Hharokat = QRadioButton('Harakat')
		self.Htanwin = QRadioButton('Tanwin')
		self.Hcampur = QRadioButton('Campur')
		
		self.modeLayout = QHBoxLayout()
		self.modeLayout.addWidget(self.belajar)
		self.modeLayout.addWidget(self.latihan)
		self.modeLayout.setAlignment(Qt.AlignCenter)
		self.modeGroup = QGroupBox()
		self.modeGroup.setLayout(self.modeLayout)
		
		self.levelLayout = QHBoxLayout()
		self.levelLayout.addWidget(self.Hdasar)
		self.levelLayout.addWidget(self.Hharokat)
		self.levelLayout.addWidget(self.Htanwin)
		self.levelLayout.addWidget(self.Hcampur)
		self.levelGroup= QGroupBox()
		self.levelGroup.setLayout(self.levelLayout)
		
		self.btMulai = QPushButton('Mulai')
		self.btKeluar = QPushButton('Keluar')
		self.btKeluar.setObjectName('btKeluar')#set css element id
		
		self.btLayout = QHBoxLayout()
		self.btLayout.addWidget(self.btMulai)
		self.btLayout.addWidget(self.btKeluar)
		
		
		self.FirstLayout = QVBoxLayout()
		self.FirstLayout.addWidget(self.modeGroup)
		self.FirstLayout.addWidget(self.levelGroup)
		self.FirstLayout.addLayout(self.btLayout)
		
		self.RecentSessionTitle = QLabel ('Kegiatan Terakhir')
		self.RecentSessionTitle.setStyleSheet("color: white; font-style: bold;")
		self.RecentSessionList = QListWidget()
		#self.RecentSessionList.addItem("31-07-2013 Belajar Tanwin 81 3 2:08")
		
		self.SecondLayout = QVBoxLayout()
		self.SecondLayout.addWidget(self.RecentSessionTitle)
		self.SecondLayout.addWidget(self.RecentSessionList)
	
                self.mainLayout = QHBoxLayout()
                self.mainLayout.addLayout(self.FirstLayout)
                self.mainLayout.addLayout(self.SecondLayout)
		
		self.setLayout(self.mainLayout)
		self.resize(700,500)
		
	
	
	def gaya(self):
		#self.setWindowFlags(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground)
		#file = QFile('menu.css')
		#file.open(QFile.ReadOnly)
		#style = file.readAll()
		#style = unicode(style, encoding='utf8') #python 2 use str for python 3
		cssFile = open('menu.css')
		style = ''.join(cssFile.readlines())
		cssFile.close()
		self.setStyleSheet(style)
		
	def senter(self):
		resolution = QDesktopWidget().screenGeometry()
		self.move((resolution.width()/2-float(self.width()/2))+1,float(resolution.height()/2)-float(self.height()/2)+1)
		
	def keluar(self):
		self.close()
		
	def listRecentSessions(self):
		fin = open('sessions.txt')
		summs = fin.readlines()
		summs= "".join(summs).split('****\n')
		summs.pop()
		fin.close()
		
		if len(summs) !=0:
			for i in summs:
				item = QListWidgetItem()
				item.setText('')
				self.RecentSessionList.addItem(item)
				self.gap = QLabel(i)
				nilai = i.split('\n')[-2]
				nilai = nilai[nilai.index(":")+1:].lstrip()
				self.btRetake = QPushButton(nilai)
				self.btRetake.setObjectName('btRetake')
				newItemLayout = QHBoxLayout()
				newItemLayout.addWidget(self.gap)
				newItemLayout.addWidget(self.btRetake)
				newItem = QWidget()
			
				newItem.setLayout(newItemLayout)
				item.setSizeHint(newItem.sizeHint())
				self.RecentSessionList.setItemWidget(item, newItem)
	
		
				self.btRetake.clicked.connect(self.viewList)
		#print dir(item.data(0).data())
		
	def sendOption(self):
		self.newSession = Session(self.mode, self.level)
		
		self.winSessi = WinSession(self.newSession)
		self.winSessi.start()
		self.close()
				
	def setOption(self, mode, level):
		self.mode = mode
		self.level = level
		
	def keyPressEvent(self, event):
		if event.key() in (Qt.Key_Enter, Qt.Key_Return):
			self.sendOption()
			
	def viewList(self):
		pass
		#print self.RecentSessionList.currentItem().text()
		
		
	def pasangSlot(self):
		self.btMulai.clicked.connect(self.sendOption)
		self.btKeluar.clicked.connect(self.keluar)
		self.belajar.clicked.connect(lambda : self.setOption('Belajar',self.level))
		self.latihan.clicked.connect(lambda : self.setOption('Latihan',self.level))
		self.Hdasar.clicked.connect(lambda : self.setOption(self.mode,'Dasar'))
		self.Hharokat.clicked.connect(lambda : self.setOption(self.mode,'Harokat'))
		self.Htanwin.clicked.connect(lambda : self.setOption(self.mode,'Tanwin'))
		self.Hcampur.clicked.connect(lambda : self.setOption(self.mode,'Campur'))
		self.RecentSessionList.clicked.connect(self.viewList)

		
		
if __name__ == '__main__':
	QA = QApplication([])
	w = Menu()
	QA.exec_()
		
		