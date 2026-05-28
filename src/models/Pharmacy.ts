import { Medication } from "./Medication";

export class Pharmacy {
  private _id: number;
  private _name: string;
  private _address: string;
  private _medications: Medication[];

  constructor(id: number, name: string, address: string) {
    this._id = id;
    this._name = name;
    this._address = address;
    this._medications = [];
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

  get address(): string {
    return this._address;
  }

  set address(value: string) {
    this._address = value;
  }

  get medications(): Medication[] {
    return this._medications;
  }

  addMedication(medication: Medication): void {
    this._medications.push(medication);
  }

  findMedicationByName(name: string): Medication | undefined {
    return this._medications.find(
      (medication) => medication.name.toLowerCase() === name.toLowerCase()
    );
  }
}
