import {PatientAttribute} from '@/types';
import {defineStore} from 'pinia';

const patientAttributesStore = defineStore('patient-attributes', {
    state: () => ({
        attributes: [] as PatientAttribute[],
    }),
    actions: {
        async fetchAttributes() {
            console.debug('Fetching patient attributes')
            const response = await fetch('http://127.0.0.1:80/patient-attributes', {
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
