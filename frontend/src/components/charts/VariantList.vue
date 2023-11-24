<script setup lang="ts">
import {onMounted, ref} from "vue";
import {Variant} from "@/types";
import VariantComponent from "@/components/variants/VariantComponent.vue";
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
          'disaggregation_attribute': 'activity',
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
        },
        series: [{
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
                show: false,
                position: 'center'
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
            data: Object.entries(variant.distribution).map((key, value) => {
                return {
                    name: key,
                    value: value
                }
            })
        }]
    }

}
</script>

<template>
    <div class="variant-list">
      <div class="row" v-for="variant in variants" :key="variant.activities" >
        <VariantComponent :variant="variant"></VariantComponent>
      </div>
    </div>
</template>

<style scoped>
.variant-list {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: scroll;
}
.row {
  margin: 1em;
}
</style>