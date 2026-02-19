from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import multiprocessing
import pyaudio
import numpy as np
import time

from tools.light_effects import waterfall
from tools.manage_light import RGBController
from tools import manage_light

app = FastAPI()

music_process: Optional[multiprocessing.Process] = None
is_listening = False

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ColorData(BaseModel):
    array1: List[str]
    array2: List[str]
    array3: List[str]


def run_music_analysis():
    CHUNK = 4096
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    DEVICE_INDEX = 1

    try:
        p = pyaudio.PyAudio()

        controller = RGBController()
        devices = controller.find_device()
        if len(devices) > 3:
            first_device = devices[3]
            controller.open_device(first_device['vendor_id'], first_device['product_id'])
        else:
            print("Не найдено устройство для управления светом")
            return

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=DEVICE_INDEX,
                        frames_per_buffer=CHUNK)

        print("Музыкальный анализ запущен")

        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            value = np.max(np.abs(audio_data))
            level = value // 1000
            if level > 0:
                waterfall(controller, level)

    except Exception as e:
        print(f"Ошибка в музыкальном анализе: {e}")
    finally:
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        if 'p' in locals():
            p.terminate()


@app.post("/set/")
async def set_color(data: ColorData):
    manage_light.sendCommand(data.array1, data.array2, data.array3)
    return {"status": "success"}


@app.post("/listen-music/")
async def listen_music():
    global music_process, is_listening

    try:
        if music_process and music_process.is_alive():
            print("Останавливаем текущий музыкальный анализ...")
            music_process.terminate()
            music_process.join(timeout=5)

            if music_process.is_alive():
                music_process.kill()
                music_process.join()

            music_process = None
            is_listening = False
            return {"status": "stopped", "message": "Музыкальный анализ остановлен"}

        print("Запускаем музыкальный анализ...")
        music_process = multiprocessing.Process(target=run_music_analysis, daemon=True)
        music_process.start()
        is_listening = True

        time.sleep(1)

        if music_process.is_alive():
            return {"status": "started", "message": "Музыкальный анализ запущен"}
        else:
            raise Exception("Процесс не запустился")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при управлении музыкальным анализом: {str(e)}")


@app.get("/music-status/")
async def music_status():
    global music_process, is_listening

    if music_process and music_process.is_alive():
        return {"status": "running", "message": "Музыкальный анализ активен"}
    else:
        music_process = None
        is_listening = False
        return {"status": "stopped", "message": "Музыкальный анализ не активен"}


@app.post("/stop-music/")
async def stop_music():
    global music_process, is_listening

    if music_process and music_process.is_alive():
        music_process.terminate()
        music_process.join(timeout=5)

        if music_process.is_alive():
            music_process.kill()
            music_process.join()

        music_process = None
        is_listening = False
        return {"status": "stopped", "message": "Музыкальный анализ остановлен"}

    return {"status": "not_running", "message": "Музыкальный анализ не был запущен"}


@app.on_event("shutdown")
def shutdown_event():
    global music_process
    if music_process and music_process.is_alive():
        print("Завершаем музыкальный анализ...")
        music_process.terminate()
        music_process.join(timeout=5)