export default {
  mounted() {
    this.writeLogEntry(`${this.$options.name}-Component ist nun vollständig geladen.`);
  },
  methods: {
    writeLogEntry(text) {
      console.log(text);
    },
  },
};
