# -*- coding: utf-8 -*-
""" Desenvolvido por PACHALY (2017) """

"""" Este algoritmo interpola o valor da precipitacao para um determinado 
        intervalo de tempo e duracao da chuva

    PARAMETROS:
        
        chuva = [...]
        tempo = [10.0, 15.0, 20.0, 30.0, 45.0, 60.0, 120.0, 240.0, 360.0, 720.0, 1440.0]
        intervalo = int
        duracao = int
        
        OBS: O tamanho da lista de chuva e tempo devem ser iguais
        
    LIMITACOES:
            
        O primeiro interalo de chuva é de 10 minuto
        A máxima duração é de 24h (1440 minutos)
        
    SAIDAS:
        
        interpolador(chuva,tempo,intervalo,duracao)[0] -> Lista do tempo interpolado (listaTempo)
        interpolador(chuva,tempo,intervalo,duracao)[1] -> Lista da precipitacao interpolada (listaChuva)
        
"""

from scipy import interpolate
import numpy as np
    
def interpolador(chuva, tempo, intervalo, duracaoChuva):

    arrayChuva = np.asarray(chuva)
    arrayTempo = np.asarray(tempo)
    interpolacao = interpolate.interp1d(arrayTempo, arrayChuva)
    
    #Pluviografos se mede de 10 em 10 minutos        
    tempoInicial = 10
    listaTempo = [10]
    listaChuva = []
    numIntervalos = (duracaoChuva*60/intervalo)
              
    quantidadeIntervalos = ((((numIntervalos*intervalo)- tempoInicial)/intervalo) + 1)
    
    
    for i in xrange(1,(int(quantidadeIntervalos))):
        listaTempo.append((i*intervalo)+tempoInicial)
    
    #print listaTempo, len(listaTempo)
    
    for x in listaTempo:
        listaChuva.append(interpolacao(x).tolist())
       
    return listaTempo, listaChuva       
                      
#TESTE

#Precipitacao = [36.8738, 46.4694, 53.8162, 64.8562, 76.296, 84.6142, 105.3318, 127.6252, 141.7626, 156.7326, 200.0]
#RelacaoTempo = [10.0, 15.0, 20.0, 30.0, 45.0, 60.0, 120.0, 240.0, 360.0, 720.0, 1440.0]

#lTempo = interpolador(Precipitacao, RelacaoTempo, 5, 24)[0]
#lChuva = interpolador(Precipitacao, RelacaoTempo, 5, 24)[1]
#print lTempo, len(lTempo)
#print lChuva, len(lChuva)