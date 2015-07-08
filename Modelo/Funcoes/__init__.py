# -*- coding: utf-8 -*-
#from Filtro import *
#from GetImageInformation import *
#from GetShapeData import *
#from Interpola import *
#from PerfilExtractor import *
#from Soma import *
#from SplitTable import *
#from teste_str import *

def adicionarSufixo(path, sufixo):
    
    ext = path.split(".")[-1]
    extPonto = "." + ext
    pathComSufixo = path.replace(extPonto, sufixo + extPonto)
    return pathComSufixo

def trocarExt(path, extNova):
    
    extVelha = path.split(".")[-1]
    pathNovaExt = path.replace(extVelha, extNova)
    return pathNovaExt
    
def CreateInterpolationTable(file_tif_out_path, file_vrt_path,  format_image_data):
      
        cvs_name = file_vrt_path.split("/")[-1].split(".")[0]
        format_image_data["fileIn"] = file_vrt_path
        format_image_data["fileOut"] = file_tif_out_path
        format_image_data["name_file"] = cvs_name
        
        return format_image_data

if __name__ == '__main__':
    
    import RasterToCSVeVRT
    import GetImageInformation
    from Modelo.beans import Dados
    import Interpola
       
    rootImgPathTeste = "C://Users//Paloschi//Desktop//data//Testes//ImagemExemploEcmwf//"
    rootImgReference = "C://Users//Paloschi//Desktop//data//Rasters//Modis//2010-2011//20101016.250m_16_dias_EVI_MOD13Q1_PR.tif"
    rootImgOut = "C://Users//Paloschi//Desktop//data//Testes//saida//"
    sufixo = "_250m_Sm1"
    
    '''
        ------------------- Criando arquivos CSV e VRT para interpolacao --------------------
    '''
    
    imgPathTeste = Dados.SerialData()
    imgPathTeste.loadListByRoot(rootImgPathTeste, "img")
    
    pathOut = Dados.SimpleData(data=rootImgOut)
    
    paramIN = Dados.TableData()
    paramIN["images"] = imgPathTeste
    paramIN["out_folder"] = pathOut
    
    getImgInfo = RasterToCSVeVRT.RasterToCSVeVRT()
    
    getImgInfo.data = paramIN
    resultado = getImgInfo.data

    VRTs = resultado["VRTs"]
    
    '''
        ------------------- Pegando informacoes da imagem de referencia --------------------
    '''
    
    imgRefer = Dados.SimpleData(data=rootImgReference)
    getImgInfo = GetImageInformation.GetImgInfo()
    
    paramIN = Dados.TableData()
    paramIN["imagem"] = imgRefer
    
    getImgInfo.data = paramIN
    imgReferInfo = getImgInfo.data
    
    paramInterpolador = imgReferInfo
    
    for i_img in range(0, len(VRTs)):
        vrt = VRTs[i_img].data
        img = trocarExt(vrt, "tif")
        img = adicionarSufixo(img, sufixo)
        
        paramInterpolador = CreateInterpolationTable(img, vrt, paramInterpolador)
        
        interpolador = Interpola.InterpoladorIvD()
        data = Dados.SimpleData(data= paramInterpolador)
        
        interpolador.data = data
        
        interpolador.data
        
        
        
        
        

    



