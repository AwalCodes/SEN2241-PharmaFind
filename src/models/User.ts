// User is the base class for all user types in the app.
// Marked as abstract so we cannot create a plain "User" directly.
export abstract class User {
  // Private fields demonstrate encapsulation:
  // they can only be accessed through getters/setters.
  private _id: number;
  private _name: string;
  private _email: string;

  constructor(id: number, name: string, email: string) {
    this._id = id;
    this._name = name;
    this._email = email;
  }

  get id(): number {
    return this._id;
  }

  get name(): string {
    return this._name;
  }

  set name(value: string) {
    this._name = value;
  }

  get email(): string {
    return this._email;
  }

  set email(value: string) {
    this._email = value;
  }

  // Every subclass will provide its own role text.
  abstract getRole(): string;
}
