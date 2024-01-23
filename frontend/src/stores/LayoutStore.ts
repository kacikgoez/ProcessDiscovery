import {Charts, EndpointURI, Filter, KPITile} from '@/types';
import { defineStore } from 'pinia';

interface StateType {
    layout: KPITile[],
    changeRegister: number
}

const defaultLayout: KPITile[] = [
  {
    title: 'A Pie Chart', type: Charts.PieChart, x: 0, y: 0, w: 4, h: 10, i: '0',
    changed: 0,
    request: {
      endpoint: EndpointURI.DISTRIBUTION,
      method: 'POST',
      disaggregation_attribute: {
        name: 'gender'
      },
      filters: [],
    },
  },
  {
    title: 'A Graph', type: Charts.Graph, x: 4, y: 0, w: 4, h: 10, i: '1',
    changed: 0,
    request: {
      endpoint: EndpointURI.DFG,
      method: 'POST',
      disaggregation_attribute: {
        name: 'gender'
      },
      filters: [],
    }
  },
  {
    title: 'A Horizontal Bar Chart', type: Charts.HorizontalBarChart, x: 4, y: 0, w: 4, h: 10, i: '2', changed: 0,
    request: {
      endpoint: EndpointURI.DISTRIBUTION,
      method: 'POST',
      disaggregation_attribute: {
        name: 'gender'
      },
      filters: []
    }
  },
  {
    title: 'Chevron Diagram using SVG & ECharts', type: Charts.VariantView, x: 0, y: 0, w: 4, h: 10, i: '3', changed: 0,
    request: {
      endpoint: EndpointURI.VARIANT,
      method: 'POST',
      disaggregation_attribute: {
        name: 'gender'
      },
      filters: [],
    }
  },
  {
    title: 'New Tile', type: Charts.NewChart, x: 8, y: 0, w: 4, h: 10, i: '4', changed: 0,
    request: {
      endpoint: EndpointURI.DISTRIBUTION,
      method: 'POST',
      disaggregation_attribute: {
        name: 'gender'
      },
      filters: [],
    },
  },
];

const layoutStore = defineStore('layout', {
    state: () : StateType => ({
        layout: defaultLayout,
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
            console.log(this.layout);
            (this.layout as KPITile[])[index].changed++;
        },
        registerChange(){
            this.changeRegister++;
        }
    },
    persist: true,
});

export { layoutStore };
