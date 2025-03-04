## programa para la gestion proyectos y horas trabajadas ##

import os						# comandos segun sistema operativo
import time						# funcionalidades de tiempo
from datetime import datetime	# funcionalidades de fecha
import sys						# funcionalidades del sistema
import sqlite3					# funcionalidades de SQL
from tabulate import tabulate	# funcionalidades de tablas




###################################################################################################################################
###################################################################################################################################

## funciones de uso ##

# creacion de tablas SQL #
def crear_tablas():
	# crear/conectar a la base de datos #
	conexion = sqlite3.connect("gestion_trabajo.db")
    
	# crear tabla de proyectos #
	conexion.execute("""
		CREATE TABLE IF NOT EXISTS proyectos (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		sigip TEXT NOT NULL,
		nombre TEXT NOT NULL,
		categoria TEXT NOT NULL,
		cliente TEXT NOT NULL,
		lider TEXT NOT NULL,
		estado TEXT NOT NULL
	)
	""")

	# crear tabla de horas #
	conexion.execute("""
		CREATE TABLE IF NOT EXISTS horas (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		fecha TEXT NOT NULL,
		sigip TEXT NOT NULL,
		hora_inicio TEXT NOT NULL,
		hora_fin TEXT NOT NULL,
		horas TEXT NOT NULL
	)
	""")

	conexion.commit()
	conexion.close()


# limpieza de consola #
def limpiar_consola():
	global anio
	global mes
	global dia
	global calendario

	if os.name == 'nt':															# para windows
		os.system('cls')
	else:																		# para unix/linux/mac
		os.system('clear')
	print("\n\t\t\t\t\t\tGestión de trabajo")									# titulo del programa
	print(f'\t\t\t\t\t\t\t\t\t\t     {dia} de {calendario[mes-1]} del {anio}')	# fecha cargada


# pausa del programa #
def pausa(t):
	time.sleep(t)


# error #
def mensaje_error():
	print('\nError de comando. Por favor, inténtelo de nuevo.')


# titulos #
def titulos(titulo):
	global anio
	global mes
	global dia
	global principio_mes

	principio_mes = f'{anio}-{mes}-1'


	# conectar base de datos
	conexion = sqlite3.connect('gestion_trabajo.db')
	cursor = conexion.cursor()
	
	# horas del mes
	cursor.execute('SELECT ROUND(SUM(horas), 2) FROM horas WHERE fecha >= ?',(principio_mes,))
	horas_mes_actual = cursor.fetchone()
	if not horas_mes_actual[0]:
		horas_mes_actual = (0,)
	horas_mes_actual = round(horas_mes_actual[0],2)

	# balance de horas
	cursor.execute('SELECT COUNT(DISTINCT fecha)*8 FROM horas WHERE fecha >= ?',(principio_mes,))
	horas_mes = cursor.fetchone()
	if not horas_mes[0]:
		horas_mes =(0,)
	cursor.execute('SELECT ROUND(SUM(horas), 2) FROM horas WHERE fecha >= ?',(principio_mes,))
	horas_actuales = cursor.fetchone()
	if not horas_actuales[0]:
		horas_actuales = (0,)
	horas_balance_mes_actual = round(horas_actuales[0] - horas_mes[0],2)

	# horas acumuladas
	cursor.execute('SELECT COUNT(DISTINCT fecha)*8 FROM horas')
	horas_mes_totales = cursor.fetchone()
	if not horas_mes_totales[0]:
		horas_mes_totales = (0,)
	cursor.execute('SELECT ROUND(SUM(horas), 2) FROM horas')
	horas_actuales_totales = cursor.fetchone()
	if not horas_actuales_totales[0]:
		horas_actuales_totales = (0,)
	horas_acumuladas = round(horas_actuales_totales[0] - horas_mes_totales[0],2)

	# cerrar conexion
	conexion.close()

	print('-' * 110)
	print(f'\t\t\t\t\t\t\t\t\t\t\ths actuales:\t{horas_mes_actual}')
	print(f'\t\t\t\t\t{titulo}\t\t\t\tbalance mes:\t{horas_balance_mes_actual}')
	print(f'\t\t\t\t\t\t\t\t\t\t\ths acumuladas:\t{horas_acumuladas}')
	print('-' * 110)




