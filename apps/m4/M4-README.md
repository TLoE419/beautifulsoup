# Milestone-4
# Making BeautifulSoup Objects Iterable

## Implementation Details

### Location
**File:** `bs4/__init__.py`
**Class:** `BeautifulSoup`
**Method:** `__iter__()` (lines 523-535)

### Design Decisions

1. **Generator Pattern**: Uses Python generators (`yield`) to avoid building an intermediate list of all nodes. This is memory-efficient for large documents.

2. **Depth-First Pre-Order**: Traverses the tree by visiting each node before its children, matching common tree traversal expectations.

3. **Override Only BeautifulSoup**: The `__iter__` method is added only to `BeautifulSoup`, not `Tag`. This means:
   - `for node in soup:` iterates over ALL nodes in the document
   - `for child in tag:` still iterates over direct children only (preserves backward compatibility)

4. **Recursive Traversal**: Uses the tree structure (`.contents` lists) rather than the linear `.next_element` chain used by `.descendants`.

## Tests

### Location
**File:** `bs4/tests/test_soup.py`
**Class:** `TestBeautifulSoupIteration` (lines 605-707)

### Test Cases

All tests use **manual iteration** with `next()` to avoid collecting nodes into lists, demonstrating the generator pattern in action.

#### 1. `test_iterate_simple_document`
Tests basic iteration functionality on a simple document.
```python
markup = "<p>Hello</p>"
# Verifies: yields <p> tag, then "Hello" text
```

#### 2. `test_iterate_nested_structure`
Verifies depth-first pre-order traversal.
```python
markup = "<div><p>A<b>B</b>C</p><span>D</span></div>"
# Verifies order: <div>, <p>, "A", <b>, "B", "C", <span>, "D"
```

#### 3. `test_iterate_mixed_node_types`
Tests iteration over different node types (Tags, NavigableStrings, Comments).
```python
markup = "<!-- comment --><p>Text</p><!-- another -->"
# Verifies: Comment, Tag, NavigableString, Comment
```

#### 4. `test_iterate_empty_document`
Tests edge cases (empty documents, text-only documents).
```python
# Empty: raises StopIteration immediately
# Text-only: yields single NavigableString
```

#### 5. `test_iteration_count_matches_descendants`
Verifies correctness and generator pattern.
```python
# Uses sum(1 for _ in soup) instead of list()
# Confirms same count as .descendants
# Verifies iter() returns a generator object
```

### Running Tests

```bash
# Run all iteration tests
python -m pytest bs4/tests/test_soup.py::TestBeautifulSoupIteration -v