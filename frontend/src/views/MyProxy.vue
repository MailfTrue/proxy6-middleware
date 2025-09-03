<template>
  <v-data-table :items="listReadable" :headers="headers" no-data-text="You have no proxies" >
    <template v-slot:item.actions="{ item }">
      <v-btn @click="deleteProxy(item)" color="error" icon outlined>
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import {mapActions, mapGetters} from 'vuex';
import {countryPretty} from "../utils";
import ProxyService from "../services/proxy.service";

export default {
  name: "MyProxy",
  data: () => ({
    headers: [
      {text: "ID", value: "id"},
      {text: "Active", value: "active"},
      {text: "Host", value: "host"},
      {text: "IP", value: "ip"},
      {text: "Port", value: "port"},
      {text: "Username", value: "user"},
      {text: "Password", value: "pass"},
      {text: "Country", value: "country"},
      {text: "Purchase Date", value: "date"},
      {text: "End Date", value: "date_end"},
      {text: "Actions", value: "actions", sortable: false},
    ]
  }),
  methods: {
    ...mapActions('proxy', ['loadList']),
    deleteProxy(proxy) {
      ProxyService.delete({ids: proxy.id})
        .then(() => this.loadList())
        .catch((error) => {
          console.error(error)
        })
    }
  },
  computed: {
    ...mapGetters('proxy', ['list']),
    listReadable() {
      if (!this.list) return;
      return this.list.map((x) => ({
        ...x,
        country: countryPretty(x.country),
        date: new Date(x.date).toLocaleString(),
        date_end: new Date(x.date_end).toLocaleString(),
        active: x.active === "1" ? '✅' : '❌'
      }))
    }
  },
  mounted() {
    this.loadList()
  }
}
</script>

<style scoped>

</style>