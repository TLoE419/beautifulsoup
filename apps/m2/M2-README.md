# Milestone 1 

### 1. BeautifulSoup()
- **Location**: `bs4/__init__.py:209`

### 2. prettify()
- **Location**: `bs4/element.py:2601`

### 3. find_all()
- **Location**: `bs4/element.py:2715`

### 4. find()
- **Location**: `bs4/element.py:2684`

### 5. find_parent()
- **Location**: `bs4/element.py:992`

### 6. new_tag()
- **Location**: `bs4/__init__.py:682`

### 7. insert_after()
- **Location**: `bs4/element.py:716`

# Milestone-2

### 1. SoupStrainer
- **Location**: `bs4/filter.py:313`

### 2. get()
- **Location**: `bs4/element.py:2160`


# Milestone-2

## Part 1 & 2: Using SoupStrainer

### 1. SoupStrainer
- **Location**: `bs4/filter.py:313`
- **Purpose**: Filter elements during parsing

### 2. get()
- **Location**: `bs4/element.py:2160`
- **Purpose**: Get attribute value from a tag

---

## Part 3: Implementing SoupReplacer

### Modified/Added Files Summary

#### 1. `bs4/filter.py` - Added SoupReplacer Class

**Lines 685-710**: SoupReplacer class definition
```python
class SoupReplacer(SoupStrainer):
    og_tag: str    # Original tag name (Line 686)
    alt_tag: str   # Alternative tag name (Line 687)

    def __init__(self, og_tag: str, alt_tag: str):  # Line 689
        super().__init__(name=og_tag)
        self.og_tag = og_tag
        self.alt_tag = alt_tag

    def replace_tag(self, tag: Tag) -> None:  # Line 698
        if self.matches_tag(tag):
            tag.name = self.alt_tag

    def __repr__(self) -> str:  # Line 704
        return f"<{self.__class__.__name__} og_tag={self.og_tag} alt_tag={self.alt_tag}>"
```

---

#### 2. `bs4/__init__.py` - Multiple Modifications

**Modification A: Import SoupReplacer (Line 94)**
```python
from .filter import (
    ElementFilter,
    SoupStrainer,
    SoupReplacer,  # ← Added
)
```

**Modification B: Add to exports list (Line 37)**
```python
__all__ = [
    # ...
    "SoupReplacer",  # ← Added
    # ...
]
```

**Modification C: Type annotation (Line 186)**
```python
soup_replacer: Optional[SoupReplacer]  # ← Added
```

**Modification D: Constructor parameters (Lines 218-220)**
```python
def __init__(
    # ...
    soup_replacer: Optional[SoupReplacer] = None,  # ← Added
    replacer: Optional[SoupReplacer] = None,       # ← Added (alias)
    # ...
):
```

**Modification E: Parameter documentation (Lines 254-255)**
```python
:param replacer: Alias for soup_replacer. A SoupReplacer that will
 replace tags during parsing (e.g., replace all <b> with <blockquote>).
```

**Modification F: Save parameter (Lines 453-455)**
```python
# Handle both 'replacer' and 'soup_replacer' parameter names
# 'replacer' takes precedence if both are provided
self.soup_replacer = replacer if replacer is not None else soup_replacer
```

**Modification G: Call during parsing (Lines 1070-1072)**
```python
# Apply SoupReplacer replacement if configured
if self.soup_replacer:
    self.soup_replacer.replace_tag(tag)
```

---

#### 3. `bs4/tests/test_soup_replacer.py` - New Test File

**Test 1: test_basic_replacement (Lines 8-27)**
- Tests single tag replacement: `<b>` → `<blockquote>`
- Verifies replacement succeeded

**Test 2: test_multiple_replacements (Lines 30-54)**
- Tests multiple tag replacements: `<i>` → `<em>`
- Verifies content preservation

---

#### 4. `apps/m2/task-6.py` - Converted to use SoupReplacer

**Before (Lines 16-17):**
```python
soup = BeautifulSoup(f, 'html.parser')
for b_tag in soup.find_all('b'):
    b_tag.name = "blockquote"
```

**After (Lines 16-21):**
```python
b_to_blockquote = SoupReplacer("b", "blockquote")
soup = BeautifulSoup(f, 'html.parser', replacer=b_to_blockquote)
```

---

### API Usage

#### Creating SoupReplacer
```python
from bs4 import BeautifulSoup, SoupReplacer

# Syntax: SoupReplacer(original_tag, alternative_tag)
replacer = SoupReplacer("b", "blockquote")
```

#### Using replacer for parsing
```python
# Method 1: Using 'replacer' parameter
soup = BeautifulSoup(html, 'html.parser', replacer=replacer)

# Method 2: Using 'soup_replacer' parameter (same effect)
soup = BeautifulSoup(html, 'html.parser', soup_replacer=replacer)
```

#### Complete Example
```python
import sys
sys.path.insert(0, '../../')
from bs4 import BeautifulSoup, SoupReplacer

html = "<p>This is <b>bold</b> text.</p>"

# Create replacer
b_to_blockquote = SoupReplacer("b", "blockquote")

# Parse with automatic replacement
soup = BeautifulSoup(html, 'html.parser', replacer=b_to_blockquote)

print(soup)
# Output: <p>This is <blockquote>bold</blockquote></p> text.
```

---

### Performance Advantage

**Traditional Method (Post-processing):**
```python
soup = BeautifulSoup(html, 'html.parser')  # Traversal 1: Parse
for b_tag in soup.find_all('b'):           # Traversal 2: Find
    b_tag.name = "blockquote"              # Modify
```
→ **Requires 2 tree traversals**

**SoupReplacer Method (During-parsing):**
```python
replacer = SoupReplacer("b", "blockquote")
soup = BeautifulSoup(html, 'html.parser', replacer=replacer)
# Replacement happens during parsing
```
→ **Requires only 1 tree traversal**

**Efficiency gain: ~50% reduction in tree traversals**

---

### Running Tests

```bash
cd beautifulsoup
PYTHONPATH=. python3 bs4/tests/test_soup_replacer.py
```

**Expected Output:**
```
============================================================
SoupReplacer Tests
============================================================

Test 1: Basic replacement (<b> → <blockquote>)
  ✓ PASS

Test 2: Multiple replacements (<i> → <em>)
  ✓ PASS

Results: 2/2 tests passed
🎉 All tests passed!
```

---

### File Modification Summary

| File Path | Modification Type | Location | Description |
|-----------|------------------|----------|-------------|
| `bs4/filter.py` | Added | Lines 685-710 | SoupReplacer class |
| `bs4/__init__.py` | Modified | Line 94 | Import SoupReplacer |
| `bs4/__init__.py` | Modified | Line 37 | Add to __all__ |
| `bs4/__init__.py` | Modified | Line 186 | Type annotation |
| `bs4/__init__.py` | Modified | Lines 218-220 | Constructor parameters |
| `bs4/__init__.py` | Modified | Lines 254-255 | Parameter documentation |
| `bs4/__init__.py` | Modified | Lines 453-455 | Parameter handling |
| `bs4/__init__.py` | Modified | Lines 1070-1072 | Parsing hook |
| `bs4/tests/test_soup_replacer.py` | Created | Entire file | Test suite |
| `apps/m2/task-6.py` | Modified | Lines 16-21 | Use SoupReplacer |

**Total:**
- Files created: 1
- Files modified: 3
- Total lines changed: ~40
