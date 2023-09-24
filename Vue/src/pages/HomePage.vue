<template>
  <TheNavOneColLayout>
    <template #default>
      <div class="container-fluid">
        <div class="row">
          <div class="col-12">
            <div class="d-flex justify-content-center mt-3">
              <h1>Soko`s Sandbox</h1>
            </div>
          <div class="d-flex justify-content-center mt-1">
            <img
              class="img-round"
              src="../../public/Toon-Portrait.jpg"
              alt=""
            />
          </div>
          <div class="d-flex justify-content-center mt-3">
            Der Name SoKo entstand aus den Initialen meines Namens.
          </div>
          <div class="d-flex justify-content-center">
            Die Leidenschaft für die Programmierung forderte einen Sandkasten.
          </div>
          <div class="d-flex justify-content-center">
            Und so entstand diese Website.
          </div>

          <div class="d-flex justify-content-center mt-3">
            Über die Navigationsleiste sind verschiedene Projekte zugänglich.  
          </div>
          <div class="d-flex justify-content-center">
            Um die Projekte effektiv nutzen zu können musst du einen Account haben und eingeloggt sein.
          </div>
          <div class="d-flex justify-content-center">
            Deine Daten werden von mir ausschliesslich für die Funktionalitäten der Website/Projekte verwendet.
          </div>
        </div>
      </div>
      </div>
    </template>
  </TheNavOneColLayout>
</template>

<script>
import TheNavOneColLayout from "@/layouts/TheNavOneColLayout.vue";
export default {
  name: "HomePage",
  components: {
    TheNavOneColLayout,
  },
  data() {
    return {};
  },
  methods: {},
};
</script>

<style scoped>
h1 {
  font-size: 5.625rem;
  font-family: "Sacramento", cursive;
}
p {
  font-family: "Montserrat", sans-serif;
}
.img-round {
  border-radius: 100%;
  width: 10rem;
  height: 10rem;
}
</style>
