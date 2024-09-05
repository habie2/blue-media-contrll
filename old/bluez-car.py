import keyboard
import os

def next_track():
    # Este comando depende de la biblioteca específica o API que uses para enviar comandos multimedia
    # os.system("echo 'next track command' | bluetoothctl")
    os.system("playerctl next")

def previous_track():
    # Este comando también depende de la API utilizada para el control de Bluetooth
    # os.system("echo 'previous track command' | bluetoothctl")
    os.system("playerctl previous")

print("Presiona 'n' para la siguiente pista y 'p' para la pista anterior. Presiona 'q' para salir.")

try:
    while True:
        if keyboard.is_pressed('n'):
            next_track()
            print("Siguiente pista")
        elif keyboard.is_pressed('p'):
            previous_track()
            print("Pista anterior")
        elif keyboard.is_pressed('q'):
            print("Saliendo...")
            break
except KeyboardInterrupt:
    pass
