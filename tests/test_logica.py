
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

	def setUp(self):
		Base.metadata.create_all(engine)
		self.logica = Eporra()
		self.session = Session()
		self.factory = Faker()
		self.total_carreras = 2
		self.total_apostadores = 4
		self.min_apuestas = 2
		self.max_apuestas = 4
		self.genera_datos()

	def tearDown(self):
		'''Abre la sesión'''
		self.session = Session()

		'''borra todos las carreras'''
		carreras = self.session.query(Carrera).all()
		for carrera  in carreras:
			self.session.delete(carrera)

		'''borra todos los apostadores '''
		apostadores = self.session.query(Apostador).all()
		for apostador  in apostadores:
			self.session.delete(apostador)

		self.session.commit()

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

	def genera_datos(self):
		self.carreras = []
		self.apostadores = []
		self.apuestas = []
		for i in range(self.total_carreras):
			c = {'Nombre': self.factory.unique.name(), 'Abierta' : True , 'Competidores' : []}
			cantidad = int(random.randint(3,5))
			proba = self.genera_probabilidad(cantidad)
			for j in range(cantidad):
				p = proba[j]
				com = {'Nombre': self.factory.unique.name(), 'Probabilidad': p}
				c["Competidores"].append(com)
			self.carreras.append(c)

		for i in range(self.total_apostadores):
			apostador = {'Nombre': self.factory.unique.name()}
			self.apostadores.append(apostador)

		self.carreras_apuestas = []
		for carrera in self.carreras:
			apuestas = []
			cantidad = random.randint(self.min_apuestas,self.max_apuestas)
			nombre = carrera['Nombre']
			for i in range(cantidad):
				competidores = carrera['Competidores']
				id_apostador = random.randint(0,len(self.apostadores)-1)
				id_competidor = random.randint(0,len(carrera['Competidores'])-1)
				apuesta = {
					'Apostador': self.apostadores[id_apostador]['Nombre'],
					'Valor': random.randint(100,800),
					'Competidor': competidores[id_competidor]['Nombre']
				}
				apuestas.append(apuesta)
			self.carreras_apuestas.append({'Carrera':nombre,'Apuestas':apuestas})

	def llenarCarreras(self):
		for cra in self.carreras:
			self.logica.crear_carrera(cra["Nombre"])
			for cdr in cra["Competidores"]:
				self.logica.aniadir_competidor(-1, cdr["Nombre"] , cdr["Probabilidad"])

	def llenarApostadores(self):
		for a in self.apostadores:
			self.logica.aniadir_apostador(a["Nombre"])

	def llenarApuestas(self):
		self.llenarCarreras()
		self.llenarApostadores()
		carreras = self.logica.dar_carreras()
		self.logica.dar_apostadores()
		for i, cra in enumerate(carreras):
			for apt in self.carreras_apuestas:
				if(apt["Carrera"] == cra["Nombre"]):
					apuestas = apt["Apuestas"]
					for a in apuestas:
						self.logica.dar_carrera(i)
						self.logica.crear_apuesta(a["Apostador"], i, a["Valor"], a["Competidor"])

	def test_01_listado_vacio(self) :
		resultado = self.logica.dar_carreras()
		self.assertEqual(resultado, [])

	def test_02_listado_en_orden_alfabetico(self):
		self.llenarCarreras()
		self.carreras = sorted(self.carreras, key=lambda carrera: carrera['Nombre'])
		for carrera in self.carreras:
			carrera['Competidores'] = sorted(carrera['Competidores'], key=lambda competidor: competidor['Nombre'])
		esperado = self.carreras
		resultado = self.logica.dar_carreras()
		self.assertEqual(resultado, esperado)

	def test_03_nombre_de_nueva_carrera_vacio(self):
		competidores = self.carreras[0]["Competidores"]
		resultado = self.logica.validar_crear_editar_carrera('', competidores)
		self.assertIn("500", resultado)

	def test_04_nombre_de_nueva_carrera_con_exceso_de_caracteres(self):
		nombre_largo = 'a' * 51
		competidores = self.carreras[0]["Competidores"]
		resultado = self.logica.validar_crear_editar_carrera(nombre_largo, competidores)
		self.assertIn("500", resultado)

	def test_05_nombre_de_nueva_carrera_repetido(self):
		self.llenarCarreras()
		nombre_repetido = self.carreras[0]["Nombre"]
		competidores = self.carreras[0]["Competidores"]
		self.logica.dar_carreras()
		resultado = self.logica.validar_crear_editar_carrera(nombre_repetido, competidores)
		self.assertIn("500", resultado)

	def test_06_nueva_carrera_sin_competidores(self):
		nombre = self.factory.unique.name()
		resultado = self.logica.validar_crear_editar_carrera(nombre, [])
		self.assertIn("500", resultado)

	def test_07_nueva_carrera_con_competidores_y_probabilidad_mayor_a_uno(self):
		nombre = self.factory.unique.name()
		cantidad = int(random.randint(3,5))
		competidores = []
		for j in range(cantidad):
			p = round(random.uniform(0.4,0.7),1)
			com = {'Nombre': self.factory.unique.name(), 'Probabilidad': p}
			competidores.append(com)
		resultado = self.logica.validar_crear_editar_carrera(nombre, competidores)
		self.assertIn("500", resultado)

	def test_08_nueva_carrera_con_competidores_y_probabilidad_menor_a_uno(self):
		nombre = self.factory.unique.name()
		cantidad = int(random.randint(2,4))
		competidores = []
		for j in range(cantidad):
			p = round(random.uniform(0.1,0.2),1)
			com = {'Nombre': self.factory.unique.name(), 'Probabilidad': p}
			competidores.append(com)		
		resultado = self.logica.validar_crear_editar_carrera(nombre, competidores)
		self.assertIn("500", resultado)

	def test_09_nuevo_competidor_con_campos_vacios(self):
		nombre = self.factory.unique.name()
		cantidad = int(random.randint(3,5))
		proba = self.genera_probabilidad(cantidad)
		competidores = []
		for j in range(cantidad):
			p = proba[j]
			com = {'Nombre': self.factory.unique.name(), 'Probabilidad': p}
			competidores.append(com)
		competidores[0]["Nombre"] = ""	
		resultado = self.logica.validar_crear_editar_carrera(nombre, competidores)
		self.assertIn("500", resultado)

	def test_10_nuevo_competidor_con_probabilidad_mayor_a_uno(self):
		nombre = self.factory.unique.name()
		cantidad = int(random.randint(3,5))
		proba = self.genera_probabilidad(cantidad)
		competidores = []
		for j in range(cantidad):
			p = proba[j]
			com = {'Nombre': self.factory.unique.name(), 'Probabilidad': p}
			competidores.append(com)
		competidores[0]["Probabilidad"] = round(random.uniform(1.1,1.5),1)	
		resultado = self.logica.validar_crear_editar_carrera(nombre, competidores)
		self.assertIn("500", resultado)

	def test_11_nuevo_competidor_repetido(self):
		nombre = self.factory.unique.name()
		cantidad = int(random.randint(3,5))
		proba = self.genera_probabilidad(cantidad)
		competidores = []
		for j in range(cantidad):
			p = proba[j]
			com = {'Nombre': self.factory.unique.name(), 'Probabilidad': p}
			competidores.append(com)
		competidores[0]["Nombre"] = competidores[1]["Nombre"]
		resultado = self.logica.validar_crear_editar_carrera(nombre, competidores)
		self.assertIn("500", resultado)

	def test_12_crear_carrera_datos_correctos(self):
		nombre = self.factory.unique.name()
		cantidad = int(random.randint(3,5))
		proba = self.genera_probabilidad(cantidad)
		competidores = []
		for j in range(cantidad):
			p = proba[j]
			com = {'Nombre': self.factory.unique.name(), 'Probabilidad': p}
			competidores.append(com)

		resultado = self.logica.validar_crear_editar_carrera(nombre, competidores)
		self.assertEqual(resultado,"")
		self.logica.crear_carrera(nombre)
		for c in competidores:
			self.logica.aniadir_competidor(-1,c["Nombre"],c["Probabilidad"])

		carrera = self.session.query(Carrera).filter(Carrera.Nombre == nombre).first()
		self.assertEqual(carrera.dar_nombre(), nombre)

	def test_13_dar_apostadores_ordenados(self):
		self.llenarApostadores()
		esperado = sorted(self.apostadores, key=lambda apostador: apostador['Nombre'])
		resultado = self.logica.dar_apostadores()
		self.assertEqual(esperado, resultado)

	def test_14_crear_apostador_nombre_vacio(self):
		resultado = self.logica.validar_crear_editar_apostador("")
		self.assertIn("500", resultado)

	def test_15_crear_apostador_nombre_largo(self):
		nombre = self.factory.unique.name() * 10
		resultado = self.logica.validar_crear_editar_apostador(nombre)
		self.assertIn("500", resultado)

	def test_16_crear_apostador_con_nombre_repetido(self):
		self.llenarApostadores()
		self.logica.dar_apostadores()
		nombre = self.apostadores[0]["Nombre"]
		resultado = self.logica.validar_crear_editar_apostador(nombre)
		self.assertIn("500", resultado)

	def test_17_crear_apostador_correctamente(self):
		self.llenarApostadores()
		self.logica.dar_apostadores()
		nombre = self.factory.unique.name() 
		resultado = self.logica.validar_crear_editar_apostador(nombre)
		self.assertIn("", resultado)
		self.logica.aniadir_apostador(nombre)
		apostador = self.session.query(Apostador).filter(Apostador.Nombre == nombre).first()
		self.assertEqual(apostador.dar_nombre(), nombre)

	def test_18_dar_apuestas_ordenadas(self):
		self.llenarApuestas()
		id = random.randint(0,self.total_carreras-1)
		self.carreras = sorted(self.carreras, key=lambda carrera: carrera['Nombre'])
		nombre = self.carreras[id]["Nombre"]
		apuestas = []
		for apt in self.carreras_apuestas:
			if(apt["Carrera"] == nombre):
				apuestas = apt["Apuestas"]
		apuestas =  sorted(apuestas, key=lambda apostador: apostador['Apostador'])
		self.logica.dar_carreras()
		resultado = self.logica.dar_apuestas_carrera(id)
		self.assertEqual(apuestas, resultado)

	def test_19_crear_apuesta_con_valor_cero(self):
		valor = 0
		apostador = self.apostadores[random.randint(0,self.total_apostadores-1)]["Nombre"]
		carrera = random.randint(0,self.total_carreras-1)
		competidor = self.carreras[carrera]["Competidores"][0]["Nombre"]
		resultado = self.logica.validar_crear_editar_apuesta(apostador, carrera, valor, competidor)
		self.assertIn("500", resultado)

	def test_20_crear_apuesta_sin_apostador(self):
		valor = random.randint(100,1000)
		apostador = ""
		carrera = random.randint(0,self.total_carreras-1)
		competidor = self.carreras[carrera]["Competidores"][0]["Nombre"]
		resultado = self.logica.validar_crear_editar_apuesta(apostador, carrera, valor, competidor)
		self.assertIn("500", resultado)

	def test_21_crear_apuesta_sin_competidor(self):
		valor = random.randint(100,1000)
		apostador = self.apostadores[random.randint(0,self.total_apostadores-1)]["Nombre"]
		carrera = random.randint(0,self.total_carreras-1)
		competidor = ""		
		resultado = self.logica.validar_crear_editar_apuesta(apostador, carrera, valor, competidor)
		self.assertIn("500", resultado)

	def test_22_crear_apuesta_en_carrera_terminada(self):
		self.llenarApuestas()
		id_carrera = random.randint(0,self.total_carreras-1)
		valor = random.randint(100,1000)
		apostador = self.apostadores[random.randint(0,self.total_apostadores-1)]["Nombre"]
		competidor = self.carreras[id_carrera]["Competidores"][0]["Nombre"]

		self.logica.dar_carreras()
		self.logica.carreras[id_carrera].Abierta = False
		self.logica.dar_carrera(id_carrera)
		resultado = self.logica.validar_crear_editar_apuesta(apostador, id_carrera, valor, competidor)
		self.assertIn("500", resultado)

	def test_23_crear_apuesta_con_datos_correctos(self):
		self.llenarApuestas()
		valor = random.randint(100,1000)
		apostador = self.apostadores[random.randint(0,self.total_apostadores-1)]["Nombre"]
		id_carrera = random.randint(0,self.total_carreras-1)
		self.carreras = sorted(self.carreras, key=lambda carrera: carrera['Nombre'])
		carrera = self.carreras[id_carrera]
		competidores = sorted(carrera['Competidores'], key=lambda competidor: competidor['Nombre'])
		competidor = competidores[0]["Nombre"]
		resultado = self.logica.validar_crear_editar_apuesta(apostador, carrera, valor, competidor)
		self.assertIn("", resultado)
		apuesta = {"Apostador": apostador, "Valor": valor, "Competidor":competidor}
		self.logica.dar_carrera(id_carrera)
		self.logica.crear_apuesta(apostador, id_carrera, valor, competidor)

		apuestas = []
		for apt in self.carreras_apuestas:
			if(apt["Carrera"] == carrera["Nombre"]):
				apuestas = apt["Apuestas"]
		apuestas.append(apuesta)
		apuestas =  sorted(apuestas, key=lambda apostador: apostador['Apostador'])

		resultado = self.logica.dar_apuestas_carrera(id_carrera)
		self.assertEqual(apuestas, resultado)

	def test_24_eliminar_carrera(self):
		self.llenarCarreras()
		self.carreras = sorted(self.carreras, key=lambda carrera: carrera['Nombre'])
		for carrera in self.carreras:
			carrera['Competidores'] = sorted(carrera['Competidores'], key=lambda competidor: competidor['Nombre'])

		id_eliminar = random.randint(0,self.total_carreras-1)
		self.logica.dar_carreras()
		self.logica.carreras[id_eliminar].apuestas.clear()
		self.logica.eliminar_carrera(id_eliminar)
		self.carreras.pop(id_eliminar)
		resultado = self.logica.dar_carreras()
		self.assertEqual(self.carreras, resultado)

	def test_25_generar_reporte(self):
		self.llenarApuestas()
		carreras = sorted(self.carreras, key=lambda carrera: carrera['Nombre'])
		id_carrera = random.randint(0,self.total_carreras-1)
		carrera = carreras[id_carrera]
		carrera['Competidores'] = sorted(carrera['Competidores'], key=lambda competidor: competidor['Nombre'])
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

		self.logica.dar_carreras()
		self.logica.dar_carrera(id_carrera)
		resultado = self.logica.dar_reporte_ganancias(id_carrera, id_ganador)
		self.assertEqual(resultado, esperado)

	def test_26_editar_apuesta_con_datos_correctos(self):
		self.llenarApuestas()
		self.logica.dar_carreras()
		self.logica.dar_apostadores()

		carreras = sorted(self.carreras, key=lambda carrera: carrera['Nombre'])
		id_carrera = random.randint(0,self.total_carreras-1)
		carrera = carreras[id_carrera]
		carrera['Competidores'] = sorted(carrera['Competidores'], key=lambda competidor: competidor['Nombre'])
		apuestas = []
		for apt in self.carreras_apuestas:
			if(apt["Carrera"] == carrera["Nombre"]):
				apuestas = apt["Apuestas"]
		apuestas =  sorted(apuestas, key=lambda apostador: apostador['Apostador'])

		id_apuesta = random.randint(0, len(apuestas)-1)
		valor = random.randint(100,900)
		apuestas[id_apuesta]["Valor"] = valor
		apostador = apuestas[id_apuesta]["Apostador"]
		competidor = apuestas[id_apuesta]["Competidor"]
		resultado = self.logica.validar_crear_editar_apuesta(apostador, id_carrera, valor, competidor)
		self.assertIn("", resultado)

		self.logica.dar_carrera(id_carrera)
		self.logica.editar_apuesta(id_apuesta, apostador, id_carrera, valor, competidor)
		resultado = self.logica.dar_apuestas_carrera(id_carrera)

		self.assertEqual(apuestas, resultado)

	def test_27_eliminar_apuesta(self):
		self.llenarApuestas()
		id_carrera = random.randint(0, self.total_carreras - 1)
		self.carreras = sorted(self.carreras, key=lambda carrera: carrera['Nombre'])
		apuestas = self.logica.dar_apuestas_carrera(id_carrera)
		id_apuesta = random.randint(0, len(apuestas) - 1)
		self.logica.eliminar_apuesta(id_carrera, id_apuesta)
		apuestas.pop(id_apuesta)

		resultado = self.logica.dar_apuestas_carrera(id_carrera)
		self.assertEqual(apuestas, resultado)

	def test_28_eliminar_competidor(self):
		self.llenarCarreras()
		self.logica.dar_carreras()

		self.assertGreater(len(self.logica.carreras), 0)
		id_carrera = random.randint(0, len(self.logica.carreras) - 1)
		self.logica.carrera_actual = self.logica.carreras[id_carrera]
		competidores = self.logica.dar_competidores_carrera(id_carrera)
		self.assertGreater(len(competidores), 0)
		id_competidor = random.randint(0, len(competidores) - 1)
		self.logica.eliminar_competidor(id_carrera, id_competidor)
		competidores.pop(id_competidor)
		self.logica.editar_carrera(id_carrera, self.logica.carrera_actual.dar_nombre())
		resultado = self.logica.dar_competidores_carrera(id_carrera)
		self.assertEqual(competidores, resultado)

	def test_29_editar_carrera(self):
		self.llenarCarreras()
		self.logica.dar_carreras()
		carrera_id = 0
		self.logica.dar_carrera(carrera_id)
		faker = Faker()
		nuevo_nombre = faker.word()

		resultado = self.logica.editar_carrera(carrera_id, nuevo_nombre)
		self.assertIsNone(resultado)

		carrera_actualizada = self.logica.dar_carrera(carrera_id)
		self.assertEqual(carrera_actualizada['Nombre'], nuevo_nombre)

	def test_30_editar_competidor(self):
		self.llenarCarreras()
		self.carreras = sorted(self.carreras, key=lambda carrera: carrera['Nombre'])
		id_carrera = random.randint(0,self.total_carreras-1)
		carrera = self.carreras[id_carrera]
		competidores = sorted(carrera['Competidores'], key=lambda competidor: competidor['Nombre'])
		
		id_competidor = random.randint(0,len(competidores)-1)
		nombre = self.factory.unique.name()
		competidores[id_competidor]["Nombre"] = nombre
		probabilidad = competidores[id_competidor]["Probabilidad"]
		competidores = sorted(carrera['Competidores'], key=lambda competidor: competidor['Nombre'])

		carrera["Competidores"] = competidores
		self.logica.dar_carreras()
		self.logica.editar_competidor(id_carrera, id_competidor, nombre, probabilidad)
		resultado = self.logica.dar_carrera(id_carrera)
		self.assertEqual(carrera, resultado)

	def test_31_editar_apostador(self):
		self.llenarApostadores()
		self.apostadores = sorted(self.apostadores, key=lambda nombre: nombre['Nombre'])
		id = random.randint(0,self.total_apostadores-1)
		nombre = self.factory.unique.name()
		self.apostadores[id]["Nombre"] = nombre
		self.apostadores = sorted(self.apostadores, key=lambda nombre: nombre['Nombre'])
		self.logica.dar_apostadores()
		self.logica.editar_apostador(id,nombre)
		resultado = self.logica.dar_apostadores()
		self.assertEqual(self.apostadores, resultado)

	def test_32_eliminar_apostador(self):
		self.llenarApostadores()
		self.apostadores = sorted(self.apostadores, key=lambda nombre: nombre['Nombre'])
		id = random.randint(0,self.total_apostadores-1)
		self.logica.dar_apostadores()
		self.logica.eliminar_apostador(id)
		self.apostadores.pop(id)
		resultado = self.logica.dar_apostadores()
		self.assertEqual(self.apostadores, resultado)
	
	def test_33_dar_apuesta(self):
		self.llenarApuestas()
		self.logica.dar_carreras()
		self.logica.dar_apostadores()

		carreras = sorted(self.carreras, key=lambda carrera: carrera['Nombre'])
		id_carrera = random.randint(0,self.total_carreras-1)
		carrera = carreras[id_carrera]
		apuestas = []
		for apt in self.carreras_apuestas:
			if(apt["Carrera"] == carrera["Nombre"]):
				apuestas = apt["Apuestas"]
		apuestas =  sorted(apuestas, key=lambda apostador: apostador['Apostador'])

		id_apuesta = random.randint(0, len(apuestas)-1)
		apuesta = apuestas[id_apuesta]
		resultado = self.logica.dar_apuesta(id_carrera,id_apuesta)

		self.assertEqual(apuesta, resultado)

