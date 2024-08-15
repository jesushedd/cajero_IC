import os
import time

class Cajero:

    def __init__(self,usuarios_actuales: dict[int, dict], max_usuarios:int = 10,  efectivo_inicial: float = 100_000):
        self.__efectivo_Disponible: float = efectivo_inicial
        self.__usuarios_registrados: dict[int, dict] = usuarios_actuales
        self.__limite_de_usuarios:int = max_usuarios
        self.id_sesion_activa:int = None
        self.__datos_usuario_activo:dict = None
        self.usuario_activo: dict[str,str]
        self.__ultimo_id:int = len(self.__usuarios_registrados) - 1

    

    def iniciar_sesion(self, in_usuario:tuple, in_contrasenia:str):
        
        #identificar usuario por nombre y apellido
        id_usuario:int = None
        identificado:bool
        nombre = in_usuario[0]
        apellido = in_usuario[1]
        contrasenia = in_contrasenia
        for id, datos in self.__usuarios_registrados.items():
            identificado = True
            identificado = identificado and (nombre == datos['nombre'])
            identificado = identificado and (apellido == datos["apellido"])
            #si se encontro al usuario, se guarda el id, que es usado como key del dicccionario de usuarios registrados
            if identificado:
                id_usuario = id
                break
        
        
        if id_usuario is None:
            raise Cajero.UsuarioNoRegistrado
        
        if self.__usuarios_registrados[id_usuario]['intentos'] == 0:
            raise Cajero.MaximosIntentos
        
        #si el id usuario eesta registrado ,comparar contraseña
        if contrasenia != self.__usuarios_registrados[id_usuario]['contraseña']:
            self.__usuarios_registrados[id_usuario]['intentos'] -= 1  #restar un intento 
            raise Cajero.ConstraseniaIncorrecta(self.__usuarios_registrados[id_usuario]['intentos'])

        #se autoriza al usuario e inicia sesion
        if contrasenia == self.__usuarios_registrados[id_usuario]['contraseña']:
            #restablecer intentos
            self.__usuarios_registrados[id_usuario]['intentos'] = 3
            #guardar el id del usuario en la sesion activa
            self.id_sesion_activa = id_usuario
            self.__datos_usuario_activo = self.__usuarios_registrados[id_usuario]
            #Actualizar datos q es visible para la ui
            self.usuario_activo = dict()
            self.usuario_activo['nombre'] = self.__datos_usuario_activo['nombre']
            self.usuario_activo['apellido'] = self.__datos_usuario_activo['apellido']
            self.usuario_activo['saldo'] = self.__datos_usuario_activo['saldo']
            return
        
        
    """Deposita un monto al usuario activo, si se tiene exito retorna True"""
    def depositar(self, monto_a_depositar:int):
        
        if (self.__datos_usuario_activo is None) or (self.id_sesion_activa is None):
            raise Cajero.SesionNoIniciada
        
        if monto_a_depositar <= 0:
            raise Cajero.MontoInvalido("Monto inferior o igual a 0.")
        
        else:
            self.__datos_usuario_activo['saldo'] += monto_a_depositar
            self.__efectivo_Disponible += monto_a_depositar
            #Actualizar saldo q es visible para la ui
            self.usuario_activo['saldo'] = self.__datos_usuario_activo['saldo']
            return True
            
        
    """Retira un monto del usuario activo, si se tiene exito retorna True"""
    def retirar(self, monto_a_retirar:int):
        if (self.__datos_usuario_activo is None) or (self.id_sesion_activa is None):
            raise Cajero.SesionNoIniciada
        
        if monto_a_retirar <= 0:
            raise Cajero.MontoInvalido("Monto inferior o igual a 0.")
        
        if monto_a_retirar > self.__efectivo_Disponible:
            raise Cajero.MontoInvalido("No hay suficiente efectivo disponible en el cajero. Pase al siguiente Cajero.")
        else:
            self.__datos_usuario_activo['saldo'] -= monto_a_retirar
            self.__efectivo_Disponible -= monto_a_retirar
            #Actualizar saldo q es visible para la ui
            self.usuario_activo['saldo'] = self.__datos_usuario_activo['saldo']
            return True


    def cerrar_sesion(self):
        if (self.__datos_usuario_activo is None) or (self.id_sesion_activa is None):
            raise Cajero.SesionNoIniciada
        self.__datos_usuario_activo = None
        self.id_sesion_activa = None
        del self.usuario_activo 

    #Entregable 1
    def registrar_usuario(self, nombre_apellido:tuple, saldo_inicial:int, contrasenia:str):
        if len(self.__usuarios_registrados) >= self.__limite_de_usuarios:
            raise Cajero.LimiteDeUsuarios
        if type(saldo_inicial) != int:
            raise Cajero.MontoInvalido("El saldo inicial ingresado no es un número")
        self.__ultimo_id += 1
        self.__usuarios_registrados[self.__ultimo_id] = {'nombre': nombre_apellido[0], 
                                                        'apellido': nombre_apellido[1],
                                                        'contraseña': contrasenia, 
                                                        'saldo': saldo_inicial, 
                                                        'intentos': 3}
        return True
        

    class LimiteDeUsuarios(Exception):
        "Si ya se alcanzo el maximo numero de usuarios registrados"
        pass

    class SesionNoIniciada(Exception):
        "No se ha iniciado sesion de ningun usuario registrado"
        pass

    class UsuarioNoRegistrado(Exception):
        "El nombre y apellido ingresados no se encuentran registrados."
        pass

    class MaximosIntentos(Exception):
        "Se ha agotado el numero maximo de intentos al iniciar sesion del usuario"
        pass

    class ConstraseniaIncorrecta(Exception):
        "La contraseña ingresada no coincide con la registrada por el usuario"
        def __init__(self, intentos) -> None:
            self.intentos_restantes = intentos

    class MontoInvalido(Exception):
        "El monto seleccionado es invalido"
        def __init__(self, causa:str) -> None:
            self.causa = causa


    

                
    



        
                
            




        













