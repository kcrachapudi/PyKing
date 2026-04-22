import streamlit as st

st.set_page_config(page_title="Python King 👑", page_icon="👑", layout="wide")

st.markdown("""
<style>
pre, code { font-family: 'Courier New', monospace; }
.stTabs [data-baseweb="tab"] { font-size: 16px; }
</style>
""", unsafe_allow_html=True)

st.title("👑 Python King — Interview Mastery")
st.caption("Phase 1 · Chapter 1: Data Structures Deep Dive")

tabs = st.tabs(["📖 Learn", "🧠 Quiz", "💻 Practice"])

with tabs[0]:
    st.header("Lists vs Tuples vs Sets vs Dicts")
    st.markdown("""
    Interviewers love asking *when* to use each. Know the tradeoffs cold.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔵 List — ordered, mutable")
        st.code("""
# O(1) append, O(n) insert/search
nums = [3, 1, 4, 1, 5]
nums.append(9)          # add to end
nums.insert(0, 0)       # insert at index
nums.sort()             # in-place sort
top = nums[-1]          # last element

# Slicing — very common in interviews
first3 = nums[:3]
reversed_ = nums[::-1]
every_other = nums[::2]

# List comprehension
evens = [x for x in nums if x % 2 == 0]
        """, language="python")

        st.subheader("🟢 Tuple — ordered, immutable")
        st.code("""
# Use when data should NOT change
point = (10, 20)
rgb = (255, 128, 0)

# Tuple unpacking (very Pythonic)
x, y = point
r, g, b = rgb

# Tuples as dict keys (lists can't be)
grid = {}
grid[(0, 0)] = "start"
grid[(3, 4)] = "end"
        """, language="python")

    with col2:
        st.subheader("🟡 Set — unordered, unique, fast lookup")
        st.code("""
# O(1) average lookup — use for membership tests
seen = set()
nums = [1, 2, 2, 3, 3, 3]
unique = set(nums)       # {1, 2, 3}

# Interview pattern: find duplicates
def has_duplicate(arr):
    return len(arr) != len(set(arr))

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a & b)   # intersection: {3, 4}
print(a | b)   # union: {1,2,3,4,5,6}
print(a - b)   # difference: {1, 2}
        """, language="python")

        st.subheader("🔴 Dict — key-value, O(1) access")
        st.code("""
# The most-used structure in interviews
freq = {}
for ch in "hello":
    freq[ch] = freq.get(ch, 0) + 1
# {'h':1, 'e':1, 'l':2, 'o':1}

# Cleaner with defaultdict
from collections import defaultdict, Counter
freq = Counter("hello")

# Common interview pattern: two-sum
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
        """, language="python")

    st.divider()
    st.subheader("⚡ Time Complexity Cheat Sheet")
    data = {
        "Operation": ["Access by index", "Search (unsorted)", "Insert at end", "Insert at index", "Delete", "Membership test"],
        "List": ["O(1)", "O(n)", "O(1)*", "O(n)", "O(n)", "O(n)"],
        "Dict/Set": ["O(1)", "O(1) avg", "O(1) avg", "—", "O(1) avg", "O(1) avg"],
        "Tuple": ["O(1)", "O(n)", "immutable", "immutable", "immutable", "O(n)"],
    }
    import pandas as pd
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

    st.info("💡 **Interview tip:** When you see a problem needing fast lookups or deduplication → think Set/Dict first.")

with tabs[1]:
    st.header("🧠 Quick Quiz")

    q1 = st.radio(
        "1. Which data structure gives O(1) average-case membership testing?",
        ["List", "Tuple", "Set", "All of them"],
        index=None
    )
    if q1 == "Set":
        st.success("✅ Correct! Sets use a hash table internally.")
    elif q1:
        st.error("❌ Sets (and dict keys) use hashing for O(1) lookup. Lists scan every element.")

    st.divider()

    q2 = st.radio(
        "2. Why can't you use a list as a dictionary key?",
        ["Lists are too slow", "Lists are mutable (unhashable)", "Python limitation", "Lists don't support == operator"],
        index=None
    )
    if q2 == "Lists are mutable (unhashable)":
        st.success("✅ Correct! Dict keys must be hashable. Mutable objects can't be hashed reliably.")
    elif q2:
        st.error("❌ Dict keys must be hashable. Only immutable objects (str, int, tuple) are hashable.")

    st.divider()

    q3 = st.radio(
        "3. What does `nums[::-1]` do?",
        ["Removes last element", "Returns reversed copy", "Sorts in reverse", "Returns every other element"],
        index=None
    )
    if q3 == "Returns reversed copy":
        st.success("✅ Correct! Step -1 walks backwards through the list.")
    elif q3:
        st.error("❌ It's a slice with step=-1, which returns a new reversed copy.")

with tabs[2]:
    st.header("💻 Practice Problems")
    st.markdown("Solve these — they appear in real interviews.")

    with st.expander("Problem 1: Two Sum (Easy — LeetCode #1)"):
        st.markdown("""
Given an array of integers and a target, return the indices of two numbers that add up to the target.

```python
# Input:  nums = [2, 7, 11, 15], target = 9
# Output: [0, 1]  (nums[0] + nums[1] = 9)
```
        """)
        st.code("""
def two_sum(nums, target):
    seen = {}                        # val -> index
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i

# Why dict? O(n) vs O(n²) with brute force
        """, language="python")
        st.success("Key insight: trade space for time. Store what you've seen in a dict.")

    with st.expander("Problem 2: Valid Anagram (Easy — LeetCode #242)"):
        st.markdown("""
Given two strings, return True if one is an anagram of the other.
```python
# "anagram", "nagaram" → True
# "rat", "car"         → False
```
        """)
        st.code("""
from collections import Counter

def is_anagram(s, t):
    return Counter(s) == Counter(t)

# Or without Counter:
def is_anagram_v2(s, t):
    if len(s) != len(t):
        return False
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    for c in t:
        if c not in freq:
            return False
        freq[c] -= 1
        if freq[c] < 0:
            return False
    return True
        """, language="python")

    with st.expander("Problem 3: Group Anagrams (Medium — LeetCode #49)"):
        st.markdown("""
Group a list of strings by anagram families.
```python
# ["eat","tea","tan","ate","nat","bat"]
# → [["eat","tea","ate"], ["tan","nat"], ["bat"]]
```
        """)
        st.code("""
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))   # "eat" → ('a','e','t')
        groups[key].append(s)
    return list(groups.values())
        """, language="python")
        st.info("Pattern: sorted string as dict key to group anagrams — classic.")

st.divider()
st.caption("Next up → Chapter 2: Strings & String Manipulation | Built with ❤️ for Python King")