import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import sys

from old.song_info_display import on_property_changed
from old.key_management import on_key_press



if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    dbus.mainloop.glib.threads_init()       # TODO: revisar si esto puede servir 
    bus = dbus.SystemBus()
    
    obj = bus.get_object('org.bluez', "/")
    iface = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
    player_iface = None
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

    
    
    # Iniciar el bucle principal de GLib
    loop = GLib.MainLoop()
    loop.run()
