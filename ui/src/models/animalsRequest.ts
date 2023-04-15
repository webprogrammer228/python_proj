import axios from "axios";
import $api from "../api/instance";
import Cookies from "js-cookie";
import { animal, newAnimalType } from "../types/animalsType";

export async function getAnimal(): Promise<animal[] | string> {
  try {
    const response = await $api.get(
      `animals/search?chipperId=${Cookies.get("id")}`
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      return error.response?.data.message;
    } else {
      return "An unexpected error occurred";
    }
  }
}

export async function addAnimal(
  newAnimal: newAnimalType
): Promise<animal | string> {
  try {
    const response = await $api.post(`animals`, newAnimal);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      return error.response?.data.message;
    } else {
      return "An unexpected error occurred";
    }
  }
}
