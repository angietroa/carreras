from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *

from functools import partial
from .Vista_crear_apostador import Dialogo_crear_apostador

class Vista_lista_apostadores(QWidget):
    #Ventana que muestra la lista de apostadores

    def __init__(self, interfaz):
        """
        Constructor de la ventana
        """
        super().__init__()

        #Se establecen las características de la ventana
        self.titulo = 'E-Porra - Apostadores'
        self.interfaz=interfaz

        self.width = 400
        self.height = 330
        self.inicializar_GUI()
        self.show()


    def inicializar_GUI(self):

        # inicializamos la ventana
        self.setWindowTitle(self.titulo)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
         
        self.distribuidor_base = QVBoxLayout(self)        



        #Creación del grupo de botones
        caja_botones = QGroupBox()
        caja_botones.setLayout(QHBoxLayout())

        #Creación de los botones
        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(150, 40)
        self.btn_volver.setToolTip("Volver")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.btn_volver.clicked.connect(self.volver)

        self.distribuidor_base.addStretch()
        self.btn_aniadir_apostador=QPushButton("Añadir Apostador",self)
        self.btn_aniadir_apostador.setFixedSize(150,40)
        self.btn_aniadir_apostador.setToolTip("Añadir Apostador")                
        self.btn_aniadir_apostador.setIcon(QIcon("src/recursos/006-add.png"))
        self.btn_aniadir_apostador.clicked.connect(self.mostrar_dialogo_aniadir_apostador)

        self.contenedor_tabla = QGroupBox(self)
        self.contenedor_tabla.setLayout(QHBoxLayout())
        self.contenedor_tabla.setTitle('Apostadores')
        self.distribuidor_base.addWidget(self.contenedor_tabla)

        #Creación de la tabla con la lista de apostadores
        self.tabla_apostadores = QScrollArea(self)
        self.tabla_apostadores.setWidgetResizable(True)
        self.tabla_apostadores.setStyleSheet('QScrollArea{border:none}')
        self.tabla_apostadores.setFixedSize(300, 250)
        self.widget_tabla_viajeros = QWidget()
        self.distribuidor_tabla_apostadores = QGridLayout(self.widget_tabla_viajeros)
        self.tabla_apostadores.setWidget(self.widget_tabla_viajeros)
        self.contenedor_tabla.layout().addWidget(self.tabla_apostadores)

        self.distribuidor_tabla_apostadores.setColumnStretch(0, 0)
        self.distribuidor_tabla_apostadores.setColumnStretch(1, 0)
        self.distribuidor_tabla_apostadores.setColumnStretch(2, 0)

        self.distribuidor_tabla_apostadores.setSpacing(0)

        #Creación de las etiquetas de encabezado
        etiqueta_nombre = QLabel("Nombre")
        etiqueta_nombre.setFixedSize(145,40)
        etiqueta_nombre.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_tabla_apostadores.addWidget(etiqueta_nombre, 0, 0, Qt.AlignTop)

        etiqueta_accion = QLabel("Accion")
        etiqueta_accion.setFixedSize(60,40)
        etiqueta_accion.setFont(QFont("Times",weight=QFont.Bold)) 
        etiqueta_accion.setAlignment(Qt.AlignCenter)
        self.distribuidor_tabla_apostadores.addWidget(etiqueta_accion, 0, 1, 0, 2, Qt.AlignTop|Qt.AlignCenter)
        

        #Se añaden los botones a la caja de botones
        caja_botones.layout().addWidget(self.btn_volver)
        caja_botones.layout().addWidget(self.btn_aniadir_apostador)
        caja_botones.layout().setContentsMargins(0, 0, 0, 0)
        caja_botones.setObjectName("MyBox")
        caja_botones.setStyleSheet("#MyBox{border:3px}")
        self.distribuidor_base.addWidget(caja_botones)



       
    def mostrar_apostadores(self, apostadores):
        """
        Esta función muestra la lista de apostadores
        """
        self.apostadores = apostadores
        
        #Este pedazo de código borra todos los contenidos anteriores de la tabla (salvo los encabezados)
        while self.distribuidor_tabla_apostadores.count()>2:
            child = self.distribuidor_tabla_apostadores.takeAt(2)
            if child.widget():
                child.widget().deleteLater()

        #Ciclo para poblar la tabla
        numero_fila = 0
        for apostador in self.apostadores:

            etiqueta_nombre=QLabel(apostador["Nombre"])          
            etiqueta_nombre.setWordWrap(True)
            etiqueta_nombre.setFixedSize(90,40)
            self.distribuidor_tabla_apostadores.addWidget(etiqueta_nombre, numero_fila+1,0, Qt.AlignTop)

            boton_editar=QPushButton("",self)
            boton_editar.setToolTip("Editar")
            boton_editar.setFixedSize(30,30)
            boton_editar.setIcon(QIcon("src/recursos/004-edit-button.png"))
            boton_editar.clicked.connect(partial(self.mostrar_dialogo_editar_apostador, numero_fila) )
            self.distribuidor_tabla_apostadores.addWidget(boton_editar, numero_fila+1,1,Qt.AlignTop)


            etiqueta_eliminar=QPushButton("",self)
            etiqueta_eliminar.setToolTip("Borrar")
            etiqueta_eliminar.setFixedSize(30,30)
            etiqueta_eliminar.setIcon(QIcon("src/recursos/005-delete.png"))
            etiqueta_eliminar.clicked.connect(partial(self.eliminar_apostador, numero_fila) )
            self.distribuidor_tabla_apostadores.addWidget(etiqueta_eliminar, numero_fila+1,2,Qt.AlignTop)


            numero_fila=numero_fila+1

        #Elemento para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        self.distribuidor_tabla_apostadores.layout().setRowStretch(numero_fila+1, 1)

    def mostrar_dialogo_editar_apostador(self, id_apostador):
        """
        Esta función ejecuta el diálogo para editar un apostador
        """    
        dialogo=Dialogo_crear_apostador(self.apostadores[id_apostador])        
        dialogo.exec_()
        if dialogo.resultado==1:            
            resultado = self.interfaz.editar_apostador(id_apostador, dialogo.texto_nombre.text())
            if resultado != "":
                self.error(resultado)

    def eliminar_apostador(self, indice_apostador):
        """
        Esta función informa a la interfaz del apostador a eliminar
        """    
        mensaje_confirmacion=QMessageBox()
        mensaje_confirmacion.setIcon(QMessageBox.Question)
        mensaje_confirmacion.setText("¿Esta seguro de que desea eliminar este apostador?\nRecuerde que esta acción es irreversible")        
        mensaje_confirmacion.setWindowTitle("¿Desea borrar este apostador?")
        mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
        mensaje_confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No ) 
        respuesta=mensaje_confirmacion.exec_()
        if respuesta == QMessageBox.Yes:
            self.interfaz.eliminar_apostador(indice_apostador)          


    def mostrar_dialogo_aniadir_apostador(self):
        """
        Esta función ejecuta el diálogo para crear un nuevo apostador
        """    
        dialogo=Dialogo_crear_apostador(None)        
        dialogo.exec_()
        if dialogo.resultado==1:            
            resultado = self.interfaz.aniadir_apostador(dialogo.texto_nombre.text())
            if resultado != "":
                self.error(resultado)

        
    def volver(self):
        """
        Esta función permite volver a la ventana de lista de carreras
        """    
        self.hide()
        self.interfaz.mostrar_vista_lista_carreras()

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
