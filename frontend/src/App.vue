<template>
  <div class="flex flex-col">
    <nav id="navigation-bar" style="border-bottom: 1px solid #efefef;">
      <div id="navbar-left">
        <button id="navbar-sidebar-btn"></button>
      </div>
      <div id="navbar-center">
        <h1 id="navbar-title">🐳 orca </h1>
      </div>
      <div id="navbar-right">
        <div id="render-version" v-if="isRenderDeployment">
          <h1>{{ commit }} - {{ branch }}</h1>
        </div>
      </div>
    </nav>
    <div class="bg-white p-3" style="border-bottom: 1px solid #efefef;">
      <input class="bg-gray-50 border-[#cecece] border-[0.5px] p-1 rounded-xl text-sm pl-2 pr-2" placeholder="Search" />
    </div>
  </div>
  <div style="max-width: 1500px; margin: auto;">
    <KPIGrid class="mr-5 ml-5" v-model:data="layout" @close="close"></KPIGrid>
  </div>
</template>

<script setup lang="ts">

import { nextTick, ref } from 'vue';
import KPIGrid from './components/grid/KPIGrid.vue';
import { Charts, KPITile } from './types';

const commit = ref()
const branch = ref()
const isRenderDeployment = ref(false)

// Checks if a render.com deployment, if so, show version info top right
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

  }).catch(() => {
    // Not a render.com deployment (or something went wrong)
  })

// Closes a KPI tile by its index
async function close(index: Number) {
  layout.value = layout.value.filter((kpi) => kpi.i !== index)
  await nextTick()
}

// This is the layout which is passed down to KPIGrid, which is then synced back up
let layout: KPITile[] = ref([
  { title: "A Pie Chart", type: Charts.PieChart, url: "google.com", x: 0, y: 0, w: 4, h: 10, i: 0 },
  { title: "A Line Chart", type: Charts.LineChart, url: "google.com", x: 4, y: 0, w: 4, h: 10, i: 1 },
  { title: "A Horizontal Bar Chart", type: Charts.HorizontalBarChart, url: "google.com", x: 4, y: 0, w: 4, h: 10, i: 2 },
  { title: "Variant", type: Charts.Variant, url: "google.com", x: 8, y: 0, w: 4, h: 10, i: 3 },
]);


</script>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

@import '@/assets/variables.css';

@font-face {
  font-family: 'Titillium Web';
  src: url('~@/assets/fonts/Titillium_Web/TitilliumWeb-Bold.ttf');
}

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
  background: var(--scroll-track-color);
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

html {
  background-color: var(--dashboard-background-color);
  font: 'Roboto', sans-serif;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: var(--app-text-color);
  -webkit-user-drag: none;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}

#navigation-bar {
  position: relative;
  display: flex;
  flex-wrap: nowrap;
  flex-direction: row;
  align-items: center;
  background-color: var(--navbar-background-color);
  width: 100%;
  height: 80px;
  padding: 0 10px;

  #navbar-left {
    display: flex;
    justify-content: left;
  }

  #navbar-center {
    display: flex;
    align-items: center;
    justify-content: center;

    #navbar-title {
      font-family: 'Titillium Web', sans-serif;
      font-weight: bold;
      font-size: 35px;
      white-space: nowrap;
    }
  }

  div {
    flex: 1;
    min-width: 0;
  }
}

/* Color of the preview tile when dragging */
.vue-grid-item.vue-grid-placeholder {
  background-color: var(--placeholder-tile-background-color);
  box-shadow: 10px 10px 10px 20px var(--placeholder-tile-shadow-color);
}

.vue-grid-item {
  color: var(--vue-tile-text-color);
  border-radius: 15px;
  background-color: var(--vue-tile-background-color);
  border: 1px solid var(--border-color);
  box-shadow: 4px 4px 13px -13px #000000ff;

  .vue-resizable-handle {
    opacity: 0.5;
    margin: 8px;
  }
}

#render-version * {
  position: relative;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: text-gray-500;
  z-index: 1000;
}
</style>
