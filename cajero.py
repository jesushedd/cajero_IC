import os
import time

class Cajero:

    def __init__(self,usuarios: list[dict], efectivo_inicial: float =100_000):
        self.efectivo_Disponible: float = efectivo_inicial
        self.usuarios: list[dict] = usuarios
        self.__usuario_activo = None
        self.sesion_activa = False

    def mensaje_bienvenida(self):
        print("Bienvenido al Cajero Automático de Nuevo Perú Bank.")
        os.system("pause")

    def iniciar_sesion(self):
        while not self.__usuario_activo:
            nombre = input("Escriba su nombre: ")
            apellido = input("Escriba su apellido: ")
            #identificar usuario
            id_usuario:dict
            identificado:bool
            for user in self.usuarios:
                identificado = True
                identificado = identificado and (nombre == user["nombre"])
                identificado = identificado and (apellido == user["apellido"])
                if identificado:
                    id_usuario = user
                    break
            
            #si el id de usuario es correcto ,pedir contraseña
            if not identificado:
                print("Usuario no registrado, ingrese su nombre y apellido nuevamente")
                continue
            while (id_usuario['intentos'] != 0) and  (not self.sesion_activa):
                
                contrasenia = input("Ingrese su contraseña: ")
                if contrasenia == id_usuario["contraseña"]:
                    self.__usuario_activo = id_usuario
                    self.sesion_activa = True
                    id_usuario['intentos'] = 3
                    print(f"Bienvenido {self.__usuario_activo["nombre"]} {self.__usuario_activo["apellido"]}")
                    return
                else:
                    id_usuario["intentos"] = id_usuario["intentos"] - 1
                    print(f"Contraseña incorrecta, tiene {id_usuario['intentos']} restantes")
                    
            
            print("Lo sentimos ya agotó sus intentos de inicio de sesión.\n"
                      "Puede volver a intentarlo en 24 horas")
            for j in range(10):
                print(" . ",end="", flush=True)
                time.sleep(1)
            print("")
            return
            

    def mostrar_menu_principal(self)-> str: 
        opciones = ["D", "R", "X"]
        print("Seleccione la Operacion de Deseea Realizar:\n\n\n"
              'Ingrese D para depositar a su cuenta.\n'
              "Ingrese R para retirar de su cuenta.\n"
              'Ingrese X para cerrar la sesión.')
        while True:
            for j in range(10):
                    print(" . ",end="", flush=True)
                    """tecla = input("").strip().upper()
                    if tecla in opciones:
                        return tecla"""
                    time.sleep(0.5)
            print("\r"+10*"   ", end="")
            print("\r", end="")
            
        
        
                
            




        













