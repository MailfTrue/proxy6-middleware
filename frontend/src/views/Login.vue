<template>
  <v-container>
    <v-row>
      <v-col lg="4" md="8" offset-lg="4" offset-md="2" sm="12">
        <v-card>
          <v-card-title>
            Авторизация
          </v-card-title>

          <v-form @submit.prevent="submit">
            <v-card-text>
              <v-container>
                <v-alert color="error" v-show="errors.detail" v-text="errors.detail"/>
                <v-row>
                  <v-text-field :error-messages="errors.username" v-model="user.username" label="Логин"></v-text-field>
                </v-row>
                <v-row>
                  <v-text-field :error-messages="errors.password" v-model="user.password" type="password" label="Пароль"></v-text-field>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-btn text :to="{name: 'Register'}">
                У меня нет аккаунта
              </v-btn>
              <v-btn
                  type="submit"
                  color="teal accent-4"
              >
                Войти
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Login",
  data: () => ({
    user: {
      username: "",
      password: ""
    },
    errors: {}
  }),
  methods: {
    submit() {
      if (this.user.username && this.user.password) {
        this.$store.dispatch('auth/login', {user: this.user}).then(
            () => {
              this.$router.push({name: "MyProxy"});
            },
            error => {
              console.error(error)
              this.errors = error.response.data;
            }
        );
      }
    }
  }
}
</script>

<style scoped>

</style>