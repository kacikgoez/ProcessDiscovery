import { defineStore } from 'pinia';
import { ref } from 'vue';

const modalStore = defineStore('modal', () => {
    const openModal = ref(false)
    const content = ref()

    function show(toShow) {
        openModal.value = true
        content.value = toShow
    }

    function hide() {
        openModal.value = false
    }

    return { show, hide }
});

export { modalStore };
