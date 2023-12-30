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
          <Button icon="pi pi-download" aria-label="Download" @click="downloadEventLog" />
          <span class="tile-btn material-symbols-outlined cursor-pointer text-xxl p-3 mt-1 float-right"
            @click="addTile">add</span>
        </div>
      </nav>
      <!-- <div class="bg-white p-3" style="border-bottom: 1px solid #efefef;">
        input class="bg-gray-50 border-[#cecece] border-[0.5px] p-1 rounded-xl text-sm pl-2 pr-2" placeholder="Search" />
    </div> -->
    </div>
    <div style="max-width: 1500px; margin: auto;">
      <KPIGrid v-model:data="layout" class="mr-5 ml-5" @close="remove"></KPIGrid>
    </div>
  </div>
</template>
<script setup lang="ts">

import { storeToRefs } from 'pinia';
import { ref } from 'vue';
import KPIGrid from './components/grid/KPIGrid.vue';
import { layoutStore } from './stores/LayoutStore';
import { Charts, EndpointURI, KPITile } from './types';

const commit = ref()
const branch = ref()
const isRenderDeployment = ref(false)


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

const globalLayout = layoutStore();
const remove = globalLayout.remove;
const { layout } = storeToRefs(globalLayout)

const defaultValue: KPITile[] = [
  {
    title: 'A Pie Chart', type: Charts.PieChart, x: 0, y: 0, w: 4, h: 10, i: '0', changed: 0, request: {
      endpoint: EndpointURI.DISTRIBUTION,
      method: 'POST',
      disaggregation_attribute: {
        name: 'gender'
      }
    },
  },
  {
    title: 'A Line Chart', type: Charts.LineChart, x: 4, y: 0, w: 4, h: 10, i: '1', changed: 0, request: {
      endpoint: EndpointURI.KPI,
      method: 'POST',
      kpi: ['PERMUTED_PATH_ADHERENCE', 'BUREAUCRATIC_DURATION'],
      disaggregation_attribute: {
        name: 'gender'
      }
    }
  },
  {
    title: 'A Horizontal Bar Chart', type: Charts.HorizontalBarChart, x: 4, y: 0, w: 4, h: 10, i: '2', changed: 0, request: {
      endpoint: EndpointURI.DISTRIBUTION,
      method: 'POST',
      disaggregation_attribute: {
        name: 'gender'
      }
    }
  },
  {
    title: 'Chevron Diagram using SVG & ECharts', type: Charts.VariantView, x: 0, y: 0, w: 4, h: 10, i: '3', changed: 0, request: {
      endpoint: EndpointURI.VARIANT,
      method: 'POST',
      disaggregation_attribute: {
        name: 'gender'
      }
    }
  },
  {
    title: 'New Tile', type: Charts.NewChart, x: 8, y: 0, w: 4, h: 10, i: '4', changed: 0, request: {
      endpoint: EndpointURI.DISTRIBUTION,
      method: 'POST',
      disaggregation_attribute: {
        name: 'gender'
      }
    }
  },
];

if (localStorage.getItem('layout') === null) {
  globalLayout.set(defaultValue);
} else {
  // globalLayout.set(JSON.parse(localStorage.getItem('layout')!))
  globalLayout.set(defaultValue);
}

const addTile = () => {
  globalLayout.add({
    title: 'New Tile',
    type: Charts.NewChart,
    changed: 0,
    request: {
      endpoint: EndpointURI.DISTRIBUTION,
      method: 'POST',
      disaggregation_attribute: {
        name: 'gender'
      }
    },
    x: 8,
    y: 20,
    w: 4,
    h: 10,
    i: (layout.value.length + 1).toString(),
  });
};


window.addEventListener('beforeunload', () => {
  localStorage.setItem('layout', JSON.stringify(layout.value))
})

function downloadEventLog() {
  window.open('/event-log', '_blank');
}

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

/* Hide scrollbar for Chrome, Safari and Opera */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.no-scrollbar {
  -ms-overflow-style: none;
  /* IE and Edge */
  scrollbar-width: none;
  /* Firefox */
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
  overscroll-behavior-x: none;
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
  border: 1px solid #888;
}

.p-inputtext {
  padding: 0.5rem;
}

.p-listbox {
  padding-top: 1rem;
}

.p-button {
  padding: 0.5rem 0.75rem;
  margin: 0.25rem;
}

.p-button.primary {
  background-color: #1da1f2;
}

.p-button.danger {
  background-color: #e9585f;
}

.p-dialog-footer {
  padding: 1rem 1rem 1rem 1rem;
  border-top: 1px solid #eee;
}

.p-dialog .p-dialog-header {
  padding: 1rem 1rem 0.5rem 1rem;
  border-bottom: 1px solid #eee;
}

.p-dialog .p-dialog-content {
  padding: 0 1rem 0.5rem 1rem;
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

.p-dialog-header-icon {
  margin-top: -25px;
  margin-right: -10px;
  scale: 0.8;
}

.p-listbox-item-group {
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.p-listbox-item-group:first-child {
  border-top: 0;
  border-bottom: 1px solid #eee;
}

* {
  -webkit-user-drag: none;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}
</style>