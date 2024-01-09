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
import { theme } from '@/theme.js';
import { DataSeries, EndpointURI, ServerRequest, formatDataSeries } from '@/types';
import { capitalizeWords } from '@/util';
import * as echarts from 'echarts';
import { PropType, defineProps, onBeforeMount, onMounted, ref, toRefs, watch } from 'vue';

const props = defineProps({
    width: { type: Number, required: true },
    height: { type: Number, required: true },
    maxWidth: { type: Number, default: -1 },
    minWidth: { type: Number, default: -1 },
    request: { type: Object as PropType<ServerRequest>, required: true },
    option: { type: Object as PropType<echarts.EChartsOption>, required: true },
});

const loaded = ref(false);
const propRefs = toRefs(props);
const chartDom = ref(null);

onBeforeMount(async () => {
    /* eslint-disable no-debugger */
    // debugger
    const requestBody: ServerRequest = {} as ServerRequest;

    if (props.request.disaggregation_attribute) requestBody['disaggregation_attribute'] = props.request.disaggregation_attribute;

    if (!Array.isArray(propRefs.option.value.series) || propRefs.option.value.series.length !== 1) {
        console.error('Series passed down must be an array with a single base item.')
        return
    }

    const baseDataItem = propRefs.option.value.series[0]

    if (props.request.endpoint === EndpointURI.KPI && props.request.kpi) {
        let promiseList = [];
        for (let i = 0; i < props.request.kpi.length; i++) {
            Object.assign(requestBody, { kpi: props.request.kpi[i] });
            promiseList.push(fetchEndpoint(requestBody, baseDataItem, i));
        }
        await Promise.all(promiseList);
    } else {
        await fetchEndpoint(requestBody, baseDataItem);
    }

    loaded.value = true;
});

onMounted(() => {
    // Initialize ECharts
    echarts.registerTheme('customed', theme);
    const myChart = echarts.init(chartDom.value, { renderer: 'canvas' });

    // Render the inital chart
    if (props.option.name) debugger;
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
});

async function fetchEndpoint(requestBody: ServerRequest, baseDataItem: echarts.SeriesOption, index: number = 0) {
    try {
        // Variant fetching is done in the VariantChart.vue component, dismiss it here
        if (props.request.endpoint && props.request.endpoint === EndpointURI.VARIANT) return;
        const response = await fetch('http://127.0.0.1:80/' + props.request.endpoint.replace('/', ''), {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });

        const responseData = await response.json();
        console.debug(responseData)

        let data = [];

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

        // TypeScript is B with this
        if (!Array.isArray(propRefs.option.value.series)) return;

        // Add a new series item to the option if multiple (besides first item, already passed by options)
        if (index > 0) propRefs.option.value.series.push(JSON.parse(JSON.stringify(baseDataItem)));

        // Assign the data to the series depending on endpoint
        switch (props.request.endpoint) {
            case EndpointURI.DISTRIBUTION: {
                const data = (responseData as DataSeries).data.map((item) => {
                  return { name: item.x, value: item.y };
                });
                Object.assign(propRefs.option.value.series[index], { name: capitalizeWords(responseData.name), data: data });
                break;
            }
            case EndpointURI.KPI: {
                data = responseData;
                const formatted = formatDataSeries(data.series[0] as DataSeries);
                Object.assign(propRefs.option.value.series[index], { name: capitalizeWords(data.name), data: formatted.data });
                break;
            }
            default:
                data = responseData;
                break;
        }
    } catch (error) {
        console.error('ERROR', error);
    }
}

</script>

<style scoped></style>