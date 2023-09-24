<template>
  <div>
    <TheShopNavbarComponent></TheShopNavbarComponent>
    <main>
      <div class="container">
        <div class="row">
          <div class="col-12">
            <transition
              enter-active-class="animate__animated animate__fadeIn"
              leave-active-class="animate__animated animate__fadeOut"
              mode="out-in"
              appear
              :key="$route.path"
            >
              <slot>
                <h1>Hauptbereich</h1>
              </slot>
            </transition>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import TheShopNavbarComponent from "@/components/TheShopNavbarComponent.vue";

export default {
  name: "TheShopLayout",
  components: {
    TheShopNavbarComponent,
  },
};
</script>

<style scoped></style>
