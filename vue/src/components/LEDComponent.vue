<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  id: number;
  color: string;
  isClick: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:color', id: number): void;
}>();

const openColorPicker = () => {
  if (props.isClick) emit('update:color', props.id);
};

const ledStyles = computed(() => {
  const shadowColor = props.color;
  return {
    backgroundColor: props.color,
    boxShadow: `
      0 0 200px 20px ${shadowColor}
    `
  };
});
</script>

<template>
  <div class="led-box">
    <div
        class="led"
        :style="ledStyles"
        @mouseover="openColorPicker"
    ></div>
  </div>
</template>

<style scoped>
.led-box {
  position: relative;
}

.led {
  position: relative;
  width: 20px;
  height: 20px;
  margin: 15px 10px;
  border-radius: 25%;
  transition: all 0.3s ease;
  cursor: pointer;
}

.color-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 0;
  opacity: 0;
  pointer-events: none;
}
</style>