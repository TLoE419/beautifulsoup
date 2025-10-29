import sys
from bs4 import BeautifulSoup, SoupStrainer

if len(sys.argv) != 2:
    print(f"Without input file")
    sys.exit(1)

filename = sys.argv[1]

try:
    with open(filename, 'r', encoding='utf-8') as f:
        strainer = SoupStrainer("a", attrs={"href": True})
        soup = BeautifulSoup(f, 'html.parser', parse_only=strainer)
except FileNotFoundError:
    print(f"File {filename} not found.")

for link in soup.find_all("a"):
    print(link.get("href"))