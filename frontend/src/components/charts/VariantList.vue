<script setup lang="ts">
import {onMounted, ref} from "vue";
import {Variant} from "@/types";
import VariantComponent from "@/components/variants/VariantComponent.vue";

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
</script>

<template>
    <div class="variant-list">
        <VariantComponent v-for="variant in variants" :key="variant.activities" :variant="variant"></VariantComponent>
    </div>
</template>

<style scoped>
.variant-list {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  overflow: scroll;
}
</style>