<template>
    <div class="flex h-full w-full">
        <div style="margin: auto;">
            <div id="main" ref="chartDom" :class="{ hidden: !loaded }">
            </div>
            <div v-if="!loaded">
                <div style="margin: auto;">
                    <ProgressSpinner></ProgressSpinner>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { globalFiltersStore } from '@/stores/GlobalFiltersStore';
import { theme } from '@/theme.js';
import { DataSeries, EndpointURI, Filter, ServerRequest, activityNameEnumMap, colorPalette, constructJson, downloadVisualizationBusKey, formatDataSeries, generateCoordinates, hashColor } from '@/types';
import { capitalizeWords } from '@/util';
import { useEventBus } from '@vueuse/core';
import * as echarts from 'echarts';
import { PropType, defineProps, onBeforeMount, onMounted, ref, toRefs, watch } from 'vue';

const props = defineProps({
    id: { type: String, required: true },
    width: { type: Number, required: true },
    height: { type: Number, required: true },
    maxWidth: { type: Number, default: -1 },
    minWidth: { type: Number, default: -1 },
    request: { type: Object as PropType<ServerRequest>, required: true },
    option: { type: Object as PropType<echarts.EChartsOption>, required: true },
    filters: { type: Array as () => Filter[], required: true },
    kpi: { type: String, required: false, default: null },
});

const loaded = ref(false);
const propRefs = toRefs(props);
const chartDom = ref(null);
const downloadBus = useEventBus(downloadVisualizationBusKey);
const globalFilters = globalFiltersStore();
let currentKPI: string | null = null;

onBeforeMount(async () => {
    const requestBody: ServerRequest = {} as ServerRequest;

    if (props.request.disaggregation_attribute) requestBody['disaggregation_attribute'] = props.request.disaggregation_attribute;

    if (!Array.isArray(propRefs.option.value.series) || propRefs.option.value.series.length !== 1) {
        console.error('Series passed down must be an array with a single base item.')
        return
    }

    const baseDataItem = propRefs.option.value.series[0]

    if (propRefs.kpi.value !== null) {
        Object.assign(requestBody, { kpi: propRefs.kpi.value })
        currentKPI = propRefs.kpi.value;
    } else if (Array.isArray(propRefs.request.value.kpi)) {
        Object.assign(requestBody, { kpi: propRefs.request.value.kpi[0] })
        currentKPI = propRefs.request.value.kpi[0];
    }


    if (props.request.statistic) {
        Object.assign(requestBody, { statistic: props.request.statistic })
    }

    await fetchEndpoint(requestBody, baseDataItem);

    loaded.value = true;
});

onMounted(() => {
    // Initialize ECharts
    echarts.registerTheme('customed', theme);
    const myChart = echarts.init(chartDom.value, { renderer: 'canvas' });

    // Render the inital chart
    myChart.setOption(props.option);
    myChart.resize({ width: propRefs.width.value, height: propRefs.height.value });

    watch(propRefs.option, (newOption) => {
        // needed for variant chart to show up
        if (Array.isArray(newOption.series) && newOption.series.length > 0 && props.request.endpoint == EndpointURI.VARIANT) {
            loaded.value = true;
        }
        myChart.setOption(newOption);
        myChart.resize({ width: propRefs.width.value, height: propRefs.height.value });
    }, { deep: true });

    // Watch for changes and update the chart
    watch([propRefs.width, propRefs.height], ([newWidth, newHeight]) => {
        if (propRefs.maxWidth.value > 0 && newWidth > propRefs.maxWidth.value) return;
        if (propRefs.minWidth.value > 0 && newWidth < propRefs.minWidth.value) return;
        myChart.resize({ width: newWidth, height: newHeight });

    });

    // Download the chart
    downloadBus.on((event) => {
        if (event.id === props.id) {
            const base64 = myChart.getDataURL();
            const link = document.createElement('a');
            link.href = base64;
            link.download = event.title + '.png';
            link.click();
        }
    });
});

