from src.logica.Fachada_EPorra import Fachada_EPorra
from src.modelo.Carrera import Carrera
from src.modelo.Competidor import Competidor
from src.modelo.Apostador import Apostador
from src.modelo.Apuesta import Apuesta
from src.modelo.declarative_base import Session

class Eporra(Fachada_EPorra):
    def __init__(self):
        self.session = Session()
        self.carreras = []
        self.apostadores = []
        self.carrera_actual = Carrera(Nombre="", Abierta=True)
        self.eliminar = []

        return None
    
    def __activar_carrera(self, id):
        if(self.carrera_actual.dar_nombre()==""):
            self.carrera_actual = self.carreras[id]

    def __dar_apostador(self, nombre):
        r = None
        for apo in self.apostadores:
            if (apo.dar_nombre() == nombre):
                r = apo
                break
        return r
    
    def __eliminar(self):
        if len(self.eliminar)>0:
            for obj in self.eliminar:
                self.session.delete(obj)
        self.session.commit()

    def dar_carreras(self):
        self.carreras = self.session.query(Carrera).order_by(Carrera.Nombre).all()
        self.carrera_actual = Carrera(Nombre="", Abierta=True)
        resultado = []
        if self.carreras:
            for c in self.carreras:
                resultado.append(c.conv_dict())
        return resultado

    def crear_carrera(self, nombre):
        nueva_carrera = Carrera(Nombre=nombre, Abierta=True)
        self.carrera_actual = nueva_carrera
        self.session.add(nueva_carrera)
        self.session.commit()

    def validar_crear_editar_carrera(self, nombre, competidores):
        r = ""
        if not (0 < len(nombre) < 50):
            r+= "500 El nombre de la carrera debe tener entre 1 y 50 caracteres \n"

        if(self.carrera_actual.dar_nombre() != nombre):
            if any(c.dar_nombre() == nombre for c in self.carreras):
                r+= "500 la carrera ya existe \n"

        if len(competidores) <= 0:
            r+= "500 no hay competidores, no se puede crear \n"

        suma = 0
        numero= len(competidores)
        for i in range(numero):
            competidor = competidores[i]
            suma+= round(float(competidor["Probabilidad"]),2)
            if not (0 < len(competidor["Nombre"]) < 50):
                r+= "500 el nombre de uno de los competidores no cumple con la longitud \n"

            if not (0 < competidor["Probabilidad"] <=1 ):
                r+= "500 la probabilidad de uno de los competidores no es correcta \n"
            
            for j in range( i+1 , numero):
                siguiente = competidores[j]
                if(competidor["Nombre"]==siguiente["Nombre"]):
                    r+= "500 hay nombres de competidores repetidos \n"

        suma = round(suma,2)
        if(suma!=1):
            r+= "500 La suma de las probabilidades debe ser igual a uno (1) y es " + str(suma) 

        return r

    def aniadir_competidor(self, id, nombre, probabilidad):
        self.__activar_carrera(id)
        competidor = Competidor(Nombre=nombre, Probabilidad=probabilidad)
        self.carrera_actual.competidores.append(competidor)
        self.session.add(competidor)
        self.session.commit()

    def dar_carrera(self, id_carrera):
        self.carrera_actual = self.carreras[id_carrera]
        return  self.carrera_actual.conv_dict()

    def dar_competidores_carrera(self, id):
        self.__activar_carrera(id)
        return  self.carrera_actual.dar_competidores()

    def editar_carrera(self, id, nombre):
        self.__activar_carrera(id)
        self.carrera_actual.cambiar_nombre(nombre)
        self.session.add(self.carrera_actual)
        self.session.commit()
        self.__eliminar()

    def editar_competidor(self, id_carrera, id_competidor, nombre, probabilidad):
        self.__activar_carrera(id_carrera)
        competidor = self.carrera_actual.competidores[id_competidor]
        competidor.cambiar_nombre(nombre)
        competidor.cambiar_probabilidad(probabilidad)
        self.session.add(competidor)
        self.session.commit()

    def dar_apostadores(self):
        self.apostadores = self.session.query(Apostador).order_by(Apostador.Nombre).all()
        resultado = []
        if self.apostadores:
            for apo in self.apostadores:
                resultado.append(apo.conv_dict())
        return resultado

    def validar_crear_editar_apostador(self, nombre):
        r = ""
        if not (0 < len(nombre) < 50):
            r+= "500 El nombre del apostador debe tener entre 1 y 50 caracteres \n"

        for apo in self.apostadores:
            if apo.dar_nombre() == nombre:
                r+= "500 El apostador ya existe \n"

        return r

    def aniadir_apostador(self, nombre):
        apostador = Apostador(Nombre=nombre)
        self.session.add(apostador)
        self.session.commit()
        return True

    def dar_apuestas_carrera(self, id_carrera):
        self.__activar_carrera(id_carrera)
        return  self.carrera_actual.dar_apuestas()

    def validar_crear_editar_apuesta(self, apostador, carrera, valor, competidor):
        r = ""
        if valor <= 0:
            r+= "500 El valor de la apuesta debe ser mayor a cero \n"
        if not apostador:
            r+= "500 El nombre del apostador no puede estar vacío \n"
        if not competidor:
            r+= "500 El nombre del competidor no puede estar vacío \n"

        if(self.carrera_actual.dar_nombre()=="" and len(self.carreras)>0):
            self.carrera_actual = self.carreras[carrera]

        if(self.carrera_actual.esta_abierta()==False):
            r+= "500 Esta carrera esta Terminada, No se puede agregar apuestas \n"

        return r

    def crear_apuesta(self, apostador, id_carrera, valor, competidor):
        self.__activar_carrera(id_carrera)
        apostador_sel = self.__dar_apostador(apostador)
        competidor_sel = self.carrera_actual.dar_competidor(competidor)

        if(apostador_sel and competidor_sel):
            apuesta = Apuesta(Valor=valor)
            apuesta.apostador = apostador_sel
            apuesta.competidor = competidor_sel
            apuesta.carrera = self.carrera_actual
            apostador_sel.apuestas.append(apuesta)
            competidor_sel.apuestas.append(apuesta)
            self.carrera_actual.apuestas.append(apuesta)
            self.session.add(apuesta)
            self.session.add(apostador_sel)
            self.session.add(competidor_sel)
            self.session.add(self.carrera_actual)
            self.session.commit()

        return True

    def editar_apostador(self, id, nombre):
        apostador = self.apostadores[id]
        if(apostador):
            apostador.cambiar_nombre(nombre)
            self.session.add(apostador)
            self.session.commit()

    def eliminar_apostador(self, id):
        apostador = self.apostadores[id]
        if(apostador):
            apuestas = apostador.apuestas
            if(len(apuestas)==0):
                self.session.delete(apostador)
                self.session.commit()

    def eliminar_carrera(self, id):
        carrera_a_eliminar = self.carreras[id]
        if carrera_a_eliminar:
            if len(carrera_a_eliminar.apuestas)<=0:
                self.session.delete(carrera_a_eliminar)
                self.session.commit()

    def dar_reporte_ganancias(self, id_carrera, id_competidor):
        self.__activar_carrera(id_carrera)
        reporte = self.carrera_actual.terminar(id_competidor)
        self.session.add(self.carrera_actual)
        self.session.commit()
        return reporte

    def editar_apuesta(self, id_apuesta, apostador, id_carrera, valor, competidor):
        self.__activar_carrera(id_carrera)
        apostador_sel = self.__dar_apostador(apostador)
        competidor_sel = self.carrera_actual.dar_competidor(competidor)

        if apostador_sel and competidor_sel:
            apuesta = self.carrera_actual.dar_apuesta(id_apuesta)
            apuesta.cambiar_valor(valor)
            apuesta.apostador = apostador_sel
            apuesta.competidor = competidor_sel
            self.session.add(apuesta)
            self.session.commit()

        return True

    def dar_apuesta(self, id_carrera, id_apuesta):
        return self.dar_apuestas_carrera(id_carrera)[id_apuesta].copy()

    def eliminar_apuesta(self, id_carrera, id_apuesta):
        apuesta_a_eliminar = self.dar_apuestas_carrera(id_carrera)[id_apuesta]

        apuesta_obj = self.session.query(Apuesta).join(Apostador).join(Competidor).filter(
            Apuesta.Valor == apuesta_a_eliminar['Valor'],
            Apostador.Nombre == apuesta_a_eliminar['Apostador'],
            Competidor.Nombre == apuesta_a_eliminar['Competidor']
        ).first()

        if apuesta_obj:
            self.session.delete(apuesta_obj)
            self.session.commit()

    def eliminar_competidor(self, id_carrera, id_competidor):
        self.__activar_carrera(id_carrera)
        competidor_a_eliminar = self.carrera_actual.competidores[id_competidor]
        if competidor_a_eliminar:
            self.eliminar.append(competidor_a_eliminar)
