
import unittest
import random

from faker import Faker

from src.logica.Eporra import Eporra

from src.modelo.Carrera import Carrera
from src.modelo.Competidor import Competidor
from src.modelo.Apostador import Apostador
from src.modelo.Apuesta import Apuesta
from src.modelo.declarative_base import engine, Base, Session

class LogicTestCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		Base.metadata.create_all(engine)
		cls.logica = Eporra()
		cls.session = Session()
		cls.factory = Faker()
		Faker.seed(1000)
		cls.carreras = []
		cls.apostadores = []
		cls.apuestas = []
		cls.genera_datos()

	def setUp(self):
		return True

	def tearDown(self):
		return True

	@classmethod
	def genera_datos(cls):
		for i in range(6):
			c = {'Nombre': cls.factory.unique.name(), 'Abierta' : True , 'Competidores' : []}
			cantidad = int(random.randint(3,5))
			proba = cls.genera_probabilidad(cantidad)
			for j in range(cantidad):
				p = proba[j]
				com = {'Nombre': cls.factory.unique.name(), 'Probabilidad': p}
				c["Competidores"].append(com)
			cls.carreras.append(c)

		for i in range(10):
			apostador = {'Nombre': cls.factory.unique.name()}
			cls.apostadores.append(apostador)

		cls.carreras_apuestas = []
		for carrera in cls.carreras:
			apuestas = []
			cantidad = random.randint(3,6)
			nombre = carrera['Nombre']
			for i in range(cantidad):
				competidores = carrera['Competidores']
				id_apostador = random.randint(0,len(cls.apostadores)-1)
				id_competidor = random.randint(0,len(carrera['Competidores'])-1)
				apuesta = {
					'Apostador': cls.apostadores[id_apostador]['Nombre'],
					'Valor': random.randint(100,800),
					'Competidor': competidores[id_competidor]['Nombre']
				}
				apuestas.append(apuesta)
			cls.carreras_apuestas.append({'Carrera':nombre,'Apuestas':apuestas})


	@classmethod
	def genera_probabilidad(cls, cantidad):
		probabilidades = [1] * cantidad
		posiciones = list(range(0,cantidad))
		random.shuffle(posiciones)
		for i in range(3):
			for id in posiciones:
				suma = sum(probabilidades)
				if(suma>7):
					probabilidades[id]+= 10-suma
				elif(suma==10):
					break
				else:
					probabilidades[id]+= random.randint(1,10-suma)
					
		probabilidades = [round(num / 10, 1) for num in probabilidades]
		return probabilidades



	def limpiarDatos(self):
		'''borra todos las carreras'''
		carreras = self.session.query(Carrera).all()
		for carrera  in carreras:
			self.session.delete(carrera)

		'''borra todos los apostadores '''
		apostadores = self.session.query(Apostador).all()
		for apostador  in apostadores:
			self.session.delete(apostador)

		self.session.commit()

	def test_1_crear_carreras(self):

		for c in self.carreras:
			nombre = c['Nombre']
			competidores = c["Competidores"]
			resultado = self.logica.validar_crear_editar_carrera(nombre, competidores)
			self.assertEqual(resultado,"")
			self.logica.crear_carrera(nombre)
			for c in competidores:
				self.logica.aniadir_competidor(-1,c["Nombre"],c["Probabilidad"])
		
	def test_2_dar_carreras_en_orden_alfabetico(self):
		# ordenar carreras para comparar
		self.carreras = sorted(self.carreras, key=lambda carrera: carrera['Nombre'])
		for carrera in self.carreras:
			carrera['Competidores'] = sorted(carrera['Competidores'], key=lambda competidor: competidor['Nombre'])
		esperado = self.carreras
		resultado = self.logica.dar_carreras()
		self.assertEqual(esperado, resultado)

	def test_3_crear_apostadores(self):
		for a in self.apostadores:
			nombre = a["Nombre"]
			resultado = self.logica.validar_crear_editar_apostador(nombre)
			self.assertIn("", resultado)
			self.logica.aniadir_apostador(nombre)
			apostador = self.session.query(Apostador).filter(Apostador.Nombre == nombre).first()
			self.assertEqual(apostador.dar_nombre(), nombre)

	def test_4_dar_apostadores_en_orden_alfabetico(self):
		self.apostadores = sorted(self.apostadores, key=lambda apostador: apostador['Nombre'])
		resultado = self.logica.dar_apostadores()
		self.assertEqual(self.apostadores, resultado)

	def test_5_crear_apuestas(self):
		carreras = self.logica.dar_carreras()
		self.logica.dar_apostadores()
		for lista in self.carreras_apuestas:
			for apuesta in lista['Apuestas']:
				id_carrera = -1 
				for i, carrera in enumerate(carreras):
					if carrera['Nombre'] == lista['Carrera']:
						id_carrera = i
						break
				valor = apuesta["Valor"]
				apostador = apuesta["Apostador"]
				competidor = apuesta["Competidor"]
				resultado = self.logica.validar_crear_editar_apuesta(apostador, id_carrera, valor, competidor)
				self.assertIn("", resultado)
				self.logica.dar_carrera(id_carrera)
				self.logica.crear_apuesta(apostador, id_carrera, valor, competidor)

	def test_6_dar_apuestas_ordenadas(self):
		carreras = self.logica.dar_carreras()
		id_carrera = random.randint(0,len(carreras)-1)
		carrera = carreras[id_carrera]
		apuestas = []
		for c in self.carreras_apuestas:
			if(carrera['Nombre']==c['Carrera']):
				apuestas = c['Apuestas']
		apuestas = sorted(apuestas, key=lambda apuesta: apuesta['Apostador'])
		resultado = self.logica.dar_apuestas_carrera(id_carrera)
		self.assertEqual(apuestas, resultado)

	def test_7_generar_reporte(self):
		carreras = self.logica.dar_carreras()
		id_carrera = random.randint(0,len(carreras)-1)
		carrera = carreras[id_carrera]
		apuestas = []
		for c in self.carreras_apuestas:
			if(carrera['Nombre']==c['Carrera']):
				apuestas = c['Apuestas']
		apuestas = sorted(apuestas, key=lambda apuesta: apuesta['Apostador'])
		id_ganador = random.randint(0,len(carrera['Competidores'])-1)
		competidor = carrera['Competidores'][id_ganador]
		cuota = competidor['Probabilidad'] / (1- competidor['Probabilidad'])
		total_pagos = 0
		total_apuestas = 0
		ganadores = []
		for apuesta in apuestas:
			total_apuestas+= apuesta['Valor']
			if apuesta['Competidor'] == competidor['Nombre']:
				ganancia = apuesta['Valor'] + (apuesta['Valor']/cuota)
				tupla = (apuesta['Apostador'], ganancia)
				total_pagos+= ganancia
				ganadores.append(tupla)
		casa = total_apuestas - total_pagos
		esperado = (ganadores, casa)
		self.logica.dar_carrera(id_carrera)
		resultado = self.logica.dar_reporte_ganancias(id_carrera, id_ganador)
		self.assertEqual(resultado, esperado)
		self.limpiarDatos()