<template>
  <v-container fluid class="main-container">
    <Navigation v-model="drawer"/>
    <v-container>
      <slot></slot>
    </v-container>
  </v-container>
</template>

<script>

import Navigation from "../components/Navigation";
export default {
  name: "AppLayoutMain",
  components: {
    Navigation
  },
  data: () => ({
    drawer: true
  }),
  mounted() {
    if (this.$store.getters["auth/userData"]) {
      this.$store.dispatch("auth/getFullUser")
    }
  }
}
</script>

<style scoped>
  .main-container {
    display: flex;
    padding: 0;
    height: 100%;
  }
</style>
