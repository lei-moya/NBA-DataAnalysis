<script setup>
import {ref, watch} from "vue";
import axios from "axios";


function togglePopup() {
  var popup = document.getElementById("popup");
  if (popup.style.display === "none") {
    popup.style.display = "inline";
  } else {
    popup.style.display = "none";
  }
}

function togglePopupclose() {
  var popup = document.getElementById("popup");
  if (popup.style.display === "none") {
    popup.style.display = "inline";
  } else {
    popup.style.display = "none";
  }
}

const imgList = ref([]);
const imageSources = ref([]);

watch(imgList, () => {
  if (imgList.value) {
    checkImg(imgList.value[imgList.value.length - 1])
  }
}, {deep: true})

function selectOption() {
  // 获取每个select元素的当前值
  // 获取所有具有 'select-box' 类的 select 元素
  let list = [];
  Array.from(document.getElementsByClassName('select-box')).map(select => {
    list.push(select.value)
  });
  // 创建一个数组来存储所有选中的选项值
  list = {
    text: list[0]
  };
  const json = JSON.stringify(list);
  axios.post('http://localhost:8000/data/explore/', json).then(res => {
    togglePopup();
    imgList.value.push(res.data['result'] + '.png');
  })
}

async function checkImg(img) {
  try {
    if (require('../assets/static/' + img)) {
      imageSources.value.push(img);
      console.log(imageSources)
    }
  } catch (error) {
    await checkImg(img)
  }
}

function ani(index) {
  const newPlus = document.getElementsByClassName('pltImg')[index]
  // 切换图片的大小
  if (newPlus.style.height === '350px') {
    newPlus.style.height = '500px'; // 放大图片的高度
    newPlus.style.width = '800px'; // 放大图片的宽度
    newPlus.style.position = 'fixed'; // 使用fixed定位
    newPlus.style.top = '45%';
    newPlus.style.right = '1%';
    newPlus.style.transform = 'translate(-50%, -50%) scale(1.5)';
    newPlus.style.boxShadow= '0 5px 15px rgba(0, 0, 0, 0.5)';
    newPlus.style.border = 'none'
    newPlus.style.zIndex = '1000';
  } else {
    newPlus.style.position = ''; // 清除定位
    newPlus.style.top = '';
    newPlus.style.left = '';
    newPlus.style.transform = ''; // 清除变换
    newPlus.style.transition = ''; // 清除过渡效果
    newPlus.style.zIndex = '';
    newPlus.style.boxShadow= 'none';
    newPlus.style.border = 'solid 2px silver'
    newPlus.style.height = '350px'; // 恢复图片的高度
    newPlus.style.width = '450px'; // 恢复图片的宽度
  }
}

const o = ref(0)

function handleOptionChange(event) {
  // 根据选中的值设置o的值
  if (event.target.value === '统计数量') {
    o.value = 0;
  } else if (event.target.value === '变量关系') {
    o.value = 1;
  } else if (event.target.value === '排序') {
    o.value = 2;
  }
}

function del(e, index) {
  imageSources.value = imageSources.value.filter((value, i) =>
      i !== index
  )
}
</script>


<template>
  <div id="main"
       style="width: 100%; height: 100%; overflow: auto; max-width: 1600px; max-height: 76s0px; text-align: left">
    <img class="pltImg" v-for="(img, index) in imageSources" :key="index" :src="require('../assets/static/'+img)"
         alt="" @click.left="ani(index)" @contextmenu.prevent="del($event, index)" style="height: 350px; width: 500px; padding: 5px; border: solid 2px silver; margin: 5px;">
  </div>
  <div class="plus-sign" @click="togglePopup()">+</div>
  <div id="popup" style="display: none;">
    <div class="container">
      <div class="item">
        <div class="label">分门别类</div>
        <select class="flex-grow: 1;" @change="handleOptionChange">
          <option>统计数量</option>
          <option>变量关系</option>
          <option>排序</option>
        </select>
      </div>
      <div v-if="o===0">
        <div class="item">
          <div class="label">统计问题</div>
          <select class="select-box" id="twoSelect">
            <option>各国在NBA的参与度</option>
            <option>工资分布</option>
            <option>各球员的评分分布情况</option>
            <option>各队伍人数情况</option>
            <option>各球员身高分布</option>
            <option>各球员体重分布</option>
            <option>各球员工资区间分布情况</option>
            <option>各球员选秀年份分布</option>
          </select>
        </div>
      </div>
      <div v-if="o===1">
        <div class="item">
          <div class="label">关系问题</div>
          <select class="select-box" id="threeSelect">
            <option>球员的排名和工资的关系</option>
            <option>球员身高和体重的分布</option>
            <option>各球员评分和工资的关系</option>
          </select>
        </div>
      </div>
      <div v-if="o===2">
        <div class="item">
          <div class="label">排序问题</div>
          <select class="select-box" id="twoSelect">
            <option>前10名球员</option>
            <option>球队排名</option>
            <option>工资排名</option>
          </select>
        </div>
      </div>
    </div>
    <button @click="togglePopupclose()" style="margin-left: 10px">Close</button>
    <button @click="selectOption()" style="margin-left: 150px" id="selectButton">select</button>
  </div>
</template>

<style scoped>
.plus-sign {
  position: absolute;
  bottom: 10px;
  right: 40vw;
  width: 100px;
  height: 100px;
  border: 3px solid black; /* 按钮边框 */
  border-radius: 50px;
  line-height: 100px; /* 使加号垂直居中 */
  font-size: 65px; /* 加号大小 */
  margin: 10px;
  z-index: 999;
}

.plus-sign:hover {
  background-color: aqua;
  color: white;
  border: white;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* 左对齐 */
  padding: 20px;
}

.item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.label {
  min-width: 50px; /* 设置标签最小宽度 */
  margin-right: 10px;
}

.select-box {
  flex-grow: 1;
}

/* 可以添加一些样式来美化选择框 */
select {
  width: 200px; /* 设置选择框的宽度 */
  padding: 10px; /* 设置内边距 */
  margin: 10px; /* 设置外边距 */
  border: 1px solid #ccc; /* 设置边框样式 */
  border-radius: 4px; /* 设置边框圆角 */
}

#popup {
  position: fixed;
  right: 22.5%;
  top: 45%;
  transform: translate(-50%, -50%);
  padding: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
  background-color: #fff;
  z-index: 1000;
}
</style>