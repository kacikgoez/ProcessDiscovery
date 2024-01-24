<template>
    <Dialog :closable="true" v-model:visible="visibleProp" :draggable="false" class="modal-window" modal
        header="Help" :breakpoints="{ '1199px': '75vw', '575px': '90vw' }" :pt="{
            mask: {
                style: 'backdrop-filter: blur(2px); background-color: rgba(0, 0, 0, 0.2);'
            }
        }" @submit="close">
        <main>
          <p class="mt-2">You can restart the tour at any time by clicking the button below.</p>
          <Button class="primary" label="Restart Tour" @click="restartTour" />
          <p class="mt-2">You can also reset the dashboard to its default state by clicking the button below.</p>
          <Button class="danger" label="Reset Dashboard" @click="resetPopup($event)" />
        </main>
    </Dialog>
</template>

<script setup lang="ts">
import {visualTour} from '@/visual-tour';
import {ref, toRef, watch} from 'vue';
import {layoutStore} from '@/stores/LayoutStore';
import {globalFiltersStore} from '@/stores/GlobalFiltersStore';
import {useConfirm} from 'primevue/useconfirm';


const props = defineProps({
    visible: { type: Boolean, required: true },
})

const emit = defineEmits(['update:visible'])

const visibleArg = toRef(props, 'visible')
const visibleProp = ref(false)

const confirm = useConfirm();
const resetPopup = (event: Event) => {
  confirm.require({
    target: event.currentTarget as HTMLElement,
    message: 'Are you sure you want to reset the dashboard?',
    icon: 'pi pi-exclamation-triangle',
    accept: () => {
      layoutStore().$reset();
      globalFiltersStore().$reset();
      // Refresh the page to reset the dashboard
      location.reload();
    },
    reject: () => {

    }
  });
};

function restartTour() {
  close()
  visualTour.start()
}

function close() {
    visibleProp.value = false
}

watch(visibleProp, async (value) => {
    emit('update:visible', value)
})

watch(visibleArg, async (value) => {
    visibleProp.value = value
})

</script>
<style scoped>
</style>