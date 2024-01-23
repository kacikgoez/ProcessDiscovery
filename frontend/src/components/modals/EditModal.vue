<template>
    <Dialog :id="id" v-model:visible="visibleProp" :closable="true" :draggable="false" class="modal-window" modal
        header="Header" :style="modalStyle" :breakpoints="{ '1199px': '75vw', '575px': '90vw' }" :pt="{
            mask: {
                style: 'backdrop-filter: blur(2px); background-color: rgba(0, 0, 0, 0.2);'
            }
        }" @submit="close">
        <template #header>
            <input id="change-title" v-model="title" type="text">
            <Dropdown v-model="dis_attr" :options="PatientAttributeKeysList" option-label="name"
                placeholder="Select an attribute" class="w-full md:w-14rem" />
        </template>
        <main>

            <Listbox v-model="selectedChart" :multiple="true" :meta-key-selection="false" :options="Endpoints"
                option-label="label" option-group-label="label" option-group-children="items" class="w-full md:w-15rem"
                list-style="max-height:250px">
                <template #optiongroup="slotProps">
                    <div class="flex align-items-center bg-slate-50 m-0">
                        <span class="tile-btn material-symbols-outlined text-xxl cursor-pointer mr-3"
                            :style="{ color: slotProps.option.color.toLowerCase() }">
                            {{ slotProps.option.code.toLowerCase() }}
                        </span>
                        <div>{{ slotProps.option.label }}</div>
                    </div>
                </template>
            </Listbox>
        </main>
        <template #footer>
            <Button class="danger" label="Close" @click="close" />
            <Button class="primary" label="Save Tile" autofocus :disabled="disableConfirm" @click="confirm" />
        </template>
    </Dialog>
</template>
<script setup lang="ts">

import { layoutStore } from '@/stores/LayoutStore';
import { Charts, EndpointURI, Endpoints, ServerAttributes } from '@/types';
import Button from 'primevue/button';
import Listbox from 'primevue/listbox';
import { Ref, computed, ref, toRef, watch } from 'vue';

const props = defineProps({
    visible: { type: Boolean, required: true },
    id: { type: String, required: true }
})

const emit = defineEmits(['update:visible'])

const globalLayout = layoutStore();

const title = ref(globalLayout.getTile(props.id)!.title)

const visibleArg = toRef(props, 'visible')
const visibleProp = ref(false)
const id = toRef(props, 'id')

const dis_attr = ref('')

// Format patient-list JSON to list & remove hospital id
const PatientAttributeKeysList = Object.values(ServerAttributes).map((key) => {
    return {
        name: key.name.replaceAll('_', ' '),
        code: key.name,
    }
}).filter((key) => key.name !== 'hospital id')

const selectedChart: Ref<{ endpoint: string, value: string } | null> = ref()

const modalStyle = ref({
    width: '50rem',
    backgroundColor: '#fff',
    boxShadow: '0 0.5rem 1rem rgba(0, 0, 0, 0.15)',
    borderRadius: '1rem',
    overflow: 'hidden'
})

function close() {
    visibleProp.value = false
}

function confirm() {
    if (!selectedChart.value === null || !Array.isArray(selectedChart.value) || selectedChart.value.length == 0) return
    const editObj = { title: title.value, request: { endpoint: selectedChart.value![0].endpoint, disaggregation_attribute: { name: dis_attr.value.code } } };
    if (dis_attr.value.code == 'age') {
        Object.assign(editObj.request.disaggregation_attribute, { bins: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100] });
    } else if (editObj.request.disaggregation_attribute.bins) {
        delete editObj.request.disaggregation_attribute;
    }

    switch (selectedChart.value![0].endpoint) {
        case EndpointURI.KPI:
            Object.assign(editObj.request, { kpi: selectedChart.value!.map(item => item.value) });
            Object.assign(editObj, { type: Charts.HorizontalBarChart });
            break;
        case EndpointURI.DFG:
            Object.assign(editObj, { type: Charts.Graph });
            break;
        case EndpointURI.DISTRIBUTION:
            Object.assign(editObj, { type: selectedChart.value![0].value });
            break;
        case EndpointURI.VARIANT:
            Object.assign(editObj, { type: selectedChart.value![0].value });
            break;
    }
    globalLayout.updateTile(props.id, editObj)
    visibleProp.value = false
}

const disableConfirm = computed(() => {
    return !(!!selectedChart.value && title.value.trim().length > 0 && !!dis_attr.value.code)
})

watch(visibleProp, async (value) => {
    emit('update:visible', value)
})

watch(visibleArg, async (value) => {
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