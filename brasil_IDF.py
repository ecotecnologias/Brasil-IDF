# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BrasilIDF
                                 A QGIS plugin
 FAZER A DESCRIÇÃO
                              -------------------
        begin                : 2016-10-03
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Ecotecnologias
        email                : robsonleopachaly@yahoo.com.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4 import QtGui
from PyQt4.QtCore import QSettings, QCoreApplication, QTranslator, qVersion, Qt
from PyQt4.QtGui import QIcon, QAction
from brasil_IDF_dialog import BrasilIDFDialog
from qgis.gui import QgsMapTool, QgsMapToolEmitPoint
from qgis.core import QgsPoint, QgsVectorLayer, QgsFeature, QgsGeometry, QgsMapLayerRegistry
from qgis.utils import *
import os
import processing
import resources
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
import webbrowser
from interpolar import interpolador
from desacumular import desacumulador

class BrasilIDF(QgsMapTool):
    
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.
	
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """

        #############################################
        #Deixa o Canvas do QGIS manuseável, não tenho muita certeza ainda
        self.iface = iface

        #QgsMapTool.__init__(self, iface.mapCanvas())   
	self.canvas = self.iface.mapCanvas()
	#QgsMapToolEmitPoint.__init__(self.canvas)
	self.clickTool = QgsMapToolEmitPoint(self.canvas)
        #############################################
                             
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'BrasilIDF_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = BrasilIDFDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Brasil IDF')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'BrasilIDF')
        self.toolbar.setObjectName(u'BrasilIDF')
        
        #======================================================================#
                
        #Limpa o texto que ja foi escrito e conecta ao select_output_file1
        self.dlg.caminhoTexto.clear()
        self.dlg.botaoTexto.clicked.connect(self.select_output_file)  
        
        #DURACAO - Pega o clique do botão rodar e conecta ao run
        self.dlg.rodarDuracao.clicked.connect(self.run)
        
        #BLOCOS_ALTERNADOS - Pega o clique do botão rodar e conecta ao run1
        self.dlg.rodarBlocos.clicked.connect(self.run1)
        
        #CURVA_I-D-F - Pega o clique do botão rodar e conecta ao run2
        self.dlg.rodarIDF.clicked.connect(self.run2)
        
        #CURVA_P-D-F - Pega o clique do botão rodar e conecta ao run3
        self.dlg.rodarPDF.clicked.connect(self.run3)
        
        #Pega o clique do botão fechar e conect a função fechar
        self.dlg.fechar.clicked.connect(self.fechar)

        #======================================================================#   
		
    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('BrasilIDF', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/BrasilIDF/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Brasil IDF'),
            callback=self.run,
            parent=self.iface.mainWindow())
            
    #============================================================      
    
    #Abre o file browser e colocar o widget do line edit com o caminho do arquivo
    def select_output_file(self):
        
        filename = QtGui.QFileDialog.getExistingDirectory(self.dlg, 'Selecione uma pasta de saida:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)   
        self.dlg.caminhoTexto.setText(filename) 
                                                                                                           
    #Quando clica no botão do + pega a coordenada do sistema e transforma pra WGS84  
     
    #def selButton(self):
        
        #self.iface.mapCanvas().xyCoordinates.connect(self.showCoordinates)
        
    #def showCoordinates(self, currentPos):
                
        #Variável com SCR do usuário   
        #crsSrc = self.iface.mapCanvas().mapRenderer().destinationCrs()
        #Variável com o SCR WGS84
        #crsWGS = QgsCoordinateReferenceSystem(4326)
        
        #Posição no mapa
        #x = currentPos.x()
        #y = currentPos.y()
        
        #Transforma do SCR do usuário para o WGS 84
        #xform = QgsCoordinateTransform(crsSrc, crsWGS)
	#point = xform.transform(QgsPoint(x,y))
        
        #Transforma em string para colocar na caixa de texto, com precisão de 2 casas decimais                     
        #xx = "%.2f" % point.x()
	#yy = "%.2f" % point.y()
        
        #Coloca na caixa de texto os valores de lat long
        #self.dlg.lat_line.setText(xx)
	#self.dlg.long_line.setText(yy)    
	
    #Fecha a janela depois de clicar em fechar          
    def fechar(self):
        self.dlg.close()
        
    #Função para plotagem de gráfico        
    def plotagem(self, x, y, titulo, teixox, teixoy, diretorio):
        plt.close()
        plt.plot(x, y)
        plt.title(titulo)
        plt.xlabel(teixox)
        plt.ylabel(teixoy)
        plt.grid(True)
        plt.savefig(diretorio)
        plt.close()
        webbrowser.open(diretorio)
        
#===================================================================================================================================        
        
    def aplicar_BlocosAlternados(self, precipitacao_desacumulada, numero_intervalos_tempo_chuva, posicao_pico):
        """
