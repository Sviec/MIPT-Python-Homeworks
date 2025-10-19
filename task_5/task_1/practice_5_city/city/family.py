from person import Person


class Family:
    def __init__(self, family_name: str, persons: list[Person]):
        self.family_name = family_name
        self.persons = persons

    def __str__(self) -> str:
        if self.persons:
            s = []
            s.append(f'Family {self.family_name} consists of:\n')
        else:
            return f'Family {self.family_name} is empty'
        for person in self.persons:
            s.append(f'\t{person}\n')
        return ''.join(s)

    def __del__(self):
        print("Family {} was removed".format(self.family_name))

    def add_person(self, person: Person):
        if person in self.persons:
            print(f'{person} is already part of the family {self.family_name}')
        else:
            self.persons.append(person)
            print(f"{person} was added to family '{self.family_name}'")

    def remove_person(self, person: Person):
        if person in self.persons:
            self.persons.remove(person)
            print(f"{person} was removed from family '{self.family_name}'")
        else:
            print(f"{person} is not part of the family '{self.family_name}'")
