<template>
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
  <Toast></Toast>
  <ConfirmPopup></ConfirmPopup>
  <div class="absolute h-full top-0 bottom-0 left-0 right-0">
=======
  <div class="absolute h-full top-0 bottom-0 left-0 right-0" :class="{ 'overflow-hidden': modalVisible }">
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
  <Toast></Toast>
  <ConfirmPopup></ConfirmPopup>
  <div class="absolute h-full top-0 bottom-0 left-0 right-0">
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
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
<<<<<<< HEAD
        </div>
      </div>
    </div>
    <div style="max-width: 1500px; margin: auto;">
      <KPIGrid v-model:data="layout" class="mr-5 ml-5" @close="close"></KPIGrid>
    </div>
  </div>
=======
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
=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
        </div>
      </div>
    </div>
    <div style="max-width: 1500px; margin: auto;">
      <KPIGrid v-model:data="layout" class="mr-5 ml-5" @close="close"></KPIGrid>
    </div>
  </div>
<<<<<<< HEAD
  <div style="max-width: 1500px; margin: auto;">
    <KPIGrid class="mr-5 ml-5" v-model:data="layout" @close="close"></KPIGrid>
  </div>
<<<<<<< HEAD
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
  <BaseModal name="example" />
>>>>>>> 7e18e45 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
</template>
<script setup lang="ts">

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import MultiSelect from 'primevue/multiselect';
import Slider from 'primevue/slider';
import { Ref, ref } from 'vue';
=======
=======
import { storeToRefs } from 'pinia';
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
import MultiSelect from 'primevue/multiselect';
import Slider from 'primevue/slider';
<<<<<<< HEAD
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
import { nextTick, ref } from 'vue';
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
import { Ref, ref } from 'vue';
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
import KPIGrid from './components/grid/KPIGrid.vue';
import { Charts, KPITile } from './types';

const commit = ref()
const branch = ref()
const isRenderDeployment = ref(false)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
const modal = modalStore();
const { modalVisible } = storeToRefs(modal);

>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
const gender = ref(null)
const genders = ref([
  { name: 'Male', code: 'male' },
  { name: 'Female', code: 'female' },
  { name: 'Other', code: 'other' },
]);
const ageRange = ref([20, 80])

<<<<<<< HEAD
=======
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
// Checks if a render.com deployment, if so, show version info top right
fetch('/render-config')
  .then(response => response.json())
  .then(data => {
    // If data is not empty, look extract "commit" and "branch" from JSON
    if (Object.keys(data).length > 0) {
<<<<<<< HEAD
<<<<<<< HEAD
      ('SHOWING DEPLOYMENT INFO')
=======
      console.log('SHOWING DEPLOYMENT INFO')
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
      ('SHOWING DEPLOYMENT INFO')
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
      commit.value = `SHA: ${data.commit.slice(0, 5)}...`
      branch.value = data.branch.match(/id-.*/i)[0].slice(12)
      isRenderDeployment.value = true
    }
<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
  }).catch(() => {
    // Not a render.com deployment (or something went wrong)
  })

// Closes a KPI tile by its index
async function close(index: Number) {
<<<<<<< HEAD
<<<<<<< HEAD
  layout.value = layout.value!.filter((kpi) => kpi.i !== index)
<<<<<<< HEAD
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
=======
  layout.value = layout.value.filter((kpi) => kpi.i !== index)
=======
  layout.value = layout.value!.filter((kpi) => kpi.i !== index)
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
  await nextTick()
}

// This is the layout which is passed down to KPIGrid, which is then synced back up
<<<<<<< HEAD
let layout: KPITile[] = ref([
  { title: "A Pie Chart", type: Charts.PieChart, url: "google.com", x: 0, y: 0, w: 4, h: 10, i: 0 },
  { title: "A Line Chart", type: Charts.LineChart, url: "google.com", x: 4, y: 0, w: 4, h: 10, i: 1 },
  { title: "A Horizontal Bar Chart", type: Charts.HorizontalBarChart, url: "google.com", x: 4, y: 0, w: 4, h: 10, i: 2 },
  { title: "Add New KPI", url: "google.com", x: 8, y: 0, w: 4, h: 10, i: 3 },
]);
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)

=======
let layout = ref<KPITile[]>();
=======
}

// This is the layout which is passed down to KPIGrid, which is then synced back up
let layout: Ref<KPITile[]> = ref<KPITile[]>([]);

>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
layout.value = [
  { title: 'A Pie Chart', type: Charts.PieChart, endpoint: 'google.com', x: 0, y: 0, w: 4, h: 10, i: 0 },
  { title: 'A Line Chart', type: Charts.LineChart, endpoint: 'google.com', x: 4, y: 0, w: 4, h: 10, i: 1 },
  { title: 'A Horizontal Bar Chart', type: Charts.HorizontalBarChart, endpoint: 'google.com', x: 4, y: 0, w: 4, h: 10, i: 2 },
  { title: 'Chevron Diagram using SVG & ECharts', type: Charts.VariantView, endpoint: 'google.com', x: 0, y: 0, w: 4, h: 10, i: 24 },
  { title: 'Add New KPI', type: Charts.NewChart, endpoint: 'google.com', x: 8, y: 0, w: 4, h: 10, i: 3 },
];
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)

</script>
<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

@import '@/assets/variables.css';

@font-face {
  font-family: 'Titillium Web';
<<<<<<< HEAD
<<<<<<< HEAD
  src: endpoint('~@/assets/fonts/Titillium_Web/TitilliumWeb-Bold.ttf');
=======
  src: url('~@/assets/fonts/Titillium_Web/TitilliumWeb-Bold.ttf');
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
  src: endpoint('~@/assets/fonts/Titillium_Web/TitilliumWeb-Bold.ttf');
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
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

<<<<<<< HEAD
<<<<<<< HEAD
=======
/* Track */
::-webkit-scrollbar-track {
  background: var(--scroll-track-color);
}

/* Handle */
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
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

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
body {
  background-color: #000;
}

<<<<<<< HEAD
=======
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
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
<<<<<<< HEAD
<<<<<<< HEAD
  /* box-shadow: 4px 4px 13px -13px #000000ff; */
  touch-action: none;
=======
  box-shadow: 4px 4px 13px -13px #000000ff;
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
  /* box-shadow: 4px 4px 13px -13px #000000ff; */
  touch-action: none;
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)

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
<<<<<<< HEAD
<<<<<<< HEAD
  padding: 0.5rem 0.75rem;
=======
  padding: 0.5rem;
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
  padding: 0.5rem 0.75rem;
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
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
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
  background-color: red;
}

.p-button.p-component.p-confirm-popup-accept {
  background-color: green;
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
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
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
}

* {
  -webkit-user-drag: none;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}
</style>