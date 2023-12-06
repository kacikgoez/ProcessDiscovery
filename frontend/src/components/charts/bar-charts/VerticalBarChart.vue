<template>
    <div class="inline-flex">
        <div id="main" ref="chartDom" :style="{ width: barChartWidth, height: barChartWidth }"></div>
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

const propRefs = toRefs(props);

const [chartDom, barChartWidth, svg] = [
    ref(null),
    ref(propRefs.width),
    ref(null),
];
const names = ref(['REF', 'EVA', 'APP', 'AUT', 'PRO', 'TRA']);
const nameRefs: IDictionary<Ref> = {};

// Dynamically create refs for each name
names.value.forEach((element) => {
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
    const render = (pWidth: number, pHeight: number) => {
        option && myChart.setOption(option);
        myChart.resize({
            width: pWidth,
            height: pHeight
        });
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