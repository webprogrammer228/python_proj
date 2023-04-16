import axios from "axios";
import $api from "../api/instance";
import { locationType } from "../types/locationsTypes";

export async function getLocations(): Promise<locationType[] | string> {
  try {
    const response = await $api.get("locations");
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      return error.response?.data.message;
    } else {
      return "An unexpected error occurred";
    }
  }
}

export async function addNewLocation(location: {
  longitude: number;
  latitude: number;
}): Promise<locationType | string> {
  try {
    const response = await $api.post("locations", location);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      return error.response?.data.message;
    } else {
      return "An unexpected error occurred";
    }
  }
}
