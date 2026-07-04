from download_content import main
from json import load
from pathlib import Path

BASE_DIR = Path(__file__).parent
json_path = str(BASE_DIR / 'config.json')

with open(json_path, 'r') as file:
    config = load(file)

if __name__ == '__main__':
    email = config['email']
    password = config['password']
    url_class = config['url_class']
    main(url_class, email, password)