###################################################################################################################################
###################################################################################################################################

## funciones del programa ##

# menu principal #
def menu_principal():
	limpiar_consola()
	titulos('Menú principal\t')
	print('1. Horas')
	print('2. Proyectos')
	print('3. Configuraciones')
	print('|. Salir')
	global error

	if error == 1:
		mensaje_error()

	opcion_menu = input('\n\nIngrese una opción (1-3): ')

	match opcion_menu:
		# menu horas
		case '1':
			error = 0
			menu_horas()
		# menu proyectos
		case '2':
			error = 0
			menu_proyectos()
		# configuracion
		case '3':
			error = 0
			configuraciones()
		# salida
		case '|':
			error = 0
			salir()
		#error
		case _:
			error = 1
			menu_principal()


###################################################################################################################################

# horas # 
def menu_horas():
	limpiar_consola()
	titulos('Horas\t\t')
	print('1. Cargar horas')
	print('2. Revisar horas')
	print('3. Modificar horas')
	print('4. Eliminar horas')
	print('|. Volver al menu principal')
	global error
	
	if error == 1:
		mensaje_error()

	opcion_menu = input('\n\nIngrese una opción (1-4): ')

	match opcion_menu:
		# cargar horas
		case '1':
			error = 0
			cargar_horas()
		# revisar horas
		case '2':
			error = 0
			revisar_horas()
		# modificar horas
		case '3':
			error = 0
			modificar_horas()
		# eliminar horas
		case '4':
			error = 0
			eliminar_horas()
		# menu principal
		case '|':
			error = 0
			menu_principal()
		#error
		case _:
			error = 1
			menu_horas()


# cargar horas #
def cargar_horas():
	limpiar_consola()
	titulos('Cargar horas\t')
	global anio
	global mes
	global dia

	fecha = f'{anio}-{mes}-{dia}'
	h_fecha = datetime(anio, mes, dia)

	# ingreso de datos
	sigip = input('Ingrese el SIGIP del proyecto (dejar vacio para cancelar): ')
	if sigip:
		# conectar base de datos
		conexion = sqlite3.connect('gestion_trabajo.db')
		cursor = conexion.cursor()
		# verificar existencia de sigip
		cursor.execute('SELECT * FROM proyectos WHERE sigip = ?', (sigip,))
		resultado = cursor.fetchall()
		if resultado:
			# ingreso de horas
			hora_inicio = input('Ingrese la hora de inicio (HH:MM): ')
			hora_fin = input('Ingrese la hora de fin (HH:MM): ')

			# calculo de horas
			h_inicio = datetime.combine(h_fecha, datetime.strptime(hora_inicio,"%H:%M").time())
			h_fin = datetime.combine(h_fecha, datetime.strptime(hora_fin,"%H:%M").time())
			horas = round((h_fin - h_inicio).seconds/3600, 2)

			# insertar datos en tabla horas
			cursor.execute('INSERT INTO horas (fecha, sigip, hora_inicio, hora_fin, horas) VALUES (?, ?, ?, ?, ?)', (fecha, sigip, hora_inicio, hora_fin, horas))
			# confirmar insercion
			conexion.commit()
			# cerrar conexion
			conexion.close()

			print('\nHoras cargadas correctamente.')
			pausa(2)
			menu_principal()

		else:
			# cerrar conexion
			conexion.close()
			print('\nNo se encuentra el proyecto seleccionado.')
			pausa(2)
			menu_principal()
	else:
		menu_principal()


# revisar horas #
def revisar_horas():
	limpiar_consola()
	titulos('Revisar horas\t')
	print('1. Horas del mes')
	print('2. Horas totales')
	print('|. Volver al menú anterior')
	global error
	
	if error == 1:
		mensaje_error()

	opcion_menu = input('\n\nIngrese una opción (1-2): ')

	match opcion_menu:
		# horas del mes
		case '1':
			error = 0
			revisar_horas_mes()
		# total de horas
		case '2':
			error = 0
			revisar_horas_totales()
		# menu horas
		case '|':
			error = 0
			menu_horas()
		#error
		case _:
			error = 1
			revisar_horas()


