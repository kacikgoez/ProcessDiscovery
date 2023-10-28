<template>
  <h1>ORCA</h1>
  <span v-if="isRenderDeployment" id="render-version">
    {{ commit }} - {{ branch }}
  </span>
  <KPIGrid :data="layout" @close="close"></KPIGrid>
</template>

<script setup lang="ts">

import { reactive, nextTick, ref } from 'vue';
import KPIGrid from './components/grid/KPIGrid.vue'
import { KPITile } from './types'
// import * as d3 from 'd3'

const commit = ref()
const branch = ref()
const isRenderDeployment = ref(false)

fetch('/render-config')
  .then(response => response.json())
  .then(data => {
    // If data is not empty, look extract "commit" and "branch" from JSON
    if (Object.keys(data).length > 0) {
      console.log("RENDERING DEPLOYMENT INFO")
      commit.value = `SHA: ${data.commit.slice(0, 5)}...`
      branch.value = data.branch.match(/id-.*/i)[0].slice(12)
      isRenderDeployment.value = true;
    }
  }).catch(err => {
    console.log(err)
  })

async function close(index: Number) {
  layout = layout.filter((kpi) => kpi.i !== index);
  await nextTick()
}

let layout: KPITile[] = reactive([
  { title: "KPI", url: "google.com", x: 0, y: 0, w: 2, h: 2, i: 0 },
  { title: "KPI", url: "google.com", x: 2, y: 0, w: 2, h: 4, i: 1 },
  { title: "KPI", url: "google.com", x: 4, y: 0, w: 2, h: 5, i: 2 },
  { title: "KPI", url: "google.com", x: 6, y: 0, w: 2, h: 3, i: 3 },
  { title: "KPI", url: "google.com", x: 8, y: 0, w: 2, h: 3, i: 4 },
  { title: "KPI", url: "google.com", x: 10, y: 0, w: 2, h: 3, i: 5 },
  { title: "KPI", url: "google.com", x: 0, y: 5, w: 2, h: 5, i: 6 },
  { title: "KPI", url: "google.com", x: 2, y: 5, w: 2, h: 5, i: 7 },
  { title: "KPI", url: "google.com", x: 4, y: 5, w: 2, h: 5, i: 8 },
  { title: "KPI", url: "google.com", x: 6, y: 4, w: 2, h: 4, i: 9 },
  { title: "KPI", url: "google.com", x: 8, y: 4, w: 2, h: 4, i: 10 },
  { title: "KPI", url: "google.com", x: 10, y: 4, w: 2, h: 4, i: 11 },
  { title: "KPI", url: "google.com", x: 0, y: 10, w: 2, h: 5, i: 12 },
  { title: "KPI", url: "google.com", x: 2, y: 10, w: 2, h: 5, i: 13 },
  { title: "KPI", url: "google.com", x: 4, y: 8, w: 2, h: 4, i: 14 },
  { title: "KPI", url: "google.com", x: 6, y: 8, w: 2, h: 4, i: 15 },
  { title: "KPI", url: "google.com", x: 8, y: 10, w: 2, h: 5, i: 16 },
  { title: "KPI", url: "google.com", x: 10, y: 4, w: 2, h: 2, i: 17 },
  { title: "KPI", url: "google.com", x: 0, y: 9, w: 2, h: 3, i: 18 },
  { title: "KPI", url: "google.com", x: 2, y: 6, w: 2, h: 2, i: 19 }
]);

</script>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

/* 
-----------------------------------
SCROLLBAR DESIGN
-----------------------------------
*/

/* width */
::-webkit-scrollbar {
  width: 2px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #fff;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* 
-----------------------------------
APP DESIGN 
-----------------------------------
*/

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  -webkit-user-drag: none;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  margin-top: 15px;
}

/* Color of the preview tile when dragging */
.vue-grid-item.vue-grid-placeholder {
  background-color: #a4e7ab;
}

.vue-grid-item {
  color: #777;
}

#render-version {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1000;
}
</style>
