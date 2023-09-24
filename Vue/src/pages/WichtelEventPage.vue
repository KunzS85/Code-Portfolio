<template>
  <TheNavOneColLayout>
    <div class="card mt-2">
      <div class="card-body">
        <h4 class="card-title">
          <b>{{ wiEvent.name }}</b>
        </h4>
        <ul class="list-group list-group-flush">
          <li class="list-group-item"><b>Datum:</b> {{ shinyDate }}</li>
          <li class="list-group-item">
            <b>Event-Passwort:</b> {{ wiEvent.password }}
          </li>
          <li class="list-group-item">
            <div class="container-fluid">
              <div class="row">
                <div
                  class="col-12 col-md-6 col-lg-4 mb-3"
                  v-for="person in wiEvent.subs"
                  :key="person.id"
                >
                  <WichtelPerson
                    :sub="person"
                    :newOne="isNewSubscriber"
                    :eventId="wiEvent.id"
                    @thatsMe="thatsMe"
                    @updateWish="updateWish"
                  />
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </TheNavOneColLayout>
</template>

<script>
import TheNavOneColLayout from "@/layouts/TheNavOneColLayout.vue";
import WichtelPerson from "@/components/wichtel/WichtelPerson.vue";
import { mapActions } from "vuex";

export default {
  name: "WichtelEventPage",
  components: {
    TheNavOneColLayout,
    WichtelPerson,
  },
  data() {
    return {};
  },
  props: {
    id: String,
  },
  computed: {
    wiEvent() {
      return this.$store.getters.getWichtelEvent(this.id);
    },
    isNewSubscriber() {
      const userId = this.$store.getters.userId;
      const subscribed = this.wiEvent.subs.find((sub) => sub.id === userId);
      return subscribed === undefined;
    },
    shinyDate() {
      const date = new Date(this.wiEvent.date);
      const shinyDate =
        date.getDate() + "." + (date.getMonth() + 1) + "." + date.getFullYear();
      return shinyDate;
    },
  },
  methods: {
    ...mapActions({
      thatsMe: "updateEvent",
      updateWish: "updateEvent",
    }),
  },
};
</script>

<style scoped></style>
