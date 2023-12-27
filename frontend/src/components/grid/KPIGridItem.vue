<template>
  <div class="tile">
    <div class="tile-navbar">
      <div class="flex-[20] flex-shrink-0 ml-6" @mouseover="draggable(true)" @mouseleave="draggable(false)">
        <h1>{{ title }}</h1>
      </div>
      <div class="flex-1 mr-2">
        <span class="tile-btn material-symbols-outlined text-base cursor-pointer" @click="downloadVisualization">
          download
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
    </div>
    <div>
      <Filters v-model="filters"></Filters>
    </div>
    <div ref="tileContent" class="tile-content">
      <div class="overflow-y-auto overflow-x-hidden h-full">
        <component :is="chart" :id="props.i" :key="changed" :type="props.type" :width="width" :height="height"
          :filters="filters" :title="title" :request="requestRef" @change="change"></component>
      </div>
    </div>
    <div class="tile-footer">
    </div>
    <EditModal :id="props.i" v-model:visible="visible">

    </EditModal>
  </div>
</template>

<script setup lang="ts">
import {Charts, downloadVisualizationBusKey, KPIActions, KPIChange, ServerRequest} from '@/types';
import {useElementSize, useEventBus} from '@vueuse/core';
import { useConfirm } from 'primevue/useconfirm';
import {
  PropType,
  defineAsyncComponent,
  defineEmits,
  defineProps,
  onBeforeMount,
  ref,
  shallowRef,
  toRef
} from 'vue';
import Filters from '../input/Filters.vue';
import EditModal from '../modals/EditModal.vue';

const tileContent = ref(null);
const { width, height } = useElementSize(tileContent);
const requestRef = ref<ServerRequest>();

const downloadBus = useEventBus(downloadVisualizationBusKey);

const confirm = useConfirm();
const openPopup = (event: Event, i: string) => {
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
  request: { type: Object as PropType<ServerRequest>, required: true },
  type: {
    type: String as PropType<Charts>,
    default: String,
  },
  i: { type: String, required: true },
});

const filters = ref([]);

const emits = defineEmits(['close', 'update:data', 'draggable', 'edit']);
const visible = ref(false);
let chart = shallowRef<Object>();
// If this is changed, the chart component will be reloaded
const changed = shallowRef(0);
// Initalize chart if type is given
let component = props.type !== undefined ? props.type : Charts.NewChart;

const title = toRef(props, 'title');

onBeforeMount(() => {
  requestRef.value = props.request;
});

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

function downloadVisualization() {
  downloadBus.emit({
    id: props.i,
    title: props.title,
  });
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
}
</style>