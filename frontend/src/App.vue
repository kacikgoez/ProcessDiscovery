<template>
  <Toast></Toast>
  <ConfirmPopup></ConfirmPopup>
  <div class="absolute h-full top-0 bottom-0 left-0 right-0">
    <div class="flex flex-col">
      <nav id="navigation-bar" style="border-bottom: 1px solid #efefef;">
        <div id="navbar-left">
          <button id="navbar-sidebar-btn"></button>
        </div>
        <div id="navbar-center">
          <h1 id="navbar-title">🐳 orca </h1>
        </div>
        <div id="navbar-right">
          <div v-if="isRenderDeployment" id="render-version">
            <h1>{{ commit }} - {{ branch }}</h1>
          </div>
        </div>
      </nav>
      <div class="bg-white p-3" style="border-bottom: 1px solid #efefef;">
        <!-- <input class="bg-gray-50 border-[#cecece] border-[0.5px] p-1 rounded-xl text-sm pl-2 pr-2" placeholder="Search" /> -->
        <div class="inline-flex">
          <MultiSelect v-model="gender" :options="genders" option-label="name" placeholder="Gender"
            :max-selected-labels="3" class="w-[200px]" />
          <div class="block ml-5">
            <span>Ages: {{ ageRange }}</span>
            <Slider v-model="ageRange" range class="w-[200px]" />
          </div>
        </div>
      </div>
    </div>
    <div style="max-width: 1500px; margin: auto;">
      <KPIGrid v-model:data="layout" class="mr-5 ml-5" @close="close"></KPIGrid>
    </div>
  </div>
</template>
<script setup lang="ts">

import MultiSelect from 'primevue/multiselect';
import Slider from 'primevue/slider';
import { Ref, ref } from 'vue';
import KPIGrid from './components/grid/KPIGrid.vue';
import { Charts, KPITile } from './types';

const commit = ref()
const branch = ref()
const isRenderDeployment = ref(false)

const gender = ref(null)
const genders = ref([
  { name: 'Male', code: 'male' },
  { name: 'Female', code: 'female' },
  { name: 'Other', code: 'other' },
]);
const ageRange = ref([20, 80])

// Checks if a render.com deployment, if so, show version info top right
fetch('/render-config')
  .then(response => response.json())
  .then(data => {
    // If data is not empty, look extract "commit" and "branch" from JSON
    if (Object.keys(data).length > 0) {
      ('SHOWING DEPLOYMENT INFO')
      commit.value = `SHA: ${data.commit.slice(0, 5)}...`
      branch.value = data.branch.match(/id-.*/i)[0].slice(12)
      isRenderDeployment.value = true
    }
  }).catch(() => {
    // Not a render.com deployment (or something went wrong)
  })

// Closes a KPI tile by its index
async function close(index: Number) {
  layout.value = layout.value!.filter((kpi) => kpi.i !== index)
}

// This is the layout which is passed down to KPIGrid, which is then synced back up
let layout: Ref<KPITile[]> = ref<KPITile[]>([]);

layout.value = [
  { title: 'A Pie Chart', type: Charts.PieChart, endpoint: 'google.com', x: 0, y: 0, w: 4, h: 10, i: 0 },
  { title: 'A Line Chart', type: Charts.LineChart, endpoint: 'google.com', x: 4, y: 0, w: 4, h: 10, i: 1 },
  { title: 'A Horizontal Bar Chart', type: Charts.HorizontalBarChart, endpoint: 'google.com', x: 4, y: 0, w: 4, h: 10, i: 2 },
  { title: 'Chevron Diagram using SVG & ECharts', type: Charts.VariantView, endpoint: 'google.com', x: 0, y: 0, w: 4, h: 10, i: 24 },
  { title: 'Add New KPI', type: Charts.NewChart, endpoint: 'google.com', x: 8, y: 0, w: 4, h: 10, i: 3 },
];

</script>
<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

@import '@/assets/variables.css';

@font-face {
  font-family: 'Titillium Web';
  src: endpoint('~@/assets/fonts/Titillium_Web/TitilliumWeb-Bold.ttf');
}

/* 
-----------------------------------
SCROLLBAR DESIGN
-----------------------------------
*/

/* WebKit (Chrome, Safari) */
::-webkit-scrollbar {
  width: 12px;
  /* Set the width of the scrollbar */
}

::-webkit-scrollbar-thumb {
  background-color: #888;
  /* Set the color of the thumb */
  border-radius: 100px;
  /* Set the border radius of the thumb */
}

::-webkit-scrollbar-track {
  background-color: #f5f5f5;
  border-radius: 20px;
  /* Set the color of the track */
}

/* Firefox */
/* Note: scrollbar-color and scrollbar-width are not yet standard and may change in the future */
/* So, use with caution and check for browser updates */
html {
  scrollbar-color: #333 #ffffff;
  /* Set the color of the thumb and track */
  scrollbar-width: thin;
  /* Set the width of the scrollbar */
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

body {
  background-color: #000;
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
  /* box-shadow: 4px 4px 13px -13px #000000ff; */
  touch-action: none;

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

/* ---- PRIMEVUE GLOBAL OVERWRITES ---- */

div.p-listbox.p-focus {
  box-shadow: none !important;
}

input.p-listbox-filter.p-inputtext {
  padding: 0.25rem;
  border: 1px solid #ccc;
}

.p-listbox {
  border: 1px solid #ccc;
}

.p-button {
  padding: 0.5rem 0.75rem;
  margin: 0.25rem;
  color: #fff;
}

.p-button.primary {
  background-color: #1da1f2;
}

.p-button.danger {
  background-color: #e9585f;
}

.p-dialog-footer {
  padding: 0 1rem 1rem 1rem;
}

.p-dialog .p-dialog-header {
  padding: 1rem 1rem 0.5rem 1rem;
}

.p-dialog .p-dialog-content {
  padding: 0 1rem 1rem 1rem;
}

.p-multiselect-label {
  padding: 0.5rem;
}

.p-multiselect {
  border: 1px solid #eee;
}

.p-slider-handle {
  background-color: #000;
}

.p-button.p-component.p-confirm-popup-reject {
  background-color: #E54F6D;
}

.p-button.p-component.p-confirm-popup-accept {
  background-color: #058E3F;
}

.p-confirm-popup {
  padding: 0.5rem;
}

.p-confirm-popup-content {
  padding: 0.5rem;
}

.p-confirm-popup-footer {
  padding: 0.5rem;
}

* {
  -webkit-user-drag: none;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}
</style>