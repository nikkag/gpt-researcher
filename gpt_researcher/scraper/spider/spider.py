import re

from bs4 import BeautifulSoup, Tag
from langchain_community.document_loaders import SpiderLoader
from markdownify import MarkdownConverter


class SpiderScraper:

    def __init__(self, link, session=None):
        self.link = link
        self.session = session

    def scrape(self) -> str:
        """
        This Python function scrapes content from a webpage using a SpiderLoader object and returns the
        concatenated page content.

        Returns:
          The `scrape` method is returning a string variable named `content` which contains the
        concatenated page content from the documents loaded by the `SpiderLoader`. If an exception
        occurs during the process, an error message is printed and an empty string is returned.
        """
        mode = "crawl"
        # mode = "scrape"
        try:
            loader = SpiderLoader(
                url=self.link,
                mode=mode,
                params={
                    "anti_bot": True,
                    "request": "smart_mode",
                    # "return_format": "markdown",
                    "limit": 50
                }
            )
            docs = loader.load()
            raw_html = ""

            for doc in docs:
                raw_html += doc.page_content

            soup = BeautifulSoup(raw_html, "lxml")
            markdown = MarkdownConverter().convert_soup(soup).strip()

            # for script_or_style in soup(["script", "style"]):
            #     script_or_style.extract()

            # content = self.get_content_from_url(soup)
            # lines = (line.strip() for line in raw_content.splitlines())
            # lines = (line.strip() for line in raw_contents)
            # chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # content = "\n".join(chunk for chunk in chunks if chunk)

            # content = raw_html
            return re.sub(r'\n{3,}', '\n\n', markdown)

        except Exception as e:
            print("Error! : " + str(e))
            return ""

    def get_content_from_url(self, soup: BeautifulSoup):
        """Get the text from the soup

        Args:
            soup (BeautifulSoup): The soup to get the text from

        Returns:
            str: The text from the soup
        """
        text = ""
        tags = ["a", "p", "h1", "h2", "h3", "h4", "h5", "table", "span"]
        element: Tag
        for element in soup.find_all(tags):
            if not element.name == "table":
                element.string = element.text.strip()
            text += f'{str(element)}\n'
        return text
        # for element in soup.find_all(tags):  # Find all the <p> and <a> elements
        #     text += element.text + "\n"
        # return text
