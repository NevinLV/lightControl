<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps<{
  modelValue: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

const colorPickerRef = ref<HTMLInputElement | null>(null);

const openColorPicker = () => {
  colorPickerRef.value?.click();
};

const updateColor = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:modelValue', target.value);
};
</script>

<template>
  <div class="color-picker-container">
    <input
        ref="colorPickerRef"
        type="color"
        :value="props.modelValue"
        @input="updateColor"
        class="color-picker-input"
        aria-label="Выберите цвет"
    >

    <div
        class="color-preview"
        :style="{ backgroundColor: props.modelValue }"
        @click="openColorPicker"
        @keydown.enter="openColorPicker"
        @keydown.space="openColorPicker"
        role="button"
    >
    </div>
  </div>
</template>

<style scoped>
.color-picker-container {
  display: inline-block;
}

.color-picker-input {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
  pointer-events: none;
}

.color-preview {
  width: 80px;
  height: 80px;
  border-radius: 15px;
  cursor: pointer;
  border: 2px solid #575757;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

.color-preview:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.color-preview:focus-visible {
  outline: 2px solid #00aaff;
  outline-offset: 2px;
}
</style>