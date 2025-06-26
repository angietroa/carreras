'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
class Fachada_EPorra():

    def dar_carreras(self):
        ''' Retorna la lista de carreras en la aplicación
        Parámetros:
            Ninguno
        Retorna:
            (list): La lista de objetos con las carreras
        '''
        raise NotImplementedError("Método no implementado")

    def dar_carrera(self, id_carrera):
        ''' Retorna una carrera a partir de su identificador
        Parámetros:
            id_carrera (int): La posición de la carrera en la lista de carreras
        Retorna:
            (dict): La carrera identificada con el id_carrera recibido como parámetro
        '''
        raise NotImplementedError("Método no implementado")
        
    def crear_carrera(self, nombre):
        ''' Crea una nueva carrera
        Parámetros:
            nombre (string): el nombre de la carrera a crear
        '''
        raise NotImplementedError("Método no implementado")

    def editar_carrera(self, id, nombre):
        ''' Edita una carrera a partir de su identificador
        Parámetros:
            id (int): La posición de la carrera en la lista de carreras
            nombre (string): El nombre de la carrera a actualizar
        '''
        raise NotImplementedError("Método no implementado")

    def validar_crear_editar_carrera(self, nombre, competidores):
        ''' Valida la información de una carrera a partir de su nombre y los competidores
        Parámetros:
            nombre (string): El nombre de la carrera
            competidores (list): Una lista de competidores con un hashmap que contiene
                - el id de posición del competidor o la palabra Nuevo si es un competidor nuevo y no tiene id
                - el nombre del competidor
                - la probabilidad del competidor
        Retorna:
            (string): Una cadena con los mensajes de error en la validación o vacío si no hay errores
        '''
        raise NotImplementedError("Método no implementado")

    def terminar_carrera(self, id, ganador):
        ''' Termina una carrera asignando un ganador y dejando su variable de terminada en verdadero
        Parámetros:
            id (int): La posición de la carrera en la lista de carreras
            ganador (int): El ganador de la carrera
        '''
        raise NotImplementedError("Método no implementado")

    def eliminar_carrera(self, id):
        ''' Elimina una carrera
        Parámetros:
            id (int): La posición de la carrera en la lista de carreras
        '''
        raise NotImplementedError("Método no implementado")

    def dar_apostadores(self):
        ''' Retorna una lista de apostadores
        Parámetros:
            Ninguno
        Retorna:
            (list): La lista de apostadores en EPorra
        '''
        raise NotImplementedError("Método no implementado")

    def aniadir_apostador(self, nombre):
        ''' Adiciona un apostador
        Parámetros:
            nombre (string): El nombre del apostador a adicionar
        '''
        raise NotImplementedError("Método no implementado")
    
    def editar_apostador(self, id, nombre):
        ''' Edita un apostador cambiando su nombre
        Parámetros:
            id (int): La posición del apostador en la lista de apostadores
            nombre (string): El nombre del apostador a actualizar
        '''
        raise NotImplementedError("Método no implementado")
    
    def validar_crear_editar_apostador(self, nombre):
        ''' Valida los datos de un apostador antes de guardarlos
        Parámetros:
            nombre (string): El nombre del apostador a crear o editar
        Retorna:
            (string): Una cadena con los mensajes de error en la validación o vacío si no hay errores
        '''
        raise NotImplementedError("Método no implementado")
    
    def eliminar_apostador(self, id):
        ''' Elimina un apostador de la lista
        Parámetros:
            id (int): La posición del apostador en la lista de apostadores
        '''
        raise NotImplementedError("Método no implementado")

    def dar_competidores_carrera(self, id):
        ''' Retorna la lista de competidores de una carrera
        Parámetros:
            id (int): La posición de la carrera en la lista de carreras
        Retorna:
            (list): La lista de competidores de una carrera
        '''
        raise NotImplementedError("Método no implementado")

    def dar_competidor(self, id_carrera, id_competidor):
        ''' Retorna un competidor en una carrera
        Parámetros:
            id_carrera (int): La posición de la carrera en la lista de carreras
            id_competidor (int): La posición del competidor en la lista de competidores de la carrera
        Retorna:
            (list): La lista de competidores d euna carrera
        '''
        raise NotImplementedError("Método no implementado")

    def aniadir_competidor(self, id, nombre, probabilidad):
        ''' Adiciona un competidor a una carrera
        Parámetros:
            id (int): La posición de la carrera en la lista de carreras
            nombre (string): El nombre del competidor a adicionar
            probabilidad (float): La probabilidad asignada al competidor
        '''
        raise NotImplementedError("Método no implementado")

    def editar_competidor(self, id_carrera, id_competidor, nombre, probabilidad):
        ''' Edita un competidor en una carrera
        Parámetros:
            id_carrera (int): La posición de la carrera en la lista de carreras
            id_competidor (int): La posición del competidor dentro de la lista de competidores en una carrera
            nombre (string): El nombre del competidor a editar
            probabilidad (float): La probabilidad asignada al competidor
        '''
        raise NotImplementedError("Método no implementado")
    
    def eliminar_competidor(self, id_carrera, id_competidor):
        ''' Elimina un competidor de una carrera
        Parámetros:
            id_carrera (int): La posición de la carrera en la lista de carreras
            id_competidor (int): La posición del competidor dentro de la lista de competidores en una carrera
        '''
        raise NotImplementedError("Método no implementado")

    def dar_apuestas_carrera(self, id_carrera):
        ''' Retorna la lista de apuestas de una carrera
        Parámetros:
            id_carrera (int): La posición de la carrera en la lista de carreras
        Retorna:
            (list): La lista de apuestas para una carrera
        '''
        raise NotImplementedError("Método no implementado")

    def dar_apuesta(self, id_carrera, id_apuesta):
        ''' Retorna una apuesta a partir de la carrera y su posición en la lista de apuestas
        Parámetros:
            id_carrera (int): La posición de la carrera en la lista de carreras
            id_apuesta (int): La posición de la apuesta en la lista de apuestas en la carrera
        Retorna:
            (dict): La apuesta de la carrera
        '''
        raise NotImplementedError("Método no implementado")

    def crear_apuesta(self, apostador, id_carrera, valor, competidor):
        ''' Crea una apuesta a partir de los datos enviados por parámetro
        Parámetros:
            apostador (string): El nombre del apostador
            id_carrera (int): La posición de la carrera en la lista de carreras
            valor (float): El valor de la apuesta
            competidor (string): El nombre del competidor sobre el que se apuesta
        '''
        raise NotImplementedError("Método no implementado")

    def editar_apuesta(self, id_apuesta, apostador, carrera, valor, competidor):
        ''' Actualiza los datos de una apuesta según los datos enviados por parámetro
        Parámetros:
            id_apuesta (int): La posición de la apuesta en la lista de apuestas de la carrera
            apostador (string): El nombre del apostador
            id_carrera (int): La posición de la carrera en la lista de carreras
            valor (float): El valor de la apuesta
            competidor (string): El nombre del competidor sobre el que se apuesta
        '''
        raise NotImplementedError("Método no implementado")

    def validar_crear_editar_apuesta(self, apostador, carrera, valor, competidor):
        ''' Valida que los datos de una apuesta sean los correctos
        Parámetros:
            apostador (string): El nombre del apostador
            carrera (int): La posición de la carrera en la lista de carreras
            valor (float): El valor de la apuesta
            competidor (string): El nombre del competidor sobre el que se apuesta
        Retorna:
            (string): Una cadena con los mensajes de error en la validación o vacío si no hay errores
        '''
        raise NotImplementedError("Método no implementado")

    def eliminar_apuesta(self, id_carrera, id_apuesta):
        ''' Elimina una apuesta de una carrera
        Parámetros:
            id_carrera (int): La posición de la carrera en la lista de carreras
            id_apuesta (int): La posición de la apuesta en la lista de apuestas
        '''
        raise NotImplementedError("Método no implementado")

    def dar_reporte_ganancias(self, id_carrera, id_competidor):
        ''' Genera la información para el reporte de ganancias
        Parámetros:
            id_carrera (int): La posición de la carrera en la lista de carreras
            id_competidor (int): La posición del competidor en la lista de competidores de la carrera
        Retorna:
            (list, float): Una lista con los valores que ganan los apostadores y el valor de las ganancias de la casa
        '''
        raise NotImplementedError("Método no implementado")
