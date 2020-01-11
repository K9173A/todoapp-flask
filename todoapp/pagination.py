"""

"""
import math

from flask import render_template


class Paginator:
    def __init__(self):
        self._current_page = 1
        self._items_per_page = 5
        self._total_items = 0

    @property
    def current_page(self):
        return self._current_page

    @property
    def items_per_page(self):
        return self._items_per_page

    @property
    def total_items(self):
        return self._total_items

    @property
    def offset(self):
        return (self._current_page - 1) * self.items_per_page

    @property
    def total_pages_count(self):
        return math.ceil(self._total_items / self._items_per_page)

    @total_items.setter
    def total_items(self, total_items):
        self._total_items = total_items if total_items > 0 else 0

    @current_page.setter
    def current_page(self, current_page):
        self._current_page = current_page if current_page > 0 else 1

    @items_per_page.setter
    def items_per_page(self, items_per_page):
        self._items_per_page = items_per_page if items_per_page > 0 else 1

    def get_pagination(self):
        range_numbers = 3

        if self._current_page - range_numbers < 1:
            first_page_number = 1
        else:
            first_page_number = self._current_page - range_numbers

        if self._current_page + range_numbers > self.total_pages_count:
            last_page_number = self.total_pages_count
        else:
            last_page_number = self._current_page + range_numbers

        prev_numbers = [
            i for i in range(first_page_number, self._current_page)
        ]
        next_numbers = [
            i for i in range(self._current_page + 1, last_page_number + 1)
        ]

        return {
            'prev_numbers': prev_numbers,
            'curr_number': self._current_page,
            'next_numbers': next_numbers,
        }
