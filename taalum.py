# -*- coding: utf-8 -*-
from soal import *

import random,sys, time, datetime		
class Session(object):
	def __init__(self, mode, soal):
		''''
		soal : dictionary
		'''
		
		self.mode = mode
		self.level = soal
		self.soal = eval(soal).copy()
		self.dijawab = []
		self.jumlahSoal = len(self.soal)
		self.benar = 0
		self.salah = 0
		self.nilai = 0
		self.waktu = "00"
	
	def __str__(self):
		ket = "mode\t\t:\t{0}\nsoal\t\t:\t{1}\njumlah soal\t:\t{2}\nbenar\t\t:\t{3}\nsalah\t\t:\t{4}\nwaktu\t\t:\t{5}\nnilai\t\t:\t{6}\n".format(
		self.mode,
		self.level,
		self.jumlahSoal,
		self.benar,
		self.salah,
		self.waktu,
		self.nilai
		)
		return ket
	
	def getTimeLength(self, startingTime):
		begin = "{0}:{1}:{2}".format(str(startingTime[3]), str(startingTime[4]), str(startingTime[5]))
		end = time.localtime()
		end = "{0}:{1}:{2}".format(str(end[3]), str(end[4]), str(end[5]))
		lama = datetime.datetime.strptime(end, "%H:%M:%S") -  datetime.datetime.strptime(begin, "%H:%M:%S")
	        minutes = lama.seconds/60
	        seconds = lama.seconds%60
	        if seconds < 10: 
			seconds = '0'+str(seconds)
		self.waktu = "{0}:{1}".format(str( minutes), str(seconds))
		
		
	def getQuestion(self):
		if len(self.soal):
			question = random.choice(self.soal.keys())	
			if not question in self.dijawab:
				return question
		return None
			
	def getAnswer(self, question):
		return self.soal[question]
	
	def takeAnswer(self, question, answer):
		self.dijawab.append(question)
		try:
			if answer== self.soal[question]:
				self.benar+=1
				del self.soal[question]
				return "BENAR"
			raise KeyError
		except KeyError:
				self.salah+=1
				return "SALAH"

	## text mode
	def start(self):
		StartTime = time.localtime()
		while True:
			q = self.getQuestion()
			if q:
				print q
				jaw = raw_input('latin :  ')
				print self.takeAnswer(q, jaw)
			else:
				self.getTimeLength(StartTime)
				self.nilai = self.benar/self.jumlahSoal*100
				print self
				break

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Com(QObject):
	enterPressed = pyqtSignal(str)

class TestedLineEdit(QLineEdit):
	def __init__(self):
		super(TestedLineEdit, self).__init__()
		self.c = Com()
	
	def keyPressEvent(self, event):
		QLineEdit.keyPressEvent(self, event)
		if event.key() == 16777220:
			self.c.enterPressed.emit(self.text())	
			
