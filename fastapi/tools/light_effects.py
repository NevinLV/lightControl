import time
import threading
from tools.manage_light import RGBController

coeff = 3
current_animation = None
last_level = 0
animation_lock = threading.Lock()


def waterfall(controller: RGBController, level: int):
    global current_animation
    global last_level

    if level > last_level:
        stop_event = threading.Event()

        with animation_lock:
            if current_animation:
                current_animation.set()
            current_animation = stop_event

        animation_thread = threading.Thread(
            target=_run_waterfall,
            args=(controller, level, stop_event),
            daemon=True
        )
        animation_thread.start()


def _run_waterfall(controller: RGBController, level: int, stop_event: threading.Event):
    global last_level
    chank1 = []
    chank2 = []
    chank3 = []


    if level > 25:
        level = 25

    for i in range(64):
        chank1.append("0x0")
        chank2.append("0x0")
        chank3.append("0x0")

    chank1[0] = '0x53'
    chank1[1] = '0x43'
    chank1[2] = '0x0'
    chank1[3] = '0xb1'
    chank1[4] = '0x82'
    chank1[5] = '0x80'

    current_level = level
    iteration = 0
    color_iteration = 0

    while current_level >= 0:
        if stop_event.is_set():
            break

        max_color_value = max(255 - color_iteration * 30, 0)
        # print(f'\r{color_iteration}', end="", flush=True)

        chank1[6] = '0x1'
        chank1[7] = number_to_hex_bytes(max_color_value)
        chank1[8] = '0x00'
        chank1[9] = '0x00'

        chank1[10] = number_to_hex_bytes(current_level)

        chank1[11] = number_to_hex_bytes(current_level + 1)
        # if current_level > 10:
        #     chank1[12] = '0xff'
        #     chank1[13] = '0xff'
        #     chank1[14] = '0xff'
        chank1[15] = number_to_hex_bytes(54 - current_level)

        chank1[16] = number_to_hex_bytes(54 - current_level + 1)
        chank1[17] = number_to_hex_bytes(max_color_value)
        chank1[18] = '0x00'
        chank1[19] = '0x00'
        chank1[20] = number_to_hex_bytes(54)

        controller.send_color(chank1, chank2, chank3)

        iteration += 1
        color_iteration += 1
        time.sleep(0.1)
        last_level = current_level
        current_level -= 1


def number_to_hex_bytes(number):
    if number == 0:
        byte_length = 1
    else:
        byte_length = (number.bit_length() + 7) // 8
    bytes_data = number.to_bytes(byte_length, byteorder='big')
    hex_string = ' '.join([f'0x{b:02X}' for b in bytes_data])
    return hex_string