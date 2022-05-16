<template>
  <component :is="layout">
    <slot/>
  </component>
</template>

<script>
import AppLayoutMain from "../layouts/AppLayoutMain";
import AppLayoutAuth from "../layouts/AppLayoutAuth";

export default {
  name: "AppLayout",
  computed: {
    layout() {
      return {
        main: AppLayoutMain,
        auth: AppLayoutAuth
      }[this.$route.meta.layout] || AppLayoutMain
    }
  }
}
</script>