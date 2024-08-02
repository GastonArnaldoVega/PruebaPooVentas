import json

class Venta:
    def __init__(self, tienda, marca, tipo, genero, talla, color, categoria, precio, fecha, hora):
        self.__tienda = tienda
        self.__marca = marca
        self.__tipo = tipo
        self.__genero = genero
        self.__talla = talla
        self.__color = color
        self.__categoria = categoria
        self.__precio = self.validar_precio(precio)
        self.__fecha = fecha
        self.__hora = hora

    def validar_precio(self, precio):
        try:
            precio = float(precio)
            if precio <= 0:
                raise ValueError("El precio debe ser un número positivo")
            return precio
        except ValueError:
            raise ValueError("El precio debe ser un número válido")

    @property
    def tienda(self):
        return self.__tienda.capitalize()

    @property
    def marca(self):
        return self.__marca.capitalize()

    @property
    def tipo(self):
        return self.__tipo.capitalize()

    @property
    def genero(self):
        return self.__genero.capitalize()

    @property
    def talla(self):
        return self.__talla

    @property
    def color(self):
        return self.__color.capitalize()

    @property
    def categoria(self):
        return self.__categoria.capitalize()

    @property
    def precio(self):
        return self.__precio

    @property
    def fecha(self):
        return self.__fecha

    @property
    def hora(self):
        return self.__hora

    def to_dict(self):
        return {
            "tienda": self.tienda,
            "marca": self.marca,
            "tipo": self.tipo,
            "genero": self.genero,
            "talla": self.talla,
            "color": self.color,
            "categoria": self.categoria,
            "precio": self.precio,
            "fecha": self.fecha,
            "hora": self.hora
        }

    def __str__(self):
        return f"Venta en {self.tienda} de {self.marca} - Precio: {self.precio}, Fecha: {self.fecha}, Hora: {self.hora}"

class VentaOnline(Venta):
    def __init__(self, tienda, marca, tipo, genero, talla, color, categoria, precio, fecha, hora, pago_credito, pago_debito):
        super().__init__(tienda, marca, tipo, genero, talla, color, categoria, precio, fecha, hora)
        self.__pago_credito = pago_credito
        self.__pago_debito = pago_debito

    @property
    def pago_credito(self):
        return self.__pago_credito

    @pago_credito.setter
    def pago_credito(self, nuevo_pago_credito):
        self.__pago_credito = nuevo_pago_credito

    @property
    def pago_debito(self):
        return self.__pago_debito

    @pago_debito.setter
    def pago_debito(self, nuevo_pago_debito):
        self.__pago_debito = nuevo_pago_debito

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "pago_credito": self.pago_credito,
            "pago_debito": self.pago_debito
        })
        return data

    def __str__(self):
        return super().__str__() + f" - Pago crédito: {self.pago_credito}, Pago débito: {self.pago_debito}"

class VentaLocal(Venta):
    def __init__(self, tienda, marca, tipo, genero, talla, color, categoria, precio, fecha, hora, efectivo, cheque):
        super().__init__(tienda, marca, tipo, genero, talla, color, categoria, precio, fecha, hora)
        self.__efectivo = efectivo
        self.__cheque = cheque

    @property
    def efectivo(self):
        return self.__efectivo

    @efectivo.setter
    def efectivo(self, nuevo_efectivo):
        self.__efectivo = nuevo_efectivo

    @property
    def cheque(self):
        return self.__cheque

    @cheque.setter
    def cheque(self, nuevo_cheque):
        self.__cheque = nuevo_cheque

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "efectivo": self.efectivo,
            "cheque": self.cheque
        })
        return data

    def __str__(self):
        return super().__str__() + f" - Efectivo: {self.efectivo}, Cheque: {self.cheque}"

class GestionVentas:
    def __init__(self, archivo):
        self.archivo = archivo
        self.ventas = self.leer_datos()

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
                ventas = []
                for venta in datos.values():
                    if 'pago_credito' in venta:
                        ventas.append(VentaOnline(**venta))
                    elif 'efectivo' in venta:
                        ventas.append(VentaLocal(**venta))
                    else:
                        ventas.append(Venta(**venta))
                return ventas
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def guardar_datos(self):
        with open(self.archivo, 'w') as file:
            json.dump({venta.fecha + venta.hora: venta.to_dict() for venta in self.ventas}, file, indent=4)

    def crear_venta(self, venta):
        try:
            identificador = venta.fecha + venta.hora
            if identificador not in [v.fecha + v.hora for v in self.ventas]:
                self.ventas.append(venta)
                self.guardar_datos()
                print('Venta registrada exitosamente')
            else:
                print('Ya existe una venta con esa fecha y hora')
        except Exception as error:
            print(f'Error inesperado al crear venta: {error}')

    def leer_venta(self, identificador):
        try:
            for venta in self.ventas:
                if (venta.fecha + venta.hora) == identificador:
                    return venta
            print(f"No se encontró venta con identificador {identificador}.")
        except Exception as error:
            print(f'Error al leer venta: {error}')

    def actualizar_venta(self, identificador, nuevo_precio):
        try:
            for venta in self.ventas:
                if (venta.fecha + venta.hora) == identificador:
                    venta._Venta__precio = venta.validar_precio(nuevo_precio)
                    self.guardar_datos()
                    print(f'Venta con identificador {identificador} actualizada exitosamente.')
                    return
            print(f"No se encontró venta con identificador {identificador}.")
        except Exception as error:
            print(f'Error al actualizar venta: {error}')

    def eliminar_venta(self, identificador):
        try:
            for i, venta in enumerate(self.ventas):
                if (venta.fecha + venta.hora) == identificador:
                    del self.ventas[i]
                    self.guardar_datos()
                    print(f'Venta con identificador {identificador} eliminada exitosamente.')
                    return
            print(f"No se encontró venta con identificador {identificador}.")
        except Exception as error:
            print(f'Error al eliminar venta: {error}')

    def mostrar_todas_las_ventas(self):
        if not self.ventas:
            print("No hay ventas registradas.")
        else:
            for venta in self.ventas:
                print(venta)