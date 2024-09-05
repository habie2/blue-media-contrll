import dbus
import time

def get_bluetooth_metadata():
    try:
        # Conectar al sistema bus y bluez
        bus = dbus.SystemBus()
        player_path = "/org/bluez/hci0/dev_8C_86_1E_5F_FA_8B/player2"
        proxy = bus.get_object("org.bluez", player_path)
        iface = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")

        # Obtener el diccionario de metadatos
        metadata = iface.GetAll("org.bluez.MediaPlayer1")
        
        # Extraer metadatos relevantes
        title = metadata.get("Track", {}).get("Title", "Desconocido")
        album = metadata.get("Track", {}).get("Album", "Desconocido")
        artist = metadata.get("Track", {}).get("Artist", "Desconocido")
        position = metadata.get("Position", 0)
        duration = metadata.get("Track", {}).get("Duration", 0)

        return title, album, artist, position, duration
    except dbus.DBusException as e:
        print(f"Error al obtener metadatos: {e}")
        return None, None, None, None, None

def hex_to_time(hex_str):
    """Convierte un valor hexadecimal a minutos y segundos."""
    # Convertir el hexadecimal a un valor decimal
    # print(hex_str)
    # print(type(hex_str))
    # milliseconds = int(hexV_str, 16)

    # Convertir milisegundos a segundos
    total_seconds = hex_str / 1000

    # Calcular minutos y segundos
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    return f"{minutes:02}:{seconds:02}"
 
def format_metadata(title, album, artist, position, duration):
    formatted_output = (
        f"🎵  Reproduciendo Ahora en tu Móvil\n"
        f"-----------------------------------\n"
        f"Canción: {title if title else 'Desconocida'}\n"
        f"Álbum: {album if album else 'Desconocido'}\n"
        f"Artista: {artist if artist else 'Desconocido'}\n"
        f"Tiempo: {hex_to_time(position) if position else '00:00'} / {hex_to_time(duration) if duration else '00:00'}\n"
    )
    return formatted_output

def main():
    while True:
        # Obtener los metadatos actuales
        # title, album, artist, position, duration = get_metadata()
        title, album, artist, position, duration = get_bluetooth_metadata()
         
        print(format_metadata(title, album, artist, position, duration))



        # Esperar 
        time.sleep(0.5)


if __name__ == "__main__":
    main()