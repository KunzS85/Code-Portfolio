<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title" :class="showMyWichtel">{{ sub.name }}   <i :class="showSelection"></i></h5>
      <button class="btn bg-vue" v-if="newOne && !itsSelected" @click="thatsMe">Das bin Ich</button>
      
      <div v-if="itsMe">
        <Form @submit="updateWish">
          <div class="form-row">
            <div class="form-group mb-1">
              <label>Meine Wünsche</label>
              <Field
                as="textarea"
                name="wishList"
                type="textarea"
                class="form-control"
                id="wishList"
                v-model="wish"
              />
            </div>
            <div class="d-flex justify-content-end">
              <button class="btn bg-vue" @click="updateWish">Hinzufügen</button>
            </div>
          </div>
        </Form>
      </div>
    </div>
    <div class="card-footer" :class="showMyWichtel" v-if="itsMyWichtel">{{ sub.wish }}</div>
  </div>
</template>

<script>
import { Form, Field } from "vee-validate";
export default {
  name: "WichtelPerson",
  components: {
    Field,
    Form,
  },
  props: {
    sub: Object,
    newOne: Boolean,
    eventId: String,
  },
  data() {
    return {
      wish: "",
    };
  },
  mounted() {
    this.wish = this.sub.wish;
  },
  computed: {
    itsMe() {
      const myId = this.$store.getters.userId;
      return this.sub.id === myId;
    },
    itsMyWichtel() {
      const myId = this.$store.getters.userId;
      return this.sub.wichtel === myId;
    },
    itsSelected(){
      return this.sub.id;
    },
    showSelection(){
      return this.itsSelected ? "fa-solid fa-check" : "fa-solid fa-xmark";
    },
    showMyWichtel(){
      return this.itsMyWichtel ? "text-success" : "";
    },
  },
  methods: {
    updateWish(values) {
      const change = {change: {
        kind: "wish",
        eventId: this.eventId,
        wish: values.wishList,
      }}
      this.$emit("updateWish", change)
    },
    thatsMe(){
      const change = {change: {
        kind: "user",
        eventId: this.eventId,
        email: this.sub.email,
        name: this.sub.name
      }}
      this.$emit("thatsMe", change)
    },
  },
};
</script>

<style scoped></style>