Aplica o metodo dos blocos alternados a partir de uma serie de dados de chuva desacumulada e retorna a precipitacao ordenada.
No metodo dos blocos alternados, os valores incrementais sao reorganizados 
de forma que o maximo incremento ocorra, aproximadamente, no meio da duracao 
da chuva total. Os incrementos (ou blocos de chuva) seguintes sao organizados 
a direita e a esquerda alternadamente, ate preencher toda a duracao, segundo 
Collischonn e Tassi, 2013.

Esta funcao retorna a chuva ordenada em uma variavel do tipo lista
        precipitacao_ordenada = [...]

    Parametros para uso:
            -> precipitacao_desacumulada: Lista que contem os dados de chuva desacumulada.
                * precipitacao_desacumulada = [...] -> Dados de chuva desacumulada [em mm/s].
                OBS: A variável precipitacao_desacumulada DEVE estar em ordem DECRESCENTE.
                
            -> numero_intervalos_tempo_chuva: Variavel do tipo inteiro que armazena o numero de intervalos de tempo COM CHUVA da operacao.
                * numero_intervalos_tempo_chuva = 1440
                
            -> posicao_pico: Variavel do tipo float que armazena a posicao da maior precipitacao desacumulada em porcentagem decimal.
                * Exemplos: posicao_pico = 0.5 -> Pico em 50 porcento do tempo da simulacao
                posicao_pico = 0.2 -> Pico em 20 porcento do tempo da simulacao"""

    #  Algoritmo original escrito por Daniel Allasia, revisado e otimizado por Vitor Geller.
    # Ordena a chuva pelo metodo dos blocos alternados
    
    #   Se o posicao_pico nao esta no range correto
        if (float(posicao_pico) < 0 or float(posicao_pico) > 1):
            iface.messageBar().pushMessage("Erro", "O valor do pico de chuvas (posicao_pico) deve estar entre zero e um (0 <= posicao_pico <= 1)", level=QgsMessageBar.CRITICAL)
            return None

    #   Se o tamanho de precipitacao_desacumulada nao e' igual ao numero de intervalos de tempo com chuva
        if len(precipitacao_desacumulada) != numero_intervalos_tempo_chuva:
            iface.messageBar().pushMessage("Erro", "O numero de intervalos de tempo com chuva deve ser igual ao tamanho da série de precipitacoes desacumuladas", level=QgsMessageBar.CRITICAL)
            return None

    #   Se nao parou ate aqui, continue...
    
    #   Se posicao_pico for zero
        if (float(posicao_pico) == 0.0):
            indice_pico = 0

    #   Se numero_intervalos_tempo_chuva for par
        elif numero_intervalos_tempo_chuva % 2 == 0:
            indice_pico = (int(posicao_pico*numero_intervalos_tempo_chuva)-1)   #estimo a localizacao do pico em numero de intervalos de tempo com relacao a duracao da chuva
        
    #   Se numero_intervalos_tempo_chuva for impar
        elif numero_intervalos_tempo_chuva % 2 == 1:
            indice_pico = int(posicao_pico*numero_intervalos_tempo_chuva)   #estimo a localizacao do pico em numero de intervalos de tempo com relacao a duracao da chuva
        
        precipitacao_ordenada = [0. for x in xrange(len(precipitacao_desacumulada))] # armazenar os valores. Variavel retornada no final da funcao.
        indice_pdes           = 0 #variavel de posicao
        indice_ordenacao      = 1 #variavel de posicao
    
        precipitacao_ordenada[indice_pico] = precipitacao_desacumulada[indice_pdes] #(Valor central se impar.... se par: arredondado para baixo) correspondente ao primeiro valor da chuva desacumulada (maior valor)
    
    #   Fazer o loop N vezes ate' que o bloco caia "fora" nos dois extremos
        while ( ((indice_pico - indice_ordenacao) >= 0) or ((indice_pico + indice_ordenacao) <= (len(precipitacao_desacumulada))) ):
        
        #   Comeco loop sempre verificando se e' possivel colocar um valor na direita do pico
            if (indice_pico + indice_ordenacao) < len(precipitacao_ordenada): # se for == ele nao entra
                indice_pdes += 1  # aumentar o indice de pdes em uma unidade para poder copiar o proximo valor de pdes
                precipitacao_ordenada[(indice_pico + indice_ordenacao)] = precipitacao_desacumulada[indice_pdes] # Entro com o valor na direita se for possivel
            
        #   Verifico se e' possivel colocar um valor a esquerda do pico
            if (indice_pico - indice_ordenacao) >= 0: # aqui pode ser igual, porque trata-se de indice (o primeiro e' zero)
                indice_pdes += 1 # Aumentar o indice de pdes em uma unidade para poder copiar o proximo valor de pdes
                precipitacao_ordenada[(indice_pico - indice_ordenacao)] = precipitacao_desacumulada[indice_pdes]   #valor abaixo se o indice nao for menor que zero

            indice_ordenacao += 1 # preparar para o proximo loop
    
    #   Retornar variavel ordenada
        return precipitacao_ordenada
        
#=========================================================================================

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Brasil IDF'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        
    #==============================================================
    
    def dadosUsuario(self):
            
        #Pega o valor da precipitação diária colocado pelo usuário
        prec_line = self.dlg.prec_line.text()
        if prec_line == '':
                iface.messageBar().pushMessage("Error", "Dados de entrada: Insira valor para precipitacao", level=QgsMessageBar.CRITICAL)
                return None 
        #Pega o valor do tempo de retorno colocado pelo usuário
        ret_line = self.dlg.ret_line.text()
        if ret_line == '':
                iface.messageBar().pushMessage("Error", "Dados de entrada: Insira valor para tempo de retorno", level=QgsMessageBar.CRITICAL)
                return None
        #Pega o valor da latitude colocado pelo usuário
        lat_line = self.dlg.lat_line.text() 
        if lat_line == '':
                iface.messageBar().pushMessage("Error", "Dados de entrada: Insira valor para latitude", level=QgsMessageBar.CRITICAL)
                return None
        #Pega o valor da longitude colocado pelo usuário  
        long_line = self.dlg.long_line.text()
        if long_line == '':
                iface.messageBar().pushMessage("Error", "Dados de entrada: Insira valor para longitude", level=QgsMessageBar.CRITICAL) 
                return None  
                
        #Cria a variável da relação tempo em minutos
        relacaoTempo = [10.0, 15.0, 20.0, 30.0, 45.0, 60.0, 120.0, 240.0, 360.0, 720.0, 1440.0]
        
        #Pega o diretorio colocado pelo usuario
        diretorio = self.dlg.caminhoTexto.text()
        if diretorio == '':
                iface.messageBar().pushMessage("Error", "Dados de entrada: Insira um diretorio de saida", level=QgsMessageBar.CRITICAL)  
                return None
          
        #self.dadosUsuario()[0], self.dadosUsuario()[1], self.dadosUsuario()[2], self.dadosUsuario()[3], self.dadosUsuario()[4], self.dadosUsuario()[5]       
        return prec_line, ret_line, relacaoTempo, diretorio, lat_line, long_line
        
    def ECOIDF(self):
        
        #Cria a lista da relacão tempo em horas
        relacaoTempo = self.dadosUsuario()[2]
        prec_line = self.dadosUsuario()[0]
        lat_line = self.dadosUsuario()[4]
        long_line = self.dadosUsuario()[5]
        transformacaoHoras = []
        for i in relacaoTempo:
            transformacaoHoras.append(i/60)
        
        # Cria uma layer tipo ponto, já em WGS84
        point_layer = QgsVectorLayer("Point?crs=EPSG:4326", "coordenada", "memory")
        provider = point_layer.dataProvider()
        # Adiciona primeiro ponto
        pt = QgsFeature()
        point = QgsPoint(float(lat_line), float(long_line))
        pt.setGeometry(QgsGeometry.fromPoint(point))
        provider.addFeatures([pt])
        # Diz para o vetor ponto para buscar mudanças com o provedor
        point_layer.updateExtents()
        #Adiciona o ponto ao mapa 
        QgsMapLayerRegistry.instance().addMapLayer(point_layer)         
        #point_layer é o ponto criado
        
        #Encontra o caminho do plugin em cada computador
        plugin_path = os.path.dirname(os.path.realpath(__file__))
        #Abrir o shape das Isozona que está na pasta do plugin
        pol_layer = QgsVectorLayer(plugin_path, "isozonas", "ogr")
        #Adiciona a Layer isozonas ao mapa (NÃO É NECESSÁRIO)
        #QgsMapLayerRegistry.instance().addMapLayer(pol_layer)
        
        #Extrai a feição do shape das Isozonas e cruza com o shape do ponto das coordenadas 
        #Como resultado a variável Isozona_zone_layer com a zona extraída
        ebl_out = processing.runalg('qgis:extractbylocation', pol_layer, point_layer, u'intersects', 0, None)
        if ebl_out is None:
            ebl_out = processing.runalg('qgis:extractbylocation', pol_layer, point_layer, u'intersects', None)
        Isozona_zone = ebl_out['OUTPUT']
        Isozona_zone_layer = QgsVectorLayer(Isozona_zone,"Isozona_zone", "ogr")
        #Adiciona a Layer Isozona_zone_layer ao mapa
        QgsMapLayerRegistry.instance().addMapLayers([Isozona_zone_layer])
                    
        #Salva em txt os campos da layer extraída separado por vírgula
        filename = self.dadosUsuario()[3] + '\dadosIsozona.txt'            
        output_file = open(filename, 'w')
        #Escreve o valor de precipitação e duração inseridos pelo usuário
        output_file.write("%s\n" %(prec_line))
        #Escreve os valores da feição do shape das isozonas
        Isozona_fields = Isozona_zone_layer.pendingFields()
        Isozona_fieldnames = [field.name() for field in Isozona_fields]
        for f in Isozona_zone_layer.getFeatures():
            line = '\n'.join(unicode(f[x]) for x in Isozona_fieldnames)
            unicode_line = line.encode('utf-8')
            output_file.write(unicode_line)
            output_file.close()
            
        #Abre o arquivo txt para leitura
        output_file = open(filename, 'r')
        #Separa os valores em lista
        porcentagemChuva = output_file.read().split('\n')
        #Remove os primeiros valores da lista
        del porcentagemChuva[0:3]
        #Transforma a lista em float
        floatChuva = []
        for i in porcentagemChuva:
            floatChuva.append(float(i))
        #Multiplica a precipitação inserida pelo usuário pelos valores da porcentagem da chuva
        chuvaFinal = []
        for i in floatChuva:
            chuvaFinal.append(i*(float(prec_line)/100))

        #Cria a lista da intensidade dividindo a precipitação pela relacaoTempo em horas
        intensidade = [chuvaFinali/transformacaoHorasi for chuvaFinali,transformacaoHorasi in zip(chuvaFinal,transformacaoHoras)]
        
        #self.ECOIDF()[0] e self.ECOIDF()[1]
        return chuvaFinal, intensidade
        
    #Esse run está pronto!        
    def run(self):
        """Run method that performs all the real work"""	
            
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            
#==================================================================================================
            
            #Pega a duracao colocada pelo usuario
            duracao = self.dlg.duracao.text()
            
            #Aparecer erro no QGIS caso falta valor para a duração
            if duracao == '':
                iface.messageBar().pushMessage("Error", "Chuva para duracao especifica: Insira valor para duracao", level=QgsMessageBar.CRITICAL)
                return None
            elif float(duracao) < 10:
                iface.messageBar().pushMessage("Error", "Chuva para duracao especifica: Insira valor maior que o mínimo (10 minutos)", level=QgsMessageBar.CRITICAL)
                return None
            
            #torna PorcentagemChuva e RelacaoTempo array
            arrayPorcentagemChuva = np.asarray(self.ECOIDF()[0])
            arrayRelacaoTempo = np.asarray(self.dadosUsuario()[2])
            arrayIntensidade = np.asarray(self.ECOIDF()[1])
                
            #transforma a duracao em float
            duracao = float(duracao)    
                
            #realiza a interpolacao para precipitacao e para a intensidade
            interPrec = interpolate.interp1d(arrayRelacaoTempo, arrayPorcentagemChuva)
            interInt = interpolate.interp1d(arrayRelacaoTempo, arrayIntensidade)        
            
            precUsuario = str(round(interPrec(duracao),2))
            intUsuario = str(round(interInt(duracao),2))
            
            self.dlg.prec_final.setText(precUsuario)
            self.dlg.int_final.setText(intUsuario)
            
            
    def run1(self):
            
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            
            #Pega o valor do intervalo de tempo colocado pelo usuário
            intervaloTempo = self.dlg.intTempo.text()
            if intervaloTempo == '':
                iface.messageBar().pushMessage("Error", "Chuva de projeto: Insira valor para intervalo de tempo", level=QgsMessageBar.CRITICAL) 
                return None              
            if float(intervaloTempo) < 10:
                iface.messageBar().pushMessage("Error", "Chuva de projeto: Valor de intervalo de tempo menor que o minimo (10 min)", level=QgsMessageBar.CRITICAL) 
                return None  
            intervaloTempo = float(intervaloTempo)
            
            #Pega número de intervalos colocado pelo usuário
            durChuva = self.dlg.durChuva.text()
            if durChuva == '':
                iface.messageBar().pushMessage("Error", "Chuva de projeto: Insira valor para duracao da chuva", level=QgsMessageBar.CRITICAL) 
                return None  
            if float(durChuva) > 24:
                iface.messageBar().pushMessage("Error", "Chuva de projeto: Valor de duracao da chuva maior que o maximo (24 horas)", level=QgsMessageBar.CRITICAL) 
                return None 
            durChuva = float(durChuva) 
                
            #Pega a posição do pico colocado pelo usuário
            posicaoPico = self.dlg.posPico.text()
            if posicaoPico == '':
                iface.messageBar().pushMessage("Error", "Chuva de projeto: Insira valor para posicao do pico", level=QgsMessageBar.CRITICAL) 
                return None  
            elif float(posicaoPico) < 1 or float(posicaoPico) > 100:
                iface.messageBar().pushMessage("Error", "Chuva de projeto: Insira valor em porcentagem para posicao do pico", level=QgsMessageBar.CRITICAL) 
                return None 
            posicaoPico = (float(posicaoPico)/100)

            ret_line = self.dadosUsuario()[1]
            relacaoTempo = self.dadosUsuario()[2]
            diretorio = self.dadosUsuario()[3]
            chuvaFinal = self.ECOIDF()[0]
            
            direBlocos = diretorio + '\\blocos_alternados_' + ret_line + 'anos_' + str(int(intervaloTempo)) + '.pdf'
            
            chuvaEntrada = interpolador(chuvaFinal, relacaoTempo, intervaloTempo, durChuva)[1]
            tempo = interpolador(chuvaFinal, relacaoTempo, intervaloTempo, durChuva)[0]
            chuvaDesacumulada = desacumulador(chuvaEntrada)
            
            if intervaloTempo == 5:
                numero_intervalos = (((durChuva*60)/intervaloTempo)-1)
            else:
                numero_intervalos = ((durChuva*60)/intervaloTempo)
                            
            blocosAlternados = self.aplicar_BlocosAlternados(chuvaDesacumulada, numero_intervalos, posicaoPico)
            titulo = 'Metodo dos Blocos Alternados para TR = ' + ret_line
            self.plotagem(tempo, blocosAlternados, titulo, 'Tempo (min)', 'Precipitacao (mm)', direBlocos)
            
            self.dlg.valorPico.setText(str(round(max(blocosAlternados), 2)))
            
            #Salva em txt
            filename = diretorio + '\BlocosAlternados_' + str(intervaloTempo) + '.txt'            
            output_file = open(filename, 'w')
            #Escreve o valor de precipitação e duração inseridos pelo usuário
            for i in range(len(blocosAlternados)):
                output_file.write(str(round(blocosAlternados[i],2)) + " " + str(int(tempo[i])) + "\n")
            output_file.close()
                
    def run2(self):
            
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            
            ret_line = self.dadosUsuario()[1]
            relacaoTempo = self.dadosUsuario()[2]
            diretorio = self.dadosUsuario()[3]
            intensidade = self.ECOIDF()[1]

            #Chama a função plotagem para configurar o gráfico de precipitação x duração
            direGrafico2 = diretorio + '\int_dur_' + ret_line + '.pdf'
            titulo2 = 'Grafico da Intensidade (mm/h) x Duracao (min) para TR = ' + ret_line
            self.plotagem(relacaoTempo, intensidade, titulo2 , 'Duracao (min)' , 'Intensidade (mm/h)', direGrafico2)
            
            #Salva em txt
            filename = diretorio + '\dadosIDF.txt'            
            output_file = open(filename, 'w')
            #Escreve o valor de precipitação e duração inseridos pelo usuário
            for i in range(len(intensidade)):
                output_file.write(str(round(intensidade[i],2)) + " " + str(int(relacaoTempo[i])) + "\n")
            output_file.close()

                
    def run3(self):
            
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            
            ret_line = self.dadosUsuario()[1]
            relacaoTempo = self.dadosUsuario()[2]
            diretorio = self.dadosUsuario()[3]
            chuvaFinal = self.ECOIDF()[0]
            
            #Chama a função plotagem para configurar o gráfico de precipitação x duração
            direGrafico1 = diretorio + '\prec_dur_' + ret_line + '.pdf'
            titulo1 = 'Grafico da Precipitacao (mm) x Duracao (min) para TR = ' + ret_line
            self.plotagem(relacaoTempo, chuvaFinal, titulo1, 'Duracao (min)', 'Precipitacao (mm)', direGrafico1)
            
            #Salva em txt
            filename = diretorio + '\dadosPDF.txt'            
            output_file = open(filename, 'w')
            #Escreve o valor de precipitação e duração inseridos pelo usuário
            for i in range(len(chuvaFinal)):
                output_file.write(str(round(chuvaFinal[i],2)) + " " + str(int(relacaoTempo[i])) + "\n")
            output_file.close()
            
            
#===================================================================================================            