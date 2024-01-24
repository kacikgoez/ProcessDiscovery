<template>
    <Dialog :id="id" :visible="true" :closable="true" :draggable="false" class="modal-window" modal
        header="Header" :style="modalStyle" :breakpoints="{ '1199px': '75vw', '575px': '90vw' }" :pt="{
            mask: {
                style: 'backdrop-filter: blur(2px); background-color: rgba(0, 0, 0, 0.2);'
            }
        }" @submit="close">
        <template #header>
            <input id="change-title" v-model="title" type="text">
            <Dropdown v-model="selectedDisaggregationAttribute" :options="disaggregationAttributes" option-label="label"
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
                <template #option="item">
                    <div v-if="item.option.label === 'Dejure Process'">
                        {{ item.option.label }}
                        <!-- Dropdown with PrimeVue on the right -->
                        <Dropdown v-model="selectedStatistic" :options="Object.values(DejureStatisticType)"
                            placeholder="Select a statistic" class="w-full md:w-14rem" />
                    </div>
                    <div v-else>
                        {{ item.option.label }}
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
import {Charts, DejureStatisticType, EndpointURI, Endpoints, ServerAttributes, KPITile, EditModalEntry} from '@/types';
import Button from 'primevue/button';
import Listbox from 'primevue/listbox';
import {Ref, computed, ref, toRef, watch, inject, onMounted} from 'vue';
import {prettyAttributeNames} from '@/util';

const dialogRef = inject('dialogRef');
const globalLayout = layoutStore();

const id = ref();
const title = ref('')
const selectedDisaggregationAttribute = ref()
const selectedChart: Ref<EditModalEntry[] | null> = ref(null)
const selectedStatistic = ref();

const disaggregationAttributes = computed(() => {
    return Object.values(ServerAttributes)
    .filter((attr) => attr.name !== 'hospital_id')
    .map((attr) => {
      return {
        ...attr,
        label: prettyAttributeNames(attr.name),
      }
    });
})

onMounted(() => {
    id.value = dialogRef.value.data.id;
    const currentTile = globalLayout.getTile(id.value)!;

    if (currentTile.type == Charts.NewChart){
      return
    }

    title.value = currentTile.title;

    const currentDis = currentTile.request.disaggregation_attribute;
    selectedDisaggregationAttribute.value = disaggregationAttributes.value.find((attr) => attr.name === currentDis.name);

    const allEndpoints: EditModalEntry[] = Endpoints.flatMap((endpoint) => endpoint.items);
    selectedChart.value = allEndpoints.filter((endpoint) => {
      if (currentTile.request.kpi != null && endpoint.endpoint === EndpointURI.KPI) {
        return currentTile.request.kpi.includes(endpoint.value);
      } else {
        return endpoint.endpoint === currentTile.request.endpoint && endpoint.value === currentTile.type;
      }
    }) || null;
    selectedStatistic.value = currentTile.request.statistic || null;
})



const modalStyle = ref({
    width: '50rem',
    backgroundColor: '#fff',
    boxShadow: '0 0.5rem 1rem rgba(0, 0, 0, 0.15)',
    borderRadius: '1rem',
    overflow: 'hidden'
})

function close() {
  dialogRef.value.close();
}

function confirm() {
    if (!selectedChart.value === null || !Array.isArray(selectedChart.value) || selectedChart.value.length == 0) return
    const editObj = { title: title.value, request: { endpoint: selectedChart.value![0].endpoint, disaggregation_attribute: { name: selectedDisaggregationAttribute.value.name } } };

    if (selectedDisaggregationAttribute.value.name == 'age') {
        Object.assign(editObj.request.disaggregation_attribute, { bins: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100] });
    } else if (editObj.request.disaggregation_attribute.bins) {
        delete editObj.request.disaggregation_attribute;
    }

    switch (selectedChart.value![0].endpoint) {
        case EndpointURI.KPI:
            Object.assign(editObj.request, { kpi: selectedChart.value!.map(item => item.value) });
            Object.assign(editObj, { type: Charts.HorizontalBarChart });
            break;
        case EndpointURI.DEJURE:
            Object.assign(editObj.request, { statistic: selectedStatistic.value });
            Object.assign(editObj, { type: Charts.Graph });
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
    globalLayout.updateTile(id.value, editObj)
    dialogRef.value.close();
}

const disableConfirm = computed(() => {
    return !(selectedChart.value?.length > 0 && title.value.trim().length > 0 && !!selectedDisaggregationAttribute.value.name)
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