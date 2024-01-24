import sys
from configparser import ConfigParser
from chatbot import ChatBot
import webbrowser
from selenium import webdriver
from bs4 import BeautifulSoup

def generate_html(output_text):
    # Replace newline characters with <br> for line breaks
    html_content = output_text.replace('\n', '<br>')

    # Replace '*' with <b> and </b> for bold formatting
    html_content = html_content.replace('*', '<b>').replace('</b>', '</b>')

    # Create an HTML file with the chatbot response
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
    url = "file:///C:/Users/kushp/Downloads/Dark%20Pattern%20Hackathon%20(3).pdf"

    content = scrape_content_from_url(url)

    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(content)

    print(f'Content extracted from the page and saved to "output.txt".')

    try:
        # Read API key from credentials.ini
        config = ConfigParser()
        config.read('credentials.ini')
        api_key = config['gemini_ai']['API_KEY']

        # Initialize ChatBot with API key
        chatbot = ChatBot(api_key=api_key)
        chatbot.start_conversation()

        # Open output.txt in read mode
        with open("output.txt", "r+", encoding="utf-8") as f1:
            # Read user input from the file
            user_input = f1.read()
            # print(user_input)
            #user_input = "quit"
            prompt = "detect the potential dark patterns in the following and list them in bullet points: "
            # Combine prompt and user input
            user_input = prompt + '\n' + user_input

            # Check if the user wants to quit
            if user_input.lower() == 'quit':
                sys.exit('Exiting Chatbot CLI...')

        # Send prompt to ChatBot and get the response
        response = chatbot.send_prompt(user_input)

        # Print the response
        print(f"{chatbot.CHATBOT_NAME}: {response}")

        # Generate HTML file with the formatted chatbot response
        generate_html(response)

        webbrowser.open('chatbot_response.html', new=2)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()