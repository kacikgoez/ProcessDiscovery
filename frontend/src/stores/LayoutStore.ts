import { defineStore } from 'pinia';
import { ref } from 'vue';

const layoutStore = defineStore('layout', () => {
    const layout = ref(false)
    return { layout }
});

export { layoutStore };
