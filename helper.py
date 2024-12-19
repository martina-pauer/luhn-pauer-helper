#!/usr/bin/python3

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


def sumar_digitos(numero:int) -> int:
    '''
        Suma digitos del numero
    '''
    if (numero < 9):
        return numero
    else:
        return (sumar_digitos(numero // 10) + (numero % 10))

def luhn(numero:str) -> dict:
    '''
        Aplica algoritmo de Luhn\npatente US-2950048A.\n\nA partir de texto con numero, devuelve un diccionario\ncon todos los resultados de aplicar algoritmo de Luhn\n\n claves de accesos:\n\t[valido, digito_de_control, suma_de_verificacion, formula_de_verificacion].
    '''
    # Conversion por si pasan un numero, codigo malicioso u otra cosa distinta a cadena
    numero = str(numero)
    # Paso 1: Obtiene numero de control, primer digito del numero
    digito_de_control = int(numero[0])
    # Paso 2: Por cada uno de los digitos sobrantes de ultimo a primero
    #         multiplicar digitos para obtener resultados menores a 9

    suma_de_verificacion = 0

    for digito in numero[::-1]:
        # Realizo conversion de tipos
        digito = int(digito)
        # Procedo con algoritmo en sí
        if ((numero.index(digito.__str__()) % 2) != 0):
            digito *= 2
        else:
            digito *= 1
        # Suma digitos del numero
        digito = sumar_digitos(digito)
        # Paso 3: Sumar cada resultado a variable externa "suma_de_verificacion" al ciclo
        suma_de_verificacion += digito
    # Paso 4: Uso suma para verificar con la diferencia de 10 y resto entre suma y 10
    formula_de_verificacion = (10 - (suma_de_verificacion % 10))
    # Debe dar digito de control y devuelvo como una lista para enriquecer la informacion que brinda
    return {
                'valido' : f'¿Numero de Luhn Valido? {(formula_de_verificacion == digito_de_control)}',
                'control' : f'Digito de control (check digit): {digito_de_control}',
                'verificacion' : f'Suma de Verificacion: {suma_de_verificacion}',
                'formula' : f'Diferencia entre 10 y resto de dividir Suma de Verificacion y 10: {formula_de_verificacion}'
            }

class Helper(Gtk.Window):

    def __init__(self):
        # Inicializa ventana

        super().__init__(title = 'Luhn Helper: Validador De Números')

        self.set_size_request(500, 500)

        # Defino widgets a usar

        self.contenedor = Gtk.VBox(spacing = 190)

        self.etiqueta_para_entrada = Gtk.Label(label = 'Validar número usando algoritmo de Luhn:')

        self.entrada = Gtk.Entry()
        # Conecto evento para caundo cambia texto en entrada
        self.entrada.connect('changed', self.cambia_entrada)
        # Conecto evento para cuando se cierra la ventana
        self.connect('delete-event', Gtk.main_quit)
        # Creo salida con el resultado de la validaacion del numero en entrada
        self.salida = Gtk.Label(label = 'Dice si el número es valido o dice\ncual podría ser el valido más cercano.')

        # Agrego widgets al contenedor

        self.contenedor.add(self.etiqueta_para_entrada)

        self.contenedor.add(self.entrada)

        self.contenedor.add(self.salida)

        # Agrego contenedor a ventana

        self.add(self.contenedor)

    # Eventos
    def cambia_entrada(self, widget):
        '''
            Evento para validar cada vez que cambia la entrada.
        '''
        if (self.entrada.get_text() == ''):
            # En caso de vaciar entrada
            return None

        resultado = ''
        # Variable de salida de validacion en diccionario
        texto = luhn(self.entrada.get_text())
        # Voy iterando sobre cada salida
        for clave in texto.keys():
            # Sumo posible salida a resultado con algoritmo de Luhn
            resultado += f'\t{texto[clave.__str__()].__str__()}\t\n\n'
        # Elimino variable que no necesito por seguridad y rendimiento
        del texto
        # Actualizo salida
        self.salida.set_text(resultado)

    def ventana_cerrada(self, widget):
        '''
            Evento finalizar ventana cuando se cierra.
        '''
        pass

if __name__ == '__main__':
    # Creo objeto que instancia ventana Helper de validador Luhn
    validador = Helper()
    # Manejador de excepciones para mostrar o cerrar ventana
    try:
        # Digo que muestre todo
        validador.show_all()
        Gtk.main()
        # Muestro ventana
    except:
        # Cierro ventana
        validador.close()
        # Libero memoria
        del luhn, sumar_digitos, validador, Helper
