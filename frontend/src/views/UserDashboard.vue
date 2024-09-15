<template>
    <div>
        <Navbar/>
        <AllBooks/>
    </div>
</template>
<script>
import AllBooks from '../components/AllBooks.vue';
import Navbar from '../components/Navbar.vue';

export default {
  name: 'UserDashboard',
  components: {
    Navbar,
    AllBooks,
  },
};
</script>
