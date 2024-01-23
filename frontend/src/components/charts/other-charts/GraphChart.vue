<template>
    <BaseChart :width="width" :height="height" :option="option" :request="request" :filters="filters"></BaseChart>
</template>
  
<script setup lang="ts">

const props = defineProps({
    request: { type: Object as PropType<ServerRequest>, required: true },
    width: { type: Number, required: true },
    height: { type: Number, required: true },
    filters: { type: Array as () => Filter[], required: true },
});

import BaseChart from '@/components/charts/BaseChart.vue';
import { Filter, ServerRequest } from '@/types';
import * as echarts from 'echarts';
import { PropType, Ref, ref } from 'vue';

const option: Ref<echarts.EChartsOption> = ref({
    tooltip: {
        // Enable tooltip
        show: true,
        // Custom formatter function
        formatter: function (params) {
            // Check if the hovered item is a link
            if (params.dataType === 'edge') {
                // Return the custom tooltip text
                // Here, it assumes your link has a property 'labelText' that holds the text you want to show
                return params.name + ': ' + params.value + ''
            }
            // Handle node tooltip or other types differently if needed
            return params.name; // Default display for nodes
        }
    },
    animationDurationUpdate: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [
        {
            type: 'graph',
            layout: 'none',
            symbolSize: 80,
            roam: false,
            label: {
                show: true
            },
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 10],
            edgeLabel: {
                fontSize: 15
            },
            data: [],
            links: [],
            lineStyle: {
                opacity: 0.9,
                width: 10,
                curveness: 0.05
            }
        }
    ]
});


</script>
<style scoped>
* {
    cursor: pointer;
}
</style>
