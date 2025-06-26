from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from functools import partial
from PyQt5.QtWidgets import QWidget

from .Vista_crear_apuesta import Dialogo_crear_apuesta

class Vista_lista_apuestas(QWidget):
    #Ventana que muestra la lista de apuestas

    def __init__(self, interfaz):
        """
        Constructor de la ventana
        """
        super().__init__()

        # Se establecen las características de la ventana
        self.titulo = 'Cuentas Claras - Apuestas de la carrera'
        self.width = 720
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

        self.widget_nombre = QWidget()
        self.distribuidor_nombre = QHBoxLayout()
        self.widget_nombre.setLayout(self.distribuidor_nombre)
        self.distribuidor_base.addWidget(self.widget_nombre, Qt.AlignTop)

        self.etiqueta_nombre=QLabel("")
        self.distribuidor_nombre.addWidget(self.etiqueta_nombre)                


        self.contenedor_tabla = QGroupBox(self)
        self.contenedor_tabla.setLayout(QHBoxLayout())
        self.contenedor_tabla.setTitle('Apuestas')
        self.distribuidor_base.addWidget(self.contenedor_tabla)

        #Creación de la tabla en donde se mostrarán las apuestas 
        self.tabla_actividades = QScrollArea(self)
        self.tabla_actividades.setFixedSize(600, 400)
        self.tabla_actividades.setStyleSheet('''
                QScrollArea{border:none}''')
        self.tabla_actividades.setWidgetResizable(True)
        self.widget_contenidos_tabla_actividades = QWidget()
        self.distribuidor_actividades = QGridLayout(self.widget_contenidos_tabla_actividades)
        self.tabla_actividades.setWidget(self.widget_contenidos_tabla_actividades)
        self.contenedor_tabla.layout().addWidget(self.tabla_actividades, Qt.AlignTop)


        etiqueta_nombre = QLabel("\tNombre")
        etiqueta_nombre.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_actividades.addWidget(etiqueta_nombre, 0, 0, Qt.AlignTop)

        etiqueta_fecha = QLabel("Valor")
        etiqueta_fecha.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_actividades.addWidget(etiqueta_fecha, 0, 1, Qt.AlignCenter|Qt.AlignTop)

        etiqueta_accion = QLabel("Competidor")
        etiqueta_accion.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_actividades.addWidget(etiqueta_accion, 0, 2, alignment=Qt.AlignCenter|Qt.AlignTop)

        etiqueta_accion = QLabel("Acciones")
        etiqueta_accion.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_actividades.addWidget(etiqueta_accion, 0, 3, 0, 2, alignment=Qt.AlignCenter|Qt.AlignTop)


        #Creación de la caja con los botones
        self.widget_botones = QWidget()
        self.distribuidor_botones = QGridLayout()
        self.widget_botones.setLayout(self.distribuidor_botones)
        self.distribuidor_base.addWidget(self.widget_botones, Qt.AlignTop)

       #Creación de los botones con las diferentes operaciones
        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(200, 40)
        self.btn_volver.setToolTip("Añadir Actividad")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.distribuidor_botones.addWidget(self.btn_volver, 0, 0, Qt.AlignCenter)
        self.btn_volver.clicked.connect(self.volver)

        self.btn_aniadir_apuesta = QPushButton("Añadir apuesta", self)
        self.btn_aniadir_apuesta.setFixedSize(200, 40)
        self.btn_aniadir_apuesta.setToolTip("Añadir competidor")
        self.btn_aniadir_apuesta.setIcon(QIcon("src/recursos/009-money.png"))
        self.distribuidor_botones.addWidget(self.btn_aniadir_apuesta, 0, 1, Qt.AlignCenter)
        self.btn_aniadir_apuesta.clicked.connect(self.aniadir_apuesta)

    def mostrar_apuestas(self, nombre_carrera,  apuestas):
        """
        Esta función construye el reporte de compensación a partir de una matriz
        """        
        self.etiqueta_nombre.setText('Apuestas para {}'.format(nombre_carrera))
        self.apuestas = apuestas

        #Este pedazo de código borra todos los contenidos anteriores de la tabla (salvo los encabezados)
        while self.distribuidor_actividades.count()>4:
            child = self.distribuidor_actividades.takeAt(4)
            if child.widget():
                child.widget().deleteLater()

        numero_fila=1
        for apuesta in self.apuestas:
            
            etiqueta_nombre = QLabel(apuesta["Apostador"])
            etiqueta_nombre.setWordWrap(True)
            self.distribuidor_actividades.addWidget(etiqueta_nombre, numero_fila, 0, alignment=Qt.AlignTop)

            etiqueta_valor = QLabel("{:,.3f}".format(apuesta["Valor"]))
            etiqueta_valor.setWordWrap(True)
            self.distribuidor_actividades.addWidget(etiqueta_valor, numero_fila, 1, alignment=Qt.AlignTop|Qt.AlignCenter)
            
            etiqueta_competidor = QLabel(apuesta["Competidor"])
            etiqueta_competidor.setWordWrap(True)
            self.distribuidor_actividades.addWidget(etiqueta_competidor, numero_fila, 2, alignment=Qt.AlignTop|Qt.AlignCenter)
            
        

            btn_editar = QPushButton("", self)
            btn_editar.setToolTip("Editar")
            btn_editar.setGeometry(0, 0, 35, 35)
            btn_editar.setFixedSize(35, 35)
            btn_editar.setIcon(QIcon("src/recursos/004-edit-button.png"))
            btn_editar.setIconSize(QSize(35, 35))
            btn_editar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn_editar.clicked.connect(partial(self.editar_apuesta, numero_fila-1))
            self.distribuidor_actividades.addWidget(btn_editar, numero_fila, 3, alignment=Qt.AlignTop)

            btn_eliminar = QPushButton("", self)
            btn_eliminar.setToolTip("Eliminar")
            btn_eliminar.setGeometry(0, 0, 35, 35)
            btn_eliminar.setFixedSize(35, 35)
            btn_eliminar.setIcon(QIcon("src/recursos/005-delete.png"))
            btn_eliminar.setIconSize(QSize(35, 35))
            btn_eliminar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn_eliminar.clicked.connect(partial(self.eliminar_apuesta, numero_fila-1))
            self.distribuidor_actividades.addWidget(btn_eliminar, numero_fila, 4, alignment=Qt.AlignTop)

            numero_fila+=1

        height = 360
        elemento_de_espacio = QSpacerItem(140, height-numero_fila*40 if numero_fila*40<=height else 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.distribuidor_actividades.addItem(elemento_de_espacio, numero_fila, 0, 1, 3)


    def volver(self):
        """
        Esta función permite volver a la ventana de la lista de carreras
        """   
        self.hide()
        self.interfaz.mostrar_vista_lista_carreras()

    def aniadir_apuesta(self):
        """
        Esta función permite ejecutar el diálogo para crear una apuesta
        """   
        dialogo = Dialogo_crear_apuesta(self.interfaz.dar_apostadores(), self.interfaz.dar_competidores())
        dialogo.exec_()
        if dialogo.resultado == 1:
            valor_texto = dialogo.texto_valor.text()
            valor = float(valor_texto) if valor_texto.strip() != "" and valor_texto.replace('.', '', 1).isdigit() else 0
            resultado = self.interfaz.aniadir_apuesta(str(dialogo.combobox_competidores.currentText()), valor, str(dialogo.combobox_apostadores.currentText()))
            if resultado != "":
                self.error(resultado)
            
    def editar_apuesta(self, id_apuesta):
        """
        Esta función permite ejecutar el diálogo para editar una apuesta
        """ 
        dialogo = Dialogo_crear_apuesta(self.interfaz.dar_apostadores(), self.interfaz.dar_competidores(), self.interfaz.dar_apuesta(id_apuesta))
        dialogo.exec_()
        if dialogo.resultado == 1:
            valor_texto = dialogo.texto_valor.text()
            valor = float(valor_texto) if valor_texto.strip() != "" and valor_texto.replace('.', '', 1).isdigit() else 0
            resultado = self.interfaz.editar_apuesta(id_apuesta, str(dialogo.combobox_competidores.currentText()), valor, str(dialogo.combobox_apostadores.currentText()))
            if resultado != "":
                self.error(resultado)
            
   
    def eliminar_apuesta(self, id_apuesta):
        """
        Esta función permite eliminar una apuesta
        """ 
        mensaje_confirmacion=QMessageBox()
        mensaje_confirmacion.setIcon(QMessageBox.Question)
        mensaje_confirmacion.setText("¿Esta seguro de que desea eliminar esta apuesta?\nRecuerde que esta acción es irreversible")        
        mensaje_confirmacion.setWindowTitle("¿Desea eliminar esta apuesta?")
        mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
        mensaje_confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No ) 
        respuesta=mensaje_confirmacion.exec_()
        if respuesta == QMessageBox.Yes:
             self.interfaz.eliminar_apuesta(id_apuesta)
             
    def closeEvent(self, event):
        self.hide()
        self.interfaz.mostrar_vista_lista_carreras()
        event.accept()

    def error(self, error):
        mensaje_error=QMessageBox()
        mensaje_error.setIcon(QMessageBox.Question)
        mensaje_error.setText("Error: " + error)
        mensaje_error.setWindowTitle("Error al guardar carrera")
        mensaje_error.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
        mensaje_error.setStandardButtons(QMessageBox.Ok ) 
        respuesta=mensaje_error.exec_()
