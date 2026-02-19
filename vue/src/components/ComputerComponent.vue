<template>
  <div class="computer"></div>
  <div class="monitor"></div>
  <div class="bottom-computer">
    <slot>

    </slot>
  </div>
  <div class="stand"></div>
</template>

<style scoped>
.computer{
  position: absolute;
  width: 950px;
  height: 450px;
  background-color: #1c1c1c;
  top: 60px;
  left: calc(50% - 475px);
  border-radius: 10px;
}

.monitor{
  position: absolute;
  width: 900px;
  height: 450px;
  background-color: #151515;
  top: 80px;
  left: calc(50% - 450px);
  border-radius: 5px;
}

.bottom-computer{
  position: absolute;
  width: 960px;
  height: 80px;
  background-color: #171717;
  bottom: -60px;
  left: calc(50% - 480px);
  border-radius: 10px;
  z-index: 2;
}

.stand{
  position: absolute;
  width: 300px;
  height: 200px;
  background-color: #131313;
  bottom: -190px;
  left: calc(50% - 150px);
  border-radius: 10px;
}
</style>