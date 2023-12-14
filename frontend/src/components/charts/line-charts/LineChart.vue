<template>
  <BaseChart :width="width" :height="height" :option="option"></BaseChart>
</template>

<script setup lang="ts">

import * as echarts from 'echarts';
import BaseChart from '../BaseChart.vue';

let option: echarts.EChartsOption;

defineProps({
  width: { type: Number, required: true },
  height: { type: Number, required: true }
})


option = {
  grid: {
    top: '10%',
    bottom: '10%'
  },
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
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
    }
  },
  series: [
    {
      data: [820, 932, 901, 934, 1290, 1330, 1320],
      type: 'line',
      smooth: true,
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            {
              offset: 0, color: '#409EFF'
            },
            {
              offset: 0.9, color: '#8975CB11'
            }
          ]
        }
      }
    }
  ]
};


</script>
<style scoped>
* {
  cursor: pointer;
}
</style>
