<template>
  <div>
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-4 offset-md-4 col-sm-10 offset-sm-1 col-xs-10 offset-xs-1">
          <h5 class="text-center text-primary">
            First, create your
            <span class="text-light">MY BLOG</span> account.
          </h5>
          <b-form
            id="register"
            @submit.prevent="register"
            class="border rounded p-3 bg-white shadow mt-4"
          >
            <div v-if="errorMessage" class="text-center">
              <h2 class="text-danger">
                <i class="fa fa-times-circle-o"></i> Opps !!!
              </h2>
              <p class="text-danger border rounded p-2 mx-2 border-danger">{{errorMessage}}</p>
            </div>
            <b-form-group>
              <label for="exampleInputEmail1">Email address</label>
              <input
                v-model="email_register"
                id="email"
                type="email"
                class="form-control"
                required
                placeholder="Email"
              />
            </b-form-group>
            <b-form-group>
              <label for="username">Username</label>
              <input
                v-model="username_register"
                id="username"
                type="text"
                class="form-control"
                placeholder="Username"
                required
              />
            </b-form-group>
            <b-form-group>
              <label for="password_register">Password</label>
              <input
                v-model="password_register"
                placeholder="Password"
                id="password"
                type="password"
                class="form-control"
                required
              />
            </b-form-group>
            <b-form-group>
              <label for="password_register">Confirm Password</label>
              <input
                v-model="confirm_password_register"
                placeholder="Confirm Password"
                id="confirm_password"
                type="password"
                class="form-control"
                required
              />
            </b-form-group>
            <div class="form-inline" style="margin: 5px auto;">
              <button type="submit" class="btn btn-outline-dark btn-sm btn-block mt-2">
                <b-spinner small v-if="loginLoading" variant="dark" label="Spinning"></b-spinner>
                <span v-if="!loginLoading">Register</span>
              </button>
            </div>
          </b-form>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import server from "@/api/server.js";

export default {
  components: {
  },
  data() {
    return {
      errorMessage: "",
      loginMessage: "",
      loginLoading: false,      
      email_register: "",
      password_register: "",
      confirm_password_register: "",
      username_register: "",
    };
  },
  methods: {
    success: function(message) {
      this.$alertify.success(message);
    },    
    async register() {
      this.loginLoading = true;
      try {
        let { data } = await server.post("/register", {
          username: this.username_register,
          email: this.email_register,
          password: this.password_register,
          confirm_password: this.confirm_password_register
        });
        this.success(data.message);
        this.$bvModal.show("modal-login");
      } catch (err) {
        console.log(err.response);
        let messages = [];
        for (let index in err.response.data) {
          messages.push(err.response.data[index]);
        }
        this.errorMessage = messages.join(', ');
        this.$alertify.error(messages.join(', '));
      } finally {
        this.loginLoading = false;
      }
    },
    clearForm() {
      this.email_register = "";
      this.username_register = "";
      this.password_register = "";
      this.confirm_password_register = "";
    }
  },
  beforeCreate: function() {
    document.body.className = "intro";
  }
};
</script>

<style>
</style>
