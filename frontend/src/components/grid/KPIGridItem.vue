<template>
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
                <span class="tile-btn material-symbols-outlined text-base cursor-pointer">
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
    </div>
</template>
<script setup lang="ts">

import { Charts, KPIActions, KPIChange } from '@/types';
import { PropType, defineAsyncComponent, defineEmits, defineProps, ref } from 'vue';

const props = defineProps({
    title: { type: String, required: true },
    type: {
        type: String as PropType<Charts>
    },
    i: { type: Number, required: true }
})

const emits = defineEmits(['close', 'update:data', 'draggable'])

let chart: Object = ref()

// If this is changed, the chart component will be reloaded
let changed = ref(0)

// Initalize chart if type is given
let component = props.type !== undefined ? props.type : Charts.NewChart;
change({ action: KPIActions.ChangeComponent, component: component })

// Function to update the component / chart (e.g. change content)
async function change(data: KPIChange) {
    switch (data.action as KPIActions) {
        // Change component
        case KPIActions.ChangeComponent:
            chart = defineAsyncComponent(() => import(`@/components/charts/${data.component}`))
            changed.value++;
            break;
        // Load default component ("New KPI" = NewChart.vue)
        default:
            chart = defineAsyncComponent(() => import('@/components/charts/NewChart.vue'))
            changed.value++;
            break;
    }
}

function draggable(state: Boolean) {
    emits("draggable", state)
}

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
        font-family: 'Roboto', sans-serif;
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
    padding: 0 20px;
    margin: 0;
    background-color: #ffffff;
}

.tile-btn {
    width: 1.5rem;
    height: 1.5rem;
    font-size: 1.0rem;
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