async function fetchEndpoint(requestBody: ServerRequest, baseDataItem: echarts.SeriesOption, index: number = 0) {
    try {
        // Variant fetching is done in the VariantChart.vue component, dismiss it here
        if (props.request.endpoint && props.request.endpoint === EndpointURI.VARIANT) return;
        const response = await fetch(`//${window.location.hostname}/` + props.request.endpoint.replace('/', ''), {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ...constructJson(propRefs.filters.value.concat(globalFilters.filters)),
                ...requestBody
            }),
        });

        const textResponse: string = await response.text();
        const responseData = JSON.parse(textResponse.replaceAll('NaN', '0'))

        let data = [];

        if (props.request.endpoint !== EndpointURI.DFG) {
            let legend = (responseData.series ? responseData.series[0].data : responseData.data)
            legend = legend.filter((item: any) => item.name !== undefined || item.x !== undefined);
            legend = legend.map((item: any) => item.name || item.x);

            // Depending on which axis is category, assign legend to it
            if (propRefs.option.value.xAxis && propRefs.option.value.xAxis.type === 'category') {
                Object.assign(propRefs.option.value, {
                    xAxis: { type: 'category', data: legend },
                });
            } else if (propRefs.option.value.yAxis && propRefs.option.value.yAxis.type === 'category') {
                Object.assign(propRefs.option.value, {
                    yAxis: { type: 'category', data: legend }
                });
            }
        }

        // TypeScript is B with this
        if (!Array.isArray(propRefs.option.value.series)) return;

        // Add a new series item to the option if multiple (besides first item, already passed by options)
        if (index > 0) propRefs.option.value.series.push(JSON.parse(JSON.stringify(baseDataItem)));
        index = propRefs.option.value.series.length - 1;

        // Assign the data to the series depending on endpoint
        switch (props.request.endpoint) {
            case EndpointURI.DISTRIBUTION: {
                const data = (responseData as DataSeries).data.map((item) => {
                    return { name: item.x, value: item.y, itemStyle: { color: hashColor(item.x + '') } };
                });
                Object.assign(propRefs.option.value.series[index], { name: capitalizeWords(responseData.name), data: data });
                break;
            }
            case EndpointURI.KPI: {
                // copy baseItem & replace with empty array
                data = responseData;
                let colors = [];
                const multi = currentKPI === 'DROP_OUT';
                const baseItem = Object.assign({}, propRefs.option.value.series[index]);
                propRefs.option.value.series = [] as any;
                for (const dataItem in data.series) {
                    const copyItem = Object.assign({}, baseItem);
                    const formatted = formatDataSeries(data.series[dataItem] as DataSeries, multi);
                    Object.assign(copyItem, { name: capitalizeWords(data.series[dataItem].name), data: formatted.data });
                    if (multi) colors.push(formatted.colors[0]);
                    propRefs.option.value.series.push(copyItem);
                }
                Object.assign(propRefs.option.value, { color: colors });
                break;
            }
            case EndpointURI.DEJURE:
            case EndpointURI.DFG: {
                // Assuming responseData.edges is an array of edges with 'source', 'target', and 'value' properties

                // Step 1: Find the maximum and minimum values among all edges
                const maxValue = Math.max(...responseData.edges.map(item => item.value));
                const minValue = Math.min(...responseData.edges.map(item => item.value));

                // Step 2: Function to determine color based on value using a gradient
                const getColorByValue = (value, minValue, maxValue) => {
                    // Normalize value between 0 and 1
                    const normalizedValue = (value - minValue) / (maxValue - minValue);
                    // Generate gradient color - simple linear interpolation between blue and red
                    const r = Math.floor(normalizedValue * 255); // More red as value increases
                    const b = 255 - r; // More blue as value decreases
                    return `rgb(${r},0,${b})`;
                };

                let nodes = responseData.nodes.map((item, index, arr) => {
                    const generatedCoordinates = generateCoordinates(arr); // Ensure this is correctly implemented to not generate coordinates every iteration
                    const { x, y } = generatedCoordinates[index]; // Assuming generateCoordinates returns an array of the same length as nodes with {x, y} for each node
                    return {
                        name: item.label, x, y,
                        itemStyle: {
                            color: colorPalette[activityNameEnumMap[item.label]]
                        }
                    };
                });

                let edges = responseData.edges.map((item) => {
                    return {
                        source: item.source,
                        target: item.target,
                        value: item.value,
                        lineStyle: {
                            normal: {
                                width: 1,
                                color: getColorByValue(item.value, minValue, maxValue) // Dynamic gradient color based on value
                            }
                        },
                        label: {
                            formatter: item.value + '',
                            show: true,
                        }
                    };
                });

                // Update your eCharts option
                Object.assign(propRefs.option.value.series[0], { data: nodes, links: edges });

                break;
            }
        }
    } catch (error) {
        console.error('ERROR', error);
    }
}

</script>

<style scoped></style>