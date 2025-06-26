from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .declarative_base import Base

class Apuesta(Base):
    __tablename__ = 'apuestas'
    id = Column(Integer, primary_key=True)
    Valor = Column(Integer, nullable=False)
    apostador_id = Column(Integer, ForeignKey('apostadores.id'), nullable=False)
    competidor_id = Column(Integer, ForeignKey('competidores.id'), nullable=False)
    carrera_id = Column(Integer, ForeignKey('carreras.id'))

    apostador = relationship('Apostador', back_populates='apuestas', foreign_keys=[apostador_id])
    competidor = relationship('Competidor', back_populates='apuestas', foreign_keys=[competidor_id])
    carrera = relationship('Carrera', back_populates='apuestas', foreign_keys=[carrera_id])

    def conv_dict(self) -> dict:
        apostador = self.apostador.Nombre
        competidor = self.competidor.Nombre
        resultado = {"Apostador": apostador, "Valor": self.Valor, "Competidor": competidor}
        return resultado

    def calcular_ganancia(self, probabilidad):
        cuota = probabilidad / (1-probabilidad)
        ganancia = self.Valor + ( self.Valor / cuota)
        apostador = self.apostador.dar_nombre()
        resultado = (apostador, ganancia)
        return resultado

    def dar_valor(self):
        return self.Valor

    def cambiar_valor(self, v):
        self.Valor = v
