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


def test_name_xformer_basic():
    """Test name_xformer with simple transformation."""
    print("Test 3: name_xformer basic (<b> → <blockquote>)")
    print("-" * 60)

    markup = "<p>This is <b>bold</b> text.</p>"
    replacer = SoupReplacer(name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name)
    soup = BeautifulSoup(markup, 'html.parser', replacer=replacer)

    b_count = len(soup.find_all('b'))
    blockquote_count = len(soup.find_all('blockquote'))

    print(f"  Input:  {markup}")
    print(f"  Output: {soup}")
    print(f"  <b> tags found: {b_count}")
    print(f"  <blockquote> tags found: {blockquote_count}")

    assert b_count == 0, "Should have no <b> tags"
    assert blockquote_count == 1, "Should have 1 <blockquote> tag"
    assert soup.blockquote.string == "bold", "Content should be preserved"
    print("PASS\n")


def test_name_xformer_conditional():
    """Test name_xformer with conditional transformation based on attributes."""
    print("Test 4: name_xformer conditional (transform based on class attribute)")
    print("-" * 60)

    markup = '<div><span class="important">Keep</span><span>Change</span></div>'

    def transform_name(tag):
        if tag.name == "span" and "important" not in tag.get("class", []):
            return "small"
        return tag.name

    replacer = SoupReplacer(name_xformer=transform_name)
    soup = BeautifulSoup(markup, 'html.parser', replacer=replacer)

    span_count = len(soup.find_all('span'))
    small_count = len(soup.find_all('small'))

    print(f"  Input:  {markup}")
    print(f"  Output: {soup}")
    print(f"  <span> tags found: {span_count}")
    print(f"  <small> tags found: {small_count}")

    assert span_count == 1, "Should have 1 <span> tag (with class='important')"
    assert small_count == 1, "Should have 1 <small> tag (transformed from plain span)"
    print("PASS\n")


def test_attrs_xformer_remove_class():
    """Test attrs_xformer removing class attributes."""
    print("Test 5: attrs_xformer remove class attributes")
    print("-" * 60)

    markup = '<div><p class="foo">Text 1</p><p class="bar" id="test">Text 2</p></div>'

    def remove_class(tag):
        return {k: v for k, v in tag.attrs.items() if k != "class"}

    replacer = SoupReplacer(attrs_xformer=remove_class)
    soup = BeautifulSoup(markup, 'html.parser', replacer=replacer)

    print(f"  Input:  {markup}")
    print(f"  Output: {soup}")

    # Check that no tags have class attributes
    all_tags = soup.find_all(True)
    for tag in all_tags:
        assert "class" not in tag.attrs, f"Tag {tag.name} should not have class attribute"

    # Check that other attributes are preserved
    p_with_id = soup.find('p', id='test')
    assert p_with_id is not None, "Should find <p> with id='test'"
    assert p_with_id.get('id') == 'test', "id attribute should be preserved"

    print("PASS\n")


def test_attrs_xformer_modify_attrs():
    """Test attrs_xformer modifying and adding attributes."""
    print("Test 6: attrs_xformer modify attributes")
    print("-" * 60)

    markup = '<div><a href="http://example.com">Link</a></div>'

    def add_target(tag):
        attrs = dict(tag.attrs)
        if tag.name == "a":
            attrs["target"] = "_blank"
            attrs["rel"] = "noopener"
        return attrs

    replacer = SoupReplacer(attrs_xformer=add_target)
    soup = BeautifulSoup(markup, 'html.parser', replacer=replacer)

    print(f"  Input:  {markup}")
    print(f"  Output: {soup}")

    a_tag = soup.find('a')
    assert a_tag is not None, "Should find <a> tag"
    assert a_tag.get('href') == 'http://example.com', "href should be preserved"
    assert a_tag.get('target') == '_blank', "target should be added"
    assert a_tag.get('rel') == 'noopener', "rel should be added"

    print("PASS\n")


def test_xformer_side_effects():
    """Test xformer with side effects."""
    print("Test 7: xformer with side effects (remove class attribute)")
    print("-" * 60)

    markup = '<div><p class="foo" id="bar">Text</p></div>'

    def remove_class_attr(tag):
        if "class" in tag.attrs:
            del tag.attrs["class"]

    replacer = SoupReplacer(xformer=remove_class_attr)
    soup = BeautifulSoup(markup, 'html.parser', replacer=replacer)

    print(f"  Input:  {markup}")
    print(f"  Output: {soup}")

    # Check that no tags have class attributes
    all_tags = soup.find_all(True)
    for tag in all_tags:
        assert "class" not in tag.attrs, f"Tag {tag.name} should not have class attribute"

    # Check that other attributes are preserved
    p_tag = soup.find('p')
    assert p_tag.get('id') == 'bar', "id attribute should be preserved"

    print("PASS\n")


def test_combined_transformers():
    """Test using multiple transformers together."""
    print("Test 8: Combined transformers (name + attrs + xformer)")
    print("-" * 60)

    markup = '<div><b class="highlight" id="test">Bold text</b></div>'

    def transform_name(tag):
        if tag.name == "b":
            return "strong"
        return tag.name

    def modify_attrs(tag):
        attrs = dict(tag.attrs)
        if "highlight" in attrs.get("class", []):
            attrs["style"] = "background-color: yellow"
        return attrs

    def remove_id(tag):
        if "id" in tag.attrs:
            del tag.attrs["id"]

    replacer = SoupReplacer(
        name_xformer=transform_name,
        attrs_xformer=modify_attrs,
        xformer=remove_id
    )
    soup = BeautifulSoup(markup, 'html.parser', replacer=replacer)

    print(f"  Input:  {markup}")
    print(f"  Output: {soup}")

    # Check name transformation
    assert soup.find('b') is None, "Should have no <b> tags"
    strong_tag = soup.find('strong')
    assert strong_tag is not None, "Should have <strong> tag"

    # Check attrs transformation
    assert strong_tag.get('style') == 'background-color: yellow', "style should be added"
    assert strong_tag.get('class') == ['highlight'], "class should be preserved"

    # Check xformer side effect
    assert 'id' not in strong_tag.attrs, "id should be removed"

    print("PASS\n")


if __name__ == '__main__':
    print("=" * 60)
    print("SoupReplacer Tests")
    print("=" * 60)
    print()

    tests = [
        ("Basic replacement", test_basic_replacement),
        ("Multiple replacements", test_multiple_replacements),
        ("name_xformer basic", test_name_xformer_basic),
        ("name_xformer conditional", test_name_xformer_conditional),
        ("attrs_xformer remove class", test_attrs_xformer_remove_class),
        ("attrs_xformer modify attrs", test_attrs_xformer_modify_attrs),
        ("xformer side effects", test_xformer_side_effects),
        ("Combined transformers", test_combined_transformers),
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
