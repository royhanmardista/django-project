<template>
  <div>
    <div>
      <div class="container">
        <div class="row">
          <div v-if="gettingUserProfile" style="position:fixed;top:50%;left:45%">
            <PacmanLoader color="#5BC0EB" :size="50"></PacmanLoader>
          </div>
        </div>
      </div>
    </div>
    <div v-if="!userProfile && !gettingUserProfile" class="text-center mt-3">
      <h3>
        <i class="fa fa-frown-o"></i> Sorry ..., it seems that the user haven't make any profile
      </h3>
    </div>
    <div v-if="!gettingUserProfile">
      <div class="container" v-if="userProfile">
        <div class="col-md-10 offset-md-1 mt-2 p-3">
          <div class="row shadow p-3">
            <div class="col-md-2 p-0 mx-2">
              <b-img
                :src="userProfile.profile.photo"
                alt
                srcset
                style=" width: 100%;
                min-height: 8vw;
                object-fit: cover;"
                class="rounded"
              />
            </div>
            <div class="col-md-9 d-flex flex-column p-0 m-2 container">
              <div class="d-flex">
                <h3 class>{{userProfile.user.username.toUpperCase()}}</h3>
                <div
                  v-if="userProfile.profile.user == loggedUser.id"
                  class="editProfile h3"
                  v-b-tooltip.hover
                  title="Edit your profile"
                  @click.prevent="toEditPage(userProfile.profile.user)"
                >
                  <i class="ml-2 fa fa-pencil"></i>
                </div>
              </div>
              <div class="d-flex justify-content-between row">
                <div class="col-md-4">
                  <div class="mt-2">
                    <div class="text-secondary font-weight-bold">
                      <i class="fa fa-phone"></i> Phone
                    </div>
                    {{userProfile.profile.phone}}
                  </div>
                </div>
                <div class="col-md-4 mb-2">
                  <div class="mt-2">
                    <div class="text-secondary font-weight-bold">
                      <i class="fa fa-envelope"></i> Email
                    </div>
                    {{userProfile.user.email}}
                  </div>
                </div>
              </div>
              <div class="ml-auto mt-auto" v-if="userProfile.profile.user == loggedUser.id">
                <b-button
                  variant="danger"
                  class="mt-2"
                  size="lg"
                  @click.prevent="deleteProfile(userProfile.profile.user)"
                >
                  <h5 class="mb-0">Delete Profile</h5>
                </b-button>
              </div>
            </div>
          </div>
          <div class="row mt-3 shadow p-3">
            <h4>Firstname</h4>
            <div class="container mt-3">
              <div class="row">
                <span class="container text-justify" v-html="userProfile.profile.firstname"></span>
              </div>
            </div>
          </div>
          <div class="row mt-3 shadow p-3">
            <h4>Lastname</h4>
            <div class="container mt-3">
              <div>{{userProfile.profile.lastname}}</div>
            </div>
          </div>

          <div class="row mt-3 shadow p-3">
            <h4>Age</h4>
            <div
              class="container mt-3"
            >{{moment().diff(userProfile.profile.date_of_birth, 'years')}} years old</div>
          </div>

          <div class="row mt-3 shadow p-3">
            <h4>Nationality</h4>
            <b-form-select v-model="userProfile.profile.nationality" :options="countries" required></b-form-select>
          </div>

          <div class="row mt-3 shadow p-3">
            <h4>Gender</h4>
            <div class="container mt-3">
              <div>{{userProfile.profile.gender}}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { PacmanLoader } from "@saeris/vue-spinners";

export default {
  name: "UserProfile",
  data() {
    return {};
  },
  components: {
    PacmanLoader
  },
  computed: {
    ...mapState([
      "userProfile",
      "loggedUser",
      "gettingUserProfile",
      "gettingCountry",
      "countries"
    ])
  },
  created() {
    this.getUserProfile();
  },
  methods: {
    toEditPage(userId) {
      this.$router.push(`/profiles/${userId}/update`);
    },
    async getUserProfile() {
      await this.$store.dispatch(
        "getUserProfile",
        this.$router.currentRoute.params.id
      );
      await this.$store.dispatch("getCountry");
    },
    deleteProfile(userId) {
      this.$alertify
        .confirm(
          () => this.$alertify.success("ok"),
          () => this.$store.dispatch("deleteProfile", userId)
        )
        .setHeader(
          '<h1 class=" text-danger"><i class="fa fa-ban"></i> Danger !!!</h1> '
        )
        .setContent(
          '<h5 class="text-justify" style="min-height:100px"> Are you sure, you want to delete your profile ? You cannot revert this action !!!</h5>'
        )
        .show();
    }
  },
  beforeCreate: function() {
    document.body.className = "edit";
  }
};
</script>

<style scoped>
.editProfile {
  cursor: pointer;
  color: rgb(104, 104, 110);
}

.editProfile:hover {
  color: rgb(45, 55, 197);
}

h3,
h4 {
  color: darkorange;
}
</style>
