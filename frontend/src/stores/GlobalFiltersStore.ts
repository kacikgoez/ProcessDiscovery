import {Filter} from '@/types';
import { defineStore } from 'pinia';

const globalFiltersStore = defineStore('global-filters', {
    state: () => ({
        filters: [] as Filter[],
    }),
});

export { globalFiltersStore };
