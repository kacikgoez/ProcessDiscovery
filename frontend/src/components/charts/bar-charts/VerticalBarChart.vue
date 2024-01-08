<template>
    <BaseChart :width="width" :height="height" :option="option" :filters="filters"></BaseChart>
</template>

<script setup lang="ts">
import { Filter } from '@/types';


defineProps({
    width: { type: Number, required: true },
    height: { type: Number, required: true },
    filters: { type: Array as () => Filter[], required: true },
})

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