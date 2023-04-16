import { makeAutoObservable } from "mobx";
import { animalType } from "../types/animalsType";

class AnimalTypeStore {
  private _animalTypes: animalType[] | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  get animalType() {
    return this._animalTypes;
  }

  set animalType(newAnimalType) {
    this._animalTypes = newAnimalType;
  }
}

const animalTypeStore = new AnimalTypeStore();
export default animalTypeStore;