# horas del mes #
def revisar_horas_mes():
	limpiar_consola()
	titulos('Horas del mes\t')
	global anio
	global mes
	global dia
	global principio_mes

	# conectar base de datos
	conexion = sqlite3.connect('gestion_trabajo.db')
	cursor = conexion.cursor()
	# recuperar registros tabla horas
	cursor.execute('SELECT * FROM horas WHERE fecha >= ?',(principio_mes,))
	resultados = cursor.fetchall()
	encabezados = ['Fecha', 'SIGIP', 'Nombre', 'Horas']
	fecha_sigip = []
	datos = []
	# verificar si la tabla tiene registros
	if resultados:
		for item in resultados:
			item_fecha_sigip = item[1] + '-' + item[2]
			if not item_fecha_sigip in fecha_sigip:
				fecha_sigip.append(item_fecha_sigip)
				cursor.execute('SELECT ROUND(SUM(horas), 2) FROM horas WHERE fecha = ? AND sigip = ?', (item[1], item[2],))
				item_horas = cursor.fetchone()
				cursor.execute('SELECT nombre FROM proyectos WHERE sigip = ?', (item[2],))
				nombre = cursor.fetchone()
				dato = (item[1], item[2],nombre[0], item_horas[0])
				datos.append(dato)
		print('\n')
		print(tabulate(datos, headers=encabezados, tablefmt='fancy_grid'))
	else:
		print('No se encuentran horas registradas.')
	# cerrar conexión
	conexion.close()

	input('\n\nPresione ENTER para continuar')
	menu_principal()


# horas totales #
def revisar_horas_totales():
	limpiar_consola()
	titulos('Horas totales\t')

	# conectar base de datos
	conexion = sqlite3.connect('gestion_trabajo.db')
	cursor = conexion.cursor()
	# recuperar registros tabla horas
	cursor.execute('SELECT * FROM horas')
	resultados = cursor.fetchall()
	encabezados = ['id', 'Fecha', 'SIGIP', 'Nombre', 'Hora inicio', 'Hora fin', 'Horas']
	datos = []
	# verificar si la tabla tiene registros
	if resultados:
		for registro in resultados:
			cursor.execute('SELECT nombre FROM proyectos WHERE sigip = ?', (registro[2],))
			nombre = cursor.fetchone()
			dato = (registro[0], registro[1], registro[2], nombre[0], registro[3], registro[4], registro[5])
			datos.append(dato)
		print('\n')
		print(tabulate(datos, headers=encabezados, tablefmt='fancy_grid'))
	else:
		print('No se encuentran horas registradas.')
	# cerrar conexión
	conexion.close()

	input('\n\nPresione ENTER para continuar')
	menu_principal()


