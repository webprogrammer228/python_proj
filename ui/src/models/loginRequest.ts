import $api from "../api/instance";
import Cookies from "js-cookie";
import axios from "axios";
import { NavigateFunction } from "react-router-dom";
import auth from "../store/authStore";

type Inputs = {
  email: string;
  password: string;
};

type Other = {
  setErrorMessage: (error: string) => void;
  navigate: NavigateFunction;
};

async function loginRequest(
  data: Inputs,
  { setErrorMessage, navigate }: Other
) {
  try {
    const user = (await $api.post("accounts/signIn", data)).data;
    Cookies.set("logged", window.btoa(data.email + ":" + data.password));
    Cookies.set("id", user.id);
    auth.logged = window.btoa(data.email + ":" + data.password);
    setErrorMessage("");
    navigate("/main");
  } catch (error) {
    if (axios.isAxiosError(error)) {
      setErrorMessage(error.message);
    } else {
      setErrorMessage("An unexpected error occurred");
    }
  }
}

export default loginRequest;
