<template>
    <div class="kpi-new-tile-choose">
        <div class="kpi-choose-graph">
<<<<<<< HEAD
<<<<<<< HEAD
            <span class="kpi-icon material-symbols-outlined text-6xl cursor-pointer text-blue-400"
<<<<<<< HEAD
<<<<<<< HEAD
                @click="emit('change', { action: KPIActions.ChangeComponent, component: Charts.PieChart } as KPIChange)">
=======
=======
            <span
class="kpi-icon material-symbols-outlined text-6xl cursor-pointer text-blue-400"
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
            <span class="kpi-icon material-symbols-outlined text-6xl cursor-pointer text-blue-400"
>>>>>>> 143d6aa (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
                @click="$emit('change', { action: KPIActions.ChangeComponent, component: Charts.PieChart } as KPIChange)">
>>>>>>> 6b9f4b2 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
                @click="emit('change', { action: KPIActions.ChangeComponent, component: Charts.PieChart } as KPIChange)">
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
                bar_chart
            </span>
        </div>
        <div class="kpi-choose-chatpgt">
            <img class="kpi-icon" src="@/assets/chatgpt.svg">
        </div>
<<<<<<< HEAD
<<<<<<< HEAD
    </div>
</template>
<script setup lang="ts">

import { Charts, KPIActions, KPIChange } from '@/types';

const emit = defineEmits(['change']);
<<<<<<< HEAD
=======

=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
    </div>
</template>
<script setup lang="ts">

<<<<<<< HEAD
>>>>>>> 6b9f4b2 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
import { Charts, KPIActions, KPIChange } from '@/types';
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)

</script>
<style scoped>
.kpi-new-tile-choose {
    position: relative;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    gap: 30px;

    * {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .kpi-icon {
        width: var(--kpi-icon-width);
        height: var(--kpi-icon-height);
        filter: grayscale(0.3);
        cursor: pointer;
        animation: out 0.2s forwards;
    }

    .kpi-icon:hover {
        cursor: pointer;
        animation: in 0.5s forwards;
    }
}

@keyframes in {

    from {
        filter: grayscale(0.3);
        opacity: 0.4;
        cursor: pointer;
    }

    to {
        transform: var(--icon-hover-scale);
        filter: grayscale(0);
        opacity: 0.9;
        cursor: pointer;
    }

}

@keyframes out {

    from {
        transform: var(--icon-hover-scale);
        filter: grayscale(0);
        opacity: 0.9;
        cursor: pointer;
    }

    to {
        filter: grayscale(0.3);
        opacity: 0.4;
        cursor: pointer;
    }

}
</style>