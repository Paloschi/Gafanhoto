# -*- coding: utf-8 -*-
'''
Created on 13/10/2015

@author: Rennan
'''
from Modelo.Funcoes.RasterTools import RasterToCSVeVRT
from Modelo.Funcoes.Interpoladores import IDW
from Modelo.beans import SerialFile, TableData
from PyQt4 import QtCore
from Controle import AbstractController
import os.path
from Modelo.beans.RasterData import RasterFile

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class Controller(AbstractController.Controller):
    '''
    classdocs
    
    '''
    def findInFolder(self):
        self.findPath(self.ui.txInFolder, "folder")
        
    def findOutFolder(self):
        self.findPath(self.ui.txOutFolder, "folder")
  
    def findImgRef(self):
        self.findPath(self.ui.txImgReference)

    def valida_form(self):
        if not os.path.exists(self.ui.txInFolder.text()):
            self.message(u"Pasta de entrada das imagens não encontrada, verifique o endereço.")
            return False   
        if not os.path.exists(self.ui.txOutFolder.text()):
            self.message(u"Pasta de saida das imagens não encontrada, verifique o endereço.")
            return False
        if not os.path.exists(self.ui.txImgReference.text()):
            self.message(u"Imagem de referencia das imagens não encontrada, verifique o endereço.")
            return False     
        return True

    def executa(self):
        
        '''
            Criando arquivos CSVs e VRTs para submeter a interpolação
        '''
        
        self.print_text(u'Criando arquivos necessários para a interpolação')
        
        self.function = RasterToCSVeVRT()
        paramIn = TableData()
        paramIn["images"] = SerialFile(root_path=str(self.ui.txInFolder.text()))
        paramIn["out_folder"] = str(self.ui.txOutFolder.text())
        
        resposta = self.function.executar(paramIn)
        
        if self.funcao_cancelada() : return
        
        CSVs = resposta["CSVs"]
        VRTs = resposta["VRTs"]
        
        self.print_text("Numero de imagens identificadas para interpolar: " + str(len(CSVs)))
        
        conf_algoritimo = TableData()
        conf_algoritimo["power"] = str(self.ui.txPower.value())
        conf_algoritimo["radius"] = str(self.ui.txRadius.value())
        conf_algoritimo["max_points"] = str(self.ui.txMaxPoint.value())
        conf_algoritimo["min_points"] = str(self.ui.txMinPoint.value())
        
        conf_img_out = RasterFile(file_full_path=str(self.ui.txImgReference.text())).getRasterInformation()
        
        self.print_text("Interpolando imagens")
           
        for i in range(len(CSVs)):
            
            img_out = RasterFile(file_full_path=VRTs[i].file_full_path)
            img_out.file_ext = "tif"           
            
            paramIn = TableData()
            paramIn["csv"] = CSVs[i]
            paramIn["vrt"] = VRTs[i]
            paramIn["img_out_config"] = conf_img_out
            paramIn["conf_algoritimo"] = conf_algoritimo
            paramIn["img_out"] = img_out
            
            self.function = IDW()
            
            self.function.progresso = (float(i+1) / len(CSVs)) * 100
            
            imagem_interpolada = self.function.executar(paramIn)
            
            self.print_text("Imagem interpolada: " + imagem_interpolada.file_name)
            
            if self.funcao_cancelada() : return


            
            
            
            
            
            
            
            
            