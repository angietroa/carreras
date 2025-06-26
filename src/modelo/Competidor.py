from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.modelo.declarative_base import Base

class Competidor(Base):
    __tablename__ = 'competidores'
    id = Column(Integer, primary_key=True)
    Nombre = Column(String, nullable=False)
    Probabilidad = Column(Float, nullable=False)
    carrera_id = Column(Integer, ForeignKey('carreras.id'))
    
    apuestas = relationship('Apuesta', cascade='all, delete, delete-orphan')

    def dar_nombre(self):
        return self.Nombre
    
    def cambiar_nombre(self,nombre):
        self.Nombre = nombre
    
    def dar_probabilidad(self):
        return self.Probabilidad
    
    def cambiar_probabilidad(self,p):
        self.Probabilidad = p

    def conv_dict(self)->dict:
        resultado = {"Nombre": self.Nombre, "Probabilidad": round(self.Probabilidad,2)}
        return resultado