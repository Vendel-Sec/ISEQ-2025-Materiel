#!/usr/bin/env python3
import serial
from serial.tools.list_ports import comports


def is_ascii(data: bytes):
    """Cette fonction retourne True si tous les éléments du tableau sont des caractères ASCII valides"""
    return all(32 <= c <= 126 or c in (9, 10, 13) for c in data)


def bruteforce_baudrate(port: str, baudrates: list[int]) -> int:
    """Cette fonction itère sur un tableau de baudrates et retourne celui qui est valide pour un port donné"""
    for baudrate in baudrates:
        print(f"Essai du baudrate {baudrate}")
        try:
            # Ouvre une connexion au port série avec le baudrate
            with serial.Serial(port=port, baudrate=baudrate, timeout=0.2) as ser:
                # TODO: tester si le baudrate est le bon
                # Indice: utiliser la fonction is_ascii
                # Pour envoyer des donnees:
                # ser.write(b"data")
                # Pour lire 100 octets:
                # data = ser.read(100)
                response = None
                if False: # Remplacer False par votre condition
                    print(f"Réponse valide détectée pour le baudrate {baudrate}: {response}")
                    return baudrate
        except Exception as e:
            print(f"Erreur lors du test du baudrate {baudrate}: {e}")
    return -1


if __name__ == "__main__":
    # Remplacez avec le chemin vers votre port série
    serial_port = "/dev/ttyACM0"
    if not serial_port in [p[0] for p in comports()]:
        print(f"Port série {serial_port} introuvable")
        exit(1)
    
    # Les baudrates à tester
    baudrates = []

    # TODO: ajouter des baudrates potentiels au tableau de baudrates
    # baudrates.append(MAVALEUR)
    
    detected_baudrate = bruteforce_baudrate(serial_port, baudrates)
    if detected_baudrate != -1:
        print(f"Baudrate détecté: {detected_baudrate}")
    else:
        print("Impossible de trouver un baudrate valide")
