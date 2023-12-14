<template>
  <BaseChart :width="width" :height="height" :option="option"></BaseChart>
</template>

<script setup lang="ts">

defineProps({
  width: { type: Number, required: true },
  height: { type: Number, required: true },
});

import BaseChart from '@/components/charts/BaseChart.vue';
import * as echarts from 'echarts';

let option: echarts.EChartsOption;

option = {
  tooltip: {
    trigger: 'item',
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
      data: [
        { value: 1048, name: 'Search Engine' },
        { value: 735, name: 'Direct' },
        { value: 580, name: 'Email' },
        { value: 484, name: 'Union Ads' },
        { value: 300, name: 'Video Ads' },
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)',
        },
      },
    },
  ],
};


</script>
<style scoped>
* {
  cursor: pointer;
}
</style>
