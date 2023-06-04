<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <router-link class="navbar-brand" to="/">Home</router-link>
      <button class="navbar-toggler" type="button" @click="isNavOpen = !isNavOpen">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" :class="{ show: isNavOpen }" id="navbarNav">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/Login">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/Register">Register</router-link>
          </li>
        </ul>
        <!-- <ul class="navbar-nav"> -->
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <i class="fa fa-user"></i> {{ getUsername }}
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <a class="dropdown-item" href="#">Profile</a>
              <a class="dropdown-item" href="#">Logout</a>
            </div>
          </li>
        <!-- </ul> -->
      </div>
    </nav>
    <div class="mt-3">
      <!-- 这里是插槽 -->
      <slot></slot>
      <div v-if="$slots.default === undefined">No content in slot</div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'UserLayout',
  data() {
    return {
      isNavOpen: false
    };
  },
  computed: {
    ...mapGetters([
      'getUsername'
    ]),
  },
};
</script>
