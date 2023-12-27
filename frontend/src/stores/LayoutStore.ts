import { KPITile } from '@/types';
import { defineStore } from 'pinia';
import { Ref, ref } from 'vue';

interface StateType {
    layout: KPITile[],
    changeRegister: Ref<number>
}

const layoutStore = defineStore('layout', {
    state: () : StateType => ({
        layout: [] as KPITile[],
        changeRegister: ref(0)
    }),
    getters: {
        getTile: (state) => (id: string) => {
            return state.layout.find((tile) => tile.i === id);
        }
    },
    actions: {
        addTile(tile: KPITile) {
            this.layout.push(tile);
        },
        removeTile(tile: KPITile) {
            const index = this.layout.indexOf(tile);
            this.layout.splice(index, 1);
        },
        updateTile(tile: KPITile) {
            const index = this.layout.indexOf(tile);
            this.layout.splice(index, 1, tile);
        },
        registerChange(){
            this.changeRegister++;
        }
    },
});

export { layoutStore };
