<script setup>
import Dataform from "./DataformComponent.vue";
import Datatable from "./DatatableComponent.vue";
import {provide, ref} from "vue";
let states = ref(0)
let params = ref(null)
provide('params', params);
provide('states', states);
</script>

<template>
  <div style="width: 100%; height: 40%">
    <Dataform/>
  </div>
  <div style="width: 100%; height: 60%">
     <Datatable v-if="states"/>
  </div>
</template>

<style scoped>

</style>