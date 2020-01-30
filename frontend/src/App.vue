<template>
  <div id="app">
    <div id="nav" class="sticky-top">
      <div class="frontpage">
        <div class>
          <nav class="navbar navbar-expand-md d-flex justify-content-between pt-1 navbarcolor">
            <div class="nav navbar d-flex justify-content-start m-0 p-0">
              <a class="navbar-brand nav-bar-title">
                <router-link to="/">
                  <i class="fa fa-wordpress"></i> MY BLOG
                </router-link>
              </a>
            </div>
            <b-navbar-toggle class target="nav-collapse">
              <i class="fa fa-align-justify"></i>
            </b-navbar-toggle>
            <b-collapse id="nav-collapse" is-nav>
              <b-navbar-nav class="ml-auto">
                <b-nav-item v-if="!isLogin" class="nav-item" v-b-modal.modal-login>Login</b-nav-item>
                <b-nav-item v-if="!isLogin" class="nav-item">
                  <router-link to="/register">Register</router-link>
                </b-nav-item>
                <b-nav-item v-if="isLogin && loggedUser.username" class="nav-item mx-auto">
                  <b-dropdown
                    id="profile"
                    variant="light"
                    :text="`Hello, ${loggedUser.username}`"
                    class="m-md-2"
                  >
                    <b-dropdown-item>
                      <div class="d-flex justify-content-between">
                        <router-link :to="`/profiles/${loggedUser.id}`">My Profile</router-link>
                        <div>
                          <i class="fa fa-user-o"></i>
                        </div>
                      </div>
                    </b-dropdown-item>
                    <b-dropdown-item>
                      <div class="d-flex justify-content-between">
                        <router-link :to="`/profiles/create`">Add Profile</router-link>
                        <div>
                          <i class="fa fa-plus"></i>
                        </div>
                      </div>
                    </b-dropdown-item>
                    <b-dropdown-item @click.prevent="logout">
                      <div class="d-flex justify-content-between">
                        <div>Signout</div>
                        <div>
                          <i class="fa fa-power-off"></i>
                        </div>
                      </div>
                    </b-dropdown-item>
                  </b-dropdown>
                </b-nav-item>
              </b-navbar-nav>
            </b-collapse>
          </nav>
        </div>
      </div>
    </div>
    <LoginModal></LoginModal>
    <router-view></router-view>
  </div>
</template>

<script>
import LoginModal from "@/components/LoginModal.vue";
import { mapState } from "vuex";

export default {
  name: "App",
  computed: {
    ...mapState(["isLogin", "loggedUser", "isSearchingUser", "userProfile"])
  },
  components: {
    LoginModal: LoginModal
  },
  methods: {
    toRegister() {
      this.$router.push("/register");
    },
    logout() {
      localStorage.removeItem("token");
      this.$store.commit("RESET");
      this.$router.push("/");
    },
    async checkLogin() {
      if (localStorage.getItem("token")) {
        await this.$store.dispatch("findUser");
      }
    },    
  },
  created() {
    this.checkLogin();
  }
};
</script>

<style>
* {
  margin: 0px;
  padding: 0px;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav {
  padding: 0px;
  margin: 0px;
}

#nav a {
  font-weight: 600;
  color: #131101;
}

#nav a:hover {
  color: #11172b;
  text-decoration: none;
  transition-delay: 1s;
}

#nav a.router-link-exact-active {
  color: #38128a;
  font-weight: 900;
}

h1,
h2,
h3,
h4,
h5 {
  font-family: "Oswald", sans-serif;
}
body.intro {
  background: rgb(22, 88, 223);
  background: linear-gradient(
    90deg,
    rgba(22, 88, 223, 1) 0%,
    rgba(234, 234, 226, 1) 0%,
    rgba(211, 201, 194, 1) 0%,
    rgba(215, 215, 215, 1) 0%,
    rgba(170, 98, 57, 1) 0%,
    rgba(202, 200, 75, 1) 0%,
    rgba(227, 208, 88, 1) 26%,
    rgba(242, 176, 85, 1) 51%,
    rgba(243, 130, 40, 1) 78%,
    rgba(242, 104, 8, 1) 96%
  );
}
.navbarcolor {
  background: rgb(22, 88, 223);
  background: linear-gradient(
    90deg,
    rgba(22, 88, 223, 1) 0%,
    rgba(234, 234, 226, 1) 0%,
    rgba(211, 201, 194, 1) 0%,
    rgba(215, 215, 215, 1) 0%,
    rgba(170, 98, 57, 1) 0%,
    rgba(202, 200, 75, 1) 0%,
    rgba(227, 208, 88, 1) 26%,
    rgba(242, 176, 85, 1) 51%,
    rgba(243, 130, 40, 1) 78%,
    rgba(242, 104, 8, 1) 96%
  );
}

body.edit {
  background-color: rgb(234, 241, 237);
}
</style>
