from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Dialogo_terminar_carrera(QDialog):
    #Diálogo para terminar una carrera

    def __init__(self, competidores):
        """
        Constructor del diálogo
        """    
        super().__init__()

        self.competidores = competidores

        self.setFixedSize(340, 150)
        self.setWindowIcon(
            QIcon("src/devcuentasclaras/recursos/smallLogo.png"))
        self.setWindowTitle("Terminar carrera")
        self.resultado = ""

        self.widget_dialogo = QListWidget()

        self.distribuidor_dialogo = QGridLayout()
        self.setLayout(self.distribuidor_dialogo)
        numero_fila = 0

        #Creación de las etiquetas
        etiqueta_ganador = QLabel("Seleccione el ganador de la carrera:")
        etiqueta_ganador.setFont(QFont("Times", weight=QFont.Bold))
        self.distribuidor_dialogo.addWidget(
            etiqueta_ganador, numero_fila, 0,1,2)
        self.distribuidor_dialogo.setAlignment(etiqueta_ganador, Qt.AlignTop)
        numero_fila+=1

        self.combobox_competidores = QComboBox(self)
        
        for i, competidor in enumerate(self.competidores):
            self.combobox_competidores.addItem(competidor["Nombre"], userData=i)             
        self.distribuidor_dialogo.addWidget(self.combobox_competidores,numero_fila,0,1,2)
        self.distribuidor_dialogo.setAlignment(self.combobox_competidores, Qt.AlignTop)
        numero_fila+=1

        self.btn_generar_reporte = QPushButton("Generar reporte")
        self.btn_generar_reporte.setIcon(QIcon("src/recursos/008-data-spreadsheet.png"))
        self.distribuidor_dialogo.addWidget(self.btn_generar_reporte, numero_fila, 0,1,1)
        
        self.btn_generar_reporte.clicked.connect(self.generar_reporte)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.distribuidor_dialogo.addWidget(self.btn_volver, numero_fila, 1,1,1)
        self.btn_volver.clicked.connect(self.cancelar)

        #self.distribuidor_dialogo.layout().setRowStretch(numero_fila, 1)

    def generar_reporte(self):
        """
        Esta función envía la información de que, al haber elegido un ganador, se genera un reporte
        """   
        self.resultado=1
        self.close()
        return self.resultado

    def cancelar(self):
        """
        Esta función envía la información de que se ha cancelado la operación
        """ 
        self.resultado = 0
        self.close()
        return self.resultado
