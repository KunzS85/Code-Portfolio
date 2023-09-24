<template>
  <div>
    <div class="my-5 text-center offset-2 col-8">
      <img src="@/assets/welcome.svg" class="img-fluid" />
    </div>
    <div class="text-center">
      <h2>Jetzt registrieren</h2>
      <p>
        oder
        <a
          class="text-vue2"
          role="button"
          @click="changeComponent('LoginComponent')"
        >
          melden sie sich mit Ihrem Konto an
        </a>
      </p>
    </div>
    <div class="alert alert-danger col-md-8 offset-2" v-if="error">
      {{ errorDisplayText }}
    </div>
    <Form @submit="submitData" :validation-schema="schema" v-slot="{ errors }">
      <div class="form-row">
        <div class="form-group col-md-8 offset-2">
          <label for="name"><strong>Name</strong></label>
          <Field
            as="input"
            name="name"
            type="name"
            class="form-control"
            id="name"
          />
          <small class="text-danger" v-if="errors.name">{{
            errors.name
          }}</small>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group col-md-8 offset-2">
          <label for="email"><strong>E-Mail-Adresse</strong></label>
          <Field
            as="input"
            name="email"
            type="email"
            class="form-control"
            id="email"
          />
          <small class="text-danger" v-if="errors.email">{{
            errors.email
          }}</small>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group col-md-8 offset-2">
          <label for="password"><strong>Password</strong></label>
          <Field
            as="input"
            name="password"
            type="password"
            class="form-control"
            id="password"
          />
          <small class="text-danger" v-if="errors.password">{{
            errors.password
          }}</small>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group col-md-8 offset-2">
          <label for="password"><strong>Password wiederholen</strong></label>
          <Field
            as="input"
            name="confirmPassword"
            type="password"
            class="form-control"
            id="confirmPassword"
          />
          <small class="text-danger" v-if="errors.confirmPassword">{{
            errors.confirmPassword
          }}</small>
        </div>
      </div>
      <div class="form-row mt-3">
        <div class="form-group col-md-8 offset-2">
          <div class="d-grid">
            <button class="btn bg-vue">
              <span v-if="!isLoading">Registrieren</span>
              <span v-else class="spinner-border spinner-border-sm"></span>
            </button>
          </div>
        </div>
      </div>
    </Form>
  </div>
</template>

<script>
import { Form, Field } from "vee-validate";
import * as yup from "yup";

export default {
  name: "RegisterComponent",
  components: {
    Field,
    Form,
  },
  props: {
    prevPath: String,
  },
  emits: {
    "change-component": (payload) => {
      if (payload.componentName !== "LoginComponent") {
        return false;
      }
      return true;
    },
  },
  data() {
    const schema = yup.object().shape({
      name: yup.string().required("Name wird benötigt").trim(),
      email: yup
        .string()
        .required("E-Mail-Adresse wird benötigt")
        .trim()
        .email("Das ist keine gültige E-Mail-Adresse"),
      password: yup
        .string()
        .required("Ein Passwort wird benötigt")
        .min(6, "Das Passwort muss mindestens 6 Zeichen lang sein"),
      confirmPassword: yup
        .string()
        .oneOf([yup.ref("password")], "Passwörter stimmen nicht überein"),
    });
    return {
      schema,
      error: "",
      isLoading: false,
    };
  },
  computed: {
    errorDisplayText() {
      if (this.error) {
        if (this.error.includes("EMAIL_EXISTS")) {
          return "Diese E-Mail-Adresse existiert bereits";
        }
        return "Es ist ein unbekannter Fehler aufgetreten. Versuch es noch einmal";
      }
      return "";
    },
  },
  methods: {
    submitData(values) {
      this.isLoading = true;
      this.error = "";
      this.$store
        .dispatch("signUp", {
          email: values.email,
          password: values.password,
          name: values.name,
        })
        .then(() => {
          this.$store.dispatch("storeUser", {
            name: values.name,
            email: values.email,
          });
          this.isLoading = false;
          this.changeComponent("LoginComponent");
        })
        .catch((error) => {
          this.error = error.message;
          this.isLoading = false;
        });
    },
    changeComponent(componentName) {
      this.$emit("change-component", { componentName });
    },
  },
};
</script>

<style scoped></style>
