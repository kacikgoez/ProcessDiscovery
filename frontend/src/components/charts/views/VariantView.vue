<template>
    <div>
        <ChevronDiagram
            v-if="variants.length > 0"
            :width="width"
            :height="height"
            :variants="variants"
        >
        </ChevronDiagram>
      <ProgressSpinner v-else></ProgressSpinner>
    </div>
</template>

<script setup lang="ts">
import ProgressSpinner from 'primevue/progressspinner';
import ChevronDiagram from '@/components/charts/other-charts/ChevronDiagram.vue';
import {Variant} from '@/types';
import {onMounted, ref} from 'vue';

defineProps({
    width: { type: Number, required: true },
    height: { type: Number, required: true },
});

const variants = ref<Variant[]>([]);

onMounted(() => {
    fetchVariants();
});

function fetchVariants() {
    fetch('http://127.0.0.1:80/variants', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          'disaggregation_attribute': {
            'name': 'race'
          },
        }),
    }).then(response => response.json())
        .then(data => {
            variants.value = data;
        });
}

</script>
<style scoped>
* {
    cursor: pointer;
}
</style>
