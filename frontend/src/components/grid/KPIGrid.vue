<template>
    <grid-layout v-model:layout="layout" :col-num="12" :row-height="20" :is-resizable="true" :is-draggable="draggable"
        :vertical-compact="true" :use-css-transforms="false" :responsive="true">
        <grid-item v-for="item in layout" :id="`vue-tile-${item.i}`" :key="item.changed" :x="item.x" :y="item.y" :w="item.w"
            :h="item.h" :i="item.i" :min-w="minWidth" :min-h="10" :is-draggable="draggable" @mousedown.prevent="">
            <KPIGridItem :title="item.title" :request="item.request" :type="(item.type as Charts)" :i="item.i" @close="exit"
                @draggable="dragChange" @edit="emits('edit',)"></KPIGridItem>
        </grid-item>
    </grid-layout>
</template>

<script setup lang="ts">

import KPIGridItem from '@/components/grid/KPIGridItem.vue';
import { layoutStore } from '@/stores/LayoutStore';
import type { Charts } from '@/types';
import { storeToRefs } from 'pinia';
import { defineEmits, ref } from 'vue';
import { GridItem, GridLayout } from 'vue3-grid-layout-next';

// Min width of the items
const minWidth = ref(3);

// Toggle the draggable state of the grid
const draggable = ref(false)

// Parent layout prop and local prop, synced down below by watches
const globalLayout = layoutStore();
const { layout } = storeToRefs(globalLayout)

const emits = defineEmits(['close', 'edit'])

function exit(index: Number): void {
    emits('close', index)
}

async function dragChange(state: boolean) {
    draggable.value = state
}

</script>


<style scoped></style>