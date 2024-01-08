import { Filter, KPITile } from '@/types';
import { defineStore } from 'pinia';

interface StateType {
    layout: KPITile[],
    changeRegister: number
}

const layoutStore = defineStore('layout', {
    state: () : StateType => ({
        layout: [] as KPITile[],
        changeRegister: 0
    }),
    getters: {
        getTile: (state) => (id: string) => {
            return state.layout.find((tile) => tile.i === id);
        },
        getTileID: (state) => (id: string) => {
            const tile : KPITile | undefined = (state.layout as KPITile[]).find((tile) => tile.i === id);
            const index = tile ? (state.layout as KPITile[]).indexOf(tile) : -1;
            return index;
        }
    },
    actions: {
        addTile(tile: KPITile) {
            (this.layout as KPITile[]).push(tile);
        },
        removeTile(id: string | number) {
            this.layout = this.layout.filter(tile => tile.i != id);
        },
        updateTile(id: string | number, tile: Object) {
            const index = this.getTileID(id + '');
            console.log('update tile', id, tile, index)
            Object.assign((this.layout as KPITile[])[index], tile);
            // update to refresh the grid
            (this.layout as KPITile[])[index].changed++;
        },
        updateKPI(id: string | number, kpis: string[]) {
            const index = this.getTileID(id + '');
            Object.assign((this.layout as KPITile[])[index].request, { kpi: kpis});
            (this.layout as KPITile[])[index].changed++;
        },
        updateFilter(id: string | number, filters: Filter[]) {
            const index = this.getTileID(id + '');
            Object.assign((this.layout as KPITile[])[index].request, { filters: filters });
            (this.layout as KPITile[])[index].changed++;
        },
        registerChange(){
            this.changeRegister++;
        }
    },
});

export { layoutStore };
