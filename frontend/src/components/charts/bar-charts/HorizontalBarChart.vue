<template>
    <ChartSkeleton :chart="chart" :id="props.id"></ChartSkeleton>
</template>

<script setup>

import ChartSkeleton from '@/components/charts/ChartSkeleton.vue';
import { defineProps } from 'vue';

const props = defineProps({
    id: { type: Number, required: true }
})


const labels = ["January", "Feburary", "March", "April", "May", "June", "July"];
const data = {
    labels: labels,
    datasets: [
        {
            label: 'Dataset 1',
            data: [1, 2, 3, 4, 8, 6, 7],
            borderColor: "#6bccda",
            backgroundColor: "#6bccda",
        },
        {
            label: 'Dataset 2',
            data: [1, 2, 3, 4, 8, 6, 7],
            borderColor: "#0000ff",
            backgroundColor: "#0000ff",
        }
    ]
};

const chart = {
    type: 'bar',
    data: data,
    options: {
        indexAxis: 'y',
        // Elements options apply to all of the options unless overridden in a dataset
        // In this case, we are setting the border of each horizontal bar to be 2px wide
        elements: {
            bar: {
                borderWidth: 2,
            }
        },
        responsive: true,
        plugins: {
            legend: {
                display: false,
                position: 'bottom',
            }
        },
        scales: {
            x: {
                grid: {
                    color: '#f0f0f0',
                    borderColor: '#f0f0f0'
                }
            },
            y: {
                grid: {
                    color: '#f0f0f0',
                    borderColor: '#f0f0f0'
                }
            }
        },
    },
};



</script>
<style scoped>
* {
    cursor: pointer;
}
</style>