# modificar horas #
def modificar_horas():
	limpiar_consola()
	titulos('Modificar horas\t')
	global anio
	global mes
	global dia

	h_fecha = datetime(anio, mes, dia)

	# conectar base de datos
	conexion = sqlite3.connect('gestion_trabajo.db')
	cursor = conexion.cursor()
	# solicitar id
	buscador = input('Ingrese el id de las horas a modificar: ')
	limpiar_consola()
	titulos('Modificar horas\t')
	# buscar proyecto
	cursor.execute('SELECT * FROM horas WHERE id = ?', (buscador,))
	resultados = cursor.fetchall()
	encabezados = ['id', 'Fecha', 'SIGIP', 'Hora inicio', 'Hora fin', 'Horas']
	datos = []
	if resultados:
		for registro in resultados:
			dato = (registro[0], registro[1], registro[2], registro[3], registro[4], registro[5])
			datos.append(dato)
		print('\n')
		print(tabulate(datos, headers=encabezados, tablefmt='fancy_grid'))
	else:
		print('\nNo se encuentran las horas seleccionadas.')
		pausa(2)
		# cerrar conexion
		conexion.close()
		menu_principal()
	
	# seleccion de item a modificar
	print('Que valor desea actualizar?')
	print('1. Fecha')
	print('2. SIGIP')
	print('3. Horas')
	print('|. Cancelar')

	opcion_editar = input('\nIngrese una opción (1-3): ')

	match opcion_editar:
		# fecha
		case '1':
			actualizar = input('Ingrese el nuevo valor (AAAA-MM-DD): ')
			# actualizar valor
			cursor.execute("UPDATE horas SET fecha = ? WHERE id = ?", (actualizar, buscador))
		# sigip
		case '2':
			actualizar = input('Ingrese el nuevo valor: ')
			# verificar existencia de sigip
			cursor.execute('SELECT * FROM proyectos WHERE sigip = ?', (actualizar,))
			resultado = cursor.fetchall()
			if resultado:
				# actualizar valor
				cursor.execute("UPDATE horas SET sigip = ? WHERE id = ?", (actualizar, buscador))
			else:
				# cerrar conexion
				conexion.close()
				print('\nNo se encuentra el proyecto seleccionado.')
				pausa(2)
				menu_principal()
		# horas
		case '3':
			# ingreso de horas
			hora_inicio = input('\nIngrese la hora de inicio (HH:MM): ')
			hora_fin = input('Ingrese la hora de fin (HH:MM): ')
			# calculo de horas
			h_inicio = datetime.combine(h_fecha, datetime.strptime(hora_inicio,"%H:%M").time())
			h_fin = datetime.combine(h_fecha, datetime.strptime(hora_fin,"%H:%M").time())
			horas = round((h_fin - h_inicio).seconds/3600, 2)
			# actualizar horas
			cursor.execute("UPDATE horas SET hora_inicio = ? WHERE id = ?", (hora_inicio, buscador))
			cursor.execute("UPDATE horas SET hora_fin = ? WHERE id = ?", (hora_fin, buscador))
			cursor.execute("UPDATE horas SET horas = ? WHERE id = ?", (horas, buscador))
		# cancelar
		case '|':
			# cerrar conexion
			conexion.close()
			menu_principal()
		# error
		case _:
			# cerrar conexion
			conexion.close()
			menu_principal()

	# confirmar insercion
	conexion.commit()
	# cerrar conexion
	conexion.close()
	print('\nHoras modificadas correctamente.')
	pausa(2)
	menu_principal()


# eliminar horas #
def eliminar_horas():
	limpiar_consola()
	titulos('Eliminar horas\t')

	# conectar base de datos
	conexion = sqlite3.connect('gestion_trabajo.db')
	cursor = conexion.cursor()
	# solicitar id
	buscador = input('Ingrese el id de las horas a eliminar: ')
	limpiar_consola()
	titulos('Eliminar horas\t')
	# buscar horas
	cursor.execute('SELECT * FROM horas WHERE id = ?', (buscador,))
	resultados = cursor.fetchall()
	encabezados = ['id', 'Fecha', 'SIGIP', 'Hora inicio', 'Hora fin', 'Horas']
	datos = []
	if resultados:
		for registro in resultados:
			dato = (registro[0], registro[1], registro[2], registro[3], registro[4], registro[5])
			datos.append(dato)
		print('\n')
		print(tabulate(datos, headers=encabezados, tablefmt='fancy_grid'))
	else:
		print('\nNo se encuentran las horas seleccionado.')
		pausa(2)
		# cerrar conexion
		conexion.close()
		menu_principal()
	eliminar = input(f'\nDesea eliminar este registro de horas? (S/N): ')
	ELIMINAR = eliminar.upper()
	if ELIMINAR == 'S':
		# eliminar proyecto
		cursor.execute("DELETE FROM horas WHERE id = ?", (buscador))
		# Guardar los cambios
		conexion.commit()
		# cerrar conexion
		conexion.close()
	else:
		# cerrar conexion
		conexion.close()
		print('\n\nCancelando...')
		pausa(2)
		menu_principal()

	print('\n\nHoras eliminadas correctamente.')
	pausa(2)
	menu_principal()


