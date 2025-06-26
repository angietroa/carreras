from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Apostador(Base):
    __tablename__ = 'apostadores'
    id = Column(Integer, primary_key=True)
    Nombre = Column(String, unique=True, nullable=False)

    apuestas = relationship('Apuesta', cascade='all, delete, delete-orphan')
    
    def dar_nombre(self)->str:
        return self.Nombre
    
    def cambiar_nombre(self, nombre):
        self.Nombre = nombre
    
    def conv_dict(self)->dict:
        return  {"Nombre": self.Nombre}
    
