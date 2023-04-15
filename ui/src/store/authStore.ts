import { makeAutoObservable } from "mobx";
import Cookies from "js-cookie";

class authStore {
  private _isLoggedIn: string = Cookies.get("logged") || false;
  private _email = "";
  private _id = Cookies.get("id") || "";
  private _firstName = "";
  private _lastName = "";

  constructor() {
    makeAutoObservable(this);
  }

  get logged() {
    return this._isLoggedIn;
  }
  set logged(newVal) {
    this._isLoggedIn = newVal;
  }

  get email() {
    return this._email;
  }
  set email(newMail) {
    this._email = newMail;
  }

  get id() {
    return this._id;
  }
  set id(newId) {
    this._id = newId;
  }

  get firstName() {
    return this._firstName;
  }
  set firstName(newFirstName) {
    this._firstName = newFirstName;
  }

  get lastName() {
    return this._lastName;
  }
  set lastName(newLastName) {
    this._lastName = newLastName;
  }
}

const auth = new authStore();
export default auth;
