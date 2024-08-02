import os
import platform
from LaboratorioPooVentas import *

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')  # Para Linux/Unix/MacOs

def mostrar_menu():
    print("\n========== Menú de Gestión de Ventas ==========")
    print('1. Registrar nueva venta online')
    print('2. Registrar nueva venta local')
    print('3. Buscar venta por identificador')
    print('4. Actualizar precio de venta')
    print('5. Eliminar venta por identificador')
    print('6. Mostrar todas las ventas')
    print('7. Salir')
    print('======================================================')

def registrar_nueva_venta(gestion, tipo_venta):
    try:
        tienda = input("Ingrese el nombre de la tienda: ")
        marca = input("Ingrese la marca del producto: ")
        tipo_producto = input("Ingrese el tipo de producto: ")
        genero = input("Ingrese el género del producto: ")
        talla = input("Ingrese la talla del producto: ")
        color = input("Ingrese el color del producto: ")
        categoria = input("Ingrese la categoría del producto: ")
        precio = input("Ingrese el precio: ")
        fecha = input("Ingrese la fecha (formato YYYY-MM-DD): ")
        hora = input("Ingrese la hora (formato HH:MM): ")

        if tipo_venta == '1':
            pago_credito = input("Ingrese el monto pagado con tarjeta de crédito: ")
            pago_debito = input("Ingrese el monto pagado con tarjeta de débito: ")
            venta = VentaOnline(tienda, marca, tipo_producto, genero, talla, color, categoria, precio, fecha, hora, pago_credito, pago_debito)
        elif tipo_venta == '2':
            efectivo = input("Ingrese el monto pagado en efectivo: ")
            cheque = input("Ingrese el monto pagado con cheque: ")
            venta = VentaLocal(tienda, marca, tipo_producto, genero, talla, color, categoria, precio, fecha, hora, efectivo, cheque)
        else:
            print('Opción inválida')
            return

        gestion.crear_venta(venta)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_venta_por_identificador(gestion):
    identificador = input('Ingrese el identificador (fecha+hora) de la venta a buscar: ')
    venta = gestion.leer_venta(identificador)
    if venta:
        print(venta)
    input('Presione enter para continuar...')

def actualizar_precio_venta(gestion):
    identificador = input('Ingrese el identificador (fecha+hora) de la venta para actualizar el precio: ')
    nuevo_precio = input('Ingrese el nuevo precio de la venta: ')
    gestion.actualizar_venta(identificador, nuevo_precio)
    input('Presione enter para continuar...')

def eliminar_venta_por_identificador(gestion):
    identificador = input('Ingrese el identificador (fecha+hora) de la venta a eliminar: ')
    gestion.eliminar_venta(identificador)
    input('Presione enter para continuar...')

def mostrar_todas_las_ventas(gestion):
    print('=============== Listado completo de las Ventas ===============')
    gestion.mostrar_todas_las_ventas()
    print('=============================================================')
    input('Presione enter para continuar...')

if __name__ == "__main__":
    archivo_ventas = 'ventas_db.json'
    gestion = GestionVentas(archivo_ventas)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            registrar_nueva_venta(gestion, opcion)

        elif opcion == '3':
            buscar_venta_por_identificador(gestion)

        elif opcion == '4':
            actualizar_precio_venta(gestion)

        elif opcion == '5':
            eliminar_venta_por_identificador(gestion)

        elif opcion == '6':
            mostrar_todas_las_ventas(gestion)

        elif opcion == '7':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-7)')
