<template>
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
    <ChartSkeleton :chart="chart" :id="props.id"></ChartSkeleton>
=======
  <div id="main" ref="chartDom"></div>
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
  <BaseChart :width="width" :height="height" :option="option"></BaseChart>
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
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
<<<<<<< HEAD
    cursor: pointer;
>>>>>>> 6b9f4b2 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
  cursor: pointer;
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
}
</style>
