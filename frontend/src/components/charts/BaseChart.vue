<template>
    <div class="overflow-hidden">
        <div id="main" ref="chartDom"></div>
    </div>
</template>

<script setup lang="ts">
import { theme } from '@/theme.js';
import { useElementSize } from '@vueuse/core';
import * as echarts from 'echarts';
import { PropType, computed, defineProps, onMounted, ref, toRefs, watch } from 'vue';


const props = defineProps({
    width: { type: Number, required: true },
    height: { type: Number, required: true },
    maxWidth: { type: Number, default: -1 },
    minWidth: { type: Number, default: -1 },
    scale: { type: Boolean, default: false },
    option: { type: Object as PropType<echarts.EChartsOption>, required: true },
});

const propRefs = toRefs(props);
const chartDom = ref(null);
let canvasSize: any = undefined;

const scaling = computed(() => {
    return (propRefs.width.value && canvasSize && canvasSize.width) ? Math.min(propRefs.width.value / canvasSize.width.value, 1) : '1';
});

onMounted(() => {
    // Initialize ECharts
    echarts.registerTheme('customed', theme);
    const myChart = echarts.init(chartDom.value);
    canvasSize = useElementSize(chartDom.value!.children[0]);

    // Render the inital chart
    myChart.setOption(props.option);
    myChart.resize({ width: propRefs.width.value, height: propRefs.height.value });

    watch(propRefs.option, (newOption) => {
        myChart.setOption(newOption);
    }, { deep: true });

    // Watch for changes and update the chart
    watch([propRefs.width, propRefs.height], ([newWidth, newHeight]) => {
        if (propRefs.maxWidth.value > 0 && newWidth > propRefs.maxWidth.value) return;
        if (propRefs.minWidth.value > 0 && newWidth < propRefs.minWidth.value) return;
        if (propRefs.scale.value) {
            return;
        }
        myChart.resize({ width: newWidth, height: newHeight });
    });
});

</script>

<style scoped>
.scale-with-max {
    scale: 2
}
</style>