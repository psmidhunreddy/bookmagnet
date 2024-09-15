<template>
    <div>
        <Navbar />
        <br>
        <h3>Log In</h3><br>
        <p v-if="msg">{{ msg }} <br><br></p>
        <label for="username">Username</label><br>
        <input id="username" name="username" required type="text" v-model="username"><br><br>
        <label for="password">Password</label><br>
        <input id="password" name="password" required type="password" v-model="password"><br><br>
        <button id="submit" name="submit" type="submit" class="btn btn-primary"
        @click.prevent="login">Login</button>
            <br><br>
        <button id="submit" name="submit" type="submit" class="btn btn-warning" @click="back">
            back</button>
    </div>
</template>
<script>
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'Login',
  components: {
    Navbar,
  },
  data() {
    return {
      username: '',
      password: '',
      msg: '',
    };
  },
  methods: {
    back() {
      this.$router.push('/');
    },
    async login() {
      const formdata = {
        username: this.username,
        password: this.password,
      };
      try {
        const response = await fetch('http://localhost:5000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formdata),
        });
        const data = await response.json();
        if (response.ok) {
          localStorage.setItem('access_token', data.access_token);
          localStorage.setItem('lastvisited', data.last_visit);
          console.log('Success', data.user.role);
          if (data.user.role === 'user') {
            localStorage.setItem('stored_rating', JSON.stringify(data.user.stored_rating));
            this.$router.push('/userdashboard');
          } else if (data.user.role === 'admin') {
            console.log(localStorage.getItem('access_token'));
            this.$router.push('/admindashboard');
          }
        } else this.msg = data.msg;
      } catch (error) {
        alert('An error occurred while attempting to Login.');
      }
    },
  },
};
</script>
