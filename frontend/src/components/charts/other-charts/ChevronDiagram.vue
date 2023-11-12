<template>
<<<<<<< HEAD
<<<<<<< HEAD
  <div class="chart-container">
    <BaseChart :width="width" :height="calculatedHeight" :max-width="maximumWidth" :option="options"></BaseChart>
=======
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
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
  <div class="chart-container">
    <BaseChart :width="width" :height="calculatedHeight" :max-width="maximumWidth" :option="options"></BaseChart>
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
  </div>
</template>

<script setup lang="ts">
<<<<<<< HEAD
<<<<<<< HEAD

import BaseChart from '@/components/charts/BaseChart.vue';
import { IDictionary, colorPalette } from '@/types';
import * as echarts from 'echarts';
import { PropType, Ref, onBeforeMount, ref, toRefs, watch } from 'vue';

const props = defineProps({
  width: { type: Number, required: true },
  height: { type: Number, required: true },
  names: { type: Array as PropType<string[]>, required: true },
});

const propRefs = toRefs(props);
const calculatedHeight = ref(propRefs.height.value);
const maximumWidth = ref(600);

const options: Ref<echarts.EChartsOption> = ref({})
const chevronCounter = ref(0);
const nameRefs: IDictionary<Ref> = {};
const data2 = [
  120,
  {
    value: 200,
    itemStyle: {
      color: '#a90000'
    }
  },
  150,
];

=======
import { IDictionary } from '@/types';
=======

import BaseChart from '@/components/charts/BaseChart.vue';
import { IDictionary, colorPalette } from '@/types';
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
import * as echarts from 'echarts';
import { PropType, Ref, onBeforeMount, ref, toRefs, watch } from 'vue';

const props = defineProps({
  width: { type: Number, required: true },
  height: { type: Number, required: true },
  names: { type: Array as PropType<string[]>, required: true },
});

const propRefs = toRefs(props);
const calculatedHeight = ref(propRefs.height.value);
const maximumWidth = ref(600);

const options: Ref<echarts.EChartsOption> = ref({})
const chevronCounter = ref(0);
const nameRefs: IDictionary<Ref> = {};
const data2 = [
  120,
  {
    value: 200,
    itemStyle: {
      color: '#a90000'
    }
  },
  150,
];

<<<<<<< HEAD
const nameRefs: IDictionary<Ref> = {};
const maxChevronWidth = 600;

console.log()
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
// Dynamically create refs for each name
propRefs.names.value.forEach((element) => {
  Object.assign(nameRefs, { [element]: ref(null) });
});

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
// Calculate the sum of the array
const sum: number = data2.reduce((prev: number, current) => {
  const value = typeof current === 'object' ? current.value : current;
  return prev + value;
}, 0);
<<<<<<< HEAD

// Calculate the percentage of the maximum value
const max: number = data2.reduce((prev: number, current) => {
  const value: number = typeof current === 'object' ? current.value : current;
  return Math.max(prev, value);
}, 0);

const percentage: string = (sum !== 0) ? ((max / sum) * 100).toFixed(1) : '0';

const addChevron: (total: number) => echarts.SeriesOption[] = (total) => {
  // Increase the id counter
  chevronCounter.value++;
  // Generate custom SVG and add it to the ECharts map
  const svg = generateSVG()
  echarts.registerMap(`chevron_${chevronCounter.value}`, { svg: svg });
  const option: echarts.SeriesOption[] = [
    // Add the chevron chart
    {
      id: `chevron_${chevronCounter.value}`,
      type: 'map',
      tooltip: {
        show: false
      },
      label: {
        show: true,
        color: '#000',
        fontSize: '10',
        position: 'inside',
      },
      selectedMode: false,
      map: `chevron_${chevronCounter.value}`,
      roam: false,
      // place the chevrons in rows, evenly spaced, with the first one at the top (that's why - 0.5)
      layoutCenter: ['56%', `${(100 / total) * (chevronCounter.value - 0.5)}%`],
      // computed in render function
      layoutSize: 0,
      itemStyle: {
        borderWidth: 0,
        areaColor: '#fff',
        color: '#000'
      },
      data: generateDataArray(),
    },
    // Add the pie chart
    {
      name: `pie_${chevronCounter.value}`,
      id: `pie_${chevronCounter.value}`,
      center: ['10%', `${(100 / total) * (chevronCounter.value - 0.5)}%`],
      radius: ['9%', '12%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 1
      },
      label: {
        show: true,
        color: '#000',
        fontSize: '12',
        position: 'center',
        formatter: () => {
          return percentage + '%';
        }
      },
      labelLine: {
        show: false
      },
      data: [
        120,
        {
          value: 200,
          itemStyle: {
            color: '#a90000'
          }
        },
        150,
      ],
      type: 'pie'
    }];
  return option;
}

function generateSVG() {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('ref', 'svg');
  svg.setAttribute('style', 'height: 0px; width: 0px;');
  svg.setAttribute('width', '320');
  svg.setAttribute('height', '50');

  // Create and append paths
  propRefs.names.value.forEach((name, i) => {
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', 'M46 0 0 0 10 18 0 36 46 36 56 18 46 0z');
    path.setAttribute('ref', nameRefs[name].value);
    path.setAttribute('name', name);
    path.setAttribute('transform', `translate(${i * 50}, 7)`);
    path.setAttribute('fill', 'blue');
    svg.appendChild(path);
  });
  return svg;
}

function generateDataArray() {
  const data = Object.keys(colorPalette).map(key => ({
    name: key,
    itemStyle: { areaColor: colorPalette[key] + 'ee' },
    emphasis: { itemStyle: { areaColor: colorPalette[key] + '88' } },
  }));

  return data;
}

