<script setup lang='ts'>
import {computed, PropType, Ref, ref, toRefs} from 'vue';
import {Filter, FilterOperators, PatientAttribute} from '@/types';
import SingleFilter from '@/components/input/SingleFilter.vue';
import {patientAttributesStore} from '@/stores/PatientAttributesStore';
import {storeToRefs} from 'pinia';

const store = patientAttributesStore();
const {attributes} = storeToRefs(store);

const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);
const selectAttributeOverlay = ref();

const filters = computed(() => {
  return (props.modelValue ?? []) as Filter[];
})

const showSelectAttribute = (event) => {
  selectAttributeOverlay.value.toggle(event);
}
const addFilter = (attribute: PatientAttribute) => {
  selectAttributeOverlay.value.hide();
  emit('update:modelValue', [...filters.value, {
    attribute: attribute,
    operator: FilterOperators.IS_NOT_EMPTY,
    value: null,
  }]);
}
</script>

<template>
  <div class="flex flex-row items-center justify-center gap-1">
    <div v-for="(filter, i) in filters" :key="i">
      <SingleFilter v-model="filters[i]" />
    </div>
    <Button label='Add filter' icon='pi pi-plus' severity="secondary" outlined @click='showSelectAttribute' aria-haspopup="true" aria-controls="overlay_panel" />
    <OverlayPanel ref="selectAttributeOverlay" appendTo="body" showCloseIcon class="overlay">
      <Listbox :options="attributes" filter optionLabel="name" class="w-full md:w-14rem" @update:modelValue="addFilter"/>
    </OverlayPanel>
  </div>
</template>

<style scoped>
.overlay {
  max-height: 25vh;
}
</style>