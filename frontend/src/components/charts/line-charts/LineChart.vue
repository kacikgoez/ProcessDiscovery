<template>
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
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

<<<<<<< HEAD
<<<<<<< HEAD
const chart = {
    type: 'line',
    data: data,
    options: {
        bezierCurve: true,
        responsive: true,
        chartArea: {
            backgroundColor: "#fff"
        },
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            x: {
                grid: {
                    color: '#f0f0f0',
                    borderColor: '#f0f0f0'
                }
            },
            y: {
                grid: {
                    color: '#f0f0f0',
                    borderColor: '#f0f0f0'
                }
            }
        },
        devicePixelRatio: 1.2
    },
};


>>>>>>> 6b9f4b2 (Feature: ID-hGqw1FNt: add dashboard customization)

=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
</script>
<style scoped>
* {
<<<<<<< HEAD
  cursor: pointer;
=======
    cursor: pointer;
>>>>>>> 6b9f4b2 (Feature: ID-hGqw1FNt: add dashboard customization)
=======

</script>
<style scoped>
* {
  cursor: pointer;
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
}
</style>
