<template>
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
  <div class="tile">
    <div class="tile-navbar">
      <div class="flex-[20] flex-shrink-0 ml-6" @mouseover="draggable(true)" @mouseleave="draggable(false)">
        <h1>{{ props.title }}</h1>
      </div>
      <div class="flex-1 mr-2">
        <span class="tile-btn material-symbols-outlined text-base cursor-pointer">
          info
        </span>
      </div>
      <div class="flex-1 mr-2">
        <span class="tile-btn material-symbols-outlined text-base cursor-pointer" @click="show">
          edit
        </span>
      </div>
      <div class="flex-1 mr-2">
        <span class="tile-btn material-symbols-outlined text-base cursor-pointer" @click="openPopup($event, props.i)">
          close
        </span>
      </div>
<<<<<<< HEAD
    </div>
    <div ref="tileContent" class="tile-content">
      <div class="overflow-y-auto overflow-x-hidden h-full">
        <div>
          <component :is="chart" :id="props.i" :key="changed" :type="props.type" :width="width" :height="height"
            @change="change"></component>
        </div>
      </div>
    </div>
    <div class="tile-footer">
    </div>
    <EditModal v-model:visible="visible" :title="props.title">

    </EditModal>
  </div>
</template>

<script setup lang="ts">
import { Charts, KPIActions, KPIChange } from '@/types';
import { useElementSize } from '@vueuse/core';
import { useConfirm } from 'primevue/useconfirm';
import {
  PropType,
  defineAsyncComponent,
  defineEmits,
  defineProps,
  ref,
  shallowRef,
} from 'vue';
import EditModal from '../modals/EditModal.vue';

const tileContent = ref(null);
const { width, height } = useElementSize(tileContent);

const confirm = useConfirm();
const openPopup = (event: Event, i: number) => {
  confirm.require({
    target: event.currentTarget as HTMLElement,
    message: 'Are you sure you want to delete this tile?',
    icon: 'pi pi-exclamation-triangle',
    accept: () => {
      emits('close', i);
    },
    reject: () => {

    }
  });
};

const props = defineProps({
  title: { type: String, required: true },
  type: {
    type: String as PropType<Charts>,
    default: String,
  },
  i: { type: Number, required: true },
});

const emits = defineEmits(['close', 'update:data', 'draggable', 'edit']);
const visible = ref(false);
let chart = shallowRef<Object>();
// If this is changed, the chart component will be reloaded
let changed = shallowRef(0);
// Initalize chart if type is given
let component = props.type !== undefined ? props.type : Charts.NewChart;

function show() {
  visible.value = true;
}

function draggable(state: Boolean) {
  emits('draggable', state);
}

// Function to update the component / chart (e.g. change content)
async function change(data: KPIChange) {
  switch (data.action as KPIActions) {
    // Change component
    case KPIActions.ChangeComponent:
      chart.value = defineAsyncComponent(
        () => import(`@/components/charts/${data.component}`)
      );
      changed.value++;
      break;
    default:
      chart.value = defineAsyncComponent(
        () => import('@/components/charts/NewChart.vue')
      );
      changed.value++;
      break;
  }
}

