import json
from bs4 import BeautifulSoup


def get_project_dictionary(html, markup='lxml'):
    """
    Finds the data-initial attribute of the project and converts it into a dictionary object.

    Attributes:
        html: The HTML of the kickstarter project as a string
        markup: the markup type to use with bs4 (default='lxml')

    Returns:
        a dictionary of the data presented in the data-initial attribute.
    """
    soup = BeautifulSoup(html, markup)
    elem = soup.find('div', attrs={'data-initial': True})

    return json.loads(elem['data-initial'])
