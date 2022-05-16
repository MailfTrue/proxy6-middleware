<template>
  <v-card>
    <v-card-title>
      Купить прокси
    </v-card-title>

    <v-form @submit.prevent="submit">
      <v-card-text>
        <v-row>
          <v-col cols="4">
            <v-select v-model="country" :items="countriesSelect" label="Страна"></v-select>
          </v-col>
          <v-col cols="4">
            <v-text-field v-model="count" label="Количество" type="number"></v-text-field>
          </v-col>
          <v-col cols="4">
            <v-select v-model="period" :items="periodOptions" label="Период"></v-select>
          </v-col>
        </v-row>
        <v-alert color="error" v-show="errors.detail" v-text="errors.detail"/>
      </v-card-text>
      <v-card-actions>
        <v-btn :disabled="!price" type="submit" color="primary" class="buy-btn">
          Купить
          <template v-if="price">
            за {{ Math.ceil(price) }} ₽
          </template></v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script>
import {mapActions, mapGetters} from 'vuex';
import {countryPretty} from '../utils';
import ProxyService from "../services/proxy.service"

export default {
  name: "BuyProxy",
  data: () => ({
    country: null,
    count: 1,
    period: 30,
    periodOptions: [
      {text: "1 месяц", value: 30},
      {text: "2 месяца", value: 60},
      {text: "3 месяца", value: 90},
    ],
    price: null,
    errors: {}
  }),
  computed: {
    ...mapGetters('proxy', ['countries']),
    countriesSelect() {
      return this.countries?.map(x => ({text: countryPretty(x), value: x}))
    }
  },
  watch: {
    country() { this.getPrice() },
    period() { this.getPrice() },
    count() { this.getPrice() },
  },
  methods: {
    ...mapActions('proxy', ['loadCountries']),
    getPrice() {
      this.price = null
      if (this.country && this.period && this.count)
        ProxyService.price({country: this.country, period: this.period, count: this.count})
            .then((res) => this.price = res.data.price)
            .catch(() => alert("Ошибка при загрузке стоимости. Неизвестная ошибка, попробуйте позже"))
    },
    submit() {
      ProxyService.buy({country: this.country, period: this.period, count: this.count})
        .then(() => this.$router.push({name: "My Proxy"}))
        .catch((error) => {
          if (error?.response?.data?.detail) {
            this.errors = error.response.data
          } else {
            alert("Ошибка при покупке. Неизвестная ошибка, попробуйте позже")
          }
        })
    }
  },
  mounted() {
    this.loadCountries()
  }

}
</script>

<style scoped>
  .buy-btn {
    width: 100%;
  }
</style>