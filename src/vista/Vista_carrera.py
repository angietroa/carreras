from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from functools import partial
from .Vista_crear_competidor import Dialogo_crear_competidor


class Vista_carrera(QWidget):
    #Ventana de la carrera

    def __init__(self,principal):
        """
        Constructor de la ventana
        """   
        super().__init__()

        self.titulo = ''
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.interfaz=principal            

        self.width = 720
        self.height = 550
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

        etiqueta_nombre=QLabel("Nombre")
        self.distribuidor_nombre.addWidget(etiqueta_nombre)                

        self.texto_nombre=QLineEdit(self)
        self.distribuidor_nombre.addWidget(self.texto_nombre)

        self.contenedor_tabla = QGroupBox(self)
        self.contenedor_tabla.setLayout(QHBoxLayout())
        self.contenedor_tabla.setTitle('Competidores')
        self.distribuidor_base.addWidget(self.contenedor_tabla)

        #Creación de la tabla en donde se mostrarán los competidores 
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

        etiqueta_fecha = QLabel("Probabilidad")
        etiqueta_fecha.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_actividades.addWidget(etiqueta_fecha, 0, 1, Qt.AlignCenter|Qt.AlignTop)

        etiqueta_accion = QLabel("Acciones")
        etiqueta_accion.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_actividades.addWidget(etiqueta_accion, 0, 2, 0, 2, alignment=Qt.AlignCenter|Qt.AlignTop)

        #Creación de la caja con los botones
        self.widget_botones = QWidget()
        self.distribuidor_botones = QGridLayout()
        self.widget_botones.setLayout(self.distribuidor_botones)
        self.distribuidor_base.addWidget(self.widget_botones, Qt.AlignTop)

       #Creación de los botones con las diferentes operaciones
        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(200, 40)
        self.btn_volver.setToolTip("Volver")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.distribuidor_botones.addWidget(self.btn_volver, 0, 0, Qt.AlignCenter)
        self.btn_volver.clicked.connect(self.volver)

        self.btn_aniadir_competidor = QPushButton("Añadir competidor", self)
        self.btn_aniadir_competidor.setFixedSize(200, 40)
        self.btn_aniadir_competidor.setToolTip("Añadir competidor")
        self.btn_aniadir_competidor.setIcon(QIcon("src/recursos/003-multiple-users-silhouette.png"))
        self.distribuidor_botones.addWidget(self.btn_aniadir_competidor, 0, 1, Qt.AlignCenter)
        self.btn_aniadir_competidor.clicked.connect(self.aniadir_competidor)

        self.btn_guardar_carrera = QPushButton("Guardar Carrera", self)
        self.btn_guardar_carrera.setFixedSize(200, 40)
        self.btn_guardar_carrera.setToolTip("Guardar Carrera")
        self.btn_guardar_carrera.setIcon(QIcon("src/recursos/floppy-disk.png"))
        self.distribuidor_botones.addWidget(self.btn_guardar_carrera, 0, 2, Qt.AlignCenter)
        self.btn_guardar_carrera.clicked.connect(self.guardar_cambios)



    def mostrar_competidores(self, nombre_carrera, competidores):
        """
        Esta función puebla los competidores de una carrera
        """   
        
        self.competidores = competidores
        
        self.titulo='E-Porra - Detalle de {}'.format(nombre_carrera)
        self.setWindowTitle(self.titulo)
        self.texto_nombre.setText(nombre_carrera)


        #Este pedazo de código borra todos los contenidos anteriores de la tabla (salvo los encabezados)
        while self.distribuidor_actividades.count()>3:
            child = self.distribuidor_actividades.takeAt(3)
            if child.widget():
                child.widget().deleteLater()

        self.distribuidor_actividades.setColumnStretch(0, 1)
        self.distribuidor_actividades.setColumnStretch(1, 1)
        self.distribuidor_actividades.setColumnStretch(2, 0)
        self.distribuidor_actividades.setColumnStretch(3, 0)

        if (len(self.competidores)<1):
            self.btn_guardar_carrera.setEnabled(False)
        else:
            self.btn_guardar_carrera.setEnabled(True)

        numero_fila=1
        
        #Ciclo para llenar los gastos
        for competidor in self.competidores:

            etiqueta_nombre = QLabel(competidor["Nombre"])
            etiqueta_nombre.setWordWrap(True)
            self.distribuidor_actividades.addWidget(etiqueta_nombre, numero_fila, 0)

            etiqueta_valor = QLabel("{:,.3f}".format(competidor["Probabilidad"]))
            etiqueta_valor.setWordWrap(True)
            self.distribuidor_actividades.addWidget(etiqueta_valor, numero_fila, 1, alignment=Qt.AlignCenter
            )

            btn_editar = QPushButton("", self)
            btn_editar.setToolTip("Edit")
            btn_editar.setGeometry(0, 0, 40, 40)
            btn_editar.setFixedSize(40, 40)
            btn_editar.setIcon(QIcon("src/recursos/004-edit-button.png"))
            btn_editar.setIconSize(QSize(40, 40))
            btn_editar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn_editar.clicked.connect(partial(self.editar_competidor, numero_fila-1))
            self.distribuidor_actividades.addWidget(btn_editar, numero_fila, 2)

            btn_eliminar = QPushButton("", self)
            btn_eliminar.setToolTip("Delete")
            btn_eliminar.setGeometry(0, 0, 40, 40)
            btn_eliminar.setFixedSize(40, 40)
            btn_eliminar.setIcon(QIcon("src/recursos/005-delete.png"))
            btn_eliminar.setIconSize(QSize(40, 40))
            btn_eliminar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn_eliminar.clicked.connect(partial(self.eliminar_competidor, numero_fila-1))
            self.distribuidor_actividades.addWidget(btn_eliminar, numero_fila, 3)

            numero_fila=numero_fila+1
        
        #Elemento para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        elemento_de_espacio = QSpacerItem(140, 360-numero_fila*40 if numero_fila*40<=360 else 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.distribuidor_actividades.addItem(elemento_de_espacio, numero_fila, 0, 1, 3)


    def eliminar_competidor(self, indice_competidor):
        """
        Esta función es para eliminar un competidor
        """    
        mensaje_confirmacion=QMessageBox()
        mensaje_confirmacion.setIcon(QMessageBox.Question)
        mensaje_confirmacion.setText("¿Esta seguro de que desea eliminar este competidor?\nRecuerde que esta acción es irreversible")        
        mensaje_confirmacion.setWindowTitle("¿Desea borrar este competidor?")
        mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/smallLogo.png"))
        mensaje_confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No ) 
        respuesta=mensaje_confirmacion.exec_()
        if respuesta == QMessageBox.Yes:
            self.interfaz.eliminar_competidor(indice_competidor)
            self.competidores.pop(indice_competidor)
            self.mostrar_competidores(self.texto_nombre.text(), self.competidores)

    def volver(self):
        """
        Esta función permite volver a la lista de carreras
        """    
        self.hide()
        self.interfaz.mostrar_vista_lista_carreras()

    
    def aniadir_competidor(self):
        """
        Esta función ejecuta el diálogo para crear un competidor
        """    
        dialogo = Dialogo_crear_competidor()
        dialogo.exec_()
        if dialogo.resultado == 1:
            probabilidad_texto = dialogo.texto_probabilidad.text()
            probabilidad = float(probabilidad_texto) if probabilidad_texto.strip() != "" and probabilidad_texto.replace('.', '', 1).isdigit() else 0
            self.competidores.append({'Nombre':dialogo.texto_nombre.text(), 'Probabilidad': probabilidad, 'Estado':'Nueva'})
            self.mostrar_competidores(self.texto_nombre.text(), self.competidores)
    
    def editar_competidor(self, indice_competidor):
        """
        Esta función ejecuta el diálogo para editar un competidor
        """    
        dialogo = Dialogo_crear_competidor(self.competidores[indice_competidor])
        dialogo.exec_()
        if dialogo.resultado == 1:
            self.competidores[indice_competidor]['Nombre']=dialogo.texto_nombre.text()
            self.competidores[indice_competidor]['Probabilidad'] = float(dialogo.texto_probabilidad.text())
            self.competidores[indice_competidor]['Estado'] = self.competidores[indice_competidor].get('Estado', 'Editada')
            self.mostrar_competidores(self.texto_nombre.text(), self.competidores)
   
    def guardar_cambios(self):
        """
        Esta función guarda los cambios a la carrera (editando o guardando los nuevos competidores)
        """    
        competidores = []
        
        for i, competidor_en_interfaz in enumerate(self.competidores):
            if competidor_en_interfaz.get('Estado') == 'Nueva':
                competidores.append({'Posicion':'Nueva', 'Nombre': competidor_en_interfaz['Nombre'], 'Probabilidad': competidor_en_interfaz['Probabilidad']})
            else:
                competidores.append({'Posicion':i, 'Nombre': competidor_en_interfaz['Nombre'], 'Probabilidad': competidor_en_interfaz['Probabilidad']})
        
        resultado = self.interfaz.guardar_carrera(self.texto_nombre.text(), competidores)
        
        if resultado == "":
            for i, competidor in enumerate(self.competidores):
                if competidor.get('Estado') == 'Nueva':
                    self.interfaz.aniadir_competidor(competidor['Nombre'], competidor['Probabilidad'])
                else:
                    self.interfaz.editar_competidor(i, competidor['Nombre'], competidor['Probabilidad'])
                    
            self.hide()
            self.interfaz.mostrar_vista_lista_carreras()
                
        else:
            self.error(resultado)
        
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
