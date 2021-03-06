# -*- coding: utf-8 -*-
'''
Created on Jul 8, 2015

@author: Paloschi
'''
from Modelo.Funcoes import AbstractFunction
from Modelo.beans.AbstractData import FILE_DATA, TABLE_DATA
from Modelo.beans.TableData import TableData
import subprocess
from Modelo.beans.FileData import FileData

class IDW(AbstractFunction):
    '''
        Essa função realiza a interpolação IDW (inverso da distancia) de arquivos CSV configurados por arquivos VRT
        ela necessita do GDAL Core instalado pra funcionar, e o path do GDAL Core tem que estar
        setado na variavel de ambiente path do windows
    '''
    
    def __setParamIN__(self):
        u'''
            Parametros de arquivos de dados (csv, vrt e imagem de saida)
        '''
        self.descriptionIN["csv"] = {"Required":True, "Type":FILE_DATA, "Description":"nome do arquivo CSV"}
        self.descriptionIN["vrt"] = {"Required":True, "Type":FILE_DATA, "Description":"caminho completo do arquivo VRT"}
        self.descriptionIN["img_out"] = {"Required":True, "Type":FILE_DATA, "Description":"Parametros de referencia para a imagem de saida"}
        
        '''
            Parametros de configuração do algorítimo
        '''
        conf_algoritimo = dict()
        conf_algoritimo["power"] = {"Required":False, "Type":None, "Description":"Weighting power (default 2.0)"}
        conf_algoritimo["smoothing"] = {"Required":False, "Type":None, "Description":"Smoothing parameter (default 0.0)"}
        conf_algoritimo["radius"] = {"Required":False, "Type":None, "Description":"The first radius (X axis if rotation angle is 0) of search ellipse. Set this parameter to zero to use whole point array. Default is 0.0"}
        conf_algoritimo["radius2"] = {"Required":False, "Type":None, "Description":"The second radius (Y axis if rotation angle is 0) of search ellipse. Set this parameter to zero to use whole point array. Default is 0.0."}
        conf_algoritimo["angle"] = {"Required":False, "Type":None, "Description":"Angle of search ellipse rotation in degrees (counter clockwise, default 0.0)"}
        conf_algoritimo["max_points"] = {"Required":False, "Type":None, "Description":"Maximum number of data points to use. Do not search for more points than this number. This is only used if search ellipse is set (both radii are non-zero). Zero means that all found points should be used. Default is 0"}
        conf_algoritimo["min_points"] = {"Required":False, "Type":None, "Description":"Minimum number of data points to use. If less amount of points found the grid node considered empty and will be filled with NODATA marker. This is only used if search ellipse is set (both radii are non-zero). Default is 0"}
        conf_algoritimo["nodata"] = {"Required":False, "Type":None, "Description":"NODATA marker to fill empty points (default 0.0)"}
        
        self.descriptionIN["conf_algoritimo"] = {"Required":False, "Type":TABLE_DATA, "Table_Description":conf_algoritimo,"Description":"tabela de parametros para configuração do algoritimo"}
        
        u'''
            Parametros de configuração da imagem de saida
        '''
        conf_img_out = dict()
        conf_img_out["xmin"] = {"Required":True, "Type":None, "Description":u"posição inicial x"}
        conf_img_out["xmax"] = {"Required":True, "Type":None, "Description":u"posição final x"}
        conf_img_out["ymin"] = {"Required":True, "Type":None, "Description":u"posição inicial y"}
        conf_img_out["ymax"] = {"Required":True, "Type":None, "Description":u"posição final y"}
        conf_img_out["ny"] = {"Required":True, "Type":None, "Description":"Numero de linhas da imagem"}
        conf_img_out["nx"] = {"Required":True, "Type":None, "Description":"Numero de colunas da imagem"}
        
        self.descriptionIN["img_out_config"] =  {"Required":True, "Type":TABLE_DATA, "Table_Description":conf_img_out, "Description":"configuração da imgagem de saida"}
        
    def __setParamOUT__(self):
        self.descriptionOUT["imagem_interpolada"] = "imagem de saida interpolada"  
        
    def __execOperation__(self):
        print "-----------------------------------------------------------------------------------"
        csv = self.paramentrosIN_carregados["csv"]
        vrt = self.paramentrosIN_carregados["vrt"]
        img_out = self.paramentrosIN_carregados["img_out"]
        img_out_config = self.paramentrosIN_carregados["img_out_config"]
        print "-----------------------------------------------------------------------------------"
        
        '''
            Monta string de de parametros para configurar o algoritimo IDW
        '''
        str_algoritimo_conf = ""
        print "-----------------------------------------------------------------------------------"
        print self.paramentrosIN_carregados["conf_algoritimo"]
        
        if self.paramentrosIN_carregados.has_key("conf_algoritimo") :
            
            conf_algoritimo = self.paramentrosIN_carregados["conf_algoritimo"]
            
            for key in conf_algoritimo.keys() :
                if (float(conf_algoritimo[key])!=float(0)):
                    str_algoritimo_conf += ":"
                    str_algoritimo_conf += (key + "=" + str(conf_algoritimo[key]))
                    
            str_algoritimo_conf += ':nodata=0'       
                
            print "configuracao do algoritimo" + str_algoritimo_conf
        
        
        '''
            Chama interpolador GDAl IDW
            http://www.gisinternals.com/query.html?content=filelist&file=release-1800-x64-gdal-mapserver.zip
        '''

        
        string_execucao = ['gdal_grid',  
                              
                              '-a', 'invdistnn' + str_algoritimo_conf,
                              '-txe', str(img_out_config["xmin"]), str(img_out_config["xmax"]), 
                              '-tye', str(img_out_config["ymin"]), str(img_out_config["ymax"]), 
                              '-outsize', str(img_out_config["nx"]), str(img_out_config["ny"]), 
                              '-of', 'GTiff', 
                              '-ot', 'Float32',
                              '-a_srs', 'EPSG:4326',
                              '-l', csv.file_name, vrt.file_full_path, img_out.file_full_path]
        
        #if str_algoritimo_conf != "":
            #string_execucao.append('-a')
            #string_execucao.append(str_algoritimo_conf)
        
            
        try:
            print ("string de execucao: ", str(string_execucao))
            resposta = subprocess.check_call(string_execucao, creationflags=subprocess.SW_HIDE, shell=True) 
            print (resposta)
   
        except Exception:  
            print Exception
            
        saida = img_out
        
        return saida

