<script setup lang="ts">
import {PropType, defineProps} from "vue";
import {Variant} from "@/types";

defineProps({
    variant: { type: Object as PropType<Variant>, required: true }
})
</script>

<template>
  <div class="variant">
    <div :class="'activity-' + activity.toLowerCase()" v-for="activity in variant.activities" :key="activity">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 36" fill="currentColor" height="4rem">
        <path d="M46 0 0 0 10 18 0 36 46 36 56 18 46 0z"/>
        <text x="50%" y="50%" text-anchor="middle" alignment-baseline="middle" font-size=".5em" fill="white">{{ activity }}</text>
      </svg>
    </div>
  </div>
</template>

<style scoped>
.variant {
  display: flex;
  flex-direction: row;
}
.activity-referral {
  color: var(--activity-referal-color);
}
.activity-evaluation {
  color: var(--activity-evaluation-color);
}
.activity-approach {
  color: var(--activity-approach-color);
}
.activity-authorization {
  color: var(--activity-authorization-color);
}
.activity-procurement {
  color : var(--activity-procurement-color);
}
.activity-transplant {
  color: var(--activity-transplant-color);
}
</style>