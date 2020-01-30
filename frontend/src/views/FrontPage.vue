<template>
  <div class="text-center" id="frontPage">
    <div class="d-flex justify-content-center container-fluid">
      <div class="row mx-1">
        <div id="search" class="d-flex flex-column justify-content-center">
          <div class="text-white">
            <h1>
              <i class="fa fa-wordpress"></i> MY BLOG
            </h1>
            <p>Helps you find your frieds</p>
            <div>
              <!-- <b-form @submit.prevent="searchUser">
                <b-input-group size="lg" class="mt-2 ml-1 pt-1" placeholder="search">
                  <b-form-input v-model="description" placeholder="Search User..."></b-form-input>
                  <b-input-group-append class="mr-1">
                    <b-button size="lg" text="Button" variant="primary" type="submit">
                      <i class="fa fa-search"></i>
                    </b-button>
                  </b-input-group-append>
                </b-input-group>
              </b-form> -->
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- list of user start -->
    <div class="container-fluid">
      <h2 class="mt-5" v-b-toggle.user-collapse style="cursor:pointer">List of User</h2>
      <h4>{{ allusers.length }} users found in MY BLOG</h4>
      <b-collapse id="user-collapse" :visible="true">
        <p>Page: {{ currentPage }}</p>
        <b-pagination
          v-model="currentPage"
          :total-rows="rows"
          :per-page="perPage"
          aria-controls="users"
        ></b-pagination>
        <!-- spinner start -->
        <div v-if="gettingAllUsers">
          <div class="text-center d-flex justify-content-center">
            <b-spinner type="grow" label="Loading..."></b-spinner>
          </div>
        </div>
        <!-- spinner end -->
        <div class="row" v-if="!gettingAllUsers">
          <div
            id="github"
            :per-page="perPage"
            :current-page="currentPage"
            class="col-md-4 col-xs-12 col-sm-12"
            v-for="user in users"
            :key="user._id"
          >
            <div
              class="border rounded px-3 py-1 mb-3 d-flex flex-column justify-content-between"
              style="min-height:100px"
            >
              <div class="d-flex flex-column justify-content-between p-2">
                <div class="border rounded-circle col-4 mx-auto userId bg-light">
                  <h1>{{user.id}}</h1>
                </div>
                <h5>
                  <a
                    href
                    class="text-dark"
                    @click.prevent="showUserDetail(user.id)"
                  >{{ user.username }}</a>
                </h5>
                <p>
                  <i class="fa fa-envelope"></i>
                  {{ user.email }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </b-collapse>
    </div>
    <!-- list of user end -->
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "FrontPage",
  created() {
    this.getAllUsers();
    this.reload();
  },
  computed: {
    ...mapState(["isLoading", "allusers", "gettingAllUsers", "isLogin"]),
    rows() {
      return this.allusers.length;
    },
    users() {
      return this.allusers.slice(
        (this.currentPage - 1) * this.perPage,
        this.currentPage * this.perPage
      );
    }
  },
  data() {
    return {
      perPage: 9,
      currentPage: 1,
      description: ""
    };
  },
  methods: {
    showUserDetail(pk) {
      this.$router.push(`profiles/${pk}`);
    },
    async reload() {
      if (this.$router.currentRoute.fullPath !== "/") {
        await this.getAllUsers();
        this.currentPage = this.$router.currentRoute.query.page;
      }
    },    
    async getAllUsers() {
      await this.$store.dispatch("getAllUsers");
    }
  },
  watch: {
    currentPage: function() {
      this.$router
        .push({
          query: {
            page: this.currentPage
          }
        })
        .catch(err => {});
    }
  },
  beforeCreate: function() {
    if (this.isLogin) {
      document.body.className = "welcome";
    } else {
      document.body.className = "intro";
    }
  }
  // beforeRouteUpdate(to, from, next) {
  //   console.log('ketrigger')
  //   this.getAllUsers();
  //   next()
  // }
};
</script>

<style>
.userId {
  width: 75px;
  height: 75px;
}
</style>
