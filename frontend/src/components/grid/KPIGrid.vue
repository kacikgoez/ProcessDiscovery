<template>
    <grid-layout v-model:layout="layout" :col-num="12" :row-height="30" :is-draggable="true" :is-resizable="true"
        :responsive="true" :vertical-compact="true" :use-css-transforms="true">
        <grid-item v-for=" (item, index) in layout " :x="item.x" :y="item.y" :w="item.w" :h="item.h" :i="index"
            :key="item.title" style="border: 1px solid rgb(239, 239, 239);">
            <div class="tile-navbar">
                <h1>{{ item.title }}</h1>
                <div class="exit-button" @click="exit(item.i)">x</div>
            </div>
        </grid-item>
    </grid-layout>
</template>
<script setup lang="ts">

import { KPITile } from '@/types';
import { ref, defineProps, PropType, defineEmits } from 'vue';
import { GridLayout, GridItem } from 'vue3-grid-layout-next';

const props = defineProps({
    data: { type: Object as PropType<KPITile[]>, required: true }
})

const emits = defineEmits(['close'])

function exit(index: Number) {
    emits("close", index)
}

const layout = ref(props.data)

</script>
<style scoped>
.tile-navbar {
    position: relative;
    display: block;
    width: 100%;
    padding: 8px 0px;
}

.exit-button {
    position: absolute;
    right: 5px;
    top: 0px;
    padding: 5px;
    color: #c2c2c2;
    cursor: pointer;
}
</style>