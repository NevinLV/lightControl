import hid
import time
from typing import List

def convert_hex_array(hex_strings):
    """Конвертация массив строк hex в массив целых чисел."""
    result = []
    for hex_str in hex_strings:
        if hex_str.startswith('0x'):
            num = int(hex_str[2:], 16)
        else:
            num = int(hex_str, 16)
        result.append(num)
    return result

class RGBController:
    def __init__(self, vid: int = None, pid: int = None):
        """
        Инициализация контроллера RGB-подсветки
        """
        self.vid = vid
        self.pid = pid
        self.device = None
        self.packet_counter = 0x1e

    def find_device(self):
        """Поиск HID-устройств"""
        devices = hid.enumerate()

        if not devices:
            print("Устройства не найдены!")
            return None

        return devices

    def open_device(self, vid: int = None, pid: int = None, path: str = None):
        """
        Открытие устройства
        """
        if vid:
            self.vid = vid
        if pid:
            self.pid = pid

        self.device = hid.device()

        try:
            if path:
                self.device.open_path(path)
            elif self.vid and self.pid:
                self.device.open(self.vid, self.pid)
            else:
                return False

            return True

        except Exception as e:
            print(f"Ошибка при открытии устройства: {e}")
            return False

    def calculate_checksum(self, r: int, g: int, b: int) -> int:
        """
        Расчет контрольной суммы
        """
        checksum = (r ^ g ^ b) & 0xFF

        if r == 255 and g == 0 and b == 0:
            checksum = 0xb3
        elif r == 0 and g == 255 and b == 0:
            checksum = 0xb6

        return checksum

    def send_color(self, arr1: List[str], arr2: List[str], arr3: List[str]):
        if not self.device:
            return

        _packet = bytearray(64)
        _packet2 = bytearray(64)
        _packet3 = bytearray(64)

        try:
            p1 = arr1
            p2= arr2
            p3= arr3

            _packet = bytes(convert_hex_array(p1))
            _packet2 = bytes(convert_hex_array(p2))
            _packet3 = bytes(convert_hex_array(p3))

            packet_with_id = b'\x00' + _packet
            packet_with_id2 = b'\x00' + _packet2
            packet_with_id3 = b'\x00' + _packet3

            self.device.write(packet_with_id)
            self.device.write(packet_with_id2)
            self.device.write(packet_with_id3)

        except Exception as e:
            print(f"✗ Ошибка при отправке: {e}")


    def send_bytes_color(self, arr1, arr2, arr3):
        if not self.device:
            print("Устройство не открыто")
            return

        _packet = bytearray(64)
        _packet2 = bytearray(64)
        _packet3 = bytearray(64)

        try:
            p1 = arr1
            p2= arr2
            p3= arr3

            _packet = p1
            _packet2 = p2
            _packet3 = p3

            packet_with_id = b'\x00' + _packet
            packet_with_id2 = b'\x00' + _packet2
            packet_with_id3 = b'\x00' + _packet3

            self.device.write(packet_with_id)
            time.sleep(0.1)
            self.device.write(packet_with_id2)
            time.sleep(0.1)
            self.device.write(packet_with_id3)
            time.sleep(0.1)

        except Exception as e:
            print(f"✗ Ошибка при отправке: {e}")


    def color_cycle(self, duration: float = 0.5, steps: int = 10):
        """Плавный переход между цветами"""

        for i in range(steps + 1):
            r = int(255 * (1 - i / steps))
            g = int(255 * (i / steps))
            b = 0
            print(f"\nШаг {i}/{steps}: RGB({r}, {g}, {b})")
            self.send_color(r, g, b)
            time.sleep(duration)

        for i in range(steps + 1):
            r = 0
            g = int(255 * (1 - i / steps))
            b = int(255 * (i / steps))
            print(f"\nШаг {i}/{steps}: RGB({r}, {g}, {b})")
            self.send_color(r, g, b)
            time.sleep(duration)

        for i in range(steps + 1):
            r = int(255 * (i / steps))
            g = 0
            b = int(255 * (1 - i / steps))
            print(f"\nШаг {i}/{steps}: RGB({r}, {g}, {b})")
            self.send_color(r, g, b)
            time.sleep(duration)

    def close(self):
        """Закрытие устройства"""
        if self.device:
            self.device.close()


def sendCommand(arr1: List[str], arr2: List[str], arr3: List[str]):
    controller = RGBController()

    try:
        devices = controller.find_device()

        if devices:
            first_device = devices[3]

            if controller.open_device(first_device['vendor_id'], first_device['product_id']):
                    try:
                        controller.send_color(arr1, arr2, arr3)
                    except Exception as e:
                        print(f"Ошибка: {e}")

    except KeyboardInterrupt:
        print("\n\nПрограмма остановлена пользователем")
    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        controller.close()

def sendByteCommand(arr1, arr2, arr3):
    controller = RGBController()

    try:
        devices = controller.find_device()

        if devices:
            first_device = devices[3]

            if controller.open_device(first_device['vendor_id'], first_device['product_id']):
                    try:
                        controller.send_color(arr1, arr2, arr3)
                    except Exception as e:
                        print(f"Ошибка: {e}")

    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        controller.close()
