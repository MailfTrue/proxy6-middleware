<template>
  <v-app>
    <v-main>
      <AppLayout>
        <router-view/>
      </AppLayout>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data: () => ({
    //
  }),
};
</script>
