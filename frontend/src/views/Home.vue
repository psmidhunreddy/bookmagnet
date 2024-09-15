<template>
  <div>
  <Navbar/>
  <h1>Welcome to BookMagnet</h1><br>
  <button class="btn" type="submit" @click="toReg">Sign Up</button>
  <br>
  <h4>Already Using?</h4>
  <button class="btn" type="submit" @click="toLog">Log In</button>
  <br><br>
</div>
</template>
<script>
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'Home',
  methods: {
    toReg() {
      this.$router.push('/register');
    },
    toLog() {
      this.$router.push('/login');
    },
  },
  components: {
    Navbar,
  },
};
</script>
<style scoped>
  h1 {
    margin: 40px 0 0;
    color: indianred;
  }
  .btn{
    width: 20%;
    background-color: white;
    color:#653187;
    cursor: pointer;
    padding: 10px 16px;
    border: none;
  }
  .btn:hover{
    background-color: #00ffff;
    color: white;
  }
</style>
