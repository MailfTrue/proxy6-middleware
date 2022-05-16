<template>
  <v-navigation-drawer permanent expand-on-hover :mini-variant="drawer">
    <v-list-item>
      <v-list-item-icon>
        <v-icon>mdi-view-dashboard</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title class="text-h6">
          Private Proxy
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list
        dense
        nav
    >
      <v-list-item link :to="{name: 'Wallet'}">
        <v-list-item-icon>
          <v-icon>mdi-wallet</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>Биллинг</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link :to="{name: 'Buy Proxy'}">
        <v-list-item-icon>
          <v-icon>mdi-plus</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>Купить прокси</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link :to="{name: 'My Proxy'}">
        <v-list-item-icon>
          <v-icon>mdi-view-list</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>Мои прокси</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list
        dense
        nav
    >
      <v-list-item link @click="$store.dispatch('auth/logout')">
        <v-list-item-icon>
          <v-icon>mdi-logout</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>Выйти</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "Navigation",
  props: {
    value: {}
  },
  computed: {
    drawer: {
      get() { return this.value },
      set(val) { this.$emit("input", val) }
    }
  }
}
</script>

<style scoped>

</style>