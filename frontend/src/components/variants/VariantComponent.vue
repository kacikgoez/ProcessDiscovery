<script setup lang="ts">
import {PropType, defineProps} from "vue";
import {Variant} from "@/types";

defineProps({
    variant: { type: Object as PropType<Variant>, required: true }
})
</script>

<template>
  <div class="variant">
    <div class="activity" v-for="activity in variant.activities" :key="activity">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 36" fill="currentColor" height="4rem">
        <path d="M46 0 0 0 10 18 0 36 46 36 56 18 46 0z"/>
        <text x="50%" y="50%" text-anchor="middle" alignment-baseline="middle" font-size=".5em" fill="white">{{ activity }}</text>
      </svg>
    </div>
  </div>
</template>

<style scoped>
.activity {
  display: inline-block;
}
</style>