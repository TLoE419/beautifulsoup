import sys
from bs4 import BeautifulSoup, SoupStrainer

if len(sys.argv) != 2:
    print(f"Without input file")
    sys.exit(1)

filename = sys.argv[1]

try:
    with open(filename, 'r', encoding='utf-8') as f:
        strainer = SoupStrainer()
        soup = BeautifulSoup(f, 'html.parser')
except FileNotFoundError:
    print(f"File {filename} not found.")
    
for tag in soup.find_all():
    print(tag)