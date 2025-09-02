<template>
  <v-container>
    <v-row>
      <v-col lg="6" md="8" offset-lg="3" offset-md="2" sm="12">
        <v-card>
          <v-card-title>
            Регистрация
          </v-card-title>

          <v-form @submit.prevent="submit" ref="form">
            <v-card-text>
              <v-container>
                <v-row>
                  <v-text-field :error-messages="errors.username" :rules="rules.username" v-model="user.username" label="Логин"></v-text-field>
                </v-row>
                <v-row>
                  <v-text-field :error-messages="errors.password" :rules="rules.password" v-model="user.password" type="password" label="Пароль"></v-text-field>
                </v-row>
                <v-row>
                  <v-text-field :rules="rules.password2" v-model="user.password2" type="password" label="Повторите пароль"></v-text-field>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-btn text :to="{name: 'Login'}">
                Я уже зарегистрирован
              </v-btn>
              <v-btn
                  type="submit"
                  color="teal accent-4"
              >
                Зарегистрироваться
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {apiService} from "../services";


export default {
  name: "Register",
  data() {
    return {
      user: {
        username: "",
        password: "",
        password2: "",
      },
      rules: {
        username: [
          (x) => !!x || "Обязательное поле",
          (x) => x && x.length >= 5 || "Минимальная длина 5 символов",
          (x) => x && x.length <= 22 || "Максимальная длина 22 символа",
          (x) => x && /^(?=[a-zA-Z0-9._]{5,22}$)(?!.*[_.]{2})[^_.].*[^_.]$/.test(x) || "Недопустимый логин",
        ],
        password: [
          (x) => !!x || "Обязательное поле",
          (x) => x && x.length >= 5 || "Минимальная длина 5 символов",
          (x) => x && x.length <= 22 || "Максимальная длина 22 символа",
        ],
        password2: [
          (x) => !!x || "Обязательное поле",
          (x) => x && this.user.password === x || "Пароли не совпадают"
        ]
      },
      errors: {}
    }
  },
  methods: {
    validate() {
      return this.$refs.form.validate()
    },
    submit() {
      const valid = this.validate();
      if (valid && this.user.username && this.user.password) {
        apiService.post("/v1/users/", {
          username: this.user.username,
          password: this.user.password,
        }).then(
            () => {
              this.$router.push({name: "Login"});
            },
            error => {
              console.log("CATCH", error)
              this.errors = error.response.data
            }
        )
      }
    }
  }
}
</script>

<style scoped>

</style>