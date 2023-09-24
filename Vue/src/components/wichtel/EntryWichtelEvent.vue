<template>
  <div class="card">
    <div class="d-flex justify-content-end" v-if="showEntryCheck">
      <i class="fa-regular fa-circle-xmark" @click="toggleEntryCheck"></i>
    </div>
    <div class="card-body d-flex justify-content-center">
      <button
        class="btn bg-vue2"
        @click="toggleEntryCheck"
        v-if="!showEntryCheck"
      >
        Einem Event beitreten
      </button>
      <div
        class="container-fluid d-flex justify-content-center"
        v-if="showEntryCheck"
      >
        <div class="card">
          <div class="card-body">
            <h5 class="card-title"><b >Einem Event beitreten:</b></h5>
            <Form
              @submit="checkEventPass"
              :validation-schema="checkSchema"
              v-slot="{ errors }"
            >
              <div class="form-row">
                <div class="form-group mb-1">
                  <label>Name des Wichtelevents</label>
                  <Field
                    as="input"
                    name="wichtelEventNameCheck"
                    type="text"
                    class="form-control"
                    id="wichtelEventNameCheck"
                  />
                  <small
                    class="text-danger"
                    v-if="errors.wichtelEventNameCheck"
                    >{{ errors.wichtelEventNameCheck }}</small
                  >
                </div>
                <div class="form-group mb-1">
                  <label>Passwort des Wichtelevents</label>
                  <Field
                    as="input"
                    name="wichtelEventPassCheck"
                    type="password"
                    class="form-control"
                    id="wichtelEventPassCheck"
                  />
                  <small
                    class="text-danger"
                    v-if="errors.wichtelEventPassCheck"
                    >{{ errors.wichtelEventPassCheck }}</small
                  >
                </div>
                <div class="container-fluid d-flex justify-content-center">
                  <button class="btn bg-vue">Prüfen</button>
                </div>
              </div>
            </Form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Form, Field } from "vee-validate";
import * as yup from "yup";

export default {
  name: "EntryWichtelEvent",
  components: {
    Form,
    Field,
  },
  data() {
    const checkSchema = yup.object().shape({
      wichtelEventNameCheck: yup.string().required("Name wird benötigt").trim(),
      wichtelEventPassCheck: yup
        .string()
        .required("Passwort wird benötigt")
        .trim(),
    });
    return {
      showEntryCheck: false,
      checkSchema,
    };
  },
  computed: {},
  methods: {
    toggleEntryCheck() {
      this.showEntryCheck = !this.showEntryCheck;
    },
    checkEventPass(values, { resetForm }) { 
      const eventName = values.wichtelEventNameCheck;
      const eventPw = values.wichtelEventPassCheck;
      const event = this.$store.getters.getAllWichtelEventbyNameAndPw(
        eventName,
        eventPw
      );
      if(event){
        this.$router.push({name: 'WichtelEvent', params: {id: event.id }})
      }else{
        resetForm();
      }
    },
  },
};
</script>

<style scoped></style>
