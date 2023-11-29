/*
* Central file for all the relevant types. 
*/

// Chart must be named like file in /charts, so PieChart.vue -> PieChart
export enum Charts {
    PieChart = "other-charts/PieChart",
    LineChart = "line-charts/LineChart",
    HorizontalBarChart = "bar-charts/HorizontalBarChart",
    NewChart = "NewChart.vue",
    Variant = "VariantList.vue",
}

export enum KPIActions {
    ChangeComponent
}

export type KPIChange = {
    action: KPIActions.ChangeComponent,
    component: Charts
};

export type KPITile = {
    title: String,
    type: Charts,
    url: String,
    x: Number,
    y: Number,
    w: Number,
    h: Number,
    i: Number
}

export type Variant = {
    id: Number,
    activities: String[],
    count: Number,
    frequency: Number,
    distribution: Object,
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