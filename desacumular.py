# -*- coding: utf-8 -*-
""" Desenvolvido por PACHALY (2017) """

"""" Este algoritmo desacumula e ordena em ordem decrescente uma precipitação

    PARAMETROS:
        
        chuva = [...]
        
    SAIDAS:
        
        desacumular(chuva) = [...]
        
"""

from interpolar import interpolador

def desacumulador(chuva):

    chuvaDesacumulada = []
    n = 0
        
    while len(chuvaDesacumulada) < len(chuva):
        if len(chuvaDesacumulada) == 0:
            chuvaDesacumulada.append(chuva[0])
        else:
            chuvaDesacumulada.append((chuva[n+1] - chuva[n]))
            n += 1
    
    chuvaDesacumulada = sorted(chuvaDesacumulada, reverse = True)
        
    return chuvaDesacumulada
    
#TESTE       

#Precipitacao = [36.8738, 46.4694, 53.8162, 64.8562, 76.296, 84.6142, 105.3318, 127.6252, 141.7626, 156.7326, 200.0]
#RelacaoTempo = [10.0, 15.0, 20.0, 30.0, 45.0, 60.0, 120.0, 240.0, 360.0, 720.0, 1440.0]

#Chuvinha = interpolador(Precipitacao, RelacaoTempo, 10, 12)[1]

#print interpolador(Precipitacao, RelacaoTempo, 10, 12)[0]
#print interpolador(Precipitacao, RelacaoTempo, 10, 12)[1]
 
#print Chuvinha
#print desacumulador(Chuvinha)

