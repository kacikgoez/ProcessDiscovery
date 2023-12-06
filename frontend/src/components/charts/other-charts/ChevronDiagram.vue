<template>
  <div class="inline-flex items-center justify-center">
    <div class="flex-1 mr-[5%]">
      <vertical-bar-chart :width="Math.min(propRefs.width.value * 0.15, 100)"
        :height="Math.min(propRefs.width.value * 0.15, 100)" />
    </div>
    <div class="flex-1">
      <div id="main" ref="chartDom" :style="{ width: propRefs.width.value }"></div>
    </div>
    <svg ref="svg" style="height: 0px; width: 0px;" :width="320" height="50" xmlns="http://www.w3.org/2000/svg">
      <path v-for="(name, i) in propRefs.names.value" :key="i" :ref="nameRefs[name]"
        d="M46 0 0 0 10 18 0 36 46 36 56 18 46 0z" :name="name" :transform="`translate(${(i) * 50}, 7)`" fill="blue" />
    </svg>
  </div>
</template>

<script setup lang="ts">
import { IDictionary } from '@/types';
import * as echarts from 'echarts';
import { PropType, Ref, onMounted, ref, toRefs, watch } from 'vue';
import VerticalBarChart from '../bar-charts/VerticalBarChart.vue';

const props = defineProps({
  names: { type: Array as PropType<string[]>, required: true },
  width: { type: Number, required: true },
  height: { type: Number, required: true },
});

const propRefs = toRefs(props);

const [chartDom, svg] = [
  ref(null),
  ref(null),
];

const nameRefs: IDictionary<Ref> = {};
const maxChevronWidth = 600;

console.log()
// Dynamically create refs for each name
propRefs.names.value.forEach((element) => {
  Object.assign(nameRefs, { [element]: ref(null) });
});

// Mapping of name to a color, consistent coloring
const colorPalette: IDictionary<string> = {
  REF: '#37A2DA',
  EVA: '#32C5E9',
  APP: '#67E0E3',
  AUT: '#9FE6B8',
  PRO: '#FFDB5C',
  TRA: '#ff9f7f',
};

onMounted(() => {
  // Add the above SVG in the template as ECharts map
  echarts.registerMap('chevron', { svg: svg.value! });
  var myChart = echarts.init(chartDom.value);

  // Rerenders the component and resets the option
  const render = (pWidth: number, pHeight: number | null = null) => {
    (option.geo.layoutSize = Math.min(pWidth, maxChevronWidth)),
      option && myChart.setOption(option);
    myChart.resize({
      width: pWidth,
      height: pHeight || pWidth / 6,
    });
  };

  // Inital resize needed for drawing
  render(propRefs.width.value * 0.8);

  // On resizing the tile, rerender the Apache ECharts
  watch([propRefs.width, propRefs.height], ([newWidth]) => {
    render(Math.min(newWidth * 0.8, maxChevronWidth));
  });
});

let regions = () => {
  let regArray: Object[] = [];
  propRefs.names.value.forEach((element, index) => {
    regArray.push({
      name: element,
      label: {
        show: true,
        position: 'inside',
      },
      itemStyle: {
        color: colorPalette[element],
        borderWidth: 0,
      },
      emphasis: {
        itemStyle: {
          color: colorPalette[element] + '88',
          borderWidth: 0,
        },
      },
    });
  });
  return regArray;
};

const option = {
  geo: {
    tooltip: {
      show: false
    },
    map: 'chevron',
    roam: false,
    layoutCenter: ['50%', '50%'],
    layoutSize: Math.min(propRefs.width.value, maxChevronWidth),
    regions: regions(),
  },
};
</script>
<style scoped>
* {
  cursor: pointer;
}
</style>
