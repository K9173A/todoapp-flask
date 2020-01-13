"""
Module for URLHandler which is a "self-made" handler of url arguments
and helps to compose new urls and pagination elements.
"""
import math

from flask import request
from flask_pymongo import (
    DESCENDING,
    ASCENDING
)


class URLHandler:
    SORT_KEY = 'sort'
    PAGE_KEY = 'page'
    PER_PAGE = 5
    RANGE = 3

    def __init__(self):
        """
        Initializes URLHandles with default values.
        """
        self.base_url = '/'
        self.sort = 'Newest'
        self.page = 1
        self.total = 0

    @property
    def offset(self):
        """
        Calculates offset which will be used to retrieve specific
        piece of tasks from MongoDB.
        :return: integer number of offset.
        """
        return (self.page - 1) * URLHandler.PER_PAGE

    @property
    def total_pages(self):
        """
        Calculates total pages in pagination.
        :return: integer number of pages.
        """
        return math.ceil(self.total / URLHandler.PER_PAGE)

    def handle_request(self):
        """
        Processes request arguments and stores them.
        :return: None.
        """
        self.sort = request.args.get(URLHandler.SORT_KEY, 'Newest')
        self.page = int(request.args.get(URLHandler.PAGE_KEY, 1))

    def get_sorting_condition(self):
        return {
            'Newest': ('date_added', DESCENDING),
            'Oldest': ('date_added', ASCENDING),
            'HighestStatus': ('status', DESCENDING),
            'LowestStatus': ('status', ASCENDING),
            'HighestPriority': ('priority', DESCENDING),
            'LowestPriority': ('priority', ASCENDING)
        }[self.sort]

    def get_pagination_data(self):
        """
        Composes all data needed for pagination rendering. The data is organized
        like so:
        {
            'prev_pages': [
                (1, '/my_url&page=1')
                (2, '/my_url&page=2')
                (3, '/my_url&page=3')
            ]
            ...
        }
        :return: pagination data for pagination.html.
        """
        lower_range_page_numbers = self.get_range_numbers(URLHandler.RANGE, False)
        upper_range_page_numbers = self.get_range_numbers(URLHandler.RANGE, True)
        return {
            'prev_pages': self.prepare_page_urls_dict(lower_range_page_numbers),
            'curr_page': self.page,
            'next_pages': self.prepare_page_urls_dict(upper_range_page_numbers),
        }

    def compose_url(self, **arguments):
        """
        Composes url with arguments.
        :param arguments: key-value pairs of arguments
        :return:
        """
        url = f'{self.base_url}?'
        for key, value in arguments.items():
            url += f'{key}={value}&'
        return url[:-1]  # Trims last '&' sign

    def prepare_page_urls_dict(self, page_numbers):
        """
        Prepares pagination list of tuples where:
        first element - integer number which represents number of page.
        second element - string with URL for this page.
        :param page_numbers: range of page numbers which will be used in
        pagination element.
        :return: pagination dictionary for the specific range of numbers.
        """
        next_pages = []
        for number in page_numbers:
            next_pages.append((number, self.compose_url(**{
                URLHandler.SORT_KEY: self.sort,
                URLHandler.PAGE_KEY: number
            })))
        return next_pages

    def get_range_numbers(self, n, ascending_order=True):
        """
        Gets list of integers which represent a range of numbers in
        pagination on the right/left from the current page.
        :param n: range.
        :param ascending_order: order (ascending or descending).
        :return: list of pagination numbers.
        """
        if ascending_order:
            if self.page + n > self.total_pages:
                last_page = self.total_pages
            else:
                last_page = self.page + n
            return [i for i in range(self.page + 1, last_page + 1)]
        if self.page - n < 1:
            first_page = 1
        else:
            first_page = self.page - n
        return [i for i in range(first_page, self.page)]
