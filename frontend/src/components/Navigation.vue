<template>
  <v-navigation-drawer :width="350" permanent expand-on-hover :mini-variant="drawer">
    <v-list-item>
      <v-list-item-icon>
        <v-icon>mdi-view-dashboard</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title class="text-h6">
          socketproxy
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
          <v-list-item-title>Wallet ({{ balance }} ₽)</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link :to="{name: 'Buy Proxy'}">
        <v-list-item-icon>
          <v-icon>mdi-plus</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>Buy Proxy</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link :to="{name: 'My Proxy'}">
        <v-list-item-icon>
          <v-icon>mdi-view-list</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>My Proxies</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link :to="{name: 'API'}">
        <v-list-item-icon>
          <v-icon>mdi-api</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>API</v-list-item-title>
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
          <v-list-item-title>Logout ({{ username }})</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import {mapState} from 'vuex';

export default {
  name: "Navigation",
  props: {
    value: {}
  },
  computed: {
    ...mapState('auth', ['fullUser']),
    drawer: {
      get() { return this.value },
      set(val) { this.$emit("input", val) }
    },
    username() {
      return this.fullUser?.username || '?'
    },
    balance() {
      return this.fullUser?.balance || '?'
    }
  }
}
</script>

<style scoped>

</style>