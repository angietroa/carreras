'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
from src.logica.Fachada_EPorra import Fachada_EPorra

class Logica_mock(Fachada_EPorra):

    def __init__(self):
        #Este constructor contiene los datos falsos para probar la interfaz
        self.carreras = [{'Nombre':'Formula 1', 'Competidores':[{'Nombre':'Juan Pablo Montoya', 'Probabilidad':0.15},\
                                                                 {'Nombre':'Kimi Räikkönen', 'Probabilidad':0.2},\
                                                                  {'Nombre':'Michael Schumacher', 'Probabilidad':0.65}],\
                                                    'Abierta':True},
                          {'Nombre':'Atletismo 100 m planos', 'Competidores':[{'Nombre':'Usain Bolt', 'Probabilidad':0.72},\
                                                                 {'Nombre':'Lamont Marcell Jacobs', 'Probabilidad':0.13},\
                                                                  {'Nombre':'Su Bingtian', 'Probabilidad':0.05},\
                                                                  {'Nombre':'Robson da Silva', 'Probabilidad':0.1}],\
                                                    'Abierta':True}]      
        self.apostadores = [{'Nombre':'Pepe Pérez'},{'Nombre':"Ana Andrade"},{'Nombre':"Aymara Castillo"}]
        self.apuestas = [{'Apostador':'Pepe Pérez', 'Carrera':'Carrera 1', 'Valor':10, 'Competidor':'Juan Pablo Montoya'},\
                        {'Apostador':'Ana Andrade', 'Carrera':'Carrera 1', 'Valor':25, 'Competidor':'Michael Schumacher'},\
                        {'Apostador':'Aymara Castillo', 'Carrera':'Carrera 1', 'Valor':14, 'Competidor':'Juan Pablo Montoya'},\
                        {'Apostador':'Aymara Castillo', 'Carrera':'Carrera 2', 'Valor':45, 'Competidor':'Usain Bolt'}]
        self.ganancias = [{'Carrera':'Formula 1', 'Ganancias':[('Pepe Pérez',13),('Ana Andrade',0), ('Aymara Castillo',15)], 'Ganancias de la casa': 4},\
            {'Carrera':'Atletismo 100 m planos', 'Ganancias':[('Pepe Pérez',32),('Ana Andrade',12), ('Aymara Castillo',34)], 'Ganancias de la casa': -10}]

    def dar_carreras(self):
        return self.carreras.copy()

    def dar_carrera(self, id_carrera):
        return self.carreras[id_carrera].copy()
        
    def crear_carrera(self, nombre):
        self.carreras.append({'Nombre':nombre, 'Competidores':[], 'Abierta':True})

    def editar_carrera(self, id, nombre):
        self.carreras[id]['Nombre'] = nombre

    def validar_crear_editar_carrera(self, nombre, competidores):
        return ""

    def terminar_carrera(self, id, ganador):
        self.carreras[id]['Ganador'] = ganador

    def eliminar_carrera(self, id):
        del self.carreras[id]

    def dar_apostadores(self):
        return self.apostadores.copy()

    def aniadir_apostador(self, nombre):
        self.apostadores.append({'Nombre': nombre})
    
    def editar_apostador(self, id, nombre):
        self.apostadores[id]['Nombre'] = nombre
    
    def validar_crear_editar_apostador(self, nombre):
        return ""
    
    def eliminar_apostador(self, id):
        del self.apostadores[id]

    def dar_competidores_carrera(self, id):
        return self.carreras[id]['Competidores'].copy()

    def dar_competidor(self, id_carrera, id_competidor):
        return self.carreras[id_carrera]['Competidores'][id_competidor].copy()

    def aniadir_competidor(self, id, nombre, probabilidad):
        self.carreras[id]['Competidores'].append({'Nombre':nombre, 'Probabilidad':probabilidad})

    def editar_competidor(self, id_carrera, id_competidor, nombre, probabilidad):
        self.carreras[id_carrera]['Competidores'][id_competidor]['Nombre']=nombre
        self.carreras[id_carrera]['Competidores'][id_competidor]['Probabilidad']=probabilidad
    
    def eliminar_competidor(self, id_carrera, id_competidor):
        del self.carreras[id_carrera]['Competidores'][id_competidor]

    def dar_apuestas_carrera(self, id_carrera):
        nombre_carrera =self.carreras[id_carrera]['Nombre']
        return list(filter(lambda x: x['Carrera']==nombre_carrera, self.apuestas))

    def dar_apuesta(self, id_carrera, id_apuesta):
        return self.dar_apuestas_carrera(id_carrera)[id_apuesta].copy()

    def crear_apuesta(self, apostador, id_carrera, valor, competidor):
        n_apuesta = {}
        n_apuesta['Apostador'] = apostador
        n_apuesta['Carrera'] = self.carreras[id_carrera]['Nombre']
        n_apuesta['Valor'] = valor
        n_apuesta['Competidor'] = competidor
        self.apuestas.append(n_apuesta)

    def editar_apuesta(self, id_apuesta, apostador, carrera, valor, competidor):
        self.apuestas[id_apuesta]['Apostador'] = apostador
        self.apuestas[id_apuesta]['Carrera'] = self.carreras[carrera]["Nombre"]
        self.apuestas[id_apuesta]['Valor'] = valor
        self.apuestas[id_apuesta]['Competidor'] = competidor

    def validar_crear_editar_apuesta(self, apostador, carrera, valor, competidor):
        return ""

    def eliminar_apuesta(self, id_carrera, id_apuesta):
        nombre_carrera =self.carreras[id_carrera]['Nombre']
        i = 0
        id = 0
        while i < len(self.apuestas):
            if self.apuestas[i]['Carrera'] == nombre_carrera:
                if id == id_apuesta:
                    self.apuestas.pop(i)
                    return True
                else:
                    id+=1
            i+=1
        
        return False
                

        del self.apuesta[id_apuesta]

    def dar_reporte_ganancias(self, id_carrera, id_competidor):
        self.carreras[id_carrera]['Abierta']=False
        n_carrera = self.carreras[id_carrera]['Nombre']
        for ganancias in self.ganancias:
            if ganancias['Carrera'] == n_carrera:
                return ganancias['Ganancias'], ganancias['Ganancias de la casa']    