if __name__ == '__main__':   
    
    from Modelo.beans import SerialFile
    from Modelo.Funcoes.RasterTools import RasterToCSVeVRT
    
    '''
        CSV e VRT
    '''
    #img_teste_path = "C:\\Users\\rennan.paloschi\\Desktop\\Dados_Gerais\\raster\\ECMWF\\Teste_raster_csv\\Imagens"
    #img_teste = SerialFile(root_path=img_teste_path)
    #img_teste.loadListByRoot()
    
    #paramIN = dict()
    #paramIN["images"] = img_teste
    #paramIN["out_folder"] = "C:\\Users\\rennan.paloschi\\Desktop\\Dados_Gerais\\raster\\ECMWF\\Teste_raster_csv\\Saida\\"
    
    #csv_vrt_files = RasterToCSVeVRT().executar(paramIN)
    
    '''
        Imagem de referencia
    '''
    from Modelo.beans import RasterFile
    
    img_referencia_path = "C:\\Gafanhoto WorkSpace\\DataTestes\\raster\\Fazer\\20110101.tif"
    img_referencia = RasterFile(file_full_path = img_referencia_path)
    
    info_img_referencia = img_referencia.getRasterInformation()
    
    '''
        Conf algoritimo 
    '''
    conf_alg = TableData()
    #conf_alg["max_points"] = "12"
    #conf_alg["radius"] = "0"
    
    '''
        Imagem de saida
    '''
    img_out = RasterFile(file_full_path = "C:\\Gafanhoto WorkSpace\\DataTestes\\out\\Primeira tentativa\\evpt_20110101.tif")
    
    '''
        Unindo e executando
    '''
    paramIN = dict()
    #paramIN["csv"] = csv_vrt_files["CSVs"][0]
    #paramIN["vrt"] = csv_vrt_files["VRTs"][0]
    paramIN["csv"] = FileData(file_full_path="C:\\Gafanhoto WorkSpace\\DataTestes\\out\\Primeira tentativa\\evpt_20110101.csv")
    paramIN["vrt"] = FileData(file_full_path="C:\\Gafanhoto WorkSpace\\DataTestes\\out\\Primeira tentativa\\evpt_20110101.vrt")
    paramIN["img_out"] = img_out
    paramIN["conf_algoritimo"] = conf_alg
    paramIN["img_out_config"] = info_img_referencia
    
    imagem_interpolada = IDW().executar(paramIN)