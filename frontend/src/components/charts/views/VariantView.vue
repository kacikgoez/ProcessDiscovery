<template>
    <div>
        <div v-for="index in 1" :key="index">
            <ChevronDiagram :names="[Step.REF, Step.EVA, Step.APP, Step.AUT, Step.PRO, Step.TRA]" :width="width"
                :height="height">
            </ChevronDiagram>
        </div>
    </div>
</template>

<script setup lang="ts">
import ChevronDiagram from '@/components/charts/other-charts/ChevronDiagram.vue';
import { Step } from '@/types';

defineProps({
    width: { type: Number, required: true },
    height: { type: Number, required: true },
});

</script>
<style scoped>
* {
    cursor: pointer;
}
</style>
