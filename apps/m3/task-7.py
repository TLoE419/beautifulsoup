import sys
import os

# Add project root to Python path so we can import bs4
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from bs4 import BeautifulSoup
from bs4.filter import SoupReplacer

def add_test_class(tag):
    if tag.name == "p":
        current_classes = tag.get("class", [])
        
        if "test" not in current_classes:
            current_classes.append("test")
            tag["class"] = current_classes 

if len(sys.argv) != 2:
    print(f"Without input file")
    sys.exit(1)

filename = sys.argv[1]

try:
    with open(filename, 'r', encoding='utf-8') as f:
        html_content = f.read()
except FileNotFoundError:
    print(f"File {filename} not found.")
    
replacer = SoupReplacer(xformer=add_test_class)

soup = BeautifulSoup(html_content, 'html.parser', replacer=replacer)

with open(filename, "w", encoding="utf-8") as f:
    f.write(soup.prettify())