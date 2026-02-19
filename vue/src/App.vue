<script setup lang="ts">
import {ref, onMounted, onUnmounted} from 'vue';
import LEDComponent from './components/LEDComponent.vue';
import ComputerComponent from './components/ComputerComponent.vue';
import ColorPicker from './components/ColorPicker.vue';
import { useLedStrip } from './composables/useLedStrip';

const { leds, currentColor, updateLEDColor, resetColors, changleListenMusicStatus } = useLedStrip();

const isMouseDown = ref(false);

const handleMouseDown = () => { isMouseDown.value = true; };
const handleMouseUp = () => { isMouseDown.value = false; };

onMounted(() => {
  document.addEventListener('mousedown', handleMouseDown);
  document.addEventListener('mouseup', handleMouseUp);
});

onUnmounted(() => {
  document.removeEventListener('mousedown', handleMouseDown);
  document.removeEventListener('mouseup', handleMouseUp);
});
</script>

<template>
  <div class="leds-container">
    <div class="left-side">
      <LEDComponent
          v-for="led of leds.slice(40, 53)"
          :id="led.id"
          :color="led.color"
          @update:color="updateLEDColor(led.id)"
          :is-click="isMouseDown"/>
    </div>

    <div class="top-side">
      <LEDComponent
          v-for="led of leds.slice(14, 39).reverse()"
          :id="led.id"
          :color="led.color"
          @update:color="updateLEDColor(led.id)"
          :is-click="isMouseDown"/>
    </div>

    <div class="right-side">
      <LEDComponent
          v-for="led of leds.slice(0, 13).reverse()"
          :id="led.id"
          :color="led.color"
          @update:color="updateLEDColor(led.id)"
          :is-click="isMouseDown"/>
    </div>

    <div class="command">
      <ColorPicker v-model="currentColor"/>
      <button class="command-button bit-button" @click="changleListenMusicStatus()">
        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-music-note" viewBox="0 0 16 16">
          <path d="M9 13c0 1.105-1.12 2-2.5 2S4 14.105 4 13s1.12-2 2.5-2 2.5.895 2.5 2z"/>
          <path fill-rule="evenodd" d="M9 3v10H8V3h1z"/>
          <path d="M8 2.82a1 1 0 0 1 .804-.98l3-.6A1 1 0 0 1 13 2.22V4L8 5V2.82z"/>
        </svg>
      </button>

    </div>

    <ComputerComponent>
      <button class="reload" @click="resetColors()">
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2z"/>
          <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466"/>
        </svg>
      </button>
    </ComputerComponent>
  </div>
</template>

<style scoped>
.command{
  position: absolute;
  display: flex;
  gap: 5px;
  top: 35%;
  left: calc(50% - 140px);

  font-size: 15px;
  padding: 50px;
  transition: 200ms;
  cursor: pointer;
  font-family: sans-serif;
  color: #d1d1d1;
  z-index: 3;
}

.right-side{
  margin-top: 40px;
  width: 50%;
  position: relative;
}

.top-side{
  width: 100%;
  display: flex;
}

.left-side{
  margin-top: 40px;
  width: 50%;
}

.leds-container{
  margin-top: 100px;
  text-align: center;
  display: flex;
  position: relative;
}

.color-picker{
  border-radius: 25%;
  width: 80px;
  height: 80px;
}

.reload{
  margin-top: 20px;
  background-color: rgba(28, 28, 28, 0);
  border: none;
  color: white;
  transition: 200ms;
  cursor: pointer;
}

.reload:hover{
  color: aquamarine;
}

.bit-button{
  background-color: #222222;
  color: white;
}
</style>