###################################################################################################################################

# proyectos #
def menu_proyectos():
	limpiar_consola()
	titulos('Proyectos\t')
	print('1. Cargar proyectos')
	print('2. Revisar proyectos')
	print('3. Modificar proyectos')
	print('4. Eliminar proyectos')
	print('|. Volver al menú principal')
	global error
	
	if error == 1:
		mensaje_error()

	opcion_menu = input('\n\nIngrese una opción (1-4): ')

	match opcion_menu:
		# cargar proyectos
		case '1':
			error = 0
			cargar_proyectos()
		# revisar proyectos
		case '2':
			error = 0
			revisar_proyectos()
		# modificar proyectos
		case '3':
			error = 0
			modificar_proyectos()
		# eliminar proyecto
		case '4':
			error = 0
			eliminar_proyectos()
		# menu principal
		case '|':
			error = 0
			menu_principal()
		#error
		case _:
			error = 1
			menu_proyectos()


# cargar proyectos #
def cargar_proyectos():
	limpiar_consola()
	titulos('Cargar proyectos')

	# ingreso de datos
	sigip = input('Ingrese el SIGIP del proyecto (dejar vacio para cancelar): ')
	if sigip:
		nombre = input('Ingrese el nombre del proyecto: ')
		categoria = input('Ingrese la norma del proyecto: ')
		cliente = input('Ingrese el cliente del proyecto: ')
		lider = input('Ingrese el lider del proyecto: ')
		estado = "En cola"

		# conectar base de datos
		conexion = sqlite3.connect('gestion_trabajo.db')
		cursor = conexion.cursor()
		# insertar datos en tabla proyectos
		cursor.execute('INSERT INTO proyectos (sigip, nombre, categoria, cliente, lider, estado) VALUES (?, ?, ?, ?, ?, ?)', (sigip, nombre, categoria, cliente, lider, estado))
		# confirmar insercion
		conexion.commit()
		# cerrar conexion
		conexion.close()

		print('\n\nProyecto cargado correctamente.\n')
		pausa(2)
		menu_principal()
	else:
		menu_principal()


# revisar proyectos #
def revisar_proyectos():
	limpiar_consola()
	titulos('Revisar proyectos')

	# conectar base de datos
	conexion = sqlite3.connect('gestion_trabajo.db')
	cursor = conexion.cursor()
	# recuperar registros tabla proyectos
	cursor.execute('SELECT * FROM proyectos')
	resultados = cursor.fetchall()
	encabezados = ['id', 'SIGIP', 'Nombre', 'Norma', 'Cliente', 'Lider', 'Horas', 'Estado']
	datos = []
	# verificar si la tabla tiene registros
	if resultados:
		for registro in resultados:
			cursor.execute('SELECT ROUND(SUM(horas), 2) FROM horas WHERE sigip = ?', (registro[1],))
			suma_horas = cursor.fetchone()
			dato = (registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], suma_horas[0], registro[6])
			datos.append(dato)
		print('\n')
		print(tabulate(datos, headers=encabezados, tablefmt='fancy_grid'))
	else:
		print('No se encuentran proyectos registrados.')
	# cerrar conexión
	conexion.close()

	input('\n\nPresione ENTER para continuar')
	menu_principal()


