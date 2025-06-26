from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget

from functools import partial

class Vista_reporte_ganancias(QWidget):
    #Ventana que muestra el reporte de ganancias para una carrera

    def __init__(self, interfaz):
        """
        Constructor de la ventana
        """
        super().__init__()

        # Se establecen las características de la ventana
        self.titulo = 'E-Porra - Reporte de ganancias'
        self.left = 80
        self.top = 80
        self.width = 400
        self.height = 560

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.interfaz = interfaz

        self.inicializar_GUI()
        self.show()

    def inicializar_GUI(self):

        # inicializamos la ventana
        self.setWindowTitle(self.titulo)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("src/recursos/smallLogo.png"))

        self.distribuidor_base = QVBoxLayout(self)

        # Creación de la tabla en dónde se hará el reporte
        self.tabla_reporte = QScrollArea(self)
        self.tabla_reporte.setWidgetResizable(True)
        self.widget_tabla_reporte = QWidget()
        self.distribuidor_tabla_reporte = QGridLayout(self.widget_tabla_reporte)
        self.tabla_reporte.setWidget(self.widget_tabla_reporte)

        self.distribuidor_tabla_reporte.setColumnStretch(0, 1)
        self.distribuidor_tabla_reporte.setColumnStretch(1, 1)


        self.contenedor_tabla = QGroupBox(self)
        self.contenedor_tabla.setLayout(QHBoxLayout())
        self.contenedor_tabla.setTitle('Ganancias')
        self.distribuidor_base.addWidget(self.contenedor_tabla)


        self.contenedor_tabla.layout().addWidget(self.tabla_reporte)
        self.tabla_reporte.setStyleSheet('QScrollArea{border:none}')
        # Creación de las etiquetas con los encabezados
        etiqueta_viajero = QLabel("Apostador")
        etiqueta_viajero.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_tabla_reporte.addWidget(etiqueta_viajero, 0, 0, Qt.AlignCenter|Qt.AlignTop)

        etiqueta_ganancia = QLabel("Ganancia")
        etiqueta_ganancia.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_tabla_reporte.addWidget(etiqueta_ganancia, 0, 1, Qt.AlignCenter|Qt.AlignTop)

        grupo_casa = QGroupBox()
        grupo_casa.setLayout(QHBoxLayout())

        etiqueta_casa = QLabel("Ganancias de la casa:")
        etiqueta_casa.setFont(QFont("Times",weight=QFont.Bold)) 
        grupo_casa.layout().addWidget(etiqueta_casa)

        self.etiqueta_valor_casa = QLabel("$\t")
        grupo_casa.layout().addWidget(self.etiqueta_valor_casa)

        grupo_casa.setStyleSheet('QGroupBox{border:none}')

        self.distribuidor_base.addWidget(grupo_casa)
        self.distribuidor_base.setAlignment(grupo_casa, Qt.AlignCenter)

        #Creación de los botones de funciones de la ventana
        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(200, 40)
        self.btn_volver.setToolTip("Añadir Actividad")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.btn_volver.setIconSize(QSize(120, 120))
        self.btn_volver.clicked.connect(self.volver)
        self.distribuidor_base.addWidget(self.btn_volver)
        self.distribuidor_base.setAlignment(self.btn_volver, Qt.AlignCenter)


    def mostrar_ganancias(self, lista_ganancias, ganancias_casa):
        """
        Esta función puebla el reporte de ganancias con la información en la lista
        """

        #Por cada iteración, llenamos con el nombre del apostador y sus ganancias
        
        numero_fila = 1
        for apostador, valor in lista_ganancias:

            etiqueta_viajero = QLabel("\t{}".format(apostador))
            etiqueta_viajero.setWordWrap(True)
            self.distribuidor_tabla_reporte.addWidget(etiqueta_viajero, numero_fila, 0, Qt.AlignLeft)

            etiqueta_total = QLabel("${:,.2f}".format(valor))
            etiqueta_total.setWordWrap(True)
            self.distribuidor_tabla_reporte.addWidget(etiqueta_total, numero_fila, 1, Qt.AlignCenter)

            numero_fila = numero_fila+1

        #Añadimos las ganancias de la casa
        self.etiqueta_valor_casa.setText("${:,.2f}".format(ganancias_casa))
        #Elemento para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        self.distribuidor_tabla_reporte.layout().setRowStretch(numero_fila+1, 1)
        
    def volver(self):
        """
        Esta función permite volver a la ventana de la lista de carreras
        """   
        self.hide()
        self.interfaz.mostrar_vista_lista_carreras()

    def closeEvent(self, event):
        self.hide()
        self.interfaz.mostrar_vista_lista_carreras()
        event.accept()