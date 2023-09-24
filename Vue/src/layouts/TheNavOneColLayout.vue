<template>
    <div>
      <TheNavbarComponent></TheNavbarComponent>
      <main>
        <div class="container-fluid">
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
  import TheNavbarComponent from "@/components/TheNavbarComponent.vue";
  
  export default {
    name: "TheShopLayout",
    components: {
      TheNavbarComponent,
    },
  };
  </script>
  
  <style scoped></style>