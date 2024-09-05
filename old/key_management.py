import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import sys
import os
import keyboard

def on_key_press(source, condition):
    """
    Esta función maneja la entrada del teclado.
    """
    if condition == GLib.IO_IN:
        key = os.read(source, 3)
        if key == b'p':  # 'p' key in bytes
            print("Tecla 'p' presionada")
            player_iface.Play()
        elif key == b'\x1b[A':  # Up arrow in bytes
            print("Flecha arriba presionada")
        elif key == b'\x1b[B':  # Down arrow in bytes
            print("Flecha abajo presionada")
        elif key == b'\x1b':  # ESC key in bytes
            print("Tecla ESC presionada, saliendo...")
            loop.quit()  # Detener el bucle principal de GLib
        return True
    return False



 
while True:
    key = keyboard.read_key()
    
    if key == "a":
        print("Tecla 'a' presionada")
    elif key == "b":
        print("Tecla 'b' presionada")
    elif key == "esc":
        print("Tecla 'esc' presionada, saliendo...")
        break
