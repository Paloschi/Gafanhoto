'''
Created on Jun 10, 2015

@author: Paloschi
'''
from PyQt4.QtGui import QFileDialog
from Modelo.Funcoes.Filtros import FiltroSavitzGolay
from Modelo.beans import FileData, TableData
from ctypes.wintypes import DOUBLE
from numpy import double
from PyQt4 import QtCore
import time
import thread

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
    
class Controller(object):
    '''
    classdocs
    '''
    def __init__(self, ui):
        
        self.ui = ui
    
    def findInFolder(self):
        self.findPath(self.ui.leInFolder)
        
    def findOutFolder(self):
        self.findPath(self.ui.leOutFolder)
  
    def findPath(self, textToWrite):
        fname = QFileDialog.getExistingDirectory()
        textToWrite.setText (fname)
        
    def action_ok(self):
        
        self.filtro = FiltroSavitzGolay()
        
        #self.executa(self.filtro)

        thread.start_new_thread( self.executa, (self.filtro,) )
        self.updatePBar, (self.filtro,)
        
    def actionCheckBox(self):
        
        if self.ui.checkBox.isChecked() :
            self.ui.leNullValue.setEnabled(True)
        else : self.ui.leNullValue.setEnabled(False)
    

    #def checa_progresso(self, extractor):
        
        #while(extractor.progresso<=100):
            #self.ui.progressBar.setProperty("value", extractor.progresso)
    
    def updatePBar(self, extractor):
        while(self.filtro.progresso<=100):
            self.ui.progressBar.setValue(self.filtro.progresso) 
            time.sleep(1)
            #print(self.extractor.progresso)
        
            
        
    def executa(self, filtro):
        
        root_out = self.ui.leOutFolder.text()
        root_out = _fromUtf8(str(root_out) + "\\")
        root_out = str(root_out).replace("\\", "/")
        
        parametrosIn = self.carregarParamIN()
        
        filtro.data = parametrosIn
        
        resultados = filtro.data
        
        imagens_filtradas = resultados["imagensFiltradas"]
        imagens = parametrosIn["images"]
        
        metadata = resultados["metaData"]
        
        imagens.metadata = metadata
    
        imagens.saveListByRoot(imagens_filtradas, root_out, "tif")
        
        
    def carregarParamIN(self):

        images = FileData()
        parametrosIN = TableData()
        root_in = self.ui.leInFolder.text()
        root_in = _fromUtf8(str(root_in) + "\\")
        root_in = str(root_in).replace("\\", "/")
        print(root_in)
        
        images.loadListByRoot(root_in, "tif")
        
        print("numero de imagens: " + str(len(images)))
        
        parametrosIN["images"] = images
        
        conf_algoritimo = dict()
        conf_algoritimo["window_size"] = self.ui.leWindowSize.text()
        conf_algoritimo["order"] = self.ui.leOrdem.text()
        if self.ui.checkBox.isChecked() : conf_algoritimo["null_value"] = FileData(file_full_path = self.ui.leNullValue.text())
        else : conf_algoritimo["null_value"] = FileData(data= None)
        
        self.descriptionIN["conf_algoritimo "] = conf_algoritimo
        
        return parametrosIN