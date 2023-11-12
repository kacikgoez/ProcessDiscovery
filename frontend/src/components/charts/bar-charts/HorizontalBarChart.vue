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
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  },
  series: [
    {
      name: 'Direct',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series',
      },
      data: [320, 302, 301, 334, 390, 330, 320],
    },
    {
      name: 'Mail Ad',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series',
      },
      data: [120, 132, 101, 134, 90, 230, 210],
    },
    {
      name: 'Affiliate Ad',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series',
      },
      data: [220, 182, 191, 234, 290, 330, 310],
    },
    {
      name: 'Video Ad',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series',
      },
      data: [150, 212, 201, 154, 190, 330, 410],
    },
    {
      name: 'Search Engine',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series',
      },
      data: [820, 832, 901, 934, 1290, 1330, 1320],
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
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  },
  series: [
    {
      name: 'Direct',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series',
      },
      data: [320, 302, 301, 334, 390, 330, 320],
    },
    {
      name: 'Mail Ad',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series',
      },
      data: [120, 132, 101, 134, 90, 230, 210],
    },
    {
      name: 'Affiliate Ad',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series',
      },
      data: [220, 182, 191, 234, 290, 330, 310],
    },
    {
      name: 'Video Ad',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series',
      },
      data: [150, 212, 201, 154, 190, 330, 410],
    },
    {
      name: 'Search Engine',
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series',
      },
      data: [820, 832, 901, 934, 1290, 1330, 1320],
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
