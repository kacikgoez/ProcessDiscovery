<template>
  <BaseChart :width="width" :height="height" :option="option" :filters="filters"></BaseChart>
</template>

<script setup lang="ts">

import { Filter } from '@/types';
import * as echarts from 'echarts';
import { Ref, ref } from 'vue';
import BaseChart from '../BaseChart.vue';


defineProps({
  width: { type: Number, required: true },
  height: { type: Number, required: true },
  filters: { type: Array as () => Filter[], required: true },
})

const option: Ref<echarts.EChartsOption> = ref({
  grid: {
    top: '10%',
    left: '15%',
    right: '5%',
    bottom: '10%'
  },
  tooltip: {
    trigger: 'axis',
    appendToBody: true,
  },
  xAxis: {
    type: 'category',
    data: [],
    axisLine: {
      lineStyle: {
        color: '#AAA'
      }
    },
    boundaryGap: false
  },
  yAxis: {
    type: 'value',
    axisLine: {
      lineStyle: {
        color: '#AAA'
      }
    },
  },
  series: [
    {
      data: [],
      type: 'line',
      smooth: true,
      // areaStyle: {
      //   color: {
      //     type: 'linear',
      //     x: 0,
      //     y: 0,
      //     x2: 0,
      //     y2: 1,
      //     colorStops: [
      //       {
      //         offset: 0, color: '#409EFF'
      //       },
      //       {
      //         offset: 0.9, color: '#8975CB11'
      //       }
      //     ]
      //   }
      // }
    }
  ]
});


</script>
<style scoped>
* {
  cursor: pointer;
}
</style>
