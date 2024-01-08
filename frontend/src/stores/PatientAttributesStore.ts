import { PatientAttribute } from '@/types';
import { defineStore } from 'pinia';

const patientAttributesStore = defineStore('patient-attributes', {
    state: () => ({
        attributes: [] as PatientAttribute[],
    }),
    actions: {
        async fetchAttributes() {
            console.debug('Fetching patient attributes')
            const response = await fetch(`//${window.location.hostname}/patient-attributes`, {
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                }
            });
            this.attributes = await response.json();
        }
    }
});

export { patientAttributesStore };
