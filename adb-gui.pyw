# An ADB shortcut tool for uploading and downloading data to the Robot SD Card
# by Aedan Cullen

#Windows ridiculousness
#import ctypes
#myappid = 'eanmanager' # random
#ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from PyQt4 import QtGui, QtCore
from gui import Ui_ADBGui
import subprocess

class ADBGui(QtGui.QWidget, Ui_ADBGui):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.setupUi(self)
		
		self.resourceList.setStyleSheet("background-image: url('evolution-small.png'); background-repeat: no-repeat; background-position: center;")
		
		self.tcpButton.clicked.connect(self.tcpButtonClicked)
		self.connectButton.clicked.connect(self.connectButtonClicked)
		self.disconnectButton.clicked.connect(self.disconnectButtonClicked)
		self.uploadButton.clicked.connect(self.uploadButtonClicked)
		self.downloadButton.clicked.connect(self.downloadButtonClicked)
		self.deleteButton.clicked.connect(self.deleteButtonClicked)
		
		self.updateUploadList();
		
	def updateUploadList(self):
		self.resourceList.clear()
		try:
			output = subprocess.check_output('adb shell ls "/mnt/sdcard/"', shell=True)
		except:
			return
		if 'error' in output or 'invalid' in output or 'No such file or directory' in output:
			QtGui.QMessageBox.warning(self, 'ADB GUI', 'Could not list files on the SD card. If you are not using one, ignore this.')
			return
		for name in output.split('\n'):
			if name != '':
				self.resourceList.addItem(QtCore.QString(name))
		
	def tcpButtonClicked(self):
		ret = subprocess.call(['adb','tcpip','5555'])
		if ret != 0:
			QtGui.QMessageBox.warning(self, 'ADB GUI', 'Could not switch to TCP/IP mode. Is a device connected by USB?')
			return
		QtGui.QMessageBox.information(self, 'ADB GUI', 'TCP/IP mode has been enabled on the USB-connected device.')
		
	def connectButtonClicked(self):
		text, ok = QtGui.QInputDialog.getText(self, 'ADB GUI', 'Enter the IP address of the device:')
		if ok:
			try:
				output = subprocess.check_output(['adb','connect',str(text)])
			except:
				QtGui.QMessageBox.warning(self, 'ADB GUI', 'Could not connect to the device.')
				return
			if 'unable to connect' in output or 'invalid' in output or 'error' in output:
				QtGui.QMessageBox.warning(self, 'ADB GUI', 'Could not connect to the device.')
				return
			QtGui.QMessageBox.information(self, 'ADB GUI', 'Connected successfully.')
			self.updateUploadList()
			
		
	def disconnectButtonClicked(self):
		subprocess.call(['adb','disconnect'])
		self.resourceList.clear()
		QtGui.QMessageBox.information(self, 'ADB GUI', 'Disconnected from any devices.')
		
	def uploadButtonClicked(self):
		name = str(QtGui.QFileDialog.getOpenFileName(self, 'Select a file to upload'))
		if not name:
			return
		else:
			filename = name.split('/')[-1]
			try:
				output = subprocess.check_output('adb push "' + name + '" "/mnt/sdcard/' + filename + '"', shell=True)
			except:
				QtGui.QMessageBox.warning(self, 'ADB GUI', 'Could not upload the file.')
				return
			if 'error' in output or 'invalid' in output or 'No such file or directory' in output:
				QtGui.QMessageBox.warning(self, 'ADB GUI', 'Could not upload the file.')
				return
			QtGui.QMessageBox.information(self, 'ADB GUI', 'Uploaded successfully!')
			self.updateUploadList()
			
		
	def downloadButtonClicked(self):
		if len(self.resourceList.selectedItems()) != 0:
			itemtext = str(self.resourceList.selectedItems()[0].text())
			location = str(QtGui.QFileDialog.getSaveFileName(self, 'Select a location to save'))
			if not location:
				return
			else:
				try:
					output = subprocess.check_output('adb pull "/mnt/sdcard/' + itemtext + '" "' + location + '"', shell=True)
				except:
					QtGui.QMessageBox.warning(self, 'ADB GUI', 'Could not download the file.')
					return
				if 'error' in output or 'invalid' in output or 'No such file or directory' in output:
					QtGui.QMessageBox.warning(self, 'ADB GUI', 'Could not download the file.')
					return
				QtGui.QMessageBox.information(self, 'ADB GUI', 'Downloaded and saved successfully!')
				self.updateUploadList()
		else:
			QtGui.QMessageBox.warning(self, 'ADB GUI', 'No resource is selected.')
			
		
	def deleteButtonClicked(self):
		if len(self.resourceList.selectedItems()) != 0:
			itemtext = str(self.resourceList.selectedItems()[0].text())
			reply = QtGui.QMessageBox.question(self, 'ADB GUI', 'Are you sure you want to delete the file "' + itemtext.strip() + '"?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes:
				try:
					output = subprocess.check_output('adb shell rm "/mnt/sdcard/' + itemtext + '"', shell=True)
				except:
					QtGui.QMessageBox.warning(self, 'ADB GUI', 'Could not delete the file.')
					return
				if 'error' in output or 'invalid' in output or 'No such file or directory' in output:
					QtGui.QMessageBox.warning(self, 'ADB GUI', 'Could not delete the file.')
					return
				QtGui.QMessageBox.information(self, 'ADB GUI', 'Deleted successfully.')
				self.updateUploadList()
		else:
			QtGui.QMessageBox.warning(self, 'ADB GUI', 'No file is selected.')
		

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	manager = ADBGui()
	manager.show()
	sys.exit(app.exec_())
