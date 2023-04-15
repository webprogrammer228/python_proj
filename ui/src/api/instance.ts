import axios from "axios";
import { BACKEND_URL } from "../constants";
import Cookies from "js-cookie";

const $api = axios.create({
  baseURL: BACKEND_URL,
});

$api.interceptors.request.use(
  function (config) {
    config.headers["Authorization"] = "Basic " + Cookies.get("logged");
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

export default $api;
