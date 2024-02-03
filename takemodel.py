import cv2
from time import strftime
from pynput import keyboard

# Inisialisasi kamera
camera = cv2.VideoCapture(0)  # Ganti 0 dengan indeks kamera jika Anda memiliki lebih dari satu kamera

photo_counter = 1  # Inisialisasi counter foto

# Fungsi callback ketika huruf "p" ditekan
def on_press(key):
    try:
        # Jika huruf "p" ditekan
        if key.char == 'p':
            # Ambil frame dari kamera
            ret, frame = camera.read()

            # Simpan frame sebagai gambar
            photo_filename = '/home/pipod/Desktop/Project/Model/Korban_{}.jpg'.format(strftime('%Y%m%d%H%M%S'))
            cv2.imwrite(photo_filename, frame)

            print("Photo captured: {}".format(photo_filename))
    except AttributeError:
        pass

# Mendeklarasikan listener keyboard
listener = keyboard.Listener(on_press=on_press)

try:
    # Mulai mendengarkan keyboard
    listener.start()

    while True:
        # Tampilkan frame dalam bentuk live preview (opsional)
        ret, frame = camera.read()
        cv2.imshow('Live Preview', frame)
        cv2.waitKey(1)

except KeyboardInterrupt:
    # Tangkap KeyboardInterrupt (Ctrl+C) dan hentikan eksekusi program
    print("\nPhoto capture stopped by user.")

finally:
    # Pastikan untuk melepas kamera dan menutup jendela tampilan (jika ada)
    camera.release()
    cv2.destroyAllWindows()

    # Hentikan listener
    listener.stop()
    listener.join()