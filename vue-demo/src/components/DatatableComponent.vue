<template>
  <div>
    <!-- 搜索框和按钮 -->
    <div style="text-align: right; margin-bottom: 20px; padding-right: 20px;">
      <select v-model="selectData" style="margin-right: 10px; height: 35px; width: 125px; font-size: 15px">
        <option v-for="item in Object.keys(Players[0][0])" :key="item">{{ item }}</option>
      </select>
      <input v-model="searchQuery" type="text" placeholder="请输入搜索内容"/>
      <button @click="searchData">搜索</button>
      <button @click="addEmptyRow">+</button>
    </div>


    <!-- 数据表格 -->
    <div style="margin-left: 115px; width: 1400px; height: 480px; overflow: auto;">
      <table id="table-data">
        <thead>
        <tr>
          <td v-for="item in Object.keys(Players[0][0])" :key="item">{{ item }}</td>
          <td>操作</td>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(player, index) in Players" :key="index">
          <td
              v-for="(value, key) in player[0]"
              :key="key"
              :contenteditable="!player[1].isLocked"
              @input="updateField(index, key, $event)"
              :style="player[1].isLocked ? '' : 'border: 1px dashed #ddd;'"
          >
            {{ value }}
          </td>
          <td>
            <!-- 使用图片作为删除按钮 -->
            <img :src="require('@/assets/delete.png')"
                 alt="删除" class="delete-icon"
                 @click="deletePlayer(index, player[0].id)"/>

            <!-- 使用图片作为更新按钮，更新按钮与确定按钮之间有 9px 的间距 -->
            <img v-if="player[1].isLocked"
                 :src="require('@/assets/update.png')"
                 alt="更新"
                 class="update-icon"
                 @click="unlockRow(index)"/>

            <!-- 使用图片作为确定按钮 -->
            <img v-else
                 :src="require('@/assets/yes.png')"
                 alt="确定"
                 class="yes-icon"
                 @click="saveRowData(index)"/>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import {ref, inject} from "vue";
import axios from "axios";

const params = JSON.parse(inject('params').value);
let Players = ref([]);
params.forEach(param => {
  let p = []
  p.push(param)
  p.push({"isLocked": true})
  Players.value.push(p)
});

const searchQuery = ref("");
const selectData = ref("");
// 解锁当前行
const unlockRow = (index) => {
  Players.value[index][1].isLocked = false;
};
// 保存当前行数据
const saveRowData = (index) => {
  const savedPlayer = Players.value[index];
  alert("数据保存中，稍安勿躁")
  axios.post('http://localhost:8000/table/update/', savedPlayer)
      .then(res => {
        if(res.data['result']==='success'){
          Players.value[index][1].isLocked = true; // 锁定表格
        }
      })
      .catch(e => {
        alert("数据保存出错，请重新提交或联系开发人员\n"+e)
      })
};

// 更新单元格内容
const updateField = (index, key, event) => {
  Players.value[index][0][key] = event.target.innerText;
};

// 添加空行数据
const addEmptyRow = () => {
  let p = Object.keys(Players.value[0][0]).reduce((obj, key) => {
    obj[key] = null;
    return obj;
  }, {});
  let NewRow = []
  NewRow.push(p)
  NewRow.push({"isLocked": false})
  Players.value.push(NewRow);
  alert("空行添加成功，请下滑至最底层");
};

// 删除选中行
const deletePlayer = (i, id) => {
  alert("数据删除中，稍安勿躁")
  axios.post('http://localhost:8000/table/del/', id)
      .then(() => {
        Players.value = Players.value.filter((element, index) => index !== i);
      })
      .catch(e => {
        alert("数据删除出错，请重新操作或联系开发人员\n"+e)
      })
};

// 搜索功能
const searchData = () => {
  var table, tr, td, i, txtValue;
  const filter = searchQuery.value;
  const index = Object.keys(Players.value[0][0]).findIndex(item => item === selectData.value);
  table = document.querySelector('table#table-data');
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[index];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.indexOf(filter) > -1) {
        tr[i-1].scrollIntoView({behavior: "smooth"});
        break;
      }
    }
  }
};
</script>

<style scoped>
/* 表格样式 */
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  text-align: center;
  vertical-align: middle;
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

/* 删除按钮图片样式 */
.delete-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
  vertical-align: middle;
}

.delete-icon:hover {
  transform: scale(1.1); /* 鼠标悬停时图片放大 */
}

/* 按钮样式 */
button {
  margin: 5px;
  padding: 5px 10px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  border-radius: 3px;
}

button:hover {
  background-color: #0056b3;
}

/* 更新按钮图片样式 */
.update-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
  vertical-align: middle;
  margin-top: 5px;
}

.update-icon:hover {
  transform: scale(1.1); /* 鼠标悬停时图片放大 */
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

/* 搜索框样式 */
input[type="text"] {
  padding: 8px;
  font-size: 14px;
  margin-right: 10px;
  width: 200px;
}
</style>
