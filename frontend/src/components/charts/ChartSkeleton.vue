<!-- 
    This defines a skeleton for charts, you can pass Chart.js params at :chart, which will directly feed into 
    "new Chart(...)" and display it using a canvas 
-->
<template>
    <div class="chart-wrapper">
        <div class="chart-item">
            <canvas :id="`chart-${props.id}`"></canvas>
        </div>
    </div>
</template>

<script setup>

import Chart from 'chart.js/auto';
import { defineProps, onMounted } from 'vue';

const props = defineProps({
    id: { type: Number, required: true },
    chart: { type: Object, required: true }
})

onMounted(() => {
    new Chart(document.getElementById(`chart-${props.id}`), props.chart);
});

</script>

<style scoped>
.chart-item {
    position: relative;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 0;
    height: 95%;
    padding: 0 8px;
}

.chart-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}

canvas {
    transition: width 10ms, height 10ms;
}
</style>
