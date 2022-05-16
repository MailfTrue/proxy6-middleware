<template>
<v-container>
  <v-row>
    <v-col cols="12" md="6">
      <v-card>
        <v-card-title>Ваш баланс: {{ fullUser.balance }} ₽</v-card-title>
        <v-card-text>
          <v-data-table :items="payments" :headers="headers" locale="ru" no-data-text="Вы еще не сделали ни одного пополнения" :items-per-page="-1"></v-data-table>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="12" md="6">
      <v-card :loading="!fullUser" :disabled="!fullUser">
        <v-card-title>Пополнить баланс</v-card-title>
        <v-card-text>
          <v-form ref="form" action="https://yoomoney.ru/quickpay/confirm.xml" method="POST">
            <v-text-field
                v-model="amountDue"
                label="Сумма пополнения, ₽"
                filled
                dense
            ></v-text-field>
            <input type="hidden" name="receiver" :value="yoomoneyNum">
            <input type="hidden" name="formcomment" value="Пополнение баланса на zxc-arena.ru">
            <input type="hidden" name="short-dest" value="Пополнение баланса на zxc-arena.ru">
            <input type="hidden" name="label" :value="`user_${fullUser.id}`">
            <input type="hidden" name="quickpay-form" value="shop">
            <input type="hidden" name="sum" :value="sum">
            <input type="hidden" name="targets" :value="`Пополнение баланса «${fullUser.username}»`">
            <input type="hidden" name="successURL" :value="successUrl">
            <input type="hidden" name="need-fio" value="false">
            <input type="hidden" name="need-email" value="false">
            <input type="hidden" name="need-phone" value="false">
            <input type="hidden" name="need-address" value="false">
            <input type="hidden" name="paymentType" value="AC">
            <v-btn
                color="primary"
                class="mr-4 pay-btn"
                type="submit"
            >
              Оплатить
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</v-container>
</template>

<script>
import {mapState} from "vuex";
import { apiService } from "../services";

export default {
  name: "Wallet",
  data: () => ({
    amountDue: 1000,  // Сумма к получению
    yoomoneyNum: process.env.VUE_APP_YOOMONEY_NUM,
    payments: [],
    headers: [
      {text: "Дата", value: "datetime"},
      {text: "ID операции", value: "operation_id"},
      {text: "Сумма", value: "amount"},
      {text: "Валюта", value: "currency"},
    ]
  }),
  computed: {
    ...mapState('auth', ['fullUser']),
    show: {
      get() {
        return true;
      },
      set(value) {
        this.$store.commit("dialogs/setShowPayment", value);
      },
    },
    sum() { // Сумма к оплате
      return this.amountDue / (1 - 0.02)  // 0.02 это коэффициент комиссии
    },
    successUrl() {
      return location.href
    }
  },
  mounted() {
    apiService.get("/payments/").then((res) => this.payments = res.data)
  }
}
</script>

<style scoped>

</style>