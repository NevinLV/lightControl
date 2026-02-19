import { ref, computed } from 'vue';
import axios from 'axios';
import type { LED } from '../types';

const LED_COUNT = 54;
const CHUNK_SIZE = 64;
const START_CODE = ['53', '43', '0', 'b1', '82', '80'];

export function useLedStrip() {
    const leds = ref<LED[]>([]);
    const currentColor = ref('#ff00ff');
    const isListeningMusic = ref<boolean>(false);

    const initializeLEDs = () => {
        leds.value = Array.from({ length: LED_COUNT }, (_, i) => ({
            id: i,
            color: '#ffffff'
        }));
    };

    initializeLEDs();

    const protocolData = computed(() => {
        const codes: string[] = [];

        for (let i = 0; i < leds.value.length; i += 2) {
            const led1 = leds.value[i];
            const led2 = leds.value[i + 1];

            codes.push((i + 1).toString(16).padStart(2, '0'));
            codes.push(led1?.color.slice(1, 3) ?? "00");
            codes.push(led1?.color.slice(3, 5) ?? "00");
            codes.push(led1?.color.slice(5, 7) ?? "00");
            codes.push((i + 2).toString(16).padStart(2, '0'));
        }

        return [...START_CODE, ...codes].map(code => `0x${code}`);
    });

    const chunkData = (data: string[]): string[][] => {
        const chunks: string[][] = [];

        for (let i = 0; i < data.length; i += CHUNK_SIZE) {
            const chunk = data.slice(i, i + CHUNK_SIZE);
            if (chunk.length < CHUNK_SIZE) {
                const padding = Array(CHUNK_SIZE - chunk.length).fill("0x00");
                chunks.push([...chunk, ...padding]);
            } else {
                chunks.push(chunk);
            }
        }
        return chunks;
    };

    const sendToServer = async (chunks: string[][]) => {
        try {
            await axios.post('http://localhost:8000/set/', {
                array1: chunks[0] || [],
                array2: chunks[1] || [],
                array3: chunks[2] || []
            });
        } catch (error) {
            console.error(error);
        }
    };

    const changleListenMusicStatus = async () => {
        try {
            await axios.post('http://localhost:8000/listen-music/');
        } catch (error) {
            console.error(error);
        }
    };

    const updateLEDColor = async (id: number) => {
        [id, id + 1].forEach(ledId => {
            const led = leds.value.find(l => l.id === ledId);
            if (led) led.color = currentColor.value;
        });

        const chunks = chunkData(protocolData.value);
        await sendToServer(chunks);
    };

    const resetColors = async () => {
        leds.value.forEach(led => {
            led.color = '#ffffff';
        });

        const chunks = chunkData(protocolData.value);
        await sendToServer(chunks);
    };

    const setSingleLED = async (id: number, color: string) => {
        const led = leds.value.find(l => l.id === id);
        if (led) {
            led.color = color;
            const chunks = chunkData(protocolData.value);
            await sendToServer(chunks);
        }
    };

    return {
        leds: leds.value,
        currentColor,
        updateLEDColor,
        resetColors,
        setSingleLED,
        changleListenMusicStatus
    };
}