change({ action: KPIActions.ChangeComponent, component: component });
</script>
<style scoped>
.tile {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

.tile-navbar {
  position: relative;
  display: flex;
  flex-grow: 1;
  text-align: left;
  width: 100%;
  left: 0;
  right: 0;

  h1 {
    font-size: 1.1rem;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    line-height: 2rem;
    color: rgb(99, 99, 99);
  }

  div {
    padding: 10px 0;
  }
}

.tile-content {
  position: relative;
  display: block;
  text-align: center;
  flex-grow: 9;
  width: 100%;
  height: 100%;
  padding: 0px 8px 16px 8px;
  margin: 0;
  background-color: #ffffff;
  overflow-y: auto;
  -ms-overflow-style: none;
  /* IE and Edge */
  scrollbar-width: none;
}


.tile-btn {
  width: 1.5rem;
  height: 1.5rem;
  font-size: 1rem;
  justify-content: center;
  text-align: center;

  &:hover {
    background-color: #e2e2e2;
    border-radius: 50%;
  }
}

.tile-footer {
  flex-grow: 1;
  padding-top: 0.8rem;
}

.exit-button {
  position: absolute;
  top: 0;
  right: 0;
  width: 50px;
  height: 50px;
  padding: 5px;
  color: var(--vue-tile-exit-button-color);
  cursor: pointer;
  z-index: 1000;
=======
    <div class="tile">
        <div class="tile-navbar">
            <div class="flex-1 flex-shrink-0"></div>
            <div class="flex-1 flex-shrink-0"></div>
            <div style="flex-grow: 20;" @mouseover="draggable(true)" @mouseleave="draggable(false)">
                <h1>{{ props.title }}</h1>
            </div>
            <div class="flex-1 mr-2">
                <span class="tile-btn material-symbols-outlined text-base cursor-pointer">
                    info
                </span>
            </div>
            <div class="flex-1 mr-2">
                <span class="tile-btn material-symbols-outlined text-base cursor-pointer" @click="store.show(true)">
                    edit
                </span>
            </div>
            <div class="flex-1 mr-2">
                <span class="tile-btn material-symbols-outlined text-base cursor-pointer" @click="emits('close', i)">
                    close
                </span>
            </div>
        </div>
        <div class="tile-content">
            <component :is="chart" :type="props.type" :id="props.i" @change="change" :key="changed"></component>
        </div>
        <div class="tile-footer">
        </div>
=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
    </div>
    <div ref="tileContent" class="tile-content">
      <div class="overflow-y-auto overflow-x-hidden h-full">
        <div>
          <component :is="chart" :id="props.i" :key="changed" :type="props.type" :width="width" :height="height"
            @change="change"></component>
        </div>
      </div>
    </div>
    <div class="tile-footer">
    </div>
    <EditModal v-model:visible="visible" :title="props.title">

    </EditModal>
  </div>
</template>

<script setup lang="ts">
import { Charts, KPIActions, KPIChange } from '@/types';
import { useElementSize } from '@vueuse/core';
import { useConfirm } from 'primevue/useconfirm';
import {
  PropType,
  defineAsyncComponent,
  defineEmits,
  defineProps,
  ref,
  shallowRef,
} from 'vue';
import EditModal from '../modals/EditModal.vue';

const tileContent = ref(null);
const { width, height } = useElementSize(tileContent);

const confirm = useConfirm();
const openPopup = (event: Event, i: number) => {
  confirm.require({
    target: event.currentTarget as HTMLElement,
    message: 'Are you sure you want to delete this tile?',
    icon: 'pi pi-exclamation-triangle',
    accept: () => {
      emits('close', i);
    },
    reject: () => {

    }
  });
};

const props = defineProps({
  title: { type: String, required: true },
  type: {
    type: String as PropType<Charts>,
    default: String,
  },
  i: { type: Number, required: true },
});

const emits = defineEmits(['close', 'update:data', 'draggable', 'edit']);
const visible = ref(false);
let chart = shallowRef<Object>();
// If this is changed, the chart component will be reloaded
let changed = shallowRef(0);
// Initalize chart if type is given
let component = props.type !== undefined ? props.type : Charts.NewChart;

function show() {
  visible.value = true;
}

function draggable(state: Boolean) {
  emits('draggable', state);
}

// Function to update the component / chart (e.g. change content)
async function change(data: KPIChange) {
  switch (data.action as KPIActions) {
    // Change component
    case KPIActions.ChangeComponent:
      chart.value = defineAsyncComponent(
        () => import(`@/components/charts/${data.component}`)
      );
      changed.value++;
      break;
    default:
      chart.value = defineAsyncComponent(
        () => import('@/components/charts/NewChart.vue')
      );
      changed.value++;
      break;
  }
}

change({ action: KPIActions.ChangeComponent, component: component });
</script>
<style scoped>
.tile {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

.tile-navbar {
  position: relative;
  display: flex;
  flex-grow: 1;
  text-align: left;
  width: 100%;
  left: 0;
  right: 0;

  h1 {
    font-size: 1.1rem;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    line-height: 2rem;
    color: rgb(99, 99, 99);
  }

  div {
    padding: 10px 0;
  }
}

.tile-content {
  position: relative;
  display: block;
  text-align: center;
  flex-grow: 9;
  width: 100%;
  height: 100%;
  padding: 0px 8px 16px 8px;
  margin: 0;
  background-color: #ffffff;
  overflow-y: auto;
  -ms-overflow-style: none;
  /* IE and Edge */
  scrollbar-width: none;
}


.tile-btn {
  width: 1.5rem;
  height: 1.5rem;
  font-size: 1rem;
  justify-content: center;
  text-align: center;

  &:hover {
    background-color: #e2e2e2;
    border-radius: 50%;
  }
}

.tile-footer {
  flex-grow: 1;
  padding-top: 0.8rem;
}

.exit-button {
<<<<<<< HEAD
    position: absolute;
    top: 0;
    right: 0;
    width: 50px;
    height: 50px;
    padding: 5px;
    color: var(--vue-tile-exit-button-color);
    cursor: pointer;
    z-index: 1000;
>>>>>>> 6b9f4b2 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
  position: absolute;
  top: 0;
  right: 0;
  width: 50px;
  height: 50px;
  padding: 5px;
  color: var(--vue-tile-exit-button-color);
  cursor: pointer;
  z-index: 1000;
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
}
</style>