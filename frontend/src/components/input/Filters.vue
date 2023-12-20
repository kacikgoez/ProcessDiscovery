<script setup lang='ts'>
import {onMounted, PropType, ref} from 'vue';
import {Filter, PatientAttribute} from '@/types';
import SingleFilter from '@/components/input/SingleFilter.vue';

const filters = ref<Filter[]>([]);
const patientAttributes = ref<PatientAttribute[]>([]);
const selectAttributeOverlay = ref();
const selectedAttribute = ref(null);

onMounted(() => {
    fetchAttributes();
});

function fetchAttributes() {
    fetch('http://127.0.0.1:80/patient-attributes', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            patientAttributes.value = data;
            console.log(patientAttributes.value)
        });
}

const showSelectAttribute = (event) => {
  selectAttributeOverlay.value.toggle(event);
}
const addFilter = (attribute) => {
  selectAttributeOverlay.value.hide();
  filters.value.push({
    attribute: attribute,
    value: null,
  });
}
</script>

<template>
  <div class="flex flex-row items-center justify-center gap-1">
    <div v-for='filter in filters' :key='filter.attribute.name'>
      <SingleFilter :filter='filter' />
    </div>
    <Button label='Add filter' icon='pi pi-plus' severity="secondary" outlined @click='showSelectAttribute' aria-haspopup="true" aria-controls="overlay_panel" />
    <OverlayPanel ref="selectAttributeOverlay" appendTo="body" showCloseIcon class="overlay">
      <Listbox v-model="selectedCity" :options="patientAttributes" filter optionLabel="name" class="w-full md:w-14rem" @update:modelValue="addFilter"/>
    </OverlayPanel>
  </div>
</template>

<style scoped>
.overlay {
  max-height: 25vh;
}
</style>