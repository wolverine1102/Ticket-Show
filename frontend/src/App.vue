<template>
  <div><Navbar /></div>
</template>

<script>
import Navbar from "./components/Navbar.vue";

export default {
  components: {
    Navbar
  },

  mounted() {
    if (sessionStorage.email) {
      this.currentUserEmail = sessionStorage.email
      this.currentUserFirstName = sessionStorage.first_name
      this.currentUserLastName = sessionStorage.last_name
      this.currentUserRoles = sessionStorage.roles
      this.token = sessionStorage.token
    }
  },

  computed: {
    currentUserEmail: {
      get() {
        return this.$store.state.CurrentUser.currentUserEmail
      },
      set(email) {
        this.$store.commit("CurrentUser/updateCurrentUserEmail", email)
      }
    },
    currentUserFirstName: {
      get() {
          return this.$store.state.CurrentUser.currentUserFirstName
      },
      set(first_name) {
          this.$store.commit("CurrentUser/updateCurrentUserFirstName", first_name)
      }
    },
    currentUserLastName: {
      get() {
          return this.$store.state.CurrentUser.currentUserLastName
      },
      set(last_name) {
          this.$store.commit("CurrentUser/updateCurrentUserLastName", last_name)
      }
    },
    currentUserRoles: {
      get() {
          return this.$store.state.CurrentUser.currentUserRoles
      },
      set(roles) {
          this.$store.commit("CurrentUser/updateRoles", roles)
      }
    },
    token: {
      get() {
          return this.$store.state.CurrentUser.token
      },
      set(token) {
          this.$store.commit("CurrentUser/updateToken", token)
      }
    },
  }
} 

</script>