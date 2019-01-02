"""
Searches for Kickstarter pages based on entered criteria.
"""
import time
import random
import json

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

ANCHOR_TAG_BUTTON = '//a[@role="button" and contains(text(), "{}")]'
DROPDOWN_CONTAINER_XPATH = '//div[@aria-hidden="false" and @id="{}"]'


class DiscoverySearcher(object):
    """
    Searches the Discover page to find links to projects based on given criteria.

    Attributes:
        driver: Selenium webdriver object
    """

    def __init__(self, driver):
        self.driver = driver
        self._wait = WebDriverWait(self.driver, 10)

    def get_search_page(self, category, sort_by, sub_category=None):
        """
        Gets the Discovery page for the given arguments

        Arguments:
            category: the category to choose from (must match exactly to category dropdown)
            sort_by: how to search the category (must match exactly from sort by dropdown)
            sub_category: category to choose after category is chosen (must match exactly from sub category dropdown)

        Returns:
            None
        """
        self.driver.get('https://kickstarter.com/discover')

        time.sleep(3)

        self._select_category(category, sub_category)
        self._select_sort_by(sort_by)

    def _select_category(self, category, sub_category):
        self._click_dropdown('category')

        category = self.driver.find_element_by_xpath(
            ANCHOR_TAG_BUTTON.format(category)
        )
        category.click()
        self._url_change_wait()

        if sub_category:
            sub_category = self.driver.find_element_by_xpath(
                ANCHOR_TAG_BUTTON.format(sub_category)
            )
            sub_category.click()
            self._url_change_wait()
    
    def _select_sort_by(self, sort_by):
        self._click_dropdown('sort')
        self.driver.find_element_by_xpath(
            ANCHOR_TAG_BUTTON.format(sort_by)
        ).click()

    def _click_dropdown(self, container_type):
        if container_type == 'category':
            parent_xpath = '//span[text()="Show me"]'
            dropdown_id = 'NS_discover__categories'
        elif container_type == 'sort':
            parent_xpath = '//span[text()="sorted by"]'
            dropdown_id = 'NS_discover__sorts'
        else:
            raise ValueError('container_type must be "category" or "sort"')

        parent = self.driver.find_element_by_xpath(parent_xpath)
        dropdown = parent.find_element_by_xpath(
            './following-sibling::span'
            '/span'
        )
        dropdown.click()
        self._category_dropdown_wait(dropdown_id)

    def _url_change_wait(self):
        self._wait.until(
            EC.url_changes(self.driver.current_url)
        )

    def _category_dropdown_wait(self, dropdown_id):
        self._wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                DROPDOWN_CONTAINER_XPATH.format(dropdown_id)
            ))
        )

    def _click_load_more(self):
        """Loads more projects"""
        self.driver.find_element_by_xpath(
            ANCHOR_TAG_BUTTON.format('Load more')
            ).click()
    
    def scroll_until_count(self, count, min_sleep=2, max_sleep=8):
        """Scrolls until 'count' is in view. Sleeps between min/max sleep times"""
        while len(self.get_project_card_elements()) < count:
            self._click_load_more()
            time.sleep(
                random.randint(min_sleep, max_sleep) + random.uniform(0, 1))

    def get_project_card_elements(self):
        return self.driver.find_elements_by_class_name('js-react-async-proj-card')

    def scroll_until_all(self, min_sleep=2, max_sleep=8):
        """Scrolls until all projects are in view. Sleeps between min/max sleep times"""
        self.scroll_until_count(self._get_project_count(), min_sleep, max_sleep)

    def _get_project_count(self):
        elem = self.driver.find_element_by_class_name('count')
        count_digits = [char for char in elem.text if char.isdigit()]
        return int(''.join(count_digits))

    def get_cards_dictionaries(self):
        """Gets project data as list of dictionaries"""
        cards = self.get_project_card_elements()
        projects = []
        for card in cards:
            projects.append(json.loads(card.get_attribute('data-project')))
        return projects
