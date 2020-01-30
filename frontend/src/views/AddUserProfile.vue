<template>
  <div class="container-fluid mt-3">
    <div class="row">
      <div class="col-md-8 offset-md-2 p-3 bg-light shadow">
        <h3 class="text-center">You have not complete your profile, please complete this form</h3>
        <b-form @submit.prevent="createProfile">
          <!-- first name -->
          <b-form-group label="Firstname">
            <b-form-input v-model="firstname" type="text" required placeholder="Enter firstname"></b-form-input>
          </b-form-group>
          <!-- last name -->
          <b-form-group label="Lastname">
            <b-form-input v-model="lastname" type="text" required placeholder="Enter lastname"></b-form-input>
          </b-form-group>
          <!-- birth date -->
          <b-form-group label="Select your birth date">
            <b-form-input v-model="date_of_birth" required type="date"></b-form-input>
          </b-form-group>
          <!-- phone -->
          <b-form-group label="Phone">
            <b-form-input
              v-model="phone"
              required
              placeholder="Insert your phone number"
              type="text"
            ></b-form-input>
          </b-form-group>
          <!-- nationality -->
          <b-form-group label="Nationality">
            <b-form-select v-model="nationality" :options="countries" required></b-form-select>
          </b-form-group>
          <!-- gender -->
          <b-form-group label="Gender">
            <b-form-select v-model="gender" :options="genders" required></b-form-select>
          </b-form-group>
          <!-- photo -->
          <b-form-group label="Photo">
            <b-form-file
              v-model="photo"
              :state="Boolean(photo)"
              placeholder="Choose your profile picture..."
              drop-placeholder="Drop file here..."
            ></b-form-file>
          </b-form-group>
          <div class="my-3">Selected file: {{ photo ? photo.name : '' }}</div>
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
import FormData from "form-data";

export default {
  name: "AddUserProfile",
  component: {},
  computed: {
    ...mapState(["countries"])
  },
  data() {
    return {
      firstname: null,
      lastname: null,
      date_of_birth: null,
      phone: null,
      nationality: null,
      gender: null,
      genders: [
        { text: "Select Gender", value: null },
        "male",
        "female",
        "other"
      ],
      photo: null
    };
  },
  methods: {
    createProfile() {
      let data = new FormData();
      data.append("firstname", this.firstname);
      data.append("lastname", this.lastname);
      data.append("date_of_birth", this.date_of_birth);
      data.append("phone", this.phone);
      data.append("nationality", this.nationality);
      data.append("gender", this.gender);
      data.append("photo", this.photo);
      this.$store.dispatch("createProfile", data);
    }
  },
  created() {
    this.$store.dispatch("getCountry");
  }
};
</script>
