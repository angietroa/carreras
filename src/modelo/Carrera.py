from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.modelo.declarative_base import Base

class Carrera(Base):
    __tablename__ = 'carreras'
    id = Column(Integer, primary_key=True)
    Nombre = Column(String, unique=True, nullable=False)
    Abierta = Column(Boolean, default=True)
    ganador_id = Column(Integer, ForeignKey('competidores.id'))

    competidores = relationship('Competidor', cascade='all, delete, delete-orphan', foreign_keys='Competidor.carrera_id')
    apuestas = relationship('Apuesta', cascade='all, delete, delete-orphan', foreign_keys='Apuesta.carrera_id')
    ganador = relationship('Competidor', uselist=False, foreign_keys=[ganador_id])

    def conv_dict(self) -> dict:
        competidores = self.dar_competidores()
        resultado = {"Nombre": self.Nombre, "Abierta": self.Abierta, "Competidores": competidores}
        return resultado
    
    def dar_competidores(self)->list:
        competidores = []
    
        if self.competidores:
            self.competidores = sorted(self.competidores, key=lambda c: c.Nombre)
            for competidor in self.competidores:
                competidores.append(competidor.conv_dict())

        return competidores
    
    def dar_apuestas(self)->list:
        apuestas = []
    
        if self.apuestas:
            self.apuestas = sorted(self.apuestas, key=lambda c: c.apostador.Nombre)
            for apuesta in self.apuestas:
                apuestas.append(apuesta.conv_dict())

        return apuestas
    
    def cambiar_nombre(self, nombre):
        self.Nombre = nombre

    def dar_nombre(self):
        return self.Nombre
    
    def esta_abierta(self):
        return self.Abierta
    
    def dar_apuesta(self, id):
        self.apuestas = sorted(self.apuestas, key=lambda c: c.apostador.Nombre)
        return self.apuestas[id]
    
    def dar_competidor(self,nombre):
        r = None
        for com in self.competidores:
            if com.dar_nombre() == nombre:
                r = com
                break
        return r   
    
    def terminar(self, id_competidor):
        self.apuestas = sorted(self.apuestas, key=lambda c: c.apostador.Nombre)
        ganador = self.competidores[id_competidor]
        self.Abierta = False
        nombre_ganador = ganador.dar_nombre()
        probabilidad = ganador.dar_probabilidad()
        ganadores = []
        total_apuestas = 0
        total_pagos = 0
        for apuesta in self.apuestas:
            total_apuestas+= apuesta.dar_valor()
            if (apuesta.competidor.dar_nombre() == nombre_ganador):
                ganancia = apuesta.calcular_ganancia(probabilidad)
                nombre , valor_ganado = ganancia
                total_pagos+= valor_ganado
                ganadores.append(ganancia)
		
        casa = total_apuestas - total_pagos
        resultado = (ganadores, casa)
        return resultado




