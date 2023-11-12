<template>
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
    <div>
        <div v-for="index in 1" :key="index">
            <ChevronDiagram :names="[Step.REF, Step.EVA, Step.APP, Step.AUT, Step.PRO, Step.TRA]" :width="width"
                :height="height">
            </ChevronDiagram>
        </div>
    </div>
<<<<<<< HEAD
</template>

<script setup lang="ts">
import ChevronDiagram from '@/components/charts/other-charts/ChevronDiagram.vue';
import { Step } from '@/types';

defineProps({
=======
    <div id="main" ref="chartDom"></div>
    <ChevronDiagram :names="[Step.REF, Step.EVA, Step.APP, Step.AUT, Step.PRO, Step.TRA]" :width="width" :height="height">
    </ChevronDiagram>
    <ChevronDiagram :names="[Step.AUT, Step.APP, Step.REF]" :width="width" :height="height"></ChevronDiagram>
    <ChevronDiagram :names="[Step.APP, Step.PRO]" :width="width" :height="height"></ChevronDiagram>
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
</template>

<script setup lang="ts">
import ChevronDiagram from '@/components/charts/other-charts/ChevronDiagram.vue';
import { Step } from '@/types';

<<<<<<< HEAD
let option: echarts.EChartsOption;
const chartDom = ref(null);
const props = defineProps({
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
defineProps({
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
    width: { type: Number, required: true },
    height: { type: Number, required: true },
});

<<<<<<< HEAD
<<<<<<< HEAD
=======
const propRefs = toRefs(props);


>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
</script>
<style scoped>
* {
    cursor: pointer;
}
<<<<<<< HEAD
<<<<<<< HEAD
</style>
=======
</style>
  
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
</style>
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
