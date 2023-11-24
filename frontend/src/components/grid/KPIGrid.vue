<template>
    <grid-layout v-model:layout="layout" :col-num="12" :row-height="20" :is-resizable="true" :responsive="true"
        :is-draggable="draggable" :vertical-compact="true" :use-css-transforms="false">
        <grid-item v-for="item in layout" :id="`vue-tile-${item.i}`" :x="item.x" :y="item.y" :w="item.w" :h="item.h"
            :i="item.i" :key="item.i" :min-w="minWidth" min-h="10" :is-draggable="draggable" @mousedown.prevent="">
            <KPIGridItem :title="item.title" :type="(item.type as Charts)" :i="item.i" @close="exit" @draggable="dragChange"
                @edit="emits('edit',)"></KPIGridItem>
        </grid-item>
    </grid-layout>
</template>

<script setup lang="ts">

import KPIGridItem from '@/components/grid/KPIGridItem.vue';
import type { Charts, KPITile } from '@/types';
import { PropType, defineEmits, defineProps, nextTick, ref, toRef, watch } from 'vue';
import { GridItem, GridLayout } from 'vue3-grid-layout-next';

const props = defineProps({
    data: { type: Object as PropType<KPITile[]>, required: true }
})

const minWidth = ref(3);

const draggable = ref(false)

// Parent layout prop and local prop, synced down below by watches
const layoutParent = toRef(props, "data")
const layout = ref(props.data)

const emits = defineEmits(['close', 'update:data', 'edit'])

function exit(index: Number): void {
    emits("close", index)
}

async function dragChange(state: Boolean) {
    draggable.value = state
    await nextTick();
}

// Watch ensures parent changes are synced to child
// Skip first change (startup)

// FIXME: Possibly replaceable by defineModel? 
const startup = ref(true)
watch(layoutParent, (newVal) => {
    if (startup.value) {
        startup.value = false
        return
    }
    layout.value = newVal
}, { deep: true })

/* Watch ensures child changes are synced to parent
    Example: change layout -> delete one of the items -> layout goes back to original state
*/
watch(layout, (newVal) => {
    emits("update:data", newVal)
}, { deep: true })


</script>


<style scoped></style>