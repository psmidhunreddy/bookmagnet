<template>
  <div>
    <Navbar />
    <br>
    <h3>Sign Up</h3><br>
    <p v-if="msg">{{ msg }} <br><br></p>
    <label for="username">Pick a Username</label><br>
    <input id="username" name="username" required type="text" v-model="username"><br><br>
    <label for="name">Name</label><br>
    <input id="name" name="name" required type="text" v-model="name"><br><br>
    <label for="email">Email Address</label><br>
    <input id="email" name="email" required type="email" v-model="email"><br><br>
    <label for="password">Password</label> <br>
    <input id="password" name="password" type="password" v-model="password"><br>
    <br><br>
    <button id="submit" name="submit" type="submit" class="btn btn-primary"
    @click.prevent="register">Sign Up</button>
    <br><br>
    <button id="submit" name="submit" type="submit" class="btn btn-warning" @click="back">
            back</button>
  </div>
</template>
<script>
import Navbar from '@/components/Navbar.vue';

function json(response) {
  return response.json();
}
export default {
  name: 'Register',
  components: {
    Navbar,
  },
  data() {
    return {
      username: '',
      name: '',
      email: '',
      password: '',
      msg: '',
    };
  },
  methods: {
    back() {
      this.$router.push('/');
    },
    register() {
      fetch('http://127.0.0.1:5000/register', {
        method: 'post',
        headers: {
          'Content-type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          username: this.username, password: this.password, name: this.name, email: this.email,
        }),
      }).then(json)
        .then((data) => {
          if (data.msg === 'Registration Successful') {
            this.msg = data.msg;
            this.username = '';
            this.name = '';
            this.email = '';
            this.password = '';
            this.$router.push('/login');
          } else this.msg = data.msg;
        });
    },
  },
};
</script>
