<script setup>
import axios from 'axios';
import {ref} from "vue";

const fileInput = ref(null);
let Players = ref({
  "data": [
    {
      "full_name": "LeBron James",
      "rating": 97,
      "jersey": "#23",
      "team": "Los Angeles Lakers",
      "position": "F",
      "b_day": "12/30/1984",
      "height": "6-9 / 2.06",
      "weight": "250 lbs. / 113.4 kg.",
      "salary": "$37,436,858 ",
      "country": "USA",
      "draft_year": 2003,
      "draft_round": 1,
      "draft_peak": 1,
      "college": "QingHua",
      "version": "NBA2k20"
    }
  ],
  "rows": 0
});


function triggerFileInput() {
  fileInput.value.click();
}

function uploadFile() {
  const file = fileInput.value.files[0];
  const formData = new FormData();
  formData.append('file', file);
  axios.post('http://localhost:8000/upload/file/', formData)
      .then(res => {
        Players.value = res.data
        fileInput.value.value = null;
        document.getElementById('word').innerText = '上传成功，是否需要再次上传'
        document.getElementById('config').style.display = 'inline'
      })
      .catch(() => {
        fileInput.value.value = null;
        document.getElementById('word').innerText = '上传失败，是否需要重新上传'
        document.getElementById('container').style.marginBlock = '16px'
        document.getElementById('reload').style.display = 'inline'
      });
}

// 更新单元格内容
const updateField = (index, key, event) => {
  Players.value['data'][index][key] = event.target.innerText;
};

// 保存当前行数据
const saveRowData = (index) => {
  const savedPlayer = Players.value['data'][index];
  axios.post('http://localhost:8000/upload/message/', savedPlayer)
      .then(res => {
        if (res.data['result'] === 'success') {
          Players.value['data'] = Players.value['data'].filter((element, i) => i !== index);
          Players.value['rows'] += 1;
        }
        if (Players.value['data'].length === 0) {
          document.getElementById('config').style.display = 'none';
          alert('成功上传所有数据，共' + Players.value['rows'] + '条');
          fileInput.value.value = null;
          Players.value = {
            "data": [
              {
                "full_name": "LeBron James",
                "rating": 97,
                "jersey": "#23",
                "team": "Los Angeles Lakers",
                "position": "F",
                "b_day": "12/30/1984",
                "height": "6-9 / 2.06",
                "weight": "250 lbs. / 113.4 kg.",
                "salary": "$37,436,858 ",
                "country": "USA",
                "draft_year": 2003,
                "draft_round": 1,
                "draft_peak": 1,
                "college": "QingHua",
                "version": "NBA2k20"
              }
            ],
            "rows": 0
          }
        }
      })
      .catch(e => {
        alert("数据保存出错，请重新提交或联系开发人员\n" + e)
      })
};

const submit = (key) => {
  const value = document.querySelector(`input[name="${key}"]`).value;
  Players.value['data'].map(player => {
    if (player[key] === null) {
      player[key] = value;
    }
  })
  axios.post('http://localhost:8000/upload/messages/', Players.value['data'])
      .then(res => {
        Players.value['rows'] += Players.value['data'].length - res.data.length
        Players.value['data'] = res.data
        Players.value['Nan'] = Players.value['Nan'].filter((element) => element !== key);
        if (Players.value['data'].length === 0) {
          document.getElementById('config').style.display = 'none';
          alert('成功上传所有数据，共' + Players.value['rows'] + '条');
          fileInput.value.value = null;
          Players.value = {
            "data": [
              {
                "full_name": "LeBron James",
                "rating": 97,
                "jersey": "#23",
                "team": "Los Angeles Lakers",
                "position": "F",
                "b_day": "12/30/1984",
                "height": "6-9 / 2.06",
                "weight": "250 lbs. / 113.4 kg.",
                "salary": "$37,436,858 ",
                "country": "USA",
                "draft_year": 2003,
                "draft_round": 1,
                "draft_peak": 1,
                "college": "QingHua",
                "version": "NBA2k20"
              }
            ],
            "rows": 0
          }
        }
      })
      .catch(e => {
        alert("数据保存出错，请重新提交或联系开发人员\n" + e)
      })
}

