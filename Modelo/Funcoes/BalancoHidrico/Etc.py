# -*- coding: utf-8 -*-
'''
Created on Jul 22, 2015

@author: Paloschi
'''
from Modelo.Funcoes import AbstractFunction
from Modelo.beans import SERIAL_FILE_DATA, RasterData
import subprocess
import gdal
import sys
from Modelo.beans.RasterData import RasterFile
progress = gdal.TermProgress_nocb
import numpy

class Etc(AbstractFunction):
    '''
        Essa função calcula a evapotranspiração da cultura ETc, baseado nas datas de plantio, evapotranspiração de referencia
    e os coeficientes da cultura.
        Formula: ETc = Kc * ET0
        Onde o Kc varia dependendo do estado fenologico da cultura.
        Para efeitos de histórico, periodos de ETc anteriores ao periodo da cultura devem ser inseridos, por default quando a
    cultura não está presente, o Kc é considerado de valor 1
        
        Esta função não entende datas por isso todos os parametros devem ser passados com referencia a cena
    '''
    
    def __setParamIN__(self):
        
        self.descriptionIN["ET0"] = {"Required":True, "Type":SERIAL_FILE_DATA, "Description":"Série de imagens de evapotranspiração de referencia"}
        self.descriptionIN["Kc"] = {"Required":True, "Type":SERIAL_FILE_DATA, "Description":"Série de imagens de Kc distribuido"}
        self.descriptionIN["ETc"] = {"Required":True, "Type":SERIAL_FILE_DATA, "Description":"Objeto série de imagens configurao para saida"}
        #self.descriptionIN["dias_inicio"] = {"Required":True, "Type":None, "Description":"Indica quantos dias anteriores a primeira data de semeadura que deve ser considerado"}
    
    def __setParamOUT__(self):
        self.descriptionOUT["ETc"] = {"Type":SERIAL_FILE_DATA, "Description":"Série de imagens de evapotranspiração da cultura"}
    
    def __execOperation__(self):
        '''
            Por padrão agora assumo que, quando uma variavel tiver como sufixo um underline "_"
            é porque esta variavel contem os valores carregados (matrizes brutas) dos dados
        '''
        
        print("Carregando imagens (ET0, semeadura, colheita): ")
        
        serie_ET0 = self.paramentrosIN_carregados["ET0"].loadListByRoot() # pucha e já carrega a lista caso não tenha sido carregada
        serie_Kc = self.paramentrosIN_carregados["Kc"].loadListByRoot() # pucha e já carrega a lista caso não tenha sido carregada
        serie_ETc = self.paramentrosIN_carregados["ETc"] # pucha lista
        
        Kc_factor = float(serie_Kc.mutiply_factor)
        ET0_factor = float(serie_ET0.mutiply_factor)
        ETC_factor = float(serie_ETc.mutiply_factor)

        for i_ET0 in range(len(serie_ET0)):
            
            #gdal_calc.py [-A <filename>] [--A_band] [-B...-Z filename] [other_options]
            ET0 = serie_ET0[i_ET0]
            
            data_ET0 = serie_ET0.getDate_time(file=ET0)
            
            kc = None
            
            for i_Kc in range(len(serie_Kc)):
                
                data = serie_Kc.getDate_time(file=serie_Kc[i_Kc])
                if data == data_ET0:
                    kc = serie_Kc[i_Kc]
            
            etc = RasterFile(file_path=serie_ETc.root_path, ext="tif", file_name=ET0.file_name)
            
            ET0_ = numpy.array(ET0.loadRasterData()).astype(dtype="float32") #* ET0_factor
            
            if kc == None: # caso não encontre nenhum kc correspondente a mesma data
                etc.data = ET0_ * ETC_factor
                
            else: 
                    
                Kc_ = numpy.array(kc.loadRasterData()).astype(dtype="float32")  #* Kc_factor
                
                #ETc_ = numpy.array(kc.loadRasterData()).astype(dtype="float32")
                
                Kc_[Kc_==0] = 100
                
                ETc_ = (Kc_ * ET0_) / 100
                
                            
                if serie_ETc.out_datatype != None:
                    ETc_ = numpy.array(ETc_).astype(serie_ETc.out_datatype)
                    
                etc.data = ETc_ #* ETC_factor
                
                #for i in range(len(ET0_)):
                #    for ii in range (len(ET0_[0])):
                #        if ET0_[i][ii] != 0 : 
                #            print "---------------------------"
                #            print Kc_[i][ii]
                 #           print ET0_[i][ii]
                #            print ETc_[i][ii]
                #            print "---------------------------"
                            
                    
                

                
                
            etc.metadata = ET0.metadata
            etc.saveRasterData()
            
    
    def procurar_descende_correspondente(self, data, serie_temporal):
        '''
            Esse método procura a imagem correspondente para a data informada (feito para capturar o descende correto)
        '''
        img_correspondente = None
        
        for i_img in range(len(serie_temporal)-1):
            data_img =  serie_temporal.getDate_time(i_img)
            data_img_1 = serie_temporal.getDate_time(i_img+1)
            if data_img == data : 
                img_correspondente = serie_temporal[i_img]
                self.dias_decend = (data_img_1 - data_img).days
                break
            elif data_img < data and data_img_1 > data: 
                img_correspondente = serie_temporal[i_img]
                self.dias_decend = (data_img_1 - data_img).days
        
        if img_correspondente == None : img_correspondente = serie_temporal[-1]
           
        return img_correspondente

if __name__ == '__main__':
    from Modelo.beans import SerialTemporalFiles
    
    serie_Kc = SerialTemporalFiles(root_path="E:\\Gafanhoto WorkSpace\\Soja11_12\\Indices_BH\\Kc_distribuido\\soltas")
    serie_Kc.mutiply_factor = 0.01
    serie_Kc.date_mask = "%Y-%m-%d"
    
    serie_ET0 = SerialTemporalFiles(root_path="E:\\Gafanhoto WorkSpace\\Soja11_12\\Tratamento de dados\\ECMWF\\8-Diario\\EVPT 07-11 _ 05-12")
    serie_ET0.mutiply_factor = 0.01
    serie_ET0.sufixo = "evpt_diario_"
    serie_ET0.date_mask = "%Y-%m-%d"
    
    serie_ETC = SerialTemporalFiles(root_path="E:\\Gafanhoto WorkSpace\\Soja11_12\\Indices_BH\\ETc\\soltas")
    serie_ETC.mutiply_factor = 100
    serie_ETC.out_datatype = "int16"
    serie_ETC.sufixo = "ETc_"
    serie_ETC.date_mask = "%Y-%m-%d"
    
    paramIN = dict()
    paramIN["ET0"] = serie_ET0
    paramIN["ETc"] = serie_ETC
    paramIN["Kc"] = serie_Kc
    
    Etc().executar(paramIN)
    


