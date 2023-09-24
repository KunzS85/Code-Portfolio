<template>
  <nav class="navbar navbar-expand-lg bg-vue navbar-dark">
    <div class="container">
      <router-link to="/shop" class="navbar-brand">Der Shop</router-link>
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <router-link to="/" class="nav-link" active-class="active">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/shop/create/product" class="nav-link" active-class="active"
            >Neuer Artikel</router-link
          >
        </li>
      </ul>
      <button class="btn bg vue me-3">
        <i class="fas fa-shopping cart"></i> Warenkorb ({{ cartSum }}.-)
      </button>
      <button class="btn bg-vue2" @click="signOut()">
        <i class="fas fa-sign-out-alt"></i> Logout
      </button>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  name: "TheNavbarComponent",
  computed: {
    ...mapGetters({cartSum: "cartTotal"}),
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
