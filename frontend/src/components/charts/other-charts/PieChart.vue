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
    trigger: 'item',
    appendToBody: true,
  },
  appendToBody: true,
  legend: {
    orient: 'horizontal',
    left: 'top',
    textStyle: {
      color: '#555',
    },
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: '50%',
      data: [],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)',
        },
      },
    },
  ],
});


</script>
<style scoped>
* {
  cursor: pointer;
}
</style>
