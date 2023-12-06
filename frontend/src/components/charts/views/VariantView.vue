<template>
    <div id="main" ref="chartDom"></div>
    <ChevronDiagram :names="[Step.REF, Step.EVA, Step.APP, Step.AUT, Step.PRO, Step.TRA]" :width="width" :height="height">
    </ChevronDiagram>
    <ChevronDiagram :names="[Step.AUT, Step.APP, Step.REF]" :width="width" :height="height"></ChevronDiagram>
    <ChevronDiagram :names="[Step.APP, Step.PRO]" :width="width" :height="height"></ChevronDiagram>
</template>
  
<script setup lang="ts">
import ChevronDiagram from '@/components/charts/other-charts/ChevronDiagram.vue';
import { Step } from '@/types';
import * as echarts from 'echarts';
import { ref, toRefs } from 'vue';

let option: echarts.EChartsOption;
const chartDom = ref(null);
const props = defineProps({
    width: { type: Number, required: true },
    height: { type: Number, required: true },
});

const propRefs = toRefs(props);


</script>
<style scoped>
* {
    cursor: pointer;
}
</style>
  