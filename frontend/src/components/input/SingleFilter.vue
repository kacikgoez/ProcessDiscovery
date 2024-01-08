<script setup lang='ts'>
import { Filter, FilterOperators } from '@/types';
import { PropType, computed, ref, watch } from 'vue';

const props = defineProps({
  modelValue: { type: Object as PropType<Filter>, required: true },
});
const emit = defineEmits(['update:modelValue']);

const editOverlay = ref();
const selectedOperator = ref<FilterOperators>(FilterOperators.IS_NOT_EMPTY);
const filterValue = ref();

const availableFilterOperators = computed(() => {
  if (props.modelValue?.attribute?.type == 'categorical') {
    return [
      FilterOperators.IS_NOT_EMPTY,
      FilterOperators.IS_EMPTY,
      FilterOperators.EQUALS,
      FilterOperators.NOT_EQUALS,
      FilterOperators.CONTAINS,
      FilterOperators.NOT_CONTAINS,
    ]
  } else {
    return [
      FilterOperators.IS_NOT_EMPTY,
      FilterOperators.IS_EMPTY,
      FilterOperators.EQUALS,
      FilterOperators.NOT_EQUALS,
      FilterOperators.GREATER_THAN,
      FilterOperators.GREATER_THAN_OR_EQUAL,
      FilterOperators.LESS_THAN,
      FilterOperators.LESS_THAN_OR_EQUAL,
    ]
  }
})

const inputType = computed(() => {
  switch (selectedOperator.value) {
    case FilterOperators.IS_NOT_EMPTY:
    case FilterOperators.IS_EMPTY:
      return 'none';
    case FilterOperators.EQUALS:
    case FilterOperators.NOT_EQUALS:
      return props.modelValue?.attribute?.type == 'categorical' ? 'dropdown' : 'number';
    case FilterOperators.CONTAINS:
    case FilterOperators.NOT_CONTAINS:
      return 'multiselect';
    case FilterOperators.GREATER_THAN:
    case FilterOperators.GREATER_THAN_OR_EQUAL:
    case FilterOperators.LESS_THAN:
    case FilterOperators.LESS_THAN_OR_EQUAL:
      return 'number';
    default:
      return 'none';
  }
})

const printFilterOperator = computed(() => {
  switch (selectedOperator.value) {
    case FilterOperators.IS_NOT_EMPTY:
      return 'is not empty';
    case FilterOperators.IS_EMPTY:
      return 'is empty';
    case FilterOperators.EQUALS:
    case FilterOperators.NOT_EQUALS:
    case FilterOperators.CONTAINS:
    case FilterOperators.NOT_CONTAINS:
      return '';
    case FilterOperators.GREATER_THAN:
      return '>';
    case FilterOperators.GREATER_THAN_OR_EQUAL:
      return '>=';
    case FilterOperators.LESS_THAN:
      return '<';
    case FilterOperators.LESS_THAN_OR_EQUAL:
      return '<=';
    default:
      return '';
  }
})
const printFilterValue = computed(() => {
  if (filterValue.value == null) {
    return '';
  }
  switch (selectedOperator.value) {
    case FilterOperators.IS_NOT_EMPTY:
    case FilterOperators.IS_EMPTY:
      return '';
    case FilterOperators.EQUALS:
    case FilterOperators.NOT_EQUALS:
    case FilterOperators.GREATER_THAN:
    case FilterOperators.GREATER_THAN_OR_EQUAL:
    case FilterOperators.LESS_THAN:
    case FilterOperators.LESS_THAN_OR_EQUAL:
      return filterValue.value;
    case FilterOperators.CONTAINS:
    case FilterOperators.NOT_CONTAINS:
      return trimString(filterValue.value.join(', '));
    default:
      return '';
  }
})

watch(inputType, (newValue, oldValue) => {
  if (newValue != oldValue) {
    filterValue.value = null;
  }
})

const trimString = (value: string) => {
  return value.length > 15 ? value.substring(0, 20) + '...' : value;
}
const showEditOverlay = (event) => {
  console.log(event)
  editOverlay.value.toggle(event);
}

watch(selectedOperator, (newValue, oldValue) => {
  if (newValue != oldValue && inputType.value == 'none') {
    emitUpdate();
  }
})

watch(filterValue, (newValue, oldValue) => {
  if (newValue != oldValue && newValue != '') {
    emitUpdate();
  }
})

const emitUpdate = () => {
  emit('update:modelValue', {
    ...props.modelValue,
    operator: selectedOperator.value,
    value: filterValue.value + '',
  });
}

const removal = (event) => {
  event.stopPropagation();
  emit('update:modelValue', {
    ...props.modelValue,
    operator: FilterOperators.NONE,
    value: null,
  });
}
</script>

<template>
  <div>
    <Chip removable @click="showEditOverlay" @remove="removal">
      <span class="font-semi-bold">{{ props.modelValue?.attribute.name }}:</span>
      <span class="ml-2">{{ printFilterOperator }}{{ printFilterValue }}</span>
    </Chip>
    <OverlayPanel ref="editOverlay" append-to="body" show-close-icon class="overlay">
      <Dropdown v-model="selectedOperator" :options="availableFilterOperators" placeholder="Select an operator"
        class="w-full md:w-14rem mb-2" />
      <InputNumber v-if="inputType == 'number'" v-model="filterValue" class="w-full md:w-14rem"
        :min="props.modelValue?.attribute.min" :max="props.modelValue?.attribute.max" />
      <Dropdown v-if="inputType == 'dropdown'" v-model="filterValue" :options="props.modelValue?.attribute.values" filter
        placeholder="Select a value" class="w-full md:w-14rem" />
      <MultiSelect v-if="inputType == 'multiselect'" v-model="filterValue" :options="props.modelValue?.attribute.values"
        filter placeholder="Select values" :max-selected-labels="3" class="w-full md:w-20rem" />
    </OverlayPanel>
  </div>
</template>

<style scoped></style>