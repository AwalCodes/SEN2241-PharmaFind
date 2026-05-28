from __future__ import annotations


class User:
    """
    Base class for users in Pharma-Find.

    Inheritance:
    - Pharmacist and Customer will inherit from this User class.

    Encapsulation:
    - We keep fields "private" using leading underscores and access them using
      @property getters/setters so we can control how data is changed.
    """

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self._user_id = user_id
        self._name = name
        self._email = email

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = value

    def get_role(self) -> str:
        # Subclasses can override this.
        return "User"


class Pharmacist(User):
    """
    Pharmacist is a type of User (Inheritance).
    """

    def __init__(self, user_id: int, name: str, email: str, pharmacy_name: str) -> None:
        super().__init__(user_id, name, email)
        self._pharmacy_name = pharmacy_name

    @property
    def pharmacy_name(self) -> str:
        return self._pharmacy_name

    @pharmacy_name.setter
    def pharmacy_name(self, value: str) -> None:
        self._pharmacy_name = value

    def get_role(self) -> str:
        return "Pharmacist"


class Customer(User):
    """
    Customer is a type of User (Inheritance).
    """

    def __init__(self, user_id: int, name: str, email: str, location: str) -> None:
        super().__init__(user_id, name, email)
        self._location = location

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str) -> None:
        self._location = value

    def get_role(self) -> str:
        return "Customer"


class Medication:
    """
    Represents a medication and the quantity available.

    Encapsulation:
    - Quantity is not changed directly, only through a property setter.
    """

    def __init__(self, med_id: int, name: str, quantity: int) -> None:
        self._med_id = med_id
        self._name = name
        self._quantity = quantity

    @property
    def med_id(self) -> int:
        return self._med_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        self._quantity = value


class Pharmacy:
    """
    Represents a pharmacy with a list of medications in stock.
    """

    def __init__(self, pharmacy_id: int, name: str, address: str) -> None:
        self._pharmacy_id = pharmacy_id
        self._name = name
        self._address = address
        self._medications: list[Medication] = []

    @property
    def pharmacy_id(self) -> int:
        return self._pharmacy_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        self._address = value

    @property
    def medications(self) -> list[Medication]:
        return self._medications

    def add_medication(self, medication: Medication) -> None:
        self._medications.append(medication)

    def find_medication_by_name(self, name: str) -> Medication | None:
        for medication in self._medications:
            if medication.name.lower() == name.lower():
                return medication
        return None
