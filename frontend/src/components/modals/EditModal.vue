<template>
    <Dialog v-model:visible="visibleProp" :closable="false" :title="title" :draggable="false" class="modal-window" modal
        header="Header" :style="modalStyle" :breakpoints="{ '1199px': '75vw', '575px': '90vw' }" :pt="{
            mask: {
                style: 'backdrop-filter: blur(2px); background-color: rgba(0, 0, 0, 0.2);'
            }
        }">
        <template #header>
            <input id="change-title" type="text" :value="title">
        </template>
        <main>
            <Dropdown v-model="endpoint" :options="charts" option-label="name" placeholder="Select an Endpoint"
                class="w-full md:w-14rem" />
            <Listbox v-model="selectedChart" :options="charts" filter option-label="name" class="w-full md:w-14rem"
                list-style="max-height:250px" filter-placeholder=" Search chart " />
        </main>
        <template #footer>
            <Button class="danger" label="Close" @click="closeModal" />
            <Button class="primary" label="Save Tile" />
        </template>
    </Dialog>
</template>
<script setup lang="ts">

import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';
import Listbox from 'primevue/listbox';
import { ref, toRef, watch } from 'vue';

const props = defineProps({
    visible: { type: Boolean, required: true },
    title: { type: String, required: true }
})

const emit = defineEmits(['update:visible'])
const visibleArg = toRef(props, 'visible')
const visibleProp = ref(false)
const title = toRef(props, 'title')
const selectedChart = ref('')
const endpoint = ref('')
const charts = ref([
    { name: 'Line Chart', code: 'line' },
    { name: 'Bar Chart', code: 'bar' },
    { name: 'Pie Chart', code: 'pie' },
    { name: 'Area Chart', code: 'area' },
    // Add more chart types as needed
]);

const modalStyle = ref({
    width: '50rem',
    backgroundColor: '#fff',
    boxShadow: '0 0.5rem 1rem rgba(0, 0, 0, 0.15)',
    borderRadius: '1rem',
    overflow: 'hidden'
})

function closeModal() {
    visibleProp.value = false
}

<<<<<<< HEAD
<<<<<<< HEAD
watch(visibleProp, async (value) => {
    emit('update:visible', value)
})

watch(visibleArg, async (value) => {
=======
watch(visibleProp, (value) => {
    emit('update:visible', value)
})

watch(visibleArg, (value) => {
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
watch(visibleProp, async (value) => {
    emit('update:visible', value)
})

watch(visibleArg, async (value) => {
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
    visibleProp.value = value
})

</script>
<style scoped>
.p-dropdown {
    border: 1px solid #ccc;
    margin: 0.25rem 0;
}

.p-dialog-content {
    padding-top: 0px;
}


#change-title {
    border: none;
    font-size: 1.5rem;
    font-weight: 600;
    width: 100%;
    padding: 0.5rem;
    margin-bottom: 0.25rem;
    line-height: 5px;
}
</style>