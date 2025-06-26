from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial


from .Vista_terminar_carrera import Dialogo_terminar_carrera


class Vista_lista_carreras(QWidget):
    #Ventana que muestra la lista de carreras

    def __init__(self, interfaz):
        """
        Constructor de la ventanas
        """
        super().__init__()
        
        self.interfaz=interfaz
       
        #Se establecen las características de la ventana
        self.title = 'Cuentas Claras'
        self.width = 720
        self.height = 600      
        self.inicializar_GUI()

    def inicializar_GUI(self):
        
        #inicializamos la ventana
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
         
        self.distribuidor_base = QVBoxLayout(self)

        #Creación del logo de encabezado
        self.logo=QLabel(self)
        self.pixmap = QPixmap("src/recursos/EporraHeader.png")    
        self.pixmap = self.pixmap.scaled(400,150, Qt.KeepAspectRatio)    
        self.logo.setPixmap(self.pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        self.distribuidor_base.addWidget(self.logo,alignment=Qt.AlignCenter)

        #Creación de las etiquetsa con textos de bienvenida
        self.etiqueta_bienvenida=QLabel("!!Bienvenido a E-Porra!!")                               
        self.etiqueta_bienvenida.setAlignment(Qt.AlignCenter)
        self.distribuidor_base.addWidget(self.etiqueta_bienvenida,Qt.AlignCenter)
        
        self.etiqueta_descripcion=QLabel("La manera más fácil y divertida de apostar")                               
        self.etiqueta_descripcion.setAlignment(Qt.AlignCenter)
        self.distribuidor_base.addWidget(self.etiqueta_descripcion,Qt.AlignCenter)

        #Creación del espacio de los botones
        self.widget_botones=QWidget()
        self.distribuidor_botones=QGridLayout()
        self.widget_botones.setLayout(self.distribuidor_botones)

        #Creación de los botones
        self.btn_aniadir_actividad=QPushButton("Añadir Carrera",self)
        self.btn_aniadir_actividad.setFixedSize(200,40)
        self.btn_aniadir_actividad.setToolTip("Añadir Carrera")                
        self.btn_aniadir_actividad.setIcon(QIcon("src/recursos/006-add.png"))
        self.btn_aniadir_actividad.setIconSize(QSize(120,120))
        self.distribuidor_botones.addWidget(self.btn_aniadir_actividad,0,0,Qt.AlignLeft)
        self.btn_aniadir_actividad.clicked.connect(self.mostrar_ventana_crear_carrera)

        self.btn_ver_viajeros=QPushButton("Ver Apostadores",self)
        self.btn_ver_viajeros.setFixedSize(200,40)
        self.btn_ver_viajeros.setToolTip("Ver Apostadores")                
        self.btn_ver_viajeros.setIcon(QIcon("src/recursos/010-people-24.png"))
        self.btn_ver_viajeros.setIconSize(QSize(120,120))                
        self.btn_ver_viajeros.clicked.connect(self.mostrar_apostadores)
        self.distribuidor_botones.addWidget(self.btn_ver_viajeros,0,1,Qt.AlignRight)        
        self.distribuidor_base.addWidget(self.widget_botones,Qt.AlignCenter)

        #Creación del área con la información de las carreras
        self.tabla_carreras = QScrollArea(self)
        self.tabla_carreras.setWidgetResizable(True)
        self.tabla_carreras.setFixedSize(700, 300)
        self.widget_tabla_actividades = QWidget()
        self.distribuidor_tabla_carreras = QGridLayout()        
        self.widget_tabla_actividades.setLayout(self.distribuidor_tabla_carreras);                
        self.tabla_carreras.setWidget(self.widget_tabla_actividades)
        self.distribuidor_base.addWidget(self.tabla_carreras)

        #Hacemos la ventana visible
        self.show()


    def mostrar_carreras(self, lista_carreras):
        """
        Esta función puebla la tabla con las carreras
        """
        self.carreras = lista_carreras

        #Este pedazo de código borra todo lo que no sean encabezados.
        while self.distribuidor_tabla_carreras.count()>2:
            child = self.distribuidor_tabla_carreras.takeAt(2)
            if child.widget():
                child.widget().deleteLater()

        self.distribuidor_tabla_carreras.setColumnStretch(0,1)
        self.distribuidor_tabla_carreras.setColumnStretch(1,0)
        self.distribuidor_tabla_carreras.setColumnStretch(2,0)
        self.distribuidor_tabla_carreras.setColumnStretch(3,0)
        self.distribuidor_tabla_carreras.setColumnStretch(4,0)
        self.distribuidor_tabla_carreras.setColumnStretch(4,0)

        #Ciclo para llenar la tabla
        if (self.carreras!= None and len(self.carreras)>0) :
            self.tabla_carreras.setVisible(True)

            #Creación de las etiquetas

            etiqueta_nombre=QLabel("Nombre")                      
            etiqueta_nombre.setMinimumSize(QSize(0,0))
            etiqueta_nombre.setMaximumSize(QSize(65525,65525))
            etiqueta_nombre.setAlignment(Qt.AlignCenter)
            etiqueta_nombre.setFont(QFont("Times",weight=QFont.Bold)) 
            self.distribuidor_tabla_carreras.addWidget(etiqueta_nombre, 0,0, Qt.AlignCenter)

            etiqueta_acciones=QLabel("Acciones")                      
            etiqueta_acciones.setMinimumSize(QSize(0,0))
            etiqueta_acciones.setMaximumSize(QSize(65525,65525))
            etiqueta_acciones.setAlignment(Qt.AlignCenter)
            etiqueta_acciones.setFont(QFont("Times",weight=QFont.Bold))               
            self.distribuidor_tabla_carreras.addWidget(etiqueta_acciones, 0,1,1,5, Qt.AlignCenter)
       
            numero_fila=0
            for dic_carrera in self.carreras:
                numero_fila=numero_fila+1

                etiqueta_nombre=QLabel(dic_carrera['Nombre'])          
                etiqueta_nombre.setWordWrap(True)
                self.distribuidor_tabla_carreras.addWidget(etiqueta_nombre,numero_fila,0)

                #Creación de los botones asociados a cada acción
                btn_ver_actividad=QPushButton("",self)
                btn_ver_actividad.setToolTip("Editar carrera")
                btn_ver_actividad.setFixedSize(40,40)
                btn_ver_actividad.setIcon(QIcon("src/recursos/004-edit-button.png"))
                btn_ver_actividad.clicked.connect(partial(self.mostrar_carrera,numero_fila-1) )
                self.distribuidor_tabla_carreras.addWidget(btn_ver_actividad,numero_fila,1,Qt.AlignCenter)

                btn_editar=QPushButton("",self)
                btn_editar.setToolTip("Añadir apuestas")
                btn_editar.setFixedSize(40,40)
                btn_editar.setIcon(QIcon("src/recursos/009-money.png"))
                btn_editar.clicked.connect(partial(self.mostrar_apuestas,numero_fila -1 ) )
                self.distribuidor_tabla_carreras.addWidget(btn_editar,numero_fila,2,Qt.AlignCenter)

                btn_terminar=QPushButton("",self)
                btn_terminar.setToolTip("Terminar")
                btn_terminar.setFixedSize(40,40)
                btn_terminar.setIcon(QIcon("src/recursos/reward.png"))
                btn_terminar.clicked.connect(partial(self.terminar_carrera,numero_fila-1) )
                self.distribuidor_tabla_carreras.addWidget(btn_terminar,numero_fila,3,Qt.AlignCenter)

                btn_eliminar=QPushButton("",self)
                btn_eliminar.setToolTip("Eliminar")
                btn_eliminar.setFixedSize(40,40)
                btn_eliminar.setIcon(QIcon("src/recursos/005-delete.png"))
                btn_eliminar.clicked.connect(partial(self.eliminar_carrera,numero_fila -1) )
                self.distribuidor_tabla_carreras.addWidget(btn_eliminar,numero_fila,4,Qt.AlignCenter)

                if not dic_carrera['Abierta']:
                    btn_ver_actividad.setDisabled(True)
                    btn_editar.setDisabled(True)
                    btn_terminar.setDisabled(True)
                    btn_eliminar.setDisabled(True)

        else:
                self.tabla_carreras.setVisible(False)

        #Elemento para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        if len(self.carreras)>0:
            self.distribuidor_tabla_carreras.layout().setRowStretch(numero_fila+2, 1)

    def terminar_carrera(self, id_carrera):
        """
        Esta función informa a la interfaz para terminar una carrera
        """
        
        self.interfaz.carrera_actual = id_carrera
        dialogo = Dialogo_terminar_carrera(self.interfaz.dar_competidores())
        dialogo.exec_()
        if dialogo.resultado == 1:
            self.hide()
            self.interfaz.mostrar_reporte_ganancias(dialogo.combobox_competidores.currentData())

    def mostrar_carrera(self,id_carrera): 
        """
        Esta función informa a la interfaz para desplegar la ventana de la carrera
        """        
        self.hide()
        self.interfaz.mostrar_carrera(id_carrera)
 
    def mostrar_apostadores(self):
        """
        Esta función informa a la interfaz para desplegar la ventana de la lista de apostadores
        """
        self.hide()
        self.interfaz.mostrar_apostadores()

    def mostrar_apuestas(self,id_carrera): 
        """
        Esta función informa a la interfaz para desplegar la ventana de la lista de apuestas
        """        
        self.hide()
        self.interfaz.mostrar_apuestas(id_carrera)
        
    def mostrar_ventana_crear_carrera(self):
        """
        Esta función informa a la interfaz para deplegar la ventana de la información de una carrera
        """
        self.hide()
        self.interfaz.mostrar_carrera()



    def eliminar_carrera(self,indice_carrera): 
        """
        Esta función elimina una carrera tras solicitar una confirmación
        """
        mensaje_confirmacion=QMessageBox()
        mensaje_confirmacion.setIcon(QMessageBox.Question)
        mensaje_confirmacion.setText("¿Esta seguro de que desea borrar esta carrera?\nRecuerde que esta acción es irreversible")        
        mensaje_confirmacion.setWindowTitle("¿Desea borrar esta carrera?")
        mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
        mensaje_confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No ) 
        respuesta=mensaje_confirmacion.exec_()
        if respuesta == QMessageBox.Yes:
             self.interfaz.eliminar_carrera(indice_carrera)
