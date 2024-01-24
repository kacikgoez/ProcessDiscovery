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
    </div>
    <div ref="tileContent" class="tile-content">
      <Carousel v-if="isMultiKPI" class="overflow-y-auto overflow-x-hidden h-full" :value="requestRef.kpi"
        :num-visible="1" :num-scroll="1">
        <template #item="{ data }">
          <div class="overflow-y-auto overflow-x-hidden h-full">
            <component :is="chart" :id="props.i" :key="changed" :type="props.type" :width="width * 0.9"
              :height="height * 0.9" :filters="filters" :title="title" :request="requestRef" :kpi="data"
              @change="change">
            </component>
          </div>
        </template>
      </Carousel>
      <div v-else class="overflow-y-auto overflow-x-hidden h-full">
        <component :is="chart" :id="props.i" :key="changed" :type="props.type" :width="width" :height="height"
          :filters="filters" :title="title" :request="requestRef" @change="change"></component>
      </div>
    </div>
    <div class="tile-footer">
      <Filters :id="props.i" v-model="filters"></Filters>
    </div>
  </div>
</template>

<script setup lang="ts">
import { layoutStore } from '@/stores/LayoutStore';
import { Charts, downloadVisualizationBusKey, EndpointURI, Filter, KPIActions, KPIChange, ServerRequest } from '@/types';
import { useElementSize, useEventBus } from '@vueuse/core';
import { useConfirm } from 'primevue/useconfirm';
import {
  computed,
  defineAsyncComponent,
  defineEmits,
  defineProps,
  onBeforeMount,
  PropType,
  ref,
  shallowRef,
  toRef,
  watch
} from 'vue';
import Filters from '../input/Filters.vue';
import EditModal from '../modals/EditModal.vue';
import {globalFiltersStore} from '@/stores/GlobalFiltersStore';
import {useDialog} from 'primevue/usedialog';

const tileContent = ref(null);
const { width, height } = useElementSize(tileContent);
const requestRef = ref<ServerRequest>();

const downloadBus = useEventBus(downloadVisualizationBusKey);
const globalFilters = globalFiltersStore();

const confirm = useConfirm();
const dialog = useDialog();

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

const emits = defineEmits(['close', 'update:data', 'draggable', 'edit']);

// Filter component
const filters = ref(props.request.filters ?? []);

const isMultiKPI = computed(() => {
  return requestRef.value?.endpoint === EndpointURI.KPI && Array.isArray(requestRef.value?.kpi) && requestRef.value?.kpi.length > 1;
});

// Needed for deep watch, otherwise old val = new val
const globalLayout = layoutStore();
const visible = ref(false);

let chart = shallowRef<Object>();
// If this is changed, the chart component will be reloaded
const changed = shallowRef(0);
// Initalize chart if type is given
let component = props.type !== undefined ? props.type : Charts.NewChart;

const title = toRef(props, 'title');

onBeforeMount(() => {
  requestRef.value = props.request;

  watch(filters, (newVal, oldVal) => {
    globalLayout.updateFilter(props.i, filters.value as Filter[] || []);
    changed.value++;
  }, { deep: true });

  globalFilters.$subscribe((mutation, state) => {
    // Update filters if global filters are changed
    changed.value++;
  });
});

function show() {
  // visible.value = true;
  dialog.open(EditModal,{
    data: {
      id: props.i,
      visible: true
    }})
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
    title: props.title
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
  padding: 0px 8px 0px 8px;
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
  padding-top: 0;
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