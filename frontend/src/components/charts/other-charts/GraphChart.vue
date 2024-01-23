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
    title: {
        text: 'Basic Graph'
    },
    tooltip: {},
    animationDurationUpdate: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [
        {
            type: 'graph',
            layout: 'none',
            symbolSize: 50,
            roam: true,
            label: {
                show: true
            },
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 10],
            edgeLabel: {
                fontSize: 20
            },
            data: [
                // {
                //     name: 'Node 1',
                //     x: 300,
                //     y: 300
                // },
            ],
            // links: [],
            links: [
                {
                    source: 'Node 2',
                    target: 'Node 1',
                    label: {
                        show: true
                    },
                    lineStyle: {
                        curveness: 0.2
                    }
                },
            ],
            lineStyle: {
                opacity: 0.9,
                width: 2,
                curveness: 0
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
