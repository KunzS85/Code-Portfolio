<template>
  <TheNavOneColLayout>
    <template #default>
      <div class="container-fluid vh-100">
        <div class="d-flex justify-content-start mt-2">
          <i
            class="fa-sharp fa-solid fa-circle-info"
            @click="toggleWichtelInfo"
          ></i>
          <WichtelInfo v-if="showWichtelInfo" />
        </div>
        <div class="container-fluid mt-2">
          <div class="row">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title"><b>Meine Wichtel-Events</b></h5>
                <div class="row">
                  <div
                    class="col-12 col-md-3 mt-2"
                    v-for="event in events"
                    :key="event.id"
                  >
                    <WichtelEvent :event="event" />
                  </div>
                </div>
                <div class="row">
                  <div class="col-12 col-lg-6 mt-2">
                    <NewWichtelEvent></NewWichtelEvent>
                  </div>
                  <div class="col-12 col-lg-6 mt-2">
                    <EntryWichtelEvent></EntryWichtelEvent>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </TheNavOneColLayout>
</template>

<script>
import TheNavOneColLayout from "@/layouts/TheNavOneColLayout.vue";
import WichtelEvent from "@/components/wichtel/WichtelEvent.vue";
import NewWichtelEvent from "@/components/wichtel/NewWichtelEvent.vue";
import EntryWichtelEvent from "@/components/wichtel/EntryWichtelEvent.vue";
import WichtelInfo from "@/components/wichtel/WichtelInfo.vue";

export default {
  name: "WichtelHomePage",
  components: {
    TheNavOneColLayout,
    WichtelEvent,
    NewWichtelEvent,
    EntryWichtelEvent,
    WichtelInfo,
  },
  beforeCreate() {
    this.$store.dispatch("setUserLocal");
  },
  data() {
    return {
      showWichtelInfo: false,
    };
  },
  computed: {
    events() {
      return this.$store.getters.getAllWichtelEventsOfUser(
        this.$store.getters.userId
      );
    },
  },
  methods: {
    toggleWichtelInfo() {
      this.showWichtelInfo = !this.showWichtelInfo;
    },
  },
};
</script>

<style scoped></style>
