/*
* Central file for all the relevant types. 
*/
import { EventBusKey } from '@vueuse/core';
import { Ref } from 'vue';
import { LayoutItem } from 'vue3-grid-layout-next/dist/helpers/utils';

// Chart must be named like file in /charts, so PieChart.vue -> PieChart
export enum Charts {
    PieChart = 'other-charts/PieChart',
    Graph = 'other-charts/GraphChart',
    LineChart = 'line-charts/LineChart',
    HorizontalBarChart = 'bar-charts/HorizontalBarChart',
    ChevronDiagram = 'other-charts/ChevronDiagram',
    VariantView = 'views/VariantView',
    NewChart = 'NewChart.vue',
}

export const chartNameEnumMap = {
    Variants : { name: 'Variant List', endpoint: '/variants' },
    Distributions : { name: 'Variant List', endpoint: '/distributions' },
    KPI : { name: 'Variant List', endpoint: '/distributions' },
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
    // index for updates, just set this to 0
    changed: number,
    request: ServerRequest,
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

/* ------------- Events ---------------- */
export interface DownloadVisualizationEvent {
    id: string,
    title: string,
}
export const downloadVisualizationBusKey: EventBusKey<DownloadVisualizationEvent> = Symbol('downloadVisualizationBusKey');

/* ------------- General Types ---------------- */

export interface IDictionary<TValue> {
    [id: string]: TValue;
}

export const ServerAttributes : PatientAttribute[] = await fetch(`//${window.location.hostname}:80/patient-attributes`,
    {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json());

export const ProcessAttributes : PatientAttribute[] = await fetch('http://127.0.0.1:80/process-attributes',
    {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json());

/* ------------- Chart Data Types ---------------- */

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

export type DataType = Graph | DataSeries | MultiDataSeries

const colors: string[] = [
    '#5470c6', '#91cc75', '#fac858', '#ee6666',
    '#73c0de', '#3ba272', '#fc8452', '#9a60b4',
    '#ea7ccc', '#7baaf7', '#276749', '#cbb142',
    '#ff6b6b', '#a0d8ef', '#008080', '#cc5500',
    '#b57edc', '#fddde6',
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
    '#bcbd22', '#17becf', '#393b79', '#e14e41',
    '#ffb14e', '#5e77ff', '#ffaae3', '#55c667',
    '#7b3b3b', '#b8892e', '#4ea3c3', '#b42f5b',
    '#ff7e45', '#736ced', '#bd63c1', '#3cb44b',
    '#ffe119', '#4363d8', '#f58231', '#e6194B',
    '#911eb4', '#42d4f4', '#fabebe', '#469990',
    '#800000', '#aaffc3', '#e6beff', '#a9a9a9',
    '#fffac8', '#4b0082', '#f032e6', '#808000',
    '#ffd8b1', '#000075', '#808080', '#000000'
    // Add more colors as needed
];

export function hashColor(key : string) {
    // Hash function: sum of character codes modulated by the colors array length
    let hash = 0;
    for (let i = 0; i < key.length; i++) {
        hash = (hash + key.charCodeAt(i) + 3) % colors.length;
    }
    return colors[hash];
}

// Formats the data from the server to ECharts format
export function formatDataSeries(p_data: DataSeries, multi = false) {
    const label: string[] = [];
    const colors: string[] = [];
    const alreadyAdded: string[] = [];
    const data: Object[] = [];

    p_data.data.forEach((item) => {
        const identifier = multi ? p_data.name + '' :  item.x + '';
        const newItem = { value: +(item.y).toFixed(3) };
        if(!multi) Object.assign(newItem, { itemStyle: { color: hashColor(identifier) } });
        label.push(String(item.x));
        data.push(newItem);
        if(!alreadyAdded.includes(identifier)){ 
            alreadyAdded.push(identifier);
            colors.push(hashColor(identifier))
        }
    });

    return { label: label, data: data, colors: colors};
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

export type ListEntry = {
    name: string,
    code: number | string,
}

export type CategoricalAttribute = {
    name: string,
    ref: Ref | null,
    type: 'categorical',
    values: string[] | ListEntry[],
}

export type NumericalAttribute = {
    name: string,
    ref: Ref<number[]> | null,
    type: 'numerical',
    min: number,
    max: number,
}

export type PatientAttribute = CategoricalAttribute | NumericalAttribute

export type DisaggregationAttribute = {
    name: string,
    bins?: number[]
}

/* ------------- Requests ---------------- */


export const DisaggregationAttributes = {
    opo_id: { label: 'OPO ID', value: 'opo_id'},
    hospital_id: { label: 'Hospital ID', value: 'hospital_id' },
    age: { label: 'Age', value: 'age' },
    gender: { label: 'Gender', value: 'gender' },
    race: { label: 'Race', value: 'race' },
    brain_death: { label: 'Brain Death', value: 'brain_death' },
    referral_year: { label: 'Referral Year', value: 'referral_year' },
    referral_day_of_week: { label: 'Referral Day of Week', value: 'referral_day_of_week' },
    cause_of_death: { label: 'Cause of Death', value: 'cause_of_death' },
    mechanism_of_death: { label: 'Mechanism of Death', value: 'mechanism_of_death' },
    circumstances_of_death: { label: 'Circumstances of Death', value: 'circumstances_of_death' },
    outcome_heart: { label: 'Outcome - Heart', value: 'outcome_heart' },
    outcome_liver: { label: 'Outcome - Liver', value: 'outcome_liver' },
    outcome_kidney_left: { label: 'Outcome - Kidney Left', value: 'outcome_kidney_left' },
    outcome_kidney_right: { label: 'Outcome - Kidney Right', value: 'outcome_kidney_right' },
    outcome_lung_left: { label: 'Outcome - Lung Left', value: 'outcome_lung_left' },
    outcome_lung_right: { label: 'Outcome - Lung Right', value: 'outcome_lung_right' },
    outcome_pancreas: { label: 'Outcome - Pancreas', value: 'outcome_pancreas' },
};

export enum EndpointURI {
    KPI = '/kpi',
    DISTRIBUTION = '/distributions',
    VARIANT = '/variants',
    DFG = '/dfg',
}

type BaseBody = {
    endpoint: EndpointURI,
    method: 'GET' | 'POST',
    disaggregation_attribute: DisaggregationAttribute,
    filters?: Filter[],
}

type BodyKPI = BaseBody & {
    endpoint: EndpointURI.KPI | EndpointURI.DFG,
    kpi: string[],
    legend_attribute?: DisaggregationAttribute,
}

type BodyDistribution = BaseBody & {
    endpoint: EndpointURI.DISTRIBUTION,
}

type BodyVariant = BaseBody & {
    endpoint: EndpointURI.VARIANT,
}

type CommonBody = BaseBody & {
    endpoint: EndpointURI,
}

export type ServerRequest = CommonBody | BodyKPI | BodyDistribution | BodyVariant

export type EditModalEntry = {
    value: string,
    label: string,
    endpoint: EndpointURI,
    // same number = can be used in same chart
    pairable: number,
}

interface EditModalEntryInt {
    [key: string]: EditModalEntry
}


// Follows the type of EditModalEntry
export const KPI : EditModalEntryInt = {
    HAPPY_PATH_ADHERENCE: { value: 'HAPPY_PATH_ADHERENCE', label: 'Happy Path Adherence', endpoint: EndpointURI.KPI, pairable: 0  },
    DROP_OUT: { value: 'DROP_OUT', label: 'Drop Out', endpoint: EndpointURI.KPI, pairable: 1},
    PERMUTED_PATH_ADHERENCE: { value: 'PERMUTED_PATH_ADHERENCE', label: 'Permuted Path Adherence', endpoint: EndpointURI.KPI, pairable: 0} ,
    PERMUTED_PATH_DFG: { value: 'PERMUTED_PATH_DFG', label: 'Permuted Path DFG', endpoint: EndpointURI.DFG, pairable: 2},
    BUREAUCRATIC_DURATION: { value: 'BUREAUCRATIC_DURATION', label: 'Bureaucratic Duration', endpoint: EndpointURI.KPI, pairable: 0 },
    EVALUATION_TO_APPROACH: { value: 'EVALUATION_TO_APPROACH', label: 'Evaluation to Approach', endpoint: EndpointURI.KPI, pairable: 0},
    AUTHORIZATION_TO_PROCUREMENT: { value: 'AUTHORIZATION_TO_PROCUREMENT', label: 'Authorization to Procurement', endpoint: EndpointURI.KPI, pairable: 0}
}

// Follows the type of EditModalEntry
export const DistributionCharts : EditModalEntryInt = {
    PieChart: { label: 'Pie Chart', value: Charts.PieChart, endpoint: EndpointURI.DISTRIBUTION, pairable: 3},
    HorizontalBarChart: { label: 'Horizontal Bar Chart', value: Charts.HorizontalBarChart, endpoint: EndpointURI.DISTRIBUTION, pairable: 4},
}

export const Endpoints = [
    {
        label: 'KPIs',
        code: 'ssid_chart',
        endpoint: EndpointURI.KPI,
        color: colorPalette.REF,
        items: Object.values(KPI)
    },
    {
        label: 'Distributions',
        code: 'leaderboard',
        color: colorPalette.AUT,
        items: Object.values(DistributionCharts)
    },
    {
        label: 'Variants',
        code: 'fork_right',
        color: colorPalette.TRA,
        items: [
            { label: 'Chevron Diagram', value: 'views/VariantView', endpoint: EndpointURI.VARIANT },
        ]
    }
];


/* ------------- Filter Data Types ---------------- */
export enum FilterOperators {
    IS_EMPTY = 'IS_EMPTY',
    IS_NOT_EMPTY = 'IS_NOT_EMPTY',
    EQUALS = 'EQUALS',
    NOT_EQUALS = 'NOT_EQUALS',
    CONTAINS = 'CONTAINS',
    NOT_CONTAINS = 'NOT_CONTAINS',
    LESS_THAN = 'LESS_THAN',
    LESS_THAN_OR_EQUAL = 'LESS_THAN_OR_EQUAL',
    GREATER_THAN = 'GREATER_THAN',
    GREATER_THAN_OR_EQUAL = 'GREATER_THAN_OR_EQUAL',
    NONE = 'NONE',
}

export type BaseFilter = {
    attribute: PatientAttribute,
    operator: FilterOperators,
}

export type CategoricalFilter = BaseFilter & {
    value: string[] | null
}

export type NumericalFilter = BaseFilter & {
    value: number | null
}

export type Filter = CategoricalFilter | NumericalFilter

export function constructJson(filters: Filter[]) {
    if (filters === undefined || filters.length === 0) {
        return {}
    }
    return {
        categorical_filters: filters.filter((filter) => filter.attribute.type === 'categorical').map(mapFilter),
        numerical_filters: filters.filter((filter) => filter.attribute.type === 'numerical').map(mapFilter),
    }
}

function mapFilter(filter: Filter) {
    if (filter.attribute.type === 'categorical') {
        const {value} = filter as CategoricalFilter;
        return {
            attribute_name: filter.attribute.name,
            operator: filter.operator,
            values: value instanceof Array ? value : ( value === null ? null : [value] ),
        }
    } else {
        const {value} = filter as NumericalFilter;
        return {
            attribute_name: filter.attribute.name,
            operator: filter.operator,
            value: value,
        }
    }
}

export function generateCoordinates(nodes : { name : string }[]) {
    const n = nodes.length;
    const angleIncrement = 360 / n;
    const radius = 100;
    const coordinates = [];

    for (let i = 0; i < n; i++) {
        const angle = i * angleIncrement;
        const x = radius * Math.cos((angle * Math.PI) / 180); // Convert degrees to radians
        const y = radius * Math.sin((angle * Math.PI) / 180); // Convert degrees to radians
        coordinates.push({ name: nodes[i].name, x, y });
    }

    return coordinates;
}
