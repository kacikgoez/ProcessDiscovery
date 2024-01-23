<script setup lang='ts'>
import SingleFilter from '@/components/input/SingleFilter.vue';
import { patientAttributesStore } from '@/stores/PatientAttributesStore';
import {Filter, ProcessAttributes, FilterOperators, PatientAttribute} from '@/types';
import { storeToRefs } from 'pinia';
import { computed, ref } from 'vue';
import {prettyAttributeNames} from '@/util';

const store = patientAttributesStore();
const { attributes } = storeToRefs(store);

const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);
const selectAttributeOverlay = ref();

const filters = computed(() => {
  return ((props.modelValue ?? []) as Filter[])
})

const filterAttributes = computed(() => {
  return [
    {
      label: 'Patient attributes',
      items: attributes.value.map(attribute => {
        return {
          ...attribute,
          label: prettyAttributeNames(attribute.name)
        }
      })
    },
    {
      label: 'Process attributes',
      items: ProcessAttributes.map(attribute => {
        return {
          ...attribute,
          label: prettyAttributeNames(attribute.name)
        }
      })
    }
  ]
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

const removeFilter = (index: number) => {
  const newFilters = [...filters.value];
  newFilters.splice(index, 1);
  emit('update:modelValue', newFilters);
}

</script>

<template>
  <div class="outer-container overflow-x-auto">
    <div class="inner-container inline-flex justify-content-center">
      <Button class="inline-block overflow-visible flex-shrink-0" label="Add filter" icon="pi pi-plus"
        severity="secondary" outlined aria-haspopup="true" aria-controls="overlay_panel" @click="showSelectAttribute" />
      <div v-for="(filter, i) in filters" :key="i" class="inline-block flex-shrink-0 m-3">
        <SingleFilter v-model="filters[i]" @remove="removeFilter(i)" class="overflow-visible flex-shrink-0" />
      </div>
      <OverlayPanel ref="selectAttributeOverlay" append-to="body" show-close-icon class="inline-block overlay">
        <Listbox
            :options="filterAttributes" filter
            option-label="label"
            option-group-label="label"
            option-group-children="items"
            class="w-full md:w-14rem"
            list-style="max-height: 25vh;"
          @update:model-value="addFilter" />
      </OverlayPanel>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  max-height: 25vh;
}
</style>