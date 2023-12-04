<script setup lang="ts">
import {onMounted, ref} from "vue";
import {Variant} from "@/types";
import VariantComponent from "@/components/variants/VariantComponent.vue";
import VChart from 'vue-echarts';
import { use } from 'echarts/core';
import { PieChart } from 'echarts/charts';
import { TooltipComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import type { ComposeOption } from 'echarts/core';
import type { PieSeriesOption } from 'echarts/charts';
import type { TooltipComponentOption } from 'echarts/components';

use([TooltipComponent, PieChart, CanvasRenderer]);

type EChartsOption = ComposeOption<TooltipComponentOption | PieSeriesOption>;

const variants = ref<Variant[]>([]);

onMounted(() => {
    fetchVariants();
});

function fetchVariants() {
    fetch('http://127.0.0.1:80/variants', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          'disaggregation_attribute': {
            'name': 'race'
          },
        }),
    }).then(response => response.json())
        .then(data => {
            variants.value = data;
        });
}

function optionsForVariant(variant: Variant): EChartsOption {
    return {
        tooltip: {
            trigger: 'item',
            position: 'right',
            formatter: '{b}: {d}% ({c})'
        },
        series: [{
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
                show: false,
                position: 'center',
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '20',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: Object.entries(variant.distribution).map(entry => {
                return {
                    name: entry[0],
                    value: entry[1]
                }
            })
        }]
    }

}
</script>

<template>
    <div class="variant-list grid grid-cols-12 items-center gap-3">
      <template v-for="variant in variants" :key="variant.activities" >
        <p class="col-span-1">{{ (variant.frequency * 100).toFixed(2) }}%</p>
        <v-chart class="col-span-2" :option="optionsForVariant(variant)" />
        <VariantComponent class="col-span-9" :variant="variant"></VariantComponent>
      </template>
    </div>
</template>

<style scoped>
.variant-list {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: scroll;
}
</style>