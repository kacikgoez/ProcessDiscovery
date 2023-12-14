<template>
    <div class="inline-flex">
        <div id="main" ref="chartDom" :style="{ width: propRefs.width.value, height: propRefs.width.value }"></div>
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

defineEmits(['change']);

const propRefs = toRefs(props);

const [chartDom, svg] = [
    ref(null),
    ref(null),
];
const names = ref(['REF', 'EVA', 'APP', 'AUT', 'PRO', 'TRA']);
const nameRefs: IDictionary<Ref> = {};

// Dynamically create refs for each name
names.value.forEach((element) => {
    Object.assign(nameRefs, { [element]: ref(null) });
});

onMounted(() => {
    // Add the above SVG in the template as ECharts map
    echarts.registerMap('chevron', { svg: svg.value! });
    var myChart = echarts.init(chartDom.value);

    // Rerenders the component and resets the option
    const render = (pWidth: number, pHeight: number) => {
        option && myChart.setOption(option);
        (async () => {
            myChart.resize({
                width: pWidth,
                height: pHeight
            });
        })();
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