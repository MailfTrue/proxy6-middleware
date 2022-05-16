<template>
  <v-container>
    <v-data-table :headers="headers" :items="tokensReadable">
      <template v-slot:top>
        <v-toolbar
            flat
        >
          <v-toolbar-title>Мои токены</v-toolbar-title>
          <v-divider
              class="mx-4"
              inset
              vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-btn @click="createToken" color="primary">Создать еще один</v-btn>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
            small
            @click="deleteToken(item)"
        >
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import userService from "../services/user.service"

export default {
  data: () => ({
    tokens: [],
    headers: [
      {text: "Ключ", value: "key"},
      {text: "Дата создания", value: "created"},
      { text: 'Действия', value: 'actions', sortable: false },
    ]
  }),
  computed: {
    tokensReadable() {
      return this.tokens.map(x => ({...x, created: (new Date(x.created)).toLocaleString()}))
    }
  },
  methods: {
    async loadTokens() {
      this.tokens = (await userService.tokens()).data
    },
    async createToken() {
      await userService.newToken();
      await this.loadTokens()
    },
    async deleteToken(token) {
      console.log(token)
      await userService.deleteToken(token.id);
      await this.loadTokens()
    }
  },
  mounted() {
    this.loadTokens()
  }
}
</script>