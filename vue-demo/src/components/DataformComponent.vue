<script setup>
import axios from "axios";
import {ref, inject} from "vue";

const allStates = ref(false)
let params = inject('params')
let states = inject('states')

function checkAll() {
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  if (!allStates.value) {
    checkboxes.forEach(function (checkbox) {
      checkbox.checked = true;
    });
    allStates.value = true;
  } else {
    checkboxes.forEach(function (checkbox) {
      checkbox.checked = false;
    });
    allStates.value = false;
  }
  return 0;
}

async function submit() {
  const checkboxes = document.querySelectorAll('input[name="options"]:checked');
  const data = Array.from(checkboxes).map(function (checkbox) {
    return checkbox.value;
  });
  if (data[0]) {
    data.unshift("id")
  }
  await axios.post('http://localhost:8000/table/check/', data).then(res => {
    params.value = JSON.stringify(res.data)
    states.value = false
  })
  states.value = true
}
</script>

<template>
  <div class="container">
    <table>
      <tbody>
      <tr>
        <td>
          <label>full_name</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="full_name">
        </td>
        <td>
          <label>rating</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="rating">
        </td>
      </tr>
      <tr>
        <td>
          <label>jersey</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="jersey">
        </td>
        <td>
          <label>team</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="team">
        </td>
      </tr>
      <tr>
        <td>
          <label>position</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="position">
        </td>
        <td>
          <label>b_day</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="b_day">
        </td>
      </tr>
      <tr>
        <td>
          <label>height</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="height">
        </td>
        <td>
          <label>weight</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="weight">
        </td>
      </tr>
      <tr>
        <td>
          <label>salary</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="salary">
        </td>
        <td>
          <label>country</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="country">
        </td>
      </tr>
      <tr>
        <td>
          <label>draft_year</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="draft_year">
        </td>
        <td>
          <label>draft_round</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="draft_round">
        </td>
      </tr>
      <tr>
        <td>
          <label>draft_peak</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="draft_peak">
        </td>
        <td>
          <label>college</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="college">
        </td>
      </tr>
      <tr>
        <td>
          <label>version</label>
        </td>
        <td>
          <input type="checkbox" name="options" value="version">
        </td>
      </tr>
      <tr>
        <td colspan="4">
          <hr>
        </td>
      </tr>
      </tbody>
      <tfoot>
      <tr>
        <td colspan="2">
          <button type="button" id="checkAllButton" @click="checkAll()">全选</button>
        </td>
        <td colspan="2">
          <button type="button" @click="submit()">提交</button>
        </td>
      </tr>
      </tfoot>
    </table>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

table {
  background-color: #f7f7f7;
  padding: 25px;
  width: 350px;
  height: 350px;
  font-size: 20px;
  transition: transform 0.3s ease;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

button {
  width: 80px;
  height: 40px;
  border: 1px solid #ddd;
  font-size: 18px;
}

button:hover {
  transform: scale(1.25);
  border-color: #007bff;
}

input:hover {
  transform: scale(1.5);
}
</style>