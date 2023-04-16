import { AxiosResponse } from "axios";
import $api from "../api/instance";
import Cookies from "js-cookie";

type accountRequestType = {
  email: string;
  firstName: string;
  lastName: string;
  id: number;
};

async function accountRequest(): Promise<
  AxiosResponse<accountRequestType, string>
> {
  return await $api
    .get(`/accounts/${Cookies.get("id")}`)
    .then((val) => val)
    .catch((e) => e.data.message);
}

export default accountRequest;