# modificar proyecto #
def modificar_proyectos():
	limpiar_consola()
	titulos('Modificar proyectos')
	
	# conectar base de datos
	conexion = sqlite3.connect('gestion_trabajo.db')
	cursor = conexion.cursor()
	# solicitar id
	buscador = input('Ingrese el ID del proyecto: ')
	limpiar_consola()
	titulos('Modificar proyectos')
	# buscar proyecto
	cursor.execute('SELECT * FROM proyectos WHERE id = ?', (buscador,))
	resultados = cursor.fetchall()
	encabezados = ['id', 'SIGIP', 'Nombre', 'Norma', 'Cliente', 'Lider', 'Horas', 'Estado']
	datos = []
	if resultados:
		for registro in resultados:
			cursor.execute('SELECT ROUND(SUM(horas), 2) FROM horas WHERE sigip = ?', (registro[1],))
			suma_horas = cursor.fetchone()
			dato = (registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], suma_horas[0], registro[6])
			datos.append(dato)
		print('\n')
		print(tabulate(datos, headers=encabezados, tablefmt='fancy_grid'))
	else:
		print('\nNo se encuentra el proyecto seleccionado.')
		pausa(2)
		# cerrar conexion
		conexion.close()
		menu_principal()

	# seleccion de item a modificar
	print('Que valor desea actualizar?')
	print('1. SIGIP')
	print('2. Nombre')
	print('3. Norma')
	print('4. Cliente')
	print('5. Lider')
	print('6. Estado')
	print('|. Cancelar')

	opcion_editar = input('\nIngrese una opción (1-6): ')

	match opcion_editar:
		# sigip
		case '1':
			actualizar = input('Ingrese el nuevo valor: ')
			# actualizar valor
			cursor.execute("UPDATE proyectos SET sigip = ? WHERE id = ?", (actualizar, buscador))
		# nombre
		case '2':
			actualizar = input('Ingrese el nuevo valor: ')
			# actualizar valor
			cursor.execute("UPDATE proyectos SET nombre = ? WHERE id = ?", (actualizar, buscador))
		# categoria
		case '3':
			actualizar = input('Ingrese el nuevo valor: ')
			# actualizar valor
			cursor.execute("UPDATE proyectos SET categoria = ? WHERE id = ?", (actualizar, buscador))
		# cliente
		case '4':
			actualizar = input('Ingrese el nuevo valor: ')
			# actualizar valor
			cursor.execute("UPDATE proyectos SET cliente = ? WHERE id = ?", (actualizar, buscador))
		# lider
		case '5':
			actualizar = input('Ingrese el nuevo valor: ')
			# actualizar valor
			cursor.execute("UPDATE proyectos SET lider = ? WHERE id = ?", (actualizar, buscador))
		# estado
		case '6':
			actualizar = input('Ingrese el nuevo valor: ')
			# actualizar valor
			cursor.execute("UPDATE proyectos SET estado = ? WHERE id = ?", (actualizar, buscador))
		# cancelar
		case '|':
			# cerrar conexion
			conexion.close()
			menu_principal()
		# error
		case _:
			# cerrar conexion
			conexion.close()
			menu_principal()

	# confirmar insercion
	conexion.commit()
	# cerrar conexion
	conexion.close()
	print('\nProyecto modificado correctamente.')
	pausa(2)
	menu_principal()


# eliminar proyectos #
def eliminar_proyectos():
	limpiar_consola()
	titulos('Eliminar proyectos')
	
	# conectar base de datos
	conexion = sqlite3.connect('gestion_trabajo.db')
	cursor = conexion.cursor()
	# solicitar id
	buscador = input('Ingrese el ID del proyecto: ')
	limpiar_consola()
	titulos('Eliminar proyectos')
	# buscar proyecto
	cursor.execute('SELECT * FROM proyectos WHERE id = ?', (buscador,))
	resultados = cursor.fetchall()
	encabezados = ['id', 'SIGIP', 'Nombre', 'Norma', 'Cliente', 'Lider', 'Horas', 'Estado']
	datos = []

	if resultados:
		for registro in resultados:
			cursor.execute('SELECT ROUND(SUM(horas), 2) FROM horas WHERE sigip = ?', (registro[1],))
			suma_horas = cursor.fetchone()
			dato = (registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], suma_horas[0], registro[6])
			datos.append(dato)
		print('\n')
		print(tabulate(datos, headers=encabezados, tablefmt='fancy_grid'))
	else:
		print('\nNo se encuentra el proyecto seleccionado.')
		pausa(2)
		# cerrar conexion
		conexion.close()
		menu_principal()

	eliminar = input(f'\nDesea eliminar el proyecto {dato[1]}? (S/N): ')
	ELIMINAR = eliminar.upper()
	if ELIMINAR == 'S':
		# eliminar proyecto
		cursor.execute("DELETE FROM proyectos WHERE id = ?", (buscador))
		# Guardar los cambios
		conexion.commit()
		# cerrar conexion
		conexion.close()
	else:
		# cerrar conexion
		conexion.close()
		print('\n\nCancelando...')
		pausa(2)
		menu_principal()

	print('\n\nProyecto eliminado correctamente.')
	pausa(2)
	menu_principal()	




