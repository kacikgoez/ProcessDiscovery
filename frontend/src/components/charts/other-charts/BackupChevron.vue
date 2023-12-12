<template>
    <div class="inline-flex items-center justify-center">
        <!-- <div class="flex-1 mr-[5%]">
        <vertical-bar-chart :width="propRefs.width.value * 0.15" :height="propRefs.width.value * 0.15" />
      </div> -->
        <div class="flex-1">
            <div id="main" ref="chartDom" :style="{ width: propRefs.width.value }"></div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { IDictionary, colorPalette } from '@/types';
import * as echarts from 'echarts';
import { PropType, Ref, onMounted, ref, toRefs, watch } from 'vue';

const props = defineProps({
    names: { type: Array as PropType<string[]>, required: true },
    width: { type: Number, required: true },
    height: { type: Number, required: true },
});

const chevronCounter = ref(0);
const propRefs = toRefs(props);

const [chartDom] = [
    ref(null),
];

const nameRefs: IDictionary<Ref> = {};
const maxChevronWidth = 600;

// Dynamically create refs for each name
propRefs.names.value.forEach((element) => {
    Object.assign(nameRefs, { [element]: ref(null) });
});

onMounted(() => {
    // Add the above SVG in the tepmplate as ECharts map
    const myChart = echarts.init(chartDom.value);
    const [option,]: [echarts.EChartsOption, number] = generateOptions()
    // Rerenders the component and resets the option
    const render = (pWidth: number,) => {

        // Iterate through all charts to add and set their size 
        (option.series! as echarts.SeriesOption[])
            .map((element) => Object.assign(element, { layoutSize: Math.min(pWidth * 0.8, maxChevronWidth) }));

        // Set the option and resize the chart
        option && myChart.setOption(option);
        (async () => {
            myChart.resize({
                width: pWidth,
                height: (pWidth / 6) * chevronCounter.value,
            })
        })();

    };

    // Inital resize needed for drawing
    render(propRefs.width.value);

    // On resizing the tile, rerender the Apache ECharts
    watch([propRefs.width, propRefs.height], ([newWidth]) => {
        render(Math.min(newWidth, maxChevronWidth));
    });
});

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

// Calculate the sum of the array
const sum: number = data2.reduce((prev: number, current) => {
    const value = typeof current === 'object' ? current.value : current;
    return prev + value;
}, 0);

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
            layoutCenter: ['56%', `${(95 / total) * (chevronCounter.value - 0.5)}%`],
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
            center: ['10%', `${(95 / total) * (chevronCounter.value - 0.5)}%`],
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
    const total: number = 10;
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

</script>
<style scoped>
* {
    cursor: pointer;
}
</style>
  