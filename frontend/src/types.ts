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

export type Graph = {
    name: string,
    edges: Edge[],
    nodes: Node[]
}

export type Edge = {
    source: string,
    target: string,
    label: string,
    value: number
}

export type Node = {
    id: string,
    label: string,
    value: number
}

export type DataSeries = {
    name: string,
    data: ({
        x: string,
        y: number
    }[]) | ({
        x: number,
        y: number
    }[])
}

export type MultiDataSeries = {
    data: DataSeries[]
}
/* ------------- Patient Data Types ---------------- */

// Activity names in the order they appear in the data
export enum Activity {
    REF = 'REF',
    EVA = 'EVA',
    APP = 'APP',
    AUT = 'AUT',
    PRO = 'PRO',
    TRA = 'TRA',
}

export const activityNameEnumMap = {
    'Referral': Activity.REF,
    'Evaluation': Activity.EVA,
    'Approach': Activity.APP,
    'Authorization': Activity.AUT,
    'Procurement': Activity.PRO,
    'Transplant': Activity.TRA,
}

// Mapping of name to a color, consistent coloring
export const colorPalette: IDictionary<string> = {
    REF: '#37A2DA',
    EVA: '#32C5E9',
    APP: '#67E0E3',
    AUT: '#9FE6B8',
    PRO: '#FFDB5C',
    TRA: '#ff9f7f',
};

export type Variant = {
    id: number,
    activities: string[],
    count: number,
    frequency: number,
    distribution: IDictionary<number>,
}

export type CategoricalAttribute = {
    name: string,
    type: 'categorical',
    values: string[]
}

export type NumericalAttribute = {
    name: string,
    type: 'numerical',
    min: number,
    max: number,
}

export type PatientAttribute = CategoricalAttribute | NumericalAttribute

export type DisaggregationAttribute = {
    name: string,
    bins: number[] | null
}