from cajero import Cajero
import os
import time
import sys



def main():
    USERS = {
    0:{"nombre": "jesus", "apellido": "huamani", "contraseña": "123456", "intentos":0, "saldo":10_000},
    1:{"nombre": "alfredo", "apellido": "escobar", "contraseña": "1925", "intentos":3, "saldo":10_000},
    2:{"nombre": "victor", "apellido": "wilber", "contraseña": "0395", "intentos":3, "saldo":5}
    }

    
    
    NuevoBank = Cajero(USERS, efectivo_inicial = 200_000) #Inicializar Cajero con usuarios y efectivo
    nombre_usuario:tuple
    contrasenia:str

    MENU_OPERACION = ('1', '2', '3')
    
    #OPERACIONES_EJECUTABLES:dict[str, function] = {NuevoBank.depositar, NuevoBank.retirar}

    while True:  #Loop Principal
        #Cuando no hay una sesion activa
        if not NuevoBank.id_sesion_activa:
            mostrar_separacion()
            # mensaje_bienvenida()   #Entregable 2
            #Entregable 1
            modo = mensaje_bienvenida()
            if modo == '2':
                mostrar_separacion()
                nombre_usuario = obtener_nombre()
                contrasenia = obtener_contrasenia()
                saldo = obtener_saldo_inicial()
                if saldo is None:
                    continue
                try:
                     if NuevoBank.registrar_usuario(nombre_usuario, saldo, contrasenia):
                         print("Nuevo Usuario Registrado Correctamente!")
                except Cajero.LimiteDeUsuarios:
                    mostrar_separacion()
                    print("Se llegó al limite de usuarios registados.")
                except Cajero.MontoInvalido as e :
                    mostrar_separacion()
                    print(e.causa)
                finally:
                    delay(0.5)
            elif modo == '1':
                mostrar_separacion()
                nombre_usuario = obtener_nombre()
                contrasenia = obtener_contrasenia()
                try:
                    NuevoBank.iniciar_sesion(nombre_usuario, contrasenia)
                except Cajero.UsuarioNoRegistrado:
                    mostrar_separacion()
                    print("Nombre o Apellido no registrados, intente nuevamente.")
                except Cajero.MaximosIntentos:
                    mostrar_separacion()
                    print("Ha agotado el numero máximo de intentos por día.\n"
                        "Vuelva a intentarlo en 24 horas")
                except Cajero.ConstraseniaIncorrecta as e:
                    mostrar_separacion()
                    print(f"La contraseña que ha ingresado es incorrecta, le quedan {e.intentos_restantes} intentos")
                finally:
                    delay(0.5)
                 
        #Si existe una sesion activa
        elif NuevoBank.id_sesion_activa:
            operacion_seleccionada = mostrar_menu_principal(NuevoBank) #Seleccionar opcion del menu principal
            #Obtener monto y ejecutar operacion
            if operacion_seleccionada == '1':#depositar
                monto = obtener_monto_deposito()
                if monto is None:
                    continue
                try:
                    if NuevoBank.depositar(monto_a_depositar=monto):
                        print("Operación Realizada Correctamente!")
                except Cajero.MontoInvalido as e:
                    print(e.causa)
                finally:
                    delay(0.5)

            elif operacion_seleccionada == '2':#retirar
                monto = obtener_monto_retiro()
                if monto is None:
                    continue
                try:
                    if NuevoBank.retirar(monto_a_retirar=monto):
                        print("Operación Realizada Correctamente!")
                except Cajero.MontoInvalido as e:
                    print(e.causa)
                finally:
                    delay(0.5)
            elif operacion_seleccionada == '3':
                NuevoBank.cerrar_sesion()
                delay(0.5)

           





def mensaje_bienvenida():
    print("Bienvenido al Cajero Automático de Nuevo Perú Bank.")
    os.system("pause")
    #Entregable 1
    print("Seleccione un modo de uso:\n"
          "1. Iniciar Sesión.\n"
          "2. Registrar Nuevo Usuario")
    modo = input().strip()
    return modo


#entregable 1
def obtener_saldo_inicial():
    return obtener_monto("de saldo inicial")

    



def obtener_nombre() -> tuple:
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    return (nombre, apellido)




def obtener_contrasenia() -> str:
    return input("Contraseña: ")




"""Muestra las opciones principales al usuario.
    Devuelve el numero de operación seleccionada como un str"""
def mostrar_menu_principal( cajero_activo: Cajero): 
        mostrar_separacion()
        
        #print menu principal
        print(f"Hola {cajero_activo.usuario_activo['nombre'].capitalize()} {cajero_activo.usuario_activo['apellido'].capitalize()}."
                f"\nSu saldo es: s/. {cajero_activo.usuario_activo['saldo']}\n")
        print("Ingrese el Número de Operacion que desea realizar:\n\n\n"
                '1: Depositar.\n'
                "2: Retirar.\n"
                '3: Cerrar Sesión.')
        
        #obtener una opcion del menu principal
        opciones = ["1", "2", "3"]
        opcion_seleccionada = 'foo'
        while opcion_seleccionada not in opciones:
            opcion_seleccionada = input().strip().upper()
            if opcion_seleccionada not in opciones:
                mensaje_entrada_invalida_temporal("Opción incorrecta. Intente Nuevamente.")
        return opcion_seleccionada
        


"""Obtiene del usuario un monto valido a depostiar.
   Se considera un monto valido un numero natural"""
def obtener_monto_deposito() -> int:
    return obtener_monto('a depositar')


"""Obtiene del usuario un monto valido a depostiar.
   Se considera un monto valido un numero natural"""
def obtener_monto_retiro() -> int:
    return obtener_monto("a retirar")


def obtener_monto(mensaje_operacion:str) -> int:
    monto = None
    mostrar_separacion()
    print("Ingrese 'X' para volver al menú anterior.\n\n")
    while monto is None:
        try:
            monto = input(f"Ingrese el monto {mensaje_operacion}: ")
            monto = int(monto)
            if monto <= 0:
                mensaje_entrada_invalida_temporal("El valor ingresado es negativo. Ingrese un número positivo")
                monto = None            
        except ValueError:
            if monto.lower() == 'x':
                return None
            mensaje_entrada_invalida_temporal("No ingresó un valor numérico. Intente nuevamente.")
            monto = None    
    return monto


"""Se usa luego de un input() de opcion que devolvio una opcion invalida.
    Borra el prompt del input(), imprime el mensaje de error y, luego de un tiempo, borra el mensaje de error"""
def mensaje_entrada_invalida_temporal(mensaje:str, tiempo:float=2):
    sys.stdout.write("\033[F") # Cursor up one line
    sys.stdout.write("\033[K") # limpiar prompt
    print(mensaje)
    sys.stdout.write("\033[F")
    time.sleep(tiempo)
    sys.stdout.write("\033[K") # limpiar mensaje



        
""". . . """
def delay(intervalo:float):
    for j in range(3):
        print(" . ",end="", flush=True)
        time.sleep(intervalo)
    print()


"""====================="""
def mostrar_separacion():
     print(50*"=")
        
     



if __name__ == '__main__':
    main()