from selenium import webdriver
from bs4 import BeautifulSoup

def scrape_content_from_url(url):
    driver = webdriver.Edge()  
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    visible_text = soup.get_text()

    driver.quit()
    return visible_text

def main():
    url = "file:///C:/Users/kushp/Downloads/Dark%20Pattern%20Hackathon%20(3).pdf"

    content = scrape_content_from_url(url)

    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(content)

    print(f'Content extracted from the page and saved to "output.txt".')

if __name__ == "__main__":
    main()
