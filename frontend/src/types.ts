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

export interface KPIChange {
    action: KPIActions.ChangeComponent,
    component: Charts
}

<<<<<<< HEAD
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

export interface KPIChange {
    action: KPIActions.ChangeComponent,
    component: Charts
}

<<<<<<< HEAD
export type KPITile = {
<<<<<<< HEAD
    title: string,
    type: Charts,
    endpoint: String,
} & LayoutItem;
=======
    title: String,
=======
export interface KPITile {
=======
export type KPITile = {
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
    title: string,
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
    type: Charts,
<<<<<<< HEAD
    url: String,
    x: Number,
    y: Number,
    w: Number,
    h: Number,
    i: Number
}
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
    endpoint: String,
} & LayoutItem;
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)

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
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)

/* ------------- Modal ---------------- */ 

export interface ModalEvent {
    name: string,
    data: Object
}

export interface EditModal {
    name: string,
    chart: Charts
}

<<<<<<< HEAD
<<<<<<< HEAD
/* ------------- General Types ---------------- */
=======
/* ------------- General ---------------- */
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
/* ------------- General Types ---------------- */
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)

export interface IDictionary<TValue> {
    [id: string]: TValue;
}
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)


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
<<<<<<< HEAD
};
=======
>>>>>>> d06c702 (Feature: ID-hGqw1FNt: add dashboard customization)
=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
};
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
