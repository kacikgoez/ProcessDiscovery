<template>
  <BaseChart :width="width" :height="height" :option="option" :filters="filters"></BaseChart>
</template>

<script setup lang="ts">

defineProps({
  width: { type: Number, required: true },
  height: { type: Number, required: true },
  filters: { type: Array as () => Filter[], required: true },
});

import BaseChart from '@/components/charts/BaseChart.vue';
import { Filter } from '@/types';
import * as echarts from 'echarts';
import { Ref, ref } from 'vue';

let option: Ref<echarts.EChartsOption>;

option = ref({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      // Use axis to trigger tooltip
      type: 'shadow', // 'shadow' as default; can also be 'line' or 'shadow'
    },
    appendToBody: true,
  },
  legend: {},
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true,
  },
  xAxis: {
    type: 'value',
  },
  yAxis: {
    type: 'category',
    data: [],
  },
  series: [
    {
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series',
      },
      data: [],
    },
  ],
});

</script>
<style scoped>
* {
  cursor: pointer;
}
</style>
