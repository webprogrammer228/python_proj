import { makeAutoObservable } from "mobx";
import { animal } from "../types/animalsType";

class AnimalStore {
  private _animal: animal[] = [];

  constructor() {
    makeAutoObservable(this);
  }

  get animal() {
    return this._animal;
  }

  set animal(newAnimal) {
    this._animal = newAnimal;
  }
}

const animalStore = new AnimalStore();
export default animalStore;
