<template>
  <div class="card">
    <img src="https://picsum.photo/200" />
    <div class="card-body">
      <h5 class="card-title">{{ product.title }}</h5>
      <p class="card-text">{{ shortenDescription }}</p>
      <div class="text-center mt-3">
        <div class="lead">
          <strong class="text-vue">{{ product.price }}.-</strong>
        </div>
      </div>
      <router-link :to="{name: 'ReadProduct', params: {id: product.id }}" class="stretched-link"></router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProductListItem",
  props: {
    product: Object,
  },
  computed: {
    shortenDescription() {
        if(this.product.description.length < 80){
            return this.product.description;
        }
        return this.product.description.slice(0,80) +"..."
    },
  },
};
</script>

<style scoped></style>
