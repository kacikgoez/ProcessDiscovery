/*
* Central file for all the relevant types. 
*/

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

export interface KPITile {
    title: string,
    type: Charts,
    url: String,
    x: Number,
    y: Number,
    w: Number,
    h: Number,
    i: Number
}

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

/* ------------- General ---------------- */

export interface IDictionary<TValue> {
    [id: string]: TValue;
}
