<template>
    <ChevronDiagram :key="update" :width="width" :height="height" :variants="variants" :request="request"
        :filters="filters">
    </ChevronDiagram>
</template>

<script setup lang="ts">
import ChevronDiagram from '@/components/charts/other-charts/ChevronDiagram.vue';
import { constructJson, Filter, ServerRequest } from '@/types';
import { onMounted, PropType, ref, toRefs, watch } from 'vue';

const props = defineProps({
    filters: { type: Array as () => Filter[], required: true },
    width: { type: Number, required: true },
    height: { type: Number, required: true },
    request: { type: Object as PropType<ServerRequest>, required: true },
});
const propRefs = toRefs(props);

const variants = ref([])
const update = ref(0);

onMounted(() => {
    fetchVariants();
});

watch(propRefs.filters, () => {
    fetchVariants();
}, { deep: true });

function fetchVariants() {
    fetch('http://127.0.0.1:80/variants', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ...constructJson(props.filters),
            'disaggregation_attribute': {
                'name': 'race'
            },
        }),
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
