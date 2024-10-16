<template>
    <button
      v-if="isVisible"
      @click="scrollToTop"
      class="back-to-top"
    >
    <i class="fa-solid fa-arrow-up"></i>
    </button>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isVisible: false,
      };
    },
    methods: {
      scrollToTop() {
        window.scrollTo({
          top: 0,
          behavior: 'smooth',
        });
      },
      toggleVisibility() {
        this.isVisible = window.scrollY > 300;
      },
    },
    mounted() {
      window.addEventListener('scroll', this.toggleVisibility);
    },
    beforeMount() {
      window.removeEventListener('scroll', this.toggleVisibility);
    },
  };
  </script>
  
  <style scoped>
  .back-to-top {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    transition: opacity 0.3s ease;
  }
  
  .back-to-top:hover {
    background-color: #2980b9;
  }
  </style>
  