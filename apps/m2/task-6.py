import sys
sys.path.insert(0, '../../')
from bs4 import BeautifulSoup, SoupReplacer

if len(sys.argv) != 2:
    print(f"Without input file")
    sys.exit(1)

filename = sys.argv[1]

try:
    with open(filename, 'r', encoding='utf-8') as f:
        b_to_blockquote = SoupReplacer("b", "blockquote")
        soup = BeautifulSoup(f, 'html.parser', replacer=b_to_blockquote)

except FileNotFoundError:
    print(f"File {filename} not found.")
    sys.exit(1)

with open(filename, "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print(f"Successfully replaced all <b> tags with <blockquote> in {filename}")
    