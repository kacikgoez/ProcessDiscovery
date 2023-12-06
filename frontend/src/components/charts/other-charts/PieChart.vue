<template>
  <div id="main" ref="chartDom"></div>
</template>

<script setup lang="ts">
import * as echarts from 'echarts';
import { onMounted, ref, toRefs, watch } from 'vue';

let option: echarts.EChartsOption;
const chartDom = ref(null);
const props = defineProps({
  width: { type: Number, required: true },
  height: { type: Number, required: true },
});

const propRefs = toRefs(props);

onMounted(() => {
  var myChart = echarts.init(chartDom.value);
  option && myChart.setOption(option);
  myChart.resize({
    width: props.width,
    height: props.height,
  });

  watch([propRefs.width, propRefs.height], ([newWidth, newHeight]) => {
    myChart.resize({
      width: newWidth,
      height: newHeight,
    });
  });
});

option = {
  tooltip: {
    trigger: 'item',
  },
  appendToBody: true,
  legend: {
    orient: 'horizontal',
    left: 'top',
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
