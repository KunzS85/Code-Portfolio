<template>
  <TheNavOneColLayout>
    <div class="container-fluid">
      <div class="row">
        <div class="offset-4 col-4">
          <transition
            enter-active-class="animate__animated animate__bounceInRight"
            leave-active-class="animate__animated animate__bounceOutRight"
            mode="out-in"
          >
            <component
              :is="componentName"
              :prevPath="prevRoute"
              @change-component="changeComponent"
            ></component>
          </transition>
        </div>
      </div>
    </div>
  </TheNavOneColLayout>
</template>

<script>
import TheNavOneColLayout from "@/layouts/TheNavOneColLayout.vue";
import RegisterComponent from "@/components/auth/RegisterComponent.vue";
import LoginComponent from "@/components/auth/LoginComponent.vue";

export default {
  name: "AuthPage",
  components: {
    TheNavOneColLayout,
    RegisterComponent,
    LoginComponent,
  },

  data() {
    return {
      componentName: null,
      prevRoute: null,
    };
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.prevRoute = from.path;
    });
  },
  methods: {
    changeComponent(payload) {
      this.componentName = payload.componentName;
    },
  },
  created() {
    switch (this.$route.params.name) {
      case "login":
        this.componentName = "LoginComponent";
        break;
      case "register":
        this.componentName = "RegisterComponent";
        break;
      default:
        this.componentName = "RegisterComponent";
    }
  },
  /* eslint-disable */
  beforeRouteUpdate(to, from) {
    switch (to.params.name) {
      case "login":
        this.componentName = "LoginComponent";
        break;
      case "register":
        this.componentName = "RegisterComponent";
        break;
      default:
        this.componentName = "RegisterComponent";
    }
  },
};
</script>

<style></style>
