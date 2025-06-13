<script setup>
import {ref} from 'vue';
import one from './components/OneComponent.vue';
import two from './components/TwoComponent.vue';
import three from './components/ThreeComponent.vue'
const num = ref(0);
</script>

<template>
  <div class="sidebar">
    <h2 style="margin-top: 40px">NBA数据分析</h2>
    <ul>
      <li @click="num=0">文件上传</li>
      <li @click="num=1">数据概览</li>
      <li @click="num=2">数据分析</li>
    </ul>
  </div>
  <div class="content">
    <one v-if="num===0"/>
    <two v-if="num===1"/>
    <three v-if="num===2"/>
  </div>
</template>

<style scoped>
.sidebar {
  width: 200px;
  background: #2d3a4b;
  color: #fff;
  padding: 20px;
}

.sidebar ul {
  margin-top: 150px;
  list-style: none;
  padding: 0;
}

.sidebar ul li {
  padding: 10px;
  margin-block: 80px;
  line-height: 40px;
  cursor: pointer;
  border-bottom: 1px solid #3c4a5b;
}

.sidebar ul li:hover {
  background: #3c4a5b;
}

.content {
  flex: 1;
  padding: 20px;
  background: #fff;
}
</style>