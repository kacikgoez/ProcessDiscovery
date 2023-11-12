<template>
<<<<<<< HEAD
<<<<<<< HEAD
    <grid-layout v-model:layout="layout" :col-num="12" :row-height="20" :is-resizable="true" :is-draggable="draggable"
        :vertical-compact="true" :use-css-transforms="false" :responsive="true">
        <grid-item v-for="item in layout" :id="`vue-tile-${item.i}`" :key="item.i" :x="item.x" :y="item.y" :w="item.w"
            :h="item.h" :i="item.i" :min-w="minWidth" :min-h="10" :is-draggable="draggable" @mousedown.prevent=""
            @resize="resizeEvent($event)">
            <KPIGridItem :title="item.title" :type="(item.type as Charts)" :i="(item.i as number)" @close="exit"
                @draggable="dragChange" @edit="emits('edit',)"></KPIGridItem>
=======
    <grid-layout v-model:layout="layout" :col-num="12" :row-height="20" :is-resizable="true" :responsive="true"
        :is-draggable="draggable" :vertical-compact="true" :use-css-transforms="false">
<<<<<<< HEAD
        <grid-item v-for="item in layout" :id="`vue-tile-${item.i}`" :x="item.x" :y="item.y" :w="item.w" :h="item.h"
            :i="item.i" :key="item.i" :min-w="minWidth" min-h="10" :is-draggable="draggable" @mousedown.prevent="">
<<<<<<< HEAD
            <KPIGridItem :title="item.title" :type="(item.type as Charts)" :i="item.i" @close="exit"
                @draggable="dragChange"></KPIGridItem>
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
=======
        <grid-item v-for="item in layout" :id="`vue-tile-${item.i}`" :key="item.i" :x="item.x" :y="item.y" :w="item.w"
            :h="item.h" :i="item.i" :min-w="minWidth" :min-h="10" :is-draggable="draggable" @mousedown.prevent="">
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
            <KPIGridItem :title="item.title" :type="(item.type as Charts)" :i="item.i" @close="exit" @draggable="dragChange"
                @edit="emits('edit',)"></KPIGridItem>
>>>>>>> 7e18e45 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
    <grid-layout v-model:layout="layout" :col-num="12" :row-height="20" :is-resizable="true" :is-draggable="draggable"
        :vertical-compact="true" :use-css-transforms="false" :responsive="true">
        <grid-item v-for="item in layout" :id="`vue-tile-${item.i}`" :key="item.i" :x="item.x" :y="item.y" :w="item.w"
            :h="item.h" :i="item.i" :min-w="minWidth" :min-h="10" :is-draggable="draggable" @mousedown.prevent=""
            @resize="resizeEvent($event)">
            <KPIGridItem :title="item.title" :type="(item.type as Charts)" :i="(item.i as number)" @close="exit"
                @draggable="dragChange" @edit="emits('edit',)"></KPIGridItem>
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
        </grid-item>
    </grid-layout>
</template>

<script setup lang="ts">

import KPIGridItem from '@/components/grid/KPIGridItem.vue';
import type { Charts, KPITile } from '@/types';
<<<<<<< HEAD
<<<<<<< HEAD
import { PropType, Ref, defineEmits, defineProps, ref, toRef, watch } from 'vue';
=======
import { PropType, defineEmits, defineProps, nextTick, ref, toRef, watch } from 'vue';
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
import { PropType, Ref, defineEmits, defineProps, ref, toRef, watch } from 'vue';
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
import { GridItem, GridLayout } from 'vue3-grid-layout-next';

const props = defineProps({
    data: { type: Object as PropType<KPITile[]>, required: true }
})

<<<<<<< HEAD
<<<<<<< HEAD
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
=======
=======
// Min width of the items
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
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
<<<<<<< HEAD
    await nextTick();
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
}

// Watch ensures parent changes are synced to child
// Skip first change (startup)

// FIXME: Possibly replaceable by defineModel? 
const startup = ref(true)
<<<<<<< HEAD
<<<<<<< HEAD
watch(layoutParent, async (newVal) => {
=======
watch(layoutParent, (newVal) => {
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
watch(layoutParent, async (newVal) => {
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
    if (startup.value) {
        startup.value = false
        return
    }
    layout.value = newVal
}, { deep: true })

/* Watch ensures child changes are synced to parent
    Example: change layout -> delete one of the items -> layout goes back to original state
*/
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
watch(layout, async (newVal) => {
    /* eslint-disable-next-line */
    emits('update:data', newVal)
=======
watch(layout, (newVal) => {
<<<<<<< HEAD
    emits("update:data", newVal)
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
    /* eslint-disable-next-line */
    emits('update:data', newVal)
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
}, { deep: true })


</script>


<style scoped></style>