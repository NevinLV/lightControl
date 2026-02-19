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
  <div>
    <input
        ref="colorPickerRef"
        type="color"
        :value="props.modelValue"
        @input="updateColor"
        class="color-picker-input"
        aria-label="Выберите цвет"
    >

    <div
        class="command-button"
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
</style>