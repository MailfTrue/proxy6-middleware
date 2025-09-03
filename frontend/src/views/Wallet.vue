<template>
<v-container>
  <v-row>
    <v-col cols="12">
      <v-card :loading="!fullUser" :disabled="!fullUser">
        <v-card-title>Top Up Balance</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="submit" ref="form" method="POST">
            <v-text-field
                v-model="amountDue"
                label="Top-up amount, ₽"
                :rules="[
                    x => !!x || 'This field is required',
                    x => x && x >= 100 || 'Minimum top-up amount is 100 ₽',
                ]"
                filled
                dense
            ></v-text-field>
            <input type="hidden" name="receiver" :value="yoomoneyNum">
            <input type="hidden" name="formcomment" value="Balance top-up on zxc-arena.ru">
            <input type="hidden" name="short-dest" value="Balance top-up on zxc-arena.ru">
            <input type="hidden" name="label" :value="`user_${fullUser.id}`">
            <input type="hidden" name="quickpay-form" value="shop">
            <input type="hidden" name="sum" :value="sum">
            <input type="hidden" name="targets" :value="`Balance top-up for «${fullUser.username}»`">
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
              Pay
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="12">
      <v-card>
        <v-card-title>Your Balance: {{ fullUser.balance }} ₽</v-card-title>
        <v-card-text>
          <v-data-table :items="paymentsReadable" :headers="headers" locale="en" no-data-text="You haven't made any top-ups yet" :items-per-page="-1"></v-data-table>
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
    amountDue: 1000,  // Amount to receive
    yoomoneyNum: process.env.VUE_APP_YOOMONEY_NUM,
    payments: [],
    headers: [
      {text: "Date", value: "datetime"},
      {text: "Operation ID", value: "operation_id"},
      {text: "Status", value: "statusText"},
      {text: "Amount", value: "amount"},
      {text: "Currency", value: "currency"},
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
    sum() { // Amount to pay
      return this.amountDue / (1 - 0.02)  // 0.02 is the commission coefficient
    },
    successUrl() {
      return location.href
    },
    paymentsReadable() {
      return this.payments.map(
        (x) => ({
          ...x, 
          datetime: (new Date(x.created_at)).toLocaleString(),
          operation_id: x.invoice_id,
          currency: x.fiat_asset,
          statusText: {
            active: "Awaiting payment",
            paid: "Paid",
            expired: "Expired",
          }[x.status],
        })
      )
    }
  },
  methods: {
    submit(e) {
      const valid = this.$refs.form.validate()
      if (!valid) {
        e.preventDefault()
        e.stopPropagation()
        return false
      }
      apiService.post("/v1/payments/cryptobot/create/", {
        amount: this.amountDue,
        currency_type: "fiat",
        fiat_asset: "RUB",
      }).then((res) => {
        window.open(res.data.url, '_blank')
      })
    }
  },
  mounted() {
    apiService.get("/v1/payments/cryptobot/").then((res) => this.payments = res.data)
  }
}
</script>

<style scoped>

</style>