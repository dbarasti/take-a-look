class ScrapingInfo:
    def __init__(self, web_page_url: str, tag: str, attribute: str, value: str, regex_pattern: str):
        self.web_page_url = web_page_url
        self.tag = tag
        self.attribute = attribute
        self.value = value
        self.regex_pattern = regex_pattern
