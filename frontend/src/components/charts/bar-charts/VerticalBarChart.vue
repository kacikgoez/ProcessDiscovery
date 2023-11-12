<template>
    <div class="inline-flex">
<<<<<<< HEAD
<<<<<<< HEAD
        <div id="main" ref="chartDom" :style="{ width: propRefs.width.value, height: propRefs.width.value }"></div>
=======
        <div id="main" ref="chartDom" :style="{ width: barChartWidth, height: barChartWidth }"></div>
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
        <div id="main" ref="chartDom" :style="{ width: propRefs.width.value, height: propRefs.width.value }"></div>
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
    </div>
</template>

<script setup lang="ts">
import { IDictionary } from '@/types';
import * as echarts from 'echarts';
import { Ref, onMounted, ref, toRefs, watch } from 'vue';

const props = defineProps({
    width: { type: Number, required: true },
    height: { type: Number, required: true },
});

<<<<<<< HEAD
<<<<<<< HEAD
defineEmits(['change']);

const propRefs = toRefs(props);

const [chartDom, svg] = [
    ref(null),
=======
=======
defineEmits(['change']);

>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
const propRefs = toRefs(props);

const [chartDom, svg] = [
    ref(null),
<<<<<<< HEAD
    ref(propRefs.width),
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
    ref(null),
];
const names = ref(['REF', 'EVA', 'APP', 'AUT', 'PRO', 'TRA']);
const nameRefs: IDictionary<Ref> = {};

// Dynamically create refs for each name
names.value.forEach((element) => {
    Object.assign(nameRefs, { [element]: ref(null) });
});

<<<<<<< HEAD
<<<<<<< HEAD
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

>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
onMounted(() => {
    // Add the above SVG in the template as ECharts map
    echarts.registerMap('chevron', { svg: svg.value! });
    var myChart = echarts.init(chartDom.value);

    // Rerenders the component and resets the option
    const render = (pWidth: number, pHeight: number) => {
        option && myChart.setOption(option);
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
        (async () => {
            myChart.resize({
                width: pWidth,
                height: pHeight
            });
        })();
<<<<<<< HEAD
=======
        myChart.resize({
            width: pWidth,
            height: pHeight
        });
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
    };

    // Inital resize needed for drawing
    render(propRefs.width.value, propRefs.height.value);

    // On resizing the tile, rerender the Apache ECharts
    watch([propRefs.width, propRefs.height], ([newWidth, newHeight]) => {
        render(newWidth, newHeight);
    });
});

const option = {
    tooltip: {
        show: true,
        appendToBody: true
    },
    avoidLabelOverlap: false,
    xAxis: {
        show: false,
        type: 'category',
        data: ['Mon', 'Tue', 'Wed']
    },
    yAxis: {
        show: false,
        min: 0,
        max: 200,
        type: 'value'
    },
    series: [
        {
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 1
            },
            label: {
                show: false,
                position: 'center'
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
        }
    ]
};
</script>
<style scoped>
* {
    cursor: pointer;
}
</style>