import json
from bs4 import BeautifulSoup


class ProjectScraper(object):
    
    def __init__(self, html, markup='lxml'):
        self.html = html
        self.soup = BeautifulSoup(html, markup)


    def get_project_dictionary(self):
        """
        Finds the data-initial attribute of the project and converts it into a dictionary object.

        Attributes:
            html: The HTML of the kickstarter project as a string
            markup: the markup type to use with bs4 (default='lxml')

        Returns:
            a dictionary of the data presented in the data-initial attribute.
        """
        elem = self.soup.find('div', attrs={'data-initial': True})
        return json.loads(elem['data-initial'])

    def get_external_creator_urls(self):
        project = self.get_project_dictionary()

        urls = []
        for website_info in project['project']['creator']['websites']:
            urls.append(website_info[['url']])

        return urls