const generateOptions: () => [echarts.EChartsOption, number] = () => {
  const total: number = 25;
  const options: echarts.EChartsOption = {
    tooltip: {
      show: true,
      appendToBody: true
    },
    series: []
  };
  for (let i = 0; i < total; i++) {
    (options.series! as echarts.SeriesOption[]).push(...addChevron(total));
  }
  return [options, total];
}

onBeforeMount(() => {
  const [option,] = generateOptions();
  // Rerenders the component and resets the option
  options.value = option;

  (options.value.series! as echarts.SeriesOption[]).map((element) => Object.assign(element, { layoutSize: '80%' }));

  const render = (newWidth: number) => {
    calculatedHeight.value = (newWidth / 6) * chevronCounter.value;
  }

  render(propRefs.width.value);

  watch([propRefs.width,], ([newWidth]) => {
    // Needed, otherwise chevron scales indefinitely
    if (newWidth > maximumWidth.value) return;
    render(newWidth);
  });
});


=======
// Mapping of name to a color, consistent coloring
const colorPalette: IDictionary<string> = {
  REF: '#37A2DA',
  EVA: '#32C5E9',
  APP: '#67E0E3',
  AUT: '#9FE6B8',
  PRO: '#FFDB5C',
  TRA: '#ff9f7f',
};
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)

// Calculate the percentage of the maximum value
const max: number = data2.reduce((prev: number, current) => {
  const value: number = typeof current === 'object' ? current.value : current;
  return Math.max(prev, value);
}, 0);

const percentage: string = (sum !== 0) ? ((max / sum) * 100).toFixed(1) : '0';

const addChevron: (total: number) => echarts.SeriesOption[] = (total) => {
  // Increase the id counter
  chevronCounter.value++;
  // Generate custom SVG and add it to the ECharts map
  const svg = generateSVG()
  echarts.registerMap(`chevron_${chevronCounter.value}`, { svg: svg });
  const option: echarts.SeriesOption[] = [
    // Add the chevron chart
    {
      id: `chevron_${chevronCounter.value}`,
      type: 'map',
      tooltip: {
        show: false
      },
      label: {
        show: true,
        color: '#000',
        fontSize: '10',
        position: 'inside',
      },
      selectedMode: false,
      map: `chevron_${chevronCounter.value}`,
      roam: false,
      // place the chevrons in rows, evenly spaced, with the first one at the top (that's why - 0.5)
      layoutCenter: ['56%', `${(100 / total) * (chevronCounter.value - 0.5)}%`],
      // computed in render function
      layoutSize: 0,
      itemStyle: {
        borderWidth: 0,
        areaColor: '#fff',
        color: '#000'
      },
      data: generateDataArray(),
    },
    // Add the pie chart
    {
      name: `pie_${chevronCounter.value}`,
      id: `pie_${chevronCounter.value}`,
      center: ['10%', `${(100 / total) * (chevronCounter.value - 0.5)}%`],
      radius: ['9%', '12%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 1
      },
      label: {
        show: true,
        color: '#000',
        fontSize: '12',
        position: 'center',
        formatter: () => {
          return percentage + '%';
        }
      },
      labelLine: {
        show: false
      },
      data: [
        120,
        {
          value: 200,
          itemStyle: {
            color: '#a90000'
          }
        },
        150,
      ],
      type: 'pie'
    }];
  return option;
}

function generateSVG() {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('ref', 'svg');
  svg.setAttribute('style', 'height: 0px; width: 0px;');
  svg.setAttribute('width', '320');
  svg.setAttribute('height', '50');

  // Create and append paths
  propRefs.names.value.forEach((name, i) => {
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', 'M46 0 0 0 10 18 0 36 46 36 56 18 46 0z');
    path.setAttribute('ref', nameRefs[name].value);
    path.setAttribute('name', name);
    path.setAttribute('transform', `translate(${i * 50}, 7)`);
    path.setAttribute('fill', 'blue');
    svg.appendChild(path);
  });
  return svg;
}

function generateDataArray() {
  const data = Object.keys(colorPalette).map(key => ({
    name: key,
    itemStyle: { areaColor: colorPalette[key] + 'ee' },
    emphasis: { itemStyle: { areaColor: colorPalette[key] + '88' } },
  }));

  return data;
}

const generateOptions: () => [echarts.EChartsOption, number] = () => {
  const total: number = 25;
  const options: echarts.EChartsOption = {
    tooltip: {
      show: true,
      appendToBody: true
    },
    series: []
  };
  for (let i = 0; i < total; i++) {
    (options.series! as echarts.SeriesOption[]).push(...addChevron(total));
  }
  return [options, total];
}

onBeforeMount(() => {
  const [option,] = generateOptions();
  // Rerenders the component and resets the option
  options.value = option;

  (options.value.series! as echarts.SeriesOption[]).map((element) => Object.assign(element, { layoutSize: '80%' }));

  const render = (newWidth: number) => {
    calculatedHeight.value = (newWidth / 6) * chevronCounter.value;
  }

  render(propRefs.width.value);

  watch([propRefs.width,], ([newWidth]) => {
    // Needed, otherwise chevron scales indefinitely
    if (newWidth > maximumWidth.value) return;
    render(newWidth);
  });
});


<<<<<<< HEAD
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
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
</script>
<style scoped>
* {
  cursor: pointer;
}
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)

.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  /* Adjust as needed */
}
<<<<<<< HEAD
=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
</style>
