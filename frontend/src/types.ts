/*
* Central file for all the relevant types. 
*/

export type KPITile = {
    title: String,
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