<template>
  <v-container>
    <v-row>
      <v-col lg="6" md="8" offset-lg="3" offset-md="2" sm="12">
        <v-card>
          <v-card-title>
            Registration
          </v-card-title>

          <v-form @submit.prevent="submit" ref="form">
            <v-card-text>
              <v-container>
                <v-row>
                  <v-text-field :error-messages="errors.username" :rules="rules.username" v-model="user.username" label="Username"></v-text-field>
                </v-row>
                <v-row>
                  <v-text-field :error-messages="errors.password" :rules="rules.password" v-model="user.password" type="password" label="Password"></v-text-field>
                </v-row>
                <v-row>
                  <v-text-field :rules="rules.password2" v-model="user.password2" type="password" label="Repeat Password"></v-text-field>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-btn text :to="{name: 'Login'}">
                I'm already registered
              </v-btn>
              <v-btn
                  type="submit"
                  color="teal accent-4"
              >
                Register
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
          (x) => !!x || "Required field",
          (x) => x && x.length >= 5 || "Minimum length 5 characters",
          (x) => x && x.length <= 22 || "Maximum length 22 characters",
          (x) => x && /^(?=[a-zA-Z0-9._]{5,22}$)(?!.*[_.]{2})[^_.].*[^_.]$/.test(x) || "Invalid username",
        ],
        password: [
          (x) => !!x || "Required field",
          (x) => x && x.length >= 5 || "Minimum length 5 characters",
          (x) => x && x.length <= 22 || "Maximum length 22 characters",
        ],
        password2: [
          (x) => !!x || "Required field",
          (x) => x && this.user.password === x || "Passwords don't match"
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