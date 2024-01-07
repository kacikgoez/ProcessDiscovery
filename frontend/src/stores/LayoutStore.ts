import { KPITile } from '@/types';
import { defineStore } from 'pinia';
import { Ref, ref } from 'vue';

const layoutStore = defineStore('layout', () => {
    const layout : Ref<KPITile[]> = ref([])
    const changeRegister = ref(0);

    function registerChange(){
        changeRegister.value++;
    }

    function set(newLayout : KPITile[]) : void {
        layout.value = newLayout;
    }

    // Add a tile to the layout
    function add(tile : KPITile){
        layout.value.push(tile);
    }

    // Update the tile by array index
    function edit(index : number, newData : KPITile){
        Object.assign(layout.value[index], newData);
        // update to refresh the grid
        layout.value[index].changed += 1;
    }

    // Update the tile by array index
    function get(index : number ){
        return layout.value[index];
    }

    // Remove from the tile
    function remove(id : string){
        layout.value = layout.value.filter(tile => tile.i != id);
    }

    return { layout, set, add, edit, get, remove, registerChange}
});

export { layoutStore };
