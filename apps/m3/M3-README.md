# Milestone-3
# SoupReplacer Transformer Functions

## Implementation Details

### Location
**File:** `bs4/filter.py`
**Class:** `SoupReplacer` (lines 685-775)
**Method:** `replace_tag()` (lines 741-772)

### Design Decisions

1. **Three Transformer Types**: Provides three distinct ways to transform tags during parsing:
   - `name_xformer`: Transform tag names (functional, returns new name)
   - `attrs_xformer`: Transform attributes (functional, returns new attributes dict)
   - `xformer`: General transformations (imperative, modifies tag via side effects)

2. **Transformation During Parsing**: Tags are transformed as they are created by the parser, before being added to the tree. This is more efficient than post-processing.

3. **Backward Compatibility**: The original simple replacement mode (`og_tag`, `alt_tag`) is preserved and works alongside the new transformer API.

4. **Execution Order**: When multiple transformers are provided, they execute in sequence:
   - `name_xformer` (transforms tag name)
   - `attrs_xformer` (transforms attributes)
   - `xformer` (applies side effects)
   - Simple replacement (fallback if no transformers)

## API Usage

### name_xformer - Transform Tag Names
```python
replacer = SoupReplacer(
    name_xformer=lambda tag: "strong" if tag.name == "b" else tag.name
)
soup = BeautifulSoup(html, 'html.parser', replacer=replacer)
# <b> → <strong> dynamically during parsing
```

### attrs_xformer - Transform Attributes
```python
def remove_class(tag):
    return {k: v for k, v in tag.attrs.items() if k != "class"}

replacer = SoupReplacer(attrs_xformer=remove_class)
soup = BeautifulSoup(html, 'html.parser', replacer=replacer)
# All class attributes removed during parsing
```

### xformer - General Side-Effect Transformations
```python
def add_target_blank(tag):
    if tag.name == "a" and tag.get("href", "").startswith("http"):
        tag["target"] = "_blank"
        tag["rel"] = "noopener noreferrer"

replacer = SoupReplacer(xformer=add_target_blank)
soup = BeautifulSoup(html, 'html.parser', replacer=replacer)
# External links get target="_blank"
```

### Combined Transformers
```python
replacer = SoupReplacer(
    name_xformer=lambda tag: "strong" if tag.name == "b" else tag.name,
    attrs_xformer=lambda tag: {k: v for k, v in tag.attrs.items() if k != "class"},
    xformer=lambda tag: tag.attrs.setdefault("data-processed", "true")
)
soup = BeautifulSoup(html, 'html.parser', replacer=replacer)
# All three transformations applied in order
```

## Tests

### Location
**File:** `bs4/tests/test_soup_replacer.py`

### Test Cases

The test suite includes 8 tests (2 for backward compatibility + 6 new for transformers):

#### 1. `test_name_xformer_basic`
Tests basic name transformation with lambda function.
```python
markup = "<p>This is <b>bold</b> text.</p>"
replacer = SoupReplacer(name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name)
# Verifies: name_xformer changes tag names dynamically
```

#### 2. `test_name_xformer_conditional`
Tests conditional transformation based on attributes.
```python
markup = '<div><span class="important">Keep</span><span>Change</span></div>'
# Transform only spans WITHOUT class="important"
# Verifies: Conditional logic works correctly
```

#### 3. `test_attrs_xformer_remove_class`
Tests removing attributes functionally.
```python
markup = '<div><p class="foo">Text 1</p><p class="bar" id="test">Text 2</p></div>'
def remove_class(tag):
    return {k: v for k, v in tag.attrs.items() if k != "class"}
# Verifies: All class attributes removed, others preserved
```

#### 4. `test_attrs_xformer_modify_attrs`
Tests adding/modifying attributes.
```python
markup = '<div><a href="http://example.com">Link</a></div>'
# Add target="_blank" and rel="noopener" to links
# Verifies: New attributes added, existing preserved
```

