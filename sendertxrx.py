import serial
import time

# Inisialisasi objek Serial dengan port dan baudrate yang sesuai
serial_port = serial.Serial('/dev/ttyACM0', 9600)  # Ubah '/dev/ttyACM0' sesuai dengan port Arduino Anda
time.sleep(2)  # Tunggu beberapa saat agar koneksi serial terbuka

try:
    while True:
        # Kirim data ke Arduino
        data_to_send = "123\n"  # Ubah sesuai dengan data yang ingin Anda kirim
        serial_port.write(data_to_send.encode())

        # Tunggu sebentar sebelum mengirim data lagi
        time.sleep(1)

except KeyboardInterrupt:
    # Tangani jika pengguna menekan Ctrl+C untuk keluar dari program
    serial_port.close()  # Tutup koneksi serial saat program berakhir
    print("Program dihentikan. Koneksi serial ditutup.")
