from cajero import Cajero


USERS = [
    {"id":0,"nombre": "jesus", "apellido": "huamani", "contraseña": "123456", "intentos":3, "saldo":10_000},
    {"id":1, "nombre": "alfredo", "apellido": "escobar", "contraseña": "1925", "intentos":3, "saldo":500 },
    {"id":2, "nombre": "victor", "apellido": "wilber", "contraseña": "0395", "intentos":3, "saldo": 50}]


NuevoBank = Cajero(USERS, 200_000)

while True:
    if not NuevoBank.sesion_activa:
        NuevoBank.mensaje_bienvenida()
        NuevoBank.iniciar_sesion()
    if NuevoBank.sesion_activa:
        NuevoBank.mostrar_menu_principal()

