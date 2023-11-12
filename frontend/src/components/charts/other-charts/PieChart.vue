<template>
    <ChartSkeleton :chart="chart" :id="props.id"></ChartSkeleton>
</template>

<script setup>

import ChartSkeleton from '@/components/charts/ChartSkeleton.vue';
import { defineProps, onMounted } from 'vue';

const props = defineProps({
    id: { type: Number, required: true }
})

onMounted(() => {
    const pieChart = document.querySelector(`*[id="chart-${props.id}"]`);
    pieChart.style.display = 'none';

    setTimeout(() => {
        pieChart.style.display = 'block';
    }, 100);
})

const labels = ["Africa", "Asia", "Europe", "Latin America", "North America"];

const chart = {
    type: 'pie',
    data: {
        labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
        datasets: [
            {
                label: "Population (millions)",
                backgroundColor: labels.map((label, index) => {
                    const hue = (index / labels.length) * 360;
                    let saturation = 100;
                    let lightness = 75;
                    let alpha = 0.9;

                    // Adjust saturation and lightness for yellows and turquoises
                    if ((hue >= 45 && hue <= 90) || (hue >= 160 && hue <= 210)) {
                        saturation = 90; // Make yellows and turquoises darker by reducing saturation
                        lightness = 75;  // Adjust lightness to make them darker
                    }

                    return `hsla(${hue}, ${saturation}%, ${lightness}%, ${alpha})`;

                    //return `hsla(200, ${50 + 40 * index / labels.length}%, ${60 + 40 * index / labels.length}%, 1)`;
                }),

                data: [2478, 5267, 734, 784, 433]
            }
        ]
    },
    options: {
        plugins: {
            legend: {
                display: false,
                position: 'bottom',
                align: 'left',
                labels: {
                    fontColor: '#000'
                }
            },
        },
        title: {
            display: true,
            text: 'Predicted world population (millions) in 2050'
        },
        animation:
        {
            duration: 1000
        }
    }
};

</script>
<style scoped>
* {
    cursor: pointer;
}
</style>
