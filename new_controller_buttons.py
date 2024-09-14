import threading
import sys
import keyboard
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
from gpiozero import Button
from signal import pause

class MediaPlayerController:
    def __init__(self):
        self.player_iface = None
        self.transport_prop_iface = None
        self.key_pressed = [""]

    def on_property_changed(self, interface, changed, invalidated):
        if interface != 'org.bluez.MediaPlayer1':
            return
        for prop, value in changed.items():
            if prop == 'Status':
                print('Playback Status: {}'.format(value))
            elif prop == 'Track':
                print('Music Info:')
                for key in ('Title', 'Artist', 'Album'):
                    print('   {}: {}'.format(key, value.get(key, '')))

    def media_thread(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        dbus.mainloop.glib.threads_init()
        bus = dbus.SystemBus()

        obj = bus.get_object('org.bluez', "/")
        iface = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')

        # Buscar las interfaces necesarias
        for path, ifaces in iface.GetManagedObjects().items():
            if 'org.bluez.MediaPlayer1' in ifaces:
                self.player_iface = dbus.Interface(
                    bus.get_object('org.bluez', path),
                    'org.bluez.MediaPlayer1'
                )
            elif 'org.bluez.MediaTransport1' in ifaces:
                self.transport_prop_iface = dbus.Interface(
                    bus.get_object('org.bluez', path),
                    'org.freedesktop.DBus.Properties'
                )

        if not self.player_iface:
            sys.exit('Error: Media Player not found.')
        if not self.transport_prop_iface:
            sys.exit('Error: DBus.Properties iface not found.')

        # Registrar el receptor de señales
        bus.add_signal_receiver(
            self.on_property_changed,
            bus_name='org.bluez',
            signal_name='PropertiesChanged',
            dbus_interface='org.freedesktop.DBus.Properties'
        )

        # Iniciar el bucle principal de GLib
        loop = GLib.MainLoop()
        loop.run()

    def keyboard_thread(self):
        
        
        play_button = Button(2)
        next_button = Button(4)
        # prev_button = Button(3)

        play_button.when_pressed = fun
        next_button.when_pressed = fun
        # prev_button.when_pressed 

        pause()
        while True:

            key_input = keyboard.read_key()

            if key_input == "a":
                self.key_pressed[0] = "a"
                print("Tecla 'a' presionada")
            elif key_input == "b":
                self.key_pressed[0] = "b"
                print("Tecla 'b' presionada")
            elif key_input == "esc":
                print("Tecla 'esc' presionada, saliendo...")
                break

    def monitor_keypress(self):
        while True:
            if self.key_pressed[0] == "a":
                if self.player_iface:
                    self.player_iface.Next()
                # Simulating a signal emission
                attributes = self.transport_prop_iface.GetAll('org.bluez.MediaTransport1')
                self.on_property_changed("org.bluez.MediaPlayer1", attributes, {})
                self.key_pressed[0] = ""

# Instantiate the controller class
controller = MediaPlayerController()

# Start media player DBus thread
dbus_thread = threading.Thread(target=controller.media_thread)
dbus_thread.start()

# Start keyboard thread
keyboard_thread = threading.Thread(target=controller.keyboard_thread)
keyboard_thread.start()

# Start monitoring for keypress actions
controller.monitor_keypress()
