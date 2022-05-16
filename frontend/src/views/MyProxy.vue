<template>
  <v-data-table :items="listReadable" :headers="headers">

  </v-data-table>
</template>

<script>
import {mapActions, mapGetters} from 'vuex';
import {countryPretty} from "../utils";

export default {
  name: "MyProxy",
  data: () => ({
    headers: [
      {text: "ID", value: "id"},
      {text: "Активен", value: "active"},
      {text: "Хост", value: "host"},
      {text: "IP", value: "ip"},
      {text: "Порт", value: "port"},
      {text: "Логин", value: "user"},
      {text: "Пароль", value: "pass"},
      {text: "Страна", value: "country"},
      {text: "Дата приобретения", value: "date"},
      {text: "Дата окончания", value: "date_end"},
    ]
  }),
  methods: {
    ...mapActions('proxy', ['loadList']),
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