import axios from "axios";
import $api from "../api/instance";
import { animalType } from "../types/animalsType";

export async function getAnimalTypes(): Promise<animalType[] | string> {
  try {
    const response = await $api.get(`animals/types`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      return error.response?.data.message;
    } else {
      return "An unexpected error occurred";
    }
  }
}

export async function addAnimalType(newType: {type: string}): Promise<animalType | string> {
  try {
    const response = await $api.post(`animals/types`, newType);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      return error.response?.data.message;
    } else {
      return "An unexpected error occurred";
    }
  }
}


