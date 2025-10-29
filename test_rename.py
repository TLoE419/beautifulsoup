#!/usr/bin/env python3
"""Test the renamed replace_tag method."""

from bs4 import BeautifulSoup, SoupReplacer

html = """
<html>
<body>
    <p>This is <b>bold</b> text.</p>
    <div><b>Another bold</b> word.</div>
</body>
</html>
"""

print("Testing renamed method: replace_tag()")
print("=" * 60)

# Create SoupReplacer
replacer = SoupReplacer("b", "blockquote")
print(f"Created: {replacer}")

# Parse with replacer
soup = BeautifulSoup(html, 'html.parser', replacer=replacer)

# Show result
print("\nResult:")
print(soup.prettify())

# Verify
b_count = len(soup.find_all('b'))
blockquote_count = len(soup.find_all('blockquote'))

print("=" * 60)
print(f"<b> tags: {b_count}")
print(f"<blockquote> tags: {blockquote_count}")

if b_count == 0 and blockquote_count > 0:
    print("\n✓ SUCCESS: Method rename works perfectly!")
else:
    print("\n✗ FAILED")