###################################################################################################################################

# configuraciones #
def configuraciones():
	limpiar_consola()
	titulos('Configuración\t')
	print('1. Modificar día actual')
	print('2. Modificar mes actual')
	print('3. Modificar año actual')
	print('|. Volver al menú principal')
	global error
	
	if error == 1:
		mensaje_error()

	opcion_menu = input('\n\nIngrese una opción (1-3): ')

	match opcion_menu:
		# modificar dia
		case '1':
			error = 0
			modificar_dia()
		# modificar mes
		case '2':
			error = 0
			modificar_mes()
		# modificar año
		case '3':
			error = 0
			modificar_anio()
		# menu principal
		case '|':
			error = 0
			menu_principal()
		# error
		case _:
			error = 1
			configuraciones()


# modificar dia actual #
def modificar_dia():
	limpiar_consola()
	titulos('Modificar día\t')
	global dia


	try:
		dia = int(input('\nIngrese el día actual (DD): '))
		if dia < 1 or dia > 31:
			dia = datetime.now().day
			limpiar_consola()
			titulos('Modificar día\t')
			print("\nEl día debe ser un valor entre 1 y 31")
			pausa(2)
			configuraciones()

	except ValueError:
		dia = datetime.now().day
		limpiar_consola()
		titulos('Modificar día\t')
		print("\nEl día debe ser un valor entre 1 y 31")
		pausa(2)
		configuraciones()
	
	limpiar_consola()
	titulos('Modificar día\t')
	print("\nDía modificado correctamente")
	pausa(2)
	menu_principal()


# modificar mes actual #
def modificar_mes():
	limpiar_consola()
	titulos('Modificar mes\t')
	global mes

	try:
		mes = int(input('\nIngrese el mes actual (MM): '))
		if mes < 1 or mes > 12:
			mes = datetime.now().month
			limpiar_consola()
			titulos('Modificar mes\t')
			print("\nEl mes debe ser un valor entre 1 y 12.")
			pausa(2)
			configuraciones()

	except ValueError:
		mes = datetime.now().month
		limpiar_consola()
		titulos('Modificar mes\t')
		print("\nEl mes debe ser un valor entre 1 y 12.")
		pausa(2)
		configuraciones()

	limpiar_consola()
	titulos('Modificar mes\t')
	print("\nMes modificado correctamente")
	pausa(2)
	menu_principal()


# modificar anio actual #
def modificar_anio():
	limpiar_consola()
	titulos('Modificar año\t')
	global anio

	try:
		anio = int(input('\nIngrese el año actual (AAAA): '))
		if anio < 1900 or anio > 2100:
			anio = datetime.now().year
			limpiar_consola()
			titulos('Modificar año\t')
			print("\nEl año debe ser un valor entre 1900 y 2100")
			pausa(2)
			configuraciones()

	except ValueError:
		anio = datetime.now().year
		limpiar_consola()
		titulos('Modificar año\t')
		print("\nEl año debe ser un valor entre 1900 y 2100")
		pausa(2)
		configuraciones()

	limpiar_consola()
	titulos('Modificar año\t')
	print("\nAño modificado correctamente")
	pausa(2)
	menu_principal()




###################################################################################################################################

# salir #
def salir():
	print('\nSaliendo...')
	pausa(1)
	os.system('cls' if os.name == 'nt' else 'clear')
	sys.exit(0)




###################################################################################################################################
###################################################################################################################################

## programa ##

crear_tablas()

opcion_menu = 0
error = 0

calendario = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

dia = datetime.now().day
mes = datetime.now().month
anio = datetime.now().year

menu_principal()
