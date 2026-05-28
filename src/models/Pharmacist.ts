import { User } from "./User";

// Pharmacist inherits from User (Inheritance).
export class Pharmacist extends User {
  private _pharmacyName: string;

  constructor(id: number, name: string, email: string, pharmacyName: string) {
    super(id, name, email);
    this._pharmacyName = pharmacyName;
  }

  get pharmacyName(): string {
    return this._pharmacyName;
  }

  set pharmacyName(value: string) {
    this._pharmacyName = value;
  }

  getRole(): string {
    return "Pharmacist";
  }
}
