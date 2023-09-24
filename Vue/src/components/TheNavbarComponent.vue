<template>
  <nav class="navbar navbar-expand-md bg-vue navbar-dark">
    <div class="container">
      <router-link to="/" class="navbar-brand">Soko`s Sandbox</router-link>
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <router-link to="/" class="nav-link" active-class="active">Home</router-link>
        </li>
        <!-- Unnötiger Inhalt 
        <li class="nav-item">
          <router-link to="/shophome" class="nav-link" active-class="active">Der Shop</router-link>
        </li>
        -->
        <li class="nav-item">
          <router-link to="/kanban" class="nav-link" active-class="active">Kanban</router-link>
        </li>
        <li class="nav-item">
          <router-link :to="{ name: 'Wichteln'}" class="nav-link" active-class="active" v-if="isAuth"
            >Wichtelfee</router-link
          >
          <router-link :to="{ name: 'Auth', params: { name: 'login' } }" class="nav-link" v-if="!isAuth"
            >Wichtelfee</router-link
          >
        </li>
      </ul>
      <div class="me-2">
        <router-link
          :to="{ name: 'Auth', params: { name: 'login' } }"
          class="btn bg-vue2"
          v-if="!isAuth"
          >Login</router-link
        >
        <router-link
          :to="{ name: 'Auth', params: { name: 'register' } }"
          class="btn bg vue"
          v-if="!isAuth"
          >Register</router-link
        >
      </div>

      <button class="btn bg-vue2 me-3" @click="signOut()" v-if="isAuth">
        <i class="fas fa-sign-out-alt"></i> Logout
      </button>
    </div>
  </nav>
</template>

<script>
export default {
  name: "TheNavbarComponent",
  data() {
    return {};
  },
  computed: {
    isAuth() {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    async signOut() {
      try {
        await this.$store.dispatch("signOut");
        this.$router.push("/");
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<style scoped></style>
