<template>
  <div>
    <b-modal
      id="modal-login"
      ref="login-modal"
      @show="resetModal"
      @hidden="resetModal"
      hide-footer
      header-text-variant="primary"
      footer-border-variant="warning"
      content-class="shadow"
      centered
    >
      <template v-slot:modal-title>
        <h4>Sign in to your account</h4>
      </template>
      <div v-if="errorMessage" class="text-center">
        <h2 class="text-danger">
          <i class="fa fa-times-circle-o"></i> Opps !!!
        </h2>
        <p class="text-danger border rounded p-2 mx-2 border-danger">
          {{ errorMessage }}
        </p>
      </div>
      <b-form ref="form" class="p-2">
        <!-- username -->
        <div class="form-group input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">
              <i class="fa fa-user"></i>
            </span>
          </div>
          <input
            name
            id="username"
            class="form-control"
            placeholder="Enter username"
            v-model="username"
            type="username"
          />
        </div>
        <!-- username end  -->

        <!-- password start -->
        <div class="form-group input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">
              <i class="fa fa-lock"></i>
            </span>
          </div>
          <input
            id="password"
            class="form-control"
            placeholder="Enter password"
            type="password"
            v-model="password"
          />
        </div>
        <!-- form-group// -->
        <div class="form-group">
          <button
            type="submit"
            class="btn btn-warning btn-block"
            @click.prevent="login"
          >
            <b-spinner
              small
              v-if="loginLoading"
              variant="light"
              label="Spinning"
            ></b-spinner>
            <span v-if="!loginLoading">Signin</span>
          </button>
        </div>
        <!-- password end -->
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import server from "@/api/server";

export default {
  name: "LoginModal",
  components: {},
  created() {},
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
      loginMessage: "",
      loginLoading: false
    };
  },
  methods: {
    success: function(message) {
      this.$alertify.success(message);
    },
    resetModal() {
      this.username = "";
      this.password = "";
      this.errorMessage = "";
    },
    async login() {
      this.errorMessage = "";
      this.loginLoading = true;
      try {
        let { data } = await server.post("/login", {
          username: this.username,
          password: this.password
        });
        localStorage.setItem("token", data.token);
        this.success(data.message);
        this.$refs["login-modal"].hide();        
        this.$store.commit("SET_LOGGED_USER", data.user);
        this.$store.commit("SET_ISLOGIN", true)
        if (this.$router.currentRoute.path != '/') {
          this.$router.push('/')
        }
      } catch (err) {
        this.errorMessage = err.response.data.error;
        this.$alertify.error(this.errorMessage);
      } finally {
        this.loginLoading = false;
      }
    }
  }
};
</script>

<style scoped>
h4 {
  color: rgb(224, 121, 36);
}
</style>
