<template>
  <!---   <router-view v-slot="{ Component }">
 <transition
      enter-active-class="animate__animated animate__fadeIn" // könnte auch mit `animate__animated animate__${$route.meta.enterTransition}` befüllt werden
      leave-active-class="animate__animated animate__fadeOut"
      mode="out-in"
    >
      <component :is="Component" :key="$rout.path"></component>
    </transition>  
  </router-view>-->
  <router-view> </router-view>
</template>

<script>
export default {
  name: "App",
  computed: {
    token() {
      return this.$store.getters.token;
    },
  },
  beforeCreate(){
    this.$store.dispatch("fetchStatusCards");
    this.$store.dispatch("fetchTasks");
  },
  created() {
    this.$store.dispatch("autoSignIn");
  },
  components: {},
  watch: {
    token: {
      handler() {
        if (this.token) {
          this.$store.dispatch("fetchUInfos");
          this.$store.dispatch("fetchProducts");
          this.$store.dispatch("fetchWichtelEvents");
        }
      },
      immediate: true,
    },
  },
};
</script>

<style>
@import "~bootstrap/dist/css/bootstrap.min.css";
@import "~animate.css/animate.min.css";

.bg-vue {
  background-color: rgb(52, 73, 94);
  color: white;
}

.bg-vue2 {
  background-color: rgb(65, 184, 131);
  color: white;
}

.text-vue {
  color: rgb(52, 73, 94);
}

.text-vue2 {
  color: rgb(65, 184, 131);
}
</style>
