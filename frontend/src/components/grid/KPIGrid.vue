<template>
    <grid-layout v-model:layout="layout" :col-num="12" :row-height="20" :is-resizable="true" :is-draggable="draggable"
        :vertical-compact="true" :use-css-transforms="false" :responsive="true">
        <grid-item v-for="item in layout" :id="`vue-tile-${item.i}`" :key="item.i" :x="item.x" :y="item.y" :w="item.w"
            :h="item.h" :i="item.i" :min-w="minWidth" :min-h="10" :is-draggable="draggable" @mousedown.prevent=""
            @resize="resizeEvent($event)">
            <KPIGridItem :title="item.title" :type="(item.type as Charts)" :i="(item.i as number)" @close="exit"
                @draggable="dragChange" @edit="emits('edit',)"></KPIGridItem>
        </grid-item>
    </grid-layout>
</template>

<script setup lang="ts">

import KPIGridItem from '@/components/grid/KPIGridItem.vue';
import type { Charts, KPITile } from '@/types';
import { PropType, Ref, defineEmits, defineProps, ref, toRef, watch } from 'vue';
import { GridItem, GridLayout } from 'vue3-grid-layout-next';

const props = defineProps({
    data: { type: Object as PropType<KPITile[]>, required: true }
})

// Min width of the items
const minWidth = ref(3);

// Toggle the draggable state of the grid
const draggable = ref(false)

// Parent layout prop and local prop, synced down below by watches
const layoutParent = toRef(props, 'data')
const layout: Ref<KPITile[]> = ref<KPITile[]>(props.data!)

const emits = defineEmits(['close', 'update:data', 'edit'])

function resizeEvent(event: string | number) {

}

function exit(index: Number): void {
    emits('close', index)
}

async function dragChange(state: boolean) {
    draggable.value = state
}

// Watch ensures parent changes are synced to child
// Skip first change (startup)

// FIXME: Possibly replaceable by defineModel? 
const startup = ref(true)
watch(layoutParent, async (newVal) => {
    if (startup.value) {
        startup.value = false
        return
    }
    layout.value = newVal
}, { deep: true })

/* Watch ensures child changes are synced to parent
    Example: change layout -> delete one of the items -> layout goes back to original state
*/
watch(layout, async (newVal) => {
    /* eslint-disable-next-line */
    emits('update:data', newVal)
}, { deep: true })


</script>


<style scoped></style>