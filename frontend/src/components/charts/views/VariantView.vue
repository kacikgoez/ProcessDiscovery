<template>
    <ChevronDiagram :key="update" :width="width" :height="height" :variants="variants" :request="request">
    </ChevronDiagram>
</template>

<script setup lang="ts">
import ChevronDiagram from '@/components/charts/other-charts/ChevronDiagram.vue';
import { ServerRequest } from '@/types';
import { PropType, onMounted, ref } from 'vue';

const props = defineProps({
    width: { type: Number, required: true },
    height: { type: Number, required: true },
    request: { type: Object as PropType<ServerRequest>, required: true },
});

const variants = ref([])
const update = ref(0);

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
        body: JSON.stringify({ disaggregation_attribute: props.request.disaggregation_attribute, }),
    }).then(response => response.json())
        .then(data => {
            variants.value = data;
            update.value += 1;
        });
}

</script>
<style scoped>
* {
    cursor: pointer;
}
</style>