class WinSession(QWidget):
	def __init__(self, session):
		self.session = session
		super(WinSession, self).__init__()
		self.pakeBaju()
		self.center()
		self.setSlotAndSignal()
		#self.bergaya()
		self.timer.start(1000, self)
		
	def pakeBaju(self):
		self.soal = QLabel()
		self.soal.setAlignment(Qt.AlignCenter)
		self.soal.setFixedSize(250,200)
		
		self.gap = QLabel()
		self.gap.setFixedSize(100,100)
		
		self.jaw = TestedLineEdit()
		self.jaw.setFont(QFont("Ubuntu", 100))
		self.jaw.setAlignment(Qt.AlignCenter)
		self.jaw.setFixedSize(300,200)
		
		self.soalJawLayout = QVBoxLayout()
		self.soalJawLayout.addWidget(self.soal)
		#self.soalJawLayout.addItem(QSpacerItem(10,10,QSizePolicy.Expanding))
		self.soalJawLayout.addWidget(self.gap)
		self.soalJawLayout.addWidget(self.jaw)
		
		self.timer = QBasicTimer()
		self.lbTimer = QLabel("0:00")
		self.lbTimer.setFont( QFont("Ubuntu", 45))
		
		self.progress = QProgressBar()
		self.progress.setValue(50)
		
		self.layout = QGridLayout()
		self.layout.addWidget(self.lbTimer, 0,0)
		self.layout.addWidget(self.progress,0,1)
		self.layout.addLayout(self.soalJawLayout,1,1)
		
		
		self.setLayout(self.layout)
		self.setWindowTitle("Hijaiyah")
		self.show()
		
	def timerEvent(self, event):
		minutes = int(str(self.lbTimer.text())[:str(self.lbTimer.text()).index(':')])
		seconds = int(str(self.lbTimer.text())[str(self.lbTimer.text()).index(':')+1:])
		if seconds >= 59:
			minutes = minutes +1
			seconds = "00"
		else:
			seconds =seconds + 1
			if seconds < 10:
				seconds = '0'+str(seconds)
		value = "{0}:{1}".format(str(minutes),str( seconds))
		self.lbTimer.setText(QString(value))
		
	def bergaya(self):
		gaya = " TestedLineEdit { border-image: url(text-background.png);}"
		self.setStyleSheet(gaya)
		self.setAttribute(Qt.WA_TranslucentBackground)
		
	def setSlotAndSignal(self):
		def sendAnswer():
			if self.session.mode == 'Belajar':
				so = unicode(self.soal.text()).encode('utf-8')
				so = so[:so.index('<')].strip()
				self.session.dijawab.append(so)
				del self.session.soal[so]
				self.putQuestion()
				return
			
			if self.session.takeAnswer(unicode(self.soal.text()).encode('utf-8'), self.jaw.text()) == "SALAH":
				ans="{0} < {1} >".format(unicode(self.soal.text()).encode('utf-8'),self.session.getAnswer(unicode(self.soal.text()).encode('utf-8')))
				del self.session.soal[unicode(self.soal.text()).encode('utf-8')]
				self.soal.setFont(QFont("KacstPen", 30))
				self.soal.setText(ans.decode('utf-8'))
				QTimer.singleShot(1000, lambda: self.putQuestion() )
			else:
				 self.putQuestion()
				 
		self.jaw.c.enterPressed.connect(sendAnswer)
		
	def putQuestion(self):
		self.progress.setValue(len(self.session.dijawab)/float(self.session.jumlahSoal)*100)
		self.jaw.clear()
		q = self.session.getQuestion()
		if q:
			
			if self.session.mode == 'Belajar':
				self.soal.setFont(QFont("KacstPen", 35))
				ans="{0} < {1} >".format(q,self.session.getAnswer(q))
				self.soal.setText(ans.decode('utf-8'))
			else:
				self.soal.setFont(QFont("KacstPen", 50))
				self.soal.setText(q.decode("utf-8"))
		else: # end session
			self.end()
	
		
	def start(self):
		self.StartTime = time.localtime()
		self.putQuestion()
	
	def end(self):
		self.session.getTimeLength(self.StartTime)
		self.timer.stop()
		self.session.nilai = round(self.session.benar/float(self.session.jumlahSoal)*100)
		self.summ =  SessionSummary(str(self.session))
		self.close()
	
	def center(self):
		resolution = QDesktopWidget().screenGeometry()
		self.move((resolution.width()/2-float(self.width()/2))+1,float(resolution.height()/2)-float(self.height()/2)+1)

class SessionSummary(QWidget):
	def __init__(self, summary):
		super(SessionSummary, self).__init__()
		self.summary = QLabel(summary)
		self.pakeBaju()
		self.show()
		self.center()
		
	def pakeBaju(self):
		self.Lay = QGridLayout()
		self.Lay.addWidget(self.summary,0,0)
		self.setLayout(self.Lay)
		self.setWindowTitle("Session Summary")
		
	def getCurrentSessionsList(self):
		inF = open('sessions.txt')
		SList = inF.readlines()
		inF.close()
		SList = "".join(SList).split('****\n')
		SList.pop()
		return SList
		
	def closeEvent(self, event):
		
		SL = self.getCurrentSessionsList()
		
		
		if len(SL) >= 4: 
			SL.pop()
		newSS = str(self.summary.text())
		SL.insert(0,newSS)
		
		
		
		fout = open('sessions.txt','w')
		for SS in SL:
			fout.write(SS)
			fout.write('****\n')
		fout.close()
		
		from menu import Menu
		mn = Menu()
		self.close()
	
	def keyPressEvent(self, event):
		if event.key() in (Qt.Key_Enter, Qt.Key_Return):
			self.close()
		
	def center(self):
		resolution = QDesktopWidget().screenGeometry()
		self.move((resolution.width()/2-float(self.width()/2))+1,float(resolution.height()/2)-float(self.height()/2)+1)

if __name__ == "__main__" :
	a = QApplication([])
	sessi1 = Session(Menu())
	winSessi = WinSession(sessi1)
	winSessi.start()
	a.exec_()