/*
* Central file for all the relevant types. 
*/
import { LayoutItem } from 'vue3-grid-layout-next/dist/helpers/utils';

// Chart must be named like file in /charts, so PieChart.vue -> PieChart
export enum Charts {
    PieChart = 'other-charts/PieChart',
    LineChart = 'line-charts/LineChart',
    HorizontalBarChart = 'bar-charts/HorizontalBarChart',
    ChevronDiagram = 'other-charts/ChevronDiagram',
    VariantView = 'views/VariantView',
    NewChart = 'NewChart.vue',
}

export enum Step {
    REF = 'REF',
    EVA = 'EVA',
    APP = 'APP',
    AUT = 'AUT',
    PRO = 'PRO',
    TRA = 'TRA'
}

/* ------------- KPI ---------------- */ 

export enum KPIActions {
    ChangeComponent
}

export type KPIChange = {
    action: KPIActions.ChangeComponent,
    component: Charts
};

export type KPITile = {
    title: string,
    type: Charts,
    endpoint: String,
} & LayoutItem;

export type CategoricalAttribute = {
    name: String,
    type: 'categorical',
    values: String[]
}

export type NumericalAttribute = {
    name: String,
    type: 'numerical',
    min: Number,
    max: Number,
    groups: Interval[]
}

export type Interval = {
    lower: Number,
    upper: Number
}

export type PatientAttribute = CategoricalAttribute | NumericalAttribute

/* ------------- Modal ---------------- */ 

export interface ModalEvent {
    name: string,
    data: Object
}

export interface EditModal {
    name: string,
    chart: Charts
}

/* ------------- General Types ---------------- */

export interface IDictionary<TValue> {
    [id: string]: TValue;
}


/* ------------- Chart Data Types ---------------- */

export type Distribution = {
    data: {
        name: string,
        value: number
    }[]
}

export type TimeSeries = {
    data: {
        name: string,
        value: number
    }[]
}

/* ------------- Patient Data Types ---------------- */

// Mapping of name to a color, consistent coloring
export const colorPalette: IDictionary<string> = {
    REF: '#37A2DA',
    EVA: '#32C5E9',
    APP: '#67E0E3',
    AUT: '#9FE6B8',
    PRO: '#FFDB5C',
    TRA: '#ff9f7f',
};
