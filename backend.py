# backend.py
import sys
import argparse
from configparser import ConfigParser
from chatbot import ChatBot
import webbrowser
from selenium import webdriver
from bs4 import BeautifulSoup

def parse_arguments():
    parser = argparse.ArgumentParser(description='Dark Pattern Detector')
    parser.add_argument('--url', type=str, help='URL of the terms and conditions page')
    return parser.parse_args()

def generate_html(output_text):
    html_content = output_text.replace('\n', '<br>')

    html_content = html_content.replace('*', '<b>').replace('</b>', '</b>')

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ChatBot Response</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #d54040;
                margin: 20px;
            }}
            h2 {{
                color: #333;
                text-align: center;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: red;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            }}
            .container:hover {{
                transform: scale(1.2);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>{html_content}</h2>
        </div>
    </body>
    </html>
    """

    with open("chatbot_response.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

def scrape_content_from_url(url):
    driver = webdriver.Edge()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    visible_text = soup.get_text()

    driver.quit()
    return visible_text

def main():
    args = parse_arguments()
    url = args.url

    if not url:
        sys.exit('Error: URL is required.')

    content = scrape_content_from_url(url)

    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(content)

    print(f'Content extracted from the page and saved to "output.txt".')

    try:
        config = ConfigParser()
        config.read('credentials.ini')
        api_key = config['gemini_ai']['API_KEY']

        chatbot = ChatBot(api_key=api_key)
        chatbot.start_conversation()

        with open("output.txt", "r+", encoding="utf-8") as f1:

            user_input = f1.read()
            prompt = "detect the potential dark patterns in the following and list them in bullet points: "

            user_input = prompt + '\n' + user_input

            if user_input.lower() == 'quit':
                sys.exit('Exiting Chatbot CLI...')

        response = chatbot.send_prompt(user_input)

        print(f"{chatbot.CHATBOT_NAME}: {response}")

        generate_html(response)

        webbrowser.open('chatbot_response.html', new=2)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()