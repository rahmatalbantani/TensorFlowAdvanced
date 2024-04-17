import cv2
import numpy as np
import serial
import time
# Inisialisasi Serial Communication
import serial.tools.list_ports


def find_serial_port(vendor_id, product_id, baudrate=9600):
    """Mencari port serial berdasarkan vendor ID dan product ID."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == vendor_id and port.pid == product_id:
            beforeser = serial.Serial(port.device, baudrate)
            return beforeser
    return None

# Vendor ID dan Product ID dari perangkat Anda
vendor_id = 0x2e8a
product_id = 0x000a

# Mencari port serial yang terhubung dengan perangkat yang memiliki VID dan PID yang sesuai
ser = find_serial_port(vendor_id, product_id)

if ser:
    print(f"Perangkat ditemukan di port serial: {ser.port}")
    # Lanjutkan dengan komunikasi serial seperti yang Anda lakukan sebelumnya
else:
    print("Perangkat tidak ditemukan.")
ser.flushInput()  # Bersihkan buffer masukan

time.sleep(2)  # Tunggu agar koneksi serial stabil

MARGIN = 10  # pixels
ROW_SIZE = 30  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (0, 0, 0)  # black

last_send_time = time.time()  # Waktu terakhir data dikirim

send_interval = 0.1  # Interval pengiriman data (dalam detik)

def extract_detection_info(detection):
    """Extracts category name, x center, and y center from a detection entity."""
    if hasattr(detection, 'categories') and detection.categories:
        category_name = detection.categories[0].category_name
    else:
        category_name = "Unknown"

    if hasattr(detection.bounding_box, 'origin_x') and hasattr(detection.bounding_box, 'origin_y') and \
            hasattr(detection.bounding_box, 'width') and hasattr(detection.bounding_box, 'height'):
        x_center = int((detection.bounding_box.origin_x + detection.bounding_box.width / 2))
        y_center = int((detection.bounding_box.origin_y + detection.bounding_box.height / 2))
        confidence_score = detection.categories[0].score
    else:
        x_center = -1
        y_center = -1
        confidence_score = 0.0
    
    return category_name, x_center, y_center, confidence_score

def send_serial_data(data):
    """Send data over Serial."""
    try:
        ser.write(data.encode())
        print("Data terkirim:", data)
        return True
    except Exception as e:
        print("Error sending data over Serial:", e)
        return False

def visualize(image, detection_result) -> np.ndarray:
    global last_send_time
    """Draws bounding boxes on the input image and return it."""
    for detection in detection_result.detections:
        category_name, x_center, y_center, confidence_score = extract_detection_info(detection)
        print("Category: {}, Center X: {}, Center Y: {}, Confidence: {}".format(category_name, x_center, y_center, confidence_score))
        
        # Only send data if the category is "korban"
        current_time = time.time()
        if current_time - last_send_time >= send_interval:
            last_send_time = current_time
            if category_name == "korban":
                data_to_send = f"{x_center}\n"  # Format data yang ingin dikirim
                send_serial_data(data_to_send)


        # Draw bounding_box
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        # Use the orange color for high visibility.
        cv2.rectangle(image, start_point, end_point, (255, 0, 255), 3)
        # Draw a circle on the image if the center coordinates are valid
        cv2.circle(image, (x_center, y_center), radius=10, color=(0, 255, 0), thickness=-1)

        # Draw label and score
        category = detection.categories[0]
        category_name = category.category_name
        probability = round(category.score, 2)
        result_text = category_name + ' (' + str(probability) + ')'
        text_location = (MARGIN + bbox.origin_x, MARGIN + ROW_SIZE + bbox.origin_y)
        cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_DUPLEX,
                    FONT_SIZE, TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

    return image
