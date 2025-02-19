# Chiffrement de la mémoire flash
Ce dossier contient tous les fichiers requis pour l'exercice sur le chiffrement de la mémoire flash du ESP32.

## Commandes
Voici les commandes qui seront à faire lors de l'exercice.

> [!WARNING]
> Veuillez attendre que les formateurs vous demandent d'entrer les commandes. Une mauvaise utilisation de ces commandes pourrait causer le bris de l'appareil.

```sh
# Ajouter les outils
source ~/esp/esp-idf/export.sh

# Effacer la flash
esptool.py --port /dev/ttyACM0 erase_flash

# Generer la cle de chiffrement
espsecure.py generate_flash_encryption_key flash_encryption_key.bin

# Generer la cle HMAC pour la NVS
export PATH=$PATH:$HOME/esp/esp-idf/components/nvs_flash/nvs_partition_generator
nvs_partition_gen.py generate-key --key_protect_hmac --kp_hmac_keygen --kp_hmac_keyfile hmac_key.bin --keyfile nvs_encr_key.bin

# Bruler les cles
espefuse.py --port /dev/ttyACM0 burn_key BLOCK_KEY0 flash_encryption_key.bin XTS_AES_128_KEY
espefuse.py --port /dev/ttyACM0 burn_key BLOCK_KEY1 keys/hmac_key.bin HMAC_UP

# Activer le chiffrement
espefuse.py --port /dev/ttyACM0 --chip esp32s3 burn_efuse SPI_BOOT_CRYPT_CNT 7

# Extraire l'image binaire
mkdir -p temp
espflash save-image --chip esp32s3 --flash-size 8mb firmware_conf_enc.elf temp/firmware.bin

# Chiffrer les partitions
espsecure.py encrypt_flash_data --aes_xts --keyfile flash_encryption_key.bin --address 0x0 --output temp/bootloader-enc.bin bootloader.bin
espsecure.py encrypt_flash_data --aes_xts --keyfile flash_encryption_key.bin --address 0x8000 --output temp/partition-table-enc.bin partition-table.bin
espsecure.py encrypt_flash_data --aes_xts --keyfile flash_encryption_key.bin --address 0x10000 --output temp/firmware-enc.bin temp/firmware.bin
python ~/esp/esp-idf/components/nvs_flash/nvs_partition_generator/nvs_partition_gen.py encrypt --inputkey keys/nvs_encr_key.bin --key_protect_hmac reponse_ne_pas_regarder/nvs.csv temp/nvs-enc.bin 0x6000

# Ecrire les donnees sur l'appareil
esptool.py --chip esp32s3 --port /dev/ttyACM0 write_flash 0 temp/bootloader-enc.bin 0x8000 temp/partition-table-enc.bin 0x9000 temp/nvs-enc.bin 0x10000 temp/firmware-enc.bin
```