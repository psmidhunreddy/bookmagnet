<template>
  <div style="padding: 1em; background-color: paleturquoise">
  <b-row>
    <b-col md="6" offset-md="3">
    <img src="/logo.png" height="100px">
    <img src="/title.png" height="100px">
    </b-col>
  <b-col md="3">
    <span v-if="loggedin"><b>Last Logout: </b> {{ lastvisited }}</span><br>
    <b-button type="submit" @click="logout" v-if="loggedin" style="display: end;"
    variant="danger" >Logout</b-button>
  </b-col>
</b-row>
  </div>
</template>

<script>
function json(response) {
  return response.json();
}
export default {
  name: 'Navbar',
  msg: 'Navigation Bar',
  data() {
    return {
      loggedin: false,
      lastvisited: '',
    };
  },
  methods: {
    async checklogin() {
      const accessToken = localStorage.getItem('access_token');
      const lastvisited = localStorage.getItem('lastvisited');
      if (accessToken) {
        this.loggedin = true;
        this.lastvisited = lastvisited;
      }
    },
    logout() {
      fetch('http://127.0.0.1:5000/logout', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          'Content-type': 'application/json',
        },
      }).then(json)
        .then((data) => {
          localStorage.removeItem('access_token');
          alert(data.msg);
          this.$router.push('/login');
        })
        .catch((error) => {
          console.error('Logout error:', error);
        });
    },
  },
  mounted() {
    this.checklogin();
  },
};
</script>
