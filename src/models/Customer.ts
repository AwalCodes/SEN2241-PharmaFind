import { User } from "./User";

// Customer inherits from User (Inheritance).
export class Customer extends User {
  private _location: string;

  constructor(id: number, name: string, email: string, location: string) {
    super(id, name, email);
    this._location = location;
  }

  get location(): string {
    return this._location;
  }

  set location(value: string) {
    this._location = value;
  }

  getRole(): string {
    return "Customer";
  }
}
