import threading
import sys
import keyboard
import dbus
import dbus.mainloop.glib
from gi.repository import GLib

def on_property_changed(interface, changed, invalidated):
    if interface != 'org.bluez.MediaPlayer1':
        return
    for prop, value in changed.items():
        if prop == 'Status':
            print('Playback Status: {}'.format(value))
        elif prop == 'Track':
            print('Music Info:')
            for key in ('Title', 'Artist', 'Album'):
                print('   {}: {}'.format(key, value.get(key, '')))

def media_thread(signal_received: list):
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    dbus.mainloop.glib.threads_init()       # TODO: revisar si esto puede servir 
    bus = dbus.SystemBus()
    
    obj = bus.get_object('org.bluez', "/")
    iface = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
    global player_iface
    player_iface = None
    global transport_prop_iface
    transport_prop_iface = None

    # Buscar las interfaces necesarias
    for path, ifaces in iface.GetManagedObjects().items():
        if 'org.bluez.MediaPlayer1' in ifaces:
            player_iface = dbus.Interface(
                bus.get_object('org.bluez', path),
                'org.bluez.MediaPlayer1'
            )
        elif 'org.bluez.MediaTransport1' in ifaces:
            transport_prop_iface = dbus.Interface(
                bus.get_object('org.bluez', path),
                'org.freedesktop.DBus.Properties'
            )

    if not player_iface:
        sys.exit('Error: Media Player not found.')
    if not transport_prop_iface:
        sys.exit('Error: DBus.Properties iface not found.')

    # Registrar el receptor de señales
    bus.add_signal_receiver(
        on_property_changed,
        bus_name='org.bluez',
        signal_name='PropertiesChanged',
        dbus_interface='org.freedesktop.DBus.Properties'
    )

    # while True:
    #     if key_pressed[0] == "a":
    #         player_iface.Next()
    #         # TODO: arreglar esto!!!
    #         attributes = transport_prop_iface.GetAll('org.bluez.MediaTransport1')
    #         on_property_changed("org.bluez.MediaPlayer1", attributes, {})
    #         key_pressed[0] = ""
    
    
    
    # Iniciar el bucle principal de GLib
    loop = GLib.MainLoop()
    loop.run()

def keyboard_thread(key_pressed: list):
    while True:
        key_input = keyboard.read_key()
            
        if key_input == "a":
            key_pressed[0] = "a"
            print("Tecla 'a' presionada")
        elif key_input == "b":
            key_pressed[0] = "b"
            print("Tecla 'b' presionada")
        elif key_input == "esc":
            print("Tecla 'esc' presionada, saliendo...")
            break


signal_received = [False]
key_pressed = [""]

dbus_thread = threading.Thread(target=media_thread, args=(signal_received, ))
dbus_thread.start()
keyboard_thread = threading.Thread(target=keyboard_thread, args=(key_pressed, ))

keyboard_thread.start()


while True:
    if key_pressed[0] == "a":
        player_iface.Next()
        # TODO: arreglar esto!!!
        attributes = transport_prop_iface.GetAll('org.bluez.MediaTransport1')
        on_property_changed("org.bluez.MediaPlayer1", attributes, {})
        key_pressed[0] = ""
