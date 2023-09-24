<template>
  <div class="card">
    <div class="d-flex justify-content-end" v-if="showNewEvent">
      <i class="fa-regular fa-circle-xmark" @click="toggleNewEvents"></i>
    </div>
    <div class="card-body d-flex justify-content-center">
      <button class="btn bg-vue2" @click="toggleNewEvents" v-if="!showNewEvent">
        Neues Event erfassen
      </button>
      <div
        class="container-fluid d-flex justify-content-center"
        v-if="showNewEvent"
      >
        <div class="row">
          <div class="col-12">
            <div class="card mb-2">
              <Form
                @submit="submitEvent"
                :validation-schema="eventSchema"
                v-slot="{ errors }"
              >
                <div class="card-body">
                  <h5 class="card-title"><b>Neues Event erfassen</b></h5>
                  <div class="form-row">
                    <div class="form-group mb-1">
                      <label>Name des Wichtelevents</label>
                      <Field
                        as="input"
                        name="wichtelEventName"
                        type="text"
                        class="form-control"
                        id="wichtelEventName"
                      />
                      <small
                        class="text-danger"
                        v-if="errors.wichtelEventName"
                        >{{ errors.wichtelEventName }}</small
                      >
                    </div>
                    <div class="form-group mb-1">
                      <label>Datum des Events</label>
                      <Field
                        as="input"
                        name="eventDatum"
                        type="date"
                        class="form-control"
                        id="eventDatum"
                      />
                      <small class="text-danger" v-if="errors.eventDatum">{{
                        errors.eventDatum
                      }}</small>
                    </div>
                    <div class="form-group mb-1">
                      <label>Event-Passwort</label>
                      <Field
                        as="input"
                        name="wichtelEventSubsPw"
                        type="text"
                        class="form-control"
                        id="wichtelEventSubsPw"
                      />
                      <small
                        class="text-danger"
                        v-if="errors.wichtelEventSubsPw"
                        >{{ errors.wichtelEventSubsPw }}</small
                      >
                    </div>
                  </div>
                  <h6><b>Teilnehmer:</b> </h6>
                  <ul v-for="sub in subs" :key="sub.email">
                    <li>{{ sub.name }}</li>
                  </ul>
                  <button
                    type="button"
                    class="btn bg-vue"
                    @click="toggleSubsForm"
                    v-if="!showSubsForm"
                  >
                    <i class="fa-solid fa-plus"></i>
                  </button>

                  <ul class="list-group list-group-flush" v-if="showSubsForm">
                    <div class="container-fluid">
                      <li class="list-group-item">
                        <div class="d-flex justify-content-end">
                          <i
                            class="fa-regular fa-circle-xmark"
                            @click="toggleSubsForm"
                          ></i>
                        </div>
                        <h6 class="card-title"><b>Teilnehmer erfassen:</b></h6>
                        <Form
                          @submit="submitSubscriber"
                          :validation-schema="subscriberSchema"
                          v-slot="{ errors }"
                        >
                          <div class="form-row">
                            <div class="form-group mb-1">
                              <label>Name</label>
                              <Field
                                as="input"
                                name="subsName"
                                type="text"
                                class="form-control"
                                id="subsName"
                              />
                              <small
                                class="text-danger"
                                v-if="errors.subsName"
                                >{{ errors.subsName }}</small
                              >
                            </div>
                            <div class="form-group mb-2">
                              <label>E-Mail Adresse</label>
                              <Field
                                as="input"
                                name="subsMail"
                                type="email"
                                class="form-control"
                                id="subsMail"
                              />
                              <small
                                class="text-danger"
                                v-if="errors.subsMail"
                                >{{ errors.subsMail }}</small
                              >
                            </div>
                            <div
                              class="container-fluid d-flex justify-content-center"
                            >
                              <button class="btn bg-vue">Hinzufügen</button>
                            </div>
                          </div>
                        </Form>
                      </li>
                    </div>
                  </ul>
                </div>
                <div class="card-footer">
                  <div class="d-grid gab-2">
                    <button class="btn bg-vue2" :class="disableAddEvent">
                      Event erstellen
                    </button>
                  </div>
                </div>
              </Form>
            </div>
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
  name: "NewWichtelEvent",
  components: {
    Field,
    Form,
  },
  beforeMount() {
    this.addActiveUserToSubscriber();
  },
  computed: {
    disableAddEvent() {
      if (this.subs.length < 2) {
        return "disabled";
      }
      return "";
    },
  },
  data() {
    const eventSchema = yup.object().shape({
      wichtelEventName: yup.string().required("Name wird benötigt").trim(),
      eventDatum: yup.date().required("Datum wird benötigt"),
      wichtelEventSubsPw: yup
        .string()
        .required("Passwort für Teilnahmebestätigung wird benötigt")
        .trim(),
    });
    const subscriberSchema = yup.object().shape({
      subsName: yup.string().required("Name wird benötigt").trim(),
      subsMail: yup
        .string()
        .required("E-Mail-Adresse wird benötigt")
        .trim()
        .email("Das ist keine gültige E-Mail-Adresse"),
    });

    return {
      showNewEvent: false,
      showSubsForm: false,
      subs: [],
      subscriberSchema,
      eventSchema,
      error: "",
    };
  },
  methods: {
    toggleNewEvents() {
      this.showNewEvent = !this.showNewEvent;
    },
    toggleSubsForm() {
      this.showSubsForm = !this.showSubsForm;
    },
    addActiveUserToSubscriber() {
      this.subs.push({
        name: localStorage.getItem("name"),
        id: localStorage.getItem("userId"),
      });
    },
    submitEvent(values, { resetForm }) {
      const subz = this.subs.map((sub) => sub);
      const wichtelEvent = {
        name: values.wichtelEventName,
        date: values.eventDatum,
        pw: values.wichtelEventSubsPw,
        subs: subz,
      };
      this.$store
        .dispatch("storeWichtelEvent", wichtelEvent)
        .then(() => {
          resetForm();
          this.subs.splice(1);
          this.toggleNewEvents();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    submitSubscriber(values, { resetForm }) {
      this.subs.push({ name: values.subsName, email: values.subsMail });
      resetForm();
      this.toggleSubsForm();
    },
  },
};
</script>

<style scoped></style>
