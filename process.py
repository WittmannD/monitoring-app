from typing import Iterable


class DataProcessing:
    storage = set()

    @staticmethod
    def find_by_isbn(data: Iterable, isbn_set: Iterable) -> list:
        return list(filter(lambda o: o['EA_ISBN'] in isbn_set, data))

    @staticmethod
    def prepare_isbn(data: Iterable) -> set:
        return set(item['EA_ISBN'] for item in data)

    def process(self, data: dict) -> None:
        data: list = data['response']['docs']

        new_isbn = self.prepare_isbn(data)
        existing_isbn = new_isbn.difference(self.storage)

        if existing_isbn:
            self.storage = new_isbn
            new_data = self.find_by_isbn(data, existing_isbn)

            notifying(new_data)
