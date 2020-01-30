<template>
  <div class="container-fluid">
    <div class="row mt-3">
      <div v-if="gettingUserProfile" style="position:fixed;top:50%;left:45%">
        <PacmanLoader color="#5BC0EB" :size="50"></PacmanLoader>
      </div>
    </div>
    <div class="row mt-3" v-if="!gettingUserProfile">
      <div class="col-md-8 offset-md-2 shadow rounded p-3 bg-light">
        <h3 class="text-center">Update Your Profile</h3>
        <b-form @submit.prevent="updateProfile()">
          <!-- first name -->
          <b-form-group label="Firstname">
            <b-form-input
              v-model="userProfile.profile.firstname"
              type="text"
              required
              placeholder="Enter Firstname"
            ></b-form-input>
          </b-form-group>

          <!-- last name -->
          <b-form-group label="Lastname">
            <b-form-input
              v-model="userProfile.profile.lastname"
              type="text"
              required
              placeholder="Enter Lastname"
            ></b-form-input>
          </b-form-group>

          <!-- birth date -->
          <b-form-group label="Select your birth date">
            <b-form-input v-model="userProfile.profile.date_of_birth" required type="date"></b-form-input>
          </b-form-group>

          <!-- phone -->
          <b-form-group label="Phone">
            <b-form-input
              v-model="userProfile.profile.phone"
              required
              placeholder="Insert your phone number"
              type="text"
            ></b-form-input>
          </b-form-group>

          <!-- Nationality -->
          <b-form-group label="Nationality">
            <b-form-select v-model="userProfile.profile.nationality" :options="countries" required></b-form-select>
          </b-form-group>

          <!-- gender -->
          <b-form-group label="Gender">
            <b-form-select v-model="userProfile.profile.gender" :options="genders" required></b-form-select>
          </b-form-group>

          <!-- photo -->
          <b-form-group label="Photo">
            <b-form-file
              v-model="photo"
              :state="Boolean(photo)"
              :placeholder="userProfile.profile.photo"
              drop-placeholder="Drop file here..."
            ></b-form-file>
          </b-form-group>
          <!-- submit -->
          <b-button type="submit" variant="primary mr-2">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import moment from "moment";
import { PacmanLoader } from "@saeris/vue-spinners";
import FormData from "form-data";

export default {
  name: "UpdateUserProfile",
  component: {
    PacmanLoader
  },
  computed: {
    ...mapState(["countries","userProfile", "gettingUserProfile"]),        
  },
  created() {
    this.getUserProfile();
  },
  data() {
    return {    
      photo : null,  
      genders: [
        { text: "Select Gender", value: null },
        "male",
        "female",
        "other"
      ],
      
    };
  },
  methods: {
    async getUserProfile() {
      await this.$store.dispatch(
        "getUserProfile",
        this.$router.currentRoute.params.id
      );
      await this.$store.dispatch("getCountry");
    },
    updateProfile() {
      let data = new FormData();
      data.append("firstname", this.userProfile.profile.firstname);
      data.append("lastname", this.userProfile.profile.lastname);
      data.append("date_of_birth", this.userProfile.profile.date_of_birth);
      data.append("phone", this.userProfile.profile.phone);
      data.append("nationality", this.userProfile.profile.nationality);
      data.append("gender", this.userProfile.profile.gender);
      if (this.photo) {
        data.append("photo", this.photo);
      }
      let payload = {
        form : data,
        userId : this.userProfile.profile.user
      }
      this.$store.dispatch("updateProfile", payload);
    }
  }
};
</script>
