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
            backgroundColor: "#ffffff",
        },
        {
            label: 'Dataset 2',
            data: [1, 2, 3, 4, 8, 6, 7],
            borderColor: "#0000ff",
            backgroundColor: "#ffffff",
        }
    ]
};

const chart = {
    type: 'line',
    data: data,
    options: {
        bezierCurve: true,
        responsive: true,
        chartArea: {
            backgroundColor: "#fff"
        },
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            x: {
                border: {
                    display: false
                },
                grid: {
                    color: function () {
                        return '#ddd';
                    },
                },
            },
            y: {
                border: {
                    display: false
                },
                grid: {
                    color: function () {
                        return '#ddd';
                    },
                },
            }
        }
    },
};



</script>
<style scoped>
* {
    cursor: pointer;
}
</style>
