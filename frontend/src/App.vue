<template>
  <UserLayout>
    <router-view />
  </UserLayout>
</template>

<script>
import UserLayout from './components/UserLayout.vue';

export default {
  name: 'App',
  components: {
    UserLayout
  }
};
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>



