#!/usr/bin/env python3
"""Simple test for SoupReplacer."""

from bs4 import BeautifulSoup
from bs4.filter import SoupReplacer


def test_basic_replacement():
    """Test basic tag replacement: <b> to <blockquote>."""
    print("Test 1: Basic replacement (<b> → <blockquote>)")
    print("-" * 60)

    markup = "<p>This is <b>bold</b> text.</p>"
    replacer = SoupReplacer("b", "blockquote")
    soup = BeautifulSoup(markup, 'html.parser', replacer=replacer)

    b_count = len(soup.find_all('b'))
    blockquote_count = len(soup.find_all('blockquote'))

    print(f"  Input:  {markup}")
    print(f"  Output: {soup}")
    print(f"  <b> tags found: {b_count}")
    print(f"  <blockquote> tags found: {blockquote_count}")

    assert b_count == 0, "Should have no <b> tags"
    assert blockquote_count == 1, "Should have 1 <blockquote> tag"
    print("PASS\n")


def test_multiple_replacements():
    """Test replacing multiple occurrences of the same tag."""
    print("Test 2: Multiple replacements (<i> → <em>)")
    print("-" * 60)

    markup = "<p><i>First</i> and <i>Second</i> and <i>Third</i></p>"
    replacer = SoupReplacer("i", "em")
    soup = BeautifulSoup(markup, 'html.parser', replacer=replacer)

    i_count = len(soup.find_all('i'))
    em_count = len(soup.find_all('em'))

    print(f"  Input:  {markup}")
    print(f"  Output: {soup}")
    print(f"  <i> tags found: {i_count}")
    print(f"  <em> tags found: {em_count}")

    assert i_count == 0, "Should have no <i> tags"
    assert em_count == 3, "Should have 3 <em> tags"

    em_tags = soup.find_all('em')
    contents = [tag.string for tag in em_tags]
    assert contents == ['First', 'Second', 'Third'], f"Expected ['First', 'Second', 'Third'], got {contents}"

    print("PASS\n")


if __name__ == '__main__':
    print("=" * 60)
    print("SoupReplacer Tests")
    print("=" * 60)
    print()

    tests = [
        ("Basic replacement", test_basic_replacement),
        ("Multiple replacements", test_multiple_replacements),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {e}\n")
            failed += 1
        except Exception as e:
            print(f"ERROR: {e}\n")
            failed += 1

    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("=" * 60)

    if failed == 0:
        print("\n All tests passed!")
    else:
        print(f"\n  {failed} test(s) failed")
