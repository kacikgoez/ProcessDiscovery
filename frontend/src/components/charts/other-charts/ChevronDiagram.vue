<template>
  <BaseChart :key="propRefs.variants.value.length" :width="width" :height="calculatedHeight" :max-width="maximumWidth"
    :option="options" :filters="filters">
  </BaseChart>
</template>

<script setup lang="ts">

import BaseChart from '@/components/charts/BaseChart.vue';
import { activityNameEnumMap, colorPalette, Filter, IDictionary, Variant } from '@/types';
import * as echarts from 'echarts';
import { onMounted, PropType, Ref, ref, toRefs, watch } from 'vue';
import {capitalizeFirstLetter} from '@/util';

const props = defineProps({
  width: { type: Number, required: true },
  height: { type: Number, required: true },
  variants: { type: Object as PropType<Variant[]>, required: true },
  filters: { type: Array as () => Filter[], required: true },
});

const propRefs = toRefs(props);
const calculatedHeight = ref(propRefs.height.value);
const maximumWidth = ref(600);

const options: Ref<echarts.EChartsOption> = ref({})
const chevronCounter = ref(0);
const nameRefs: IDictionary<Ref> = {};

// Dynamically create refs for each name
Object.keys(colorPalette).forEach((element) => {
  Object.assign(nameRefs, { [element]: ref(null) });
});

const addChevron: (variant: Variant, total_count: number) => echarts.SeriesOption[] = (variant, total_count) => {
  // Increase the id counter
  chevronCounter.value++;
  // Generate custom SVG and add it to the ECharts map
  const svg = generateSVG(variant);
  echarts.registerMap(`chevron_${chevronCounter.value}`, { svg: svg });
  const option: echarts.SeriesOption[] = [
    // Add the chevron chart
    {
      id: `chevron_${chevronCounter.value}`,
      type: 'map',
      tooltip: {
        show: true,
        formatter: (e) => {
          return Object.keys(activityNameEnumMap).find(key => activityNameEnumMap[key] === e.name);
        },
        appendToBody: true,
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
      layoutCenter: ['57%', `${(100 / total_count) * (chevronCounter.value - 0.5)}%`],
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
      name: `Variant ${chevronCounter.value} - ${capitalizeFirstLetter(variant.distribution.name)}`,
      id: `pie_${chevronCounter.value}`,
      center: ['10%', `${(100 / total_count) * (chevronCounter.value - 0.5)}%`],
      radius: ['10%', '13%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 1
      },
      tooltip: {
        trigger: 'item',
        position: 'right',
      },
      label: {
        show: true,
        color: '#000',
        fontSize: '12',
        position: 'center',
        formatter: () => {
          return (variant.frequency * 100).toFixed(2) + '%';
        }
      },
      labelLine: {
        show: false
      },
      data: variant.distribution.data.map(entry => {
        return {
          name: entry.x,
          value: entry.y,
        }
      }),
      type: 'pie'
    }];
  return option;
}

function generateSVG(variant: Variant) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('ref', 'svg');
  svg.setAttribute('style', 'height: 0px; width: 0px;');
  svg.setAttribute('width', '320');
  svg.setAttribute('height', '50');

  // Create and append paths
  variant.activities.forEach((name, i) => {
    const activityEnum = activityNameEnumMap[name];
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', 'M46 0 0 0 10 18 0 36 46 36 56 18 46 0z');
    path.setAttribute('ref', nameRefs[activityEnum].value);
    path.setAttribute('name', activityEnum);
    path.setAttribute('transform', `translate(${i * 50}, 7)`);
    path.setAttribute('fill', 'blue');
    svg.appendChild(path);
  });
  return svg;
}

function generateDataArray() {
  return Object.keys(colorPalette).map(key => ({
    name: key,
    itemStyle: { areaColor: colorPalette[key] + 'ee' },
    emphasis: { itemStyle: { areaColor: colorPalette[key] + '88' } },
  }));
}

const generateOptions: () => [echarts.EChartsOption, number] = () => {
  const total: number = propRefs.variants.value.length;
  const option = {
    tooltip: {
      show: true,
      appendToBody: true
    },
    series: []
  }

  if (!Array.isArray(propRefs.variants.value)) return [option, total];

  for (const variant of propRefs.variants.value) {
    (option.series! as echarts.SeriesOption[]).push(...addChevron(variant, total));
  }
  return [option, total];
}

onMounted(() => {
  const [option,] = generateOptions();
  // Rerenders the component and resets the option
  options.value = option;

  (options.value.series! as echarts.SeriesOption[]).map((element) => element.layoutSize = '80%');

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


</script>
<style scoped>
* {
  cursor: pointer;
}
</style>
