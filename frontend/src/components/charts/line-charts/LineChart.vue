<template>
    <div id="main" ref="chartDom"></div>
</template>

<script setup lang="ts">

import * as echarts from 'echarts';
import { onMounted, ref, toRefs, watch } from 'vue';

let option: EChartsOption;
const chartDom = ref(null);
const props = defineProps({
    width: { type: Number, required: true },
    height: { type: Number, required: true }
})

const propRefs = toRefs(props)

onMounted(() => {
    var myChart = echarts.init(chartDom.value);
    option && myChart.setOption(option)
    myChart.resize({
            width: props.width,
            height: props.height
        })

    watch([propRefs.width, propRefs.height], ([newWidth, newHeight]) => {
        myChart.resize({
            width: newWidth,
            height: newHeight
        })
    });

});

option = {
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [820, 932, 901, 934, 1290, 1330, 1320],
      type: 'line',
      smooth: true
    }
  ]
};

</script>
<style scoped>
* {
    cursor: pointer;
}
</style>
