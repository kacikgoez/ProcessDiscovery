<template>
    <div class="modal-background-wrapper fixed left-0 right-0 top-0 bottom-0 w-full h-full z-40 bg-black opacity-30 inline-block"
        v-show="openModal">
    </div>
    <div class="modal-window-wrapper flex items-center absolute left-0 top-0 w-full h-full" v-show="openModal">
        <div class="flex flex-1 flex-col items-center">
            <div class="block relative modal-window max-w-[1000px] w-full h-auto z-50 bg-white rounded-md pb-8">
                <div class="relative block w-full">
                    <span class="tile-btn material-symbols-outlined text-base cursor-pointer absolute right-1 top-1"
                        @click="exit" @open="open">
                        close
                    </span>
                </div>
                <div class="relative mt-[30px] max-w-[1000px] max-h-[700px] overflow-y-scroll">
                    <component :is="content" :key="content"></component>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>

import { modalStore } from '@/stores/ModalStore';
import { storeToRefs } from 'pinia';
import { onMounted, watch } from 'vue';

const store = modalStore();
const { openModal, content } = storeToRefs(store)

onMounted(() => {
    watch(openModal, (change,) => {
        /* eslint-disable */
        if (change) {
            open()
        } else {
            exit()
        }
    });
});

</script>

<style scoped></style>