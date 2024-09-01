<style scoped>
h1 {
    font-weight: 500;
    font-size: 2.6rem;
    position: relative;
    top: -10px;
}

h3 {
    font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
    text-align: center;
}

@media (min-width: 1024px) {
    .greetings h1,
    .greetings h3 {
        text-align: left;
    }
}
</style>

<template>
  <h1 class="green">{{ msg }}</h1>
</template>

<script>
  import axios from 'axios';
  export default {
    data() {
      return {
        msg: ""
      };
    },
    methods: {
      getReponse() {
        const path = 'http://localhost:5000';
        axios.get(path)
        .then ((res) => {
          console.log(res.data)
          this.msg = res.data;
        }) 
        .catch ((err) => {
          console.error(err);
        });
      }
    },
    created() {
      this.getReponse();
    }
  }
</script>