const nothing = () => {
  document.getElementById('config').style.display = 'none';
  alert('成功上传所有数据，共' + Players.value['rows'] + '条');
  fileInput.value.value = null;
  Players.value = {
    "data": [
      {
        "full_name": "LeBron James",
        "rating": 97,
        "jersey": "#23",
        "team": "Los Angeles Lakers",
        "position": "F",
        "b_day": "12/30/1984",
        "height": "6-9 / 2.06",
        "weight": "250 lbs. / 113.4 kg.",
        "salary": "$37,436,858 ",
        "country": "USA",
        "draft_year": 2003,
        "draft_round": 1,
        "draft_peak": 1,
        "college": "QingHua",
        "version": "NBA2k20"
      }
    ],
    "rows": 0
  }
}
</script>


<template>
  <div v-if="Players['data'].length!==0" id="config"
       :style="Players['data'].length===0 ? 'display: inline;' : 'display: none;'">
    <div style="font-size: 20px;">有效上传数据量：{{ Players['rows'] }}</div>
    <div class="container">
      <div class="item" v-for="key in Players['Nan']" :key="key" style="font-size: 20px">
        <div style="width: 100px; height: 30px; display: inline-block">{{ key }}</div>
        <input :name='key' type="text" value="None" style="width: 145px; height: 30px; font-size: 15px">
        <img :src="require('@/assets/yes.png')"
             alt="确定"
             class="yes-icon"
             @click="submit(key)"
             style="margin-left: 7px"/>
      </div>
      <div class="item" style="width: 598px;cursor: pointer" @click="nothing()">去除所有含缺失值的数据项</div>
    </div>
    <div style="margin-left: 0; width: 1400px; height: 550px; overflow: auto; margin-top: 15px">
      <table id="table-data">
        <thead>
        <tr>
          <td v-for="item in Object.keys(Players['data'][0])" :key="item">{{ item }}</td>
          <td>操作</td>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(player, index) in Players['data']" :key="index">
          <td
              v-for="(value, key) in player"
              :key="key"
              :contenteditable="true"
              @input="updateField(index, key, $event)"
          >
            {{ value }}
          </td>
          <td>
            <!-- 使用图片作为确定按钮 -->
            <img :src="require('@/assets/yes.png')"
                 alt="确定"
                 class="yes-icon"
                 @click="saveRowData(index)"/>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
  <ul style="list-style: none; justify-content: center; padding: 0; margin: 100px 0 0 0">
    <li>
      <input
          type="file"
          id="fileInput"
          ref="fileInput"
          @change="uploadFile"
          style="display: none;"
      >
      <label @click="triggerFileInput" style="cursor: pointer;">
        <img src="../assets/File.png" alt="Upload File">
      </label>
    </li>
    <li id="container" style="margin-block: 20px">
      <label id="word" @click="triggerFileInput" style="cursor: pointer; font-size: 30px">上传文件</label>
      <img id="reload" @click="triggerFileInput" src="../assets/reload.png"
           style="width: 35px; position: relative; top: 7px; cursor: pointer">
    </li>
  </ul>
</template>

<style scoped>
.container {
  display: flex;
  flex-wrap: wrap;
  max-width: 700px;
  margin: 0 auto;
}

.item {
  flex: 0 1 auto;
  margin: 5px;
  padding: 10px;
  background-color: #f0f0f0;
}

#config {
  position: absolute;
  right: 5%;
  top: 7%;
  width: 1400px;
  height: 800px;
  background-color: white;
}

img {
  width: 250px;
}

#reload {
  display: none;
}

/* 表格样式 */
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  text-align: center;
  vertical-align: middle;
  border: 1px dashed #ddd;
}

tbody td {
  font-size: 15px;
}

thead {
  background-color: #f2f2f2;
  position: sticky;
  top: 0;
  z-index: 10;
  font-size: 17px;
}

/* 确定按钮图片样式 */
.yes-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
  vertical-align: middle;
  margin-top: 6px; /* 上下间距 9px */
}

.yes-icon:hover {
  transform: scale(1.1); /* 鼠标悬停时图片放大 */
}
</style>