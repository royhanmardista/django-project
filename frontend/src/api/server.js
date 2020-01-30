import axios from "axios";

const server = axios.create({
  // baseURL: "http://127.0.0.1:8000/"
  baseURL: "http://34.87.8.107/"

});

export default server;