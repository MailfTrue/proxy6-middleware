<template>
  <v-container>
    <v-row>
      <v-col lg="4" md="6" offset-lg="4" offset-md="3" sm="12">
        <v-card>
          <v-card-title>
            Авторизация
          </v-card-title>

          <v-form @submit.prevent="submit">
            <v-card-text>
              <v-container>
                <v-row>
                  <v-text-field v-model="user.username" label="Логин"></v-text-field>
                </v-row>
                <v-row>
                  <v-text-field v-model="user.password" type="password" label="Пароль"></v-text-field>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-btn
                  type="submit"
                  color="teal accent-4"
                  @click="reveal = true"
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
    }
  }),
  methods: {
    submit() {
      if (this.user.username && this.user.password) {
        this.$store.dispatch('auth/login', {user: this.user}).then(
            () => {
              this.$router.push({name: "Home"});
            },
            error => {
              this.message =
                  (error.response && error.response.data && error.response.data.message) ||
                  error.message ||
                  error.toString();
            }
        );
      }
    }
  }
}
</script>

<style scoped>

</style>