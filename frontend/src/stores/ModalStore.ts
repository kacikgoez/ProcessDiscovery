import { ModalEvent } from '@/types';
import { defineStore } from 'pinia';
import { Component, ref } from 'vue';

const modalStore = defineStore('modal', () => {
    const modalVisible = ref(false)
    const content = ref()
    let eventBus : ((after : ModalEvent ) => void) | undefined  =  () => {}

    // Show the modal and activate the event bus
    function show(toShow : Component, callback : (after : ModalEvent ) => void) {
        modalVisible.value = true
        content.value = toShow
        eventBus = callback
    }

    function sendEvent(event : ModalEvent) {
        if(eventBus) eventBus(event)
    }

    // Close modal and unwatch the event bus
    function hide() {
        modalVisible.value = false
        content.value = null
        eventBus = undefined
    }

    return { modalVisible, content, sendEvent, show, hide }
});

export { modalStore };