#### 5. `test_xformer_side_effects`
Tests imperative modifications with side effects.
```python
markup = '<div><p class="foo" id="bar">Text</p></div>'
def remove_class_attr(tag):
    if "class" in tag.attrs:
        del tag.attrs["class"]
# Verifies: Direct attribute deletion works
```

#### 6. `test_combined_transformers`
Tests using all three transformers together.
```python
markup = '<div><b class="highlight" id="test">Bold text</b></div>'
# name_xformer: b→strong
# attrs_xformer: add style attribute
# xformer: remove id attribute
# Verifies: All transformers execute in correct order
```

### Running Tests

```bash
# Run all SoupReplacer tests
PYTHONPATH=. python3 bs4/tests/test_soup_replacer.py

# Or use pytest
python -m pytest bs4/tests/test_soup_replacer.py -v
```

## Application Program

### Location
**File:** `apps/m3/task-7.py`

### Implementation

**Before (without xformer):**
```python
# Parse first, then modify
soup = BeautifulSoup(html, 'html.parser')
for p_tag in soup.find_all('p'):
    p_tag['class'] = "test"
```

**After (with xformer):**
```python
# Transform during parsing
def add_test_class(tag):
    if tag.name == "p":
        current_classes = tag.get("class", [])
        if "test" not in current_classes:
            current_classes.append("test")
            tag["class"] = current_classes

replacer = SoupReplacer(xformer=add_test_class)
soup = BeautifulSoup(html, 'html.parser', replacer=replacer)
# All <p> tags already have class="test"!
```

### Running the Application

```bash
# From project root
python apps/m3/task-7.py <html_file>

# Example
python apps/m3/task-7.py apps/m3/very_large-1.html
```

## Advantages of Transformer API

1. **Efficiency**: Transformations happen during parsing, not as a separate post-processing step
2. **Flexibility**: Three different approaches for different use cases
3. **Composability**: Multiple transformers can be combined
4. **Clean Code**: Declarative transformer functions are more readable than imperative loops
5. **Backward Compatible**: Original simple replacement API still works

## Common Use Cases

### Data Cleaning: Remove All Class Attributes
```python
replacer = SoupReplacer(
    attrs_xformer=lambda tag: {k: v for k, v in tag.attrs.items() if k != "class"}
)
```

### Complex Workflow: Multiple Transformations
```python
replacer = SoupReplacer(
    name_xformer=modernize_name,
    attrs_xformer=clean_attrs,
    xformer=add_metadata
)
# All three execute in sequence during parsing
```

## Summary

The SoupReplacer transformer API provides a powerful, flexible way to transform HTML during parsing. With three distinct transformer types (`name_xformer`, `attrs_xformer`, `xformer`), developers can handle any transformation scenario from simple tag renaming to complex document restructuring, all while maintaining backward compatibility with the original simple replacement API.

---

## SoupReplacer API Evolution

---

### Milestone 2 API: Simple Replacement

#### Strengths
1. **Simplicity**: Extremely easy to understand and use
2. **Declarative**: Clear intent - "replace this tag with that tag"
3. **Low Learning Curve**: No functions or callbacks required
4. **Performance**: Direct replacement is fast and efficient
5. **Type Safety**: String parameters are straightforward to validate

---

### Milestone 3 API: Transformer Functions

#### Strengths
1. **Flexibility**: Handle any transformation scenario
2. **Composability**: Multiple transformers work together in sequence
3. **Conditional Logic**: Functions can inspect tag state and make decisions
4. **Single Pass**: All transformations happen during parsing (efficient)
5. **Extensibility**: Easy to add new transformation types
6. **Functional Programming**: Aligns with modern Python patterns
7. **Complex Workflows**: Supports sophisticated document manipulation

---

### Conclusion

The Milestone 3 transformer API represents a significant improvement over Milestone 2's simple replacement approach. While M2 excels in simplicity for basic use cases, M3's flexibility, composability, and alignment with modern programming patterns make it the superior choice for production use.
