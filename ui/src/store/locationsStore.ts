import { makeAutoObservable } from "mobx";
import { locationType } from "../types/locationsTypes";

class LocationsStore {
  private _locations: locationType[] = [];

  constructor() {
    makeAutoObservable(this);
  }

  get locations() {
    return this._locations;
  }

  set locations(newLocation) {
    this._locations = newLocation;
  }
}

const locationsStore = new LocationsStore();
export default locationsStore;
