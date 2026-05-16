# ============================================================
#  CHAPTER 10 — INTERVIEW PREP: DATA STRUCTURES & ALGORITHMS
#  Your complete reference. Come back anytime.
# ============================================================


# ------------------------------------------------------------
# 1. HOW TO APPROACH ANY INTERVIEW PROBLEM
# ------------------------------------------------------------
# Follow this framework every single time:
#
#   1. UNDERSTAND  → repeat the problem in your own words
#                    ask clarifying questions (edge cases, constraints)
#                    "Can input be empty? Can numbers be negative?"
#
#   2. EXAMPLES    → walk through 2-3 examples by hand
#                    include edge cases: empty, one element, duplicates
#
#   3. BRUTE FORCE → state the naive solution first
#                    "I could do X which is O(n²) — let me optimize"
#
#   4. OPTIMIZE    → think about better data structures
#                    can I trade space for time? (dict/set for O(1) lookup)
#
#   5. CODE        → write clean code, talk while you type
#
#   6. TEST        → trace through your code with examples
#                    test edge cases explicitly


# ------------------------------------------------------------
# 2. BIG O — TIME & SPACE COMPLEXITY
# ------------------------------------------------------------
# Big O describes how runtime or memory SCALES with input size n.
#
#   O(1)       → constant    — dict lookup, list index access
#   O(log n)   → logarithmic — binary search, balanced BST
#   O(n)       → linear      — single loop, linear search
#   O(n log n) → linearithmic— merge sort, heap sort, Python sort
#   O(n²)      → quadratic   — nested loops, bubble sort
#   O(2^n)     → exponential — recursive subsets, fibonacci naive
#   O(n!)      → factorial   — permutations
#
# Fastest → Slowest:
#   O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2^n) < O(n!)

def time_complexity_examples():

    # O(1) — same time regardless of n
    def get_first(lst):
        return lst[0]          # index access is always O(1)

    # O(n) — time grows linearly with n
    def find_max(lst):
        max_val = lst[0]
        for x in lst:          # one pass through the list
            if x > max_val:
                max_val = x
        return max_val

    # O(n²) — nested loops, each 0..n
    def has_duplicate_naive(lst):
        for i in range(len(lst)):
            for j in range(i+1, len(lst)):   # n*(n-1)/2 comparisons
                if lst[i] == lst[j]:
                    return True
        return False

    # O(n) — using a set for O(1) lookup (space-time tradeoff)
    def has_duplicate_fast(lst):
        seen = set()
        for x in lst:
            if x in seen:      # O(1) set lookup
                return True
            seen.add(x)
        return False


# ------------------------------------------------------------
# 3. ARRAYS & STRINGS — most common interview topic
# ------------------------------------------------------------

# Pattern: TWO POINTERS
# Use when: searching pairs, palindromes, sorted arrays
# Key insight: start pointers at both ends, move toward center

def is_palindrome(s):
    """Check if string is a palindrome using two pointers. O(n) time O(1) space."""
    s = s.lower().replace(" ", "")    # normalize
    left, right = 0, len(s) - 1      # pointers start at both ends
    while left < right:
        if s[left] != s[right]:
            return False    # mismatch — not a palindrome
        left  += 1          # move left pointer right
        right -= 1          # move right pointer left
    return True

print(is_palindrome("racecar"))    # True
print(is_palindrome("hello"))      # False


def two_sum(nums, target):
    """Find indices of two numbers that add to target. O(n) time O(n) space.
    Key insight: for each number, check if (target - number) was seen before."""
    seen = {}    # value → index map
    for i, n in enumerate(nums):
        complement = target - n         # what we need to find
        if complement in seen:          # O(1) dict lookup
            return [seen[complement], i]
        seen[n] = i                     # record this number and its index
    return []

print(two_sum([2, 7, 11, 15], 9))    # [0, 1]  (2 + 7 = 9)
print(two_sum([3, 2, 4], 6))         # [1, 2]  (2 + 4 = 6)


def max_subarray(nums):
    """Kadane's algorithm — find max sum contiguous subarray. O(n) time.
    Key insight: at each position, decide: extend previous subarray or start fresh."""
    max_sum     = nums[0]    # best sum found so far
    current_sum = nums[0]    # best sum ending at current position

    for num in nums[1:]:
        # Should we extend the previous subarray or start a new one here?
        current_sum = max(num, current_sum + num)
        max_sum     = max(max_sum, current_sum)

    return max_sum

print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))    # 6 → [4,-1,2,1]


# Pattern: SLIDING WINDOW
# Use when: contiguous subarray/substring problems
# Key insight: expand right pointer, shrink left pointer to maintain constraint

def max_sum_subarray_k(nums, k):
    """Maximum sum of any subarray of size k. O(n) time.
    Key insight: slide a window of size k across the array."""
    window_sum = sum(nums[:k])    # sum of first window
    max_sum    = window_sum

    for i in range(k, len(nums)):
        window_sum += nums[i]       # add new right element
        window_sum -= nums[i - k]   # remove old left element
        max_sum = max(max_sum, window_sum)

    return max_sum

print(max_sum_subarray_k([2, 1, 5, 1, 3, 2], 3))    # 9 → [5,1,3]


def longest_substring_no_repeat(s):
    """Longest substring without repeating characters. O(n) time.
    Key insight: use a set to track chars in current window."""
    char_set   = set()       # chars currently in our window
    left       = 0           # left boundary of window
    max_length = 0

    for right in range(len(s)):    # right pointer expands the window
        while s[right] in char_set:
            char_set.remove(s[left])   # shrink window from left until no duplicate
            left += 1
        char_set.add(s[right])         # add new char to window
        max_length = max(max_length, right - left + 1)

    return max_length

print(longest_substring_no_repeat("abcabcbb"))    # 3 → "abc"
print(longest_substring_no_repeat("pwwkew"))      # 3 → "wke"


# ------------------------------------------------------------
# 4. LINKED LISTS
# ------------------------------------------------------------

class ListNode:
    """Standard linked list node used in interview problems."""
    def __init__(self, val=0, next=None):
        self.val  = val
        self.next = next    # pointer to next node (None if last)

    def __repr__(self):
        return f"{self.val} → {self.next}"


def make_list(values):
    """Helper: create linked list from a Python list."""
    if not values: return None
    head = ListNode(values[0])    # first node is the head
    curr = head
    for val in values[1:]:
        curr.next = ListNode(val)  # attach each node to the previous
        curr = curr.next           # advance current pointer
    return head


def reverse_linked_list(head):
    """Reverse a linked list in place. O(n) time O(1) space.
    Key insight: keep track of previous, current, and next nodes."""
    prev = None     # previous node starts as None (new tail)
    curr = head     # start at head

    while curr:
        next_node  = curr.next    # save next before we overwrite it
        curr.next  = prev         # reverse the pointer
        prev       = curr         # advance prev to current
        curr       = next_node    # advance curr to saved next

    return prev    # prev is now the new head (last node we processed)

lst = make_list([1, 2, 3, 4, 5])
print(reverse_linked_list(lst))    # 5 → 4 → 3 → 2 → 1


def has_cycle(head):
    """Detect a cycle in linked list using Floyd's algorithm. O(n) O(1).
    Key insight: slow pointer moves 1 step, fast moves 2 steps.
    If there's a cycle, fast will eventually lap slow and they'll meet."""
    slow = head    # tortoise — moves 1 step at a time
    fast = head    # hare — moves 2 steps at a time

    while fast and fast.next:
        slow = slow.next          # advance slow by 1
        fast = fast.next.next     # advance fast by 2
        if slow is fast:
            return True    # they met — there's a cycle!

    return False    # fast reached the end — no cycle


def find_middle(head):
    """Find the middle node of a linked list. O(n) O(1).
    Key insight: when fast reaches end, slow is at middle."""
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next        # slow: 1 step
        fast = fast.next.next  # fast: 2 steps

    return slow    # slow is at the middle when fast reaches end

lst = make_list([1, 2, 3, 4, 5])
print(find_middle(lst).val)    # 3


def merge_sorted_lists(l1, l2):
    """Merge two sorted linked lists into one sorted list. O(n+m) O(1).
    Key insight: use a dummy node to simplify edge cases."""
    dummy = ListNode(0)    # dummy head — avoids special case for empty list
    curr  = dummy          # pointer to build the merged list

    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1    # attach smaller node
            l1 = l1.next      # advance l1
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next      # advance our builder pointer

    curr.next = l1 or l2      # attach remaining nodes (one list may have more)

    return dummy.next    # skip the dummy, return real head


# ------------------------------------------------------------
# 5. STACKS & QUEUES
# ------------------------------------------------------------
# Stack: LIFO (Last In First Out) — use a Python list
# Queue: FIFO (First In First Out) — use collections.deque

from collections import deque

# Stack operations using Python list
stack = []
stack.append(1)     # push — O(1)
stack.append(2)
stack.append(3)
top = stack[-1]     # peek — O(1)
stack.pop()         # pop  — O(1)

# Queue operations using deque
queue = deque()
queue.append(1)     # enqueue — O(1)
queue.append(2)
queue.append(3)
front = queue[0]    # peek front — O(1)
queue.popleft()     # dequeue — O(1) (list.pop(0) is O(n) — don't use it!)


def is_valid_parentheses(s):
    """Check if brackets are balanced. O(n) time O(n) space.
    Key insight: push open brackets, pop and match on close brackets."""
    stack    = []
    matching = {')': '(', '}': '{', ']': '['}    # close → open mapping

    for char in s:
        if char in "({[":
            stack.append(char)     # push open bracket
        elif char in ")}]":
            if not stack or stack[-1] != matching[char]:
                return False       # no matching open bracket
            stack.pop()            # matched — pop the open bracket

    return len(stack) == 0    # True if all brackets were matched

print(is_valid_parentheses("()[]{}"))     # True
print(is_valid_parentheses("([)]"))       # False
print(is_valid_parentheses("{[]}"))       # True


def daily_temperatures(temps):
    """For each day, how many days until a warmer temp? O(n).
    Key insight: monotonic stack stores indices of unresolved days."""
    result = [0] * len(temps)    # default: 0 means no warmer day found
    stack  = []                   # stack of indices waiting for a warmer day

    for i, temp in enumerate(temps):
        # While top of stack has a cooler day than today
        while stack and temps[stack[-1]] < temp:
            prev_day       = stack.pop()          # that day found its warmer day
            result[prev_day] = i - prev_day       # distance = today - that day
        stack.append(i)    # today is unresolved — push its index

    return result

print(daily_temperatures([73,74,75,71,69,72,76,73]))
# [1, 1, 4, 2, 1, 1, 0, 0]


# ------------------------------------------------------------
# 6. BINARY SEARCH
# ------------------------------------------------------------
# Use when: sorted array, find target, minimize/maximize something
# Key insight: eliminate HALF the search space each iteration

def binary_search(nums, target):
    """Find target in sorted array. O(log n) time O(1) space."""
    left, right = 0, len(nums) - 1    # search space: entire array

    while left <= right:
        mid = left + (right - left) // 2    # avoid overflow (vs (left+right)//2)

        if nums[mid] == target:
            return mid           # found it!
        elif nums[mid] < target:
            left = mid + 1       # target is in right half — discard left
        else:
            right = mid - 1      # target is in left half — discard right

    return -1    # not found

print(binary_search([1,3,5,7,9,11,13], 7))     # 3 (index)
print(binary_search([1,3,5,7,9,11,13], 6))     # -1 (not found)


def search_rotated(nums, target):
    """Binary search in a rotated sorted array. O(log n).
    Key: one half is ALWAYS sorted — determine which half, search it."""
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid

        # Left half is sorted (normal order)
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:    # target in left half
                right = mid - 1
            else:
                left = mid + 1                      # target in right half
        else:
            # Right half is sorted
            if nums[mid] < target <= nums[right]:   # target in right half
                left = mid + 1
            else:
                right = mid - 1                     # target in left half

    return -1

print(search_rotated([4,5,6,7,0,1,2], 0))    # 4
print(search_rotated([4,5,6,7,0,1,2], 3))    # -1


# ------------------------------------------------------------
# 7. TREES
# ------------------------------------------------------------

class TreeNode:
    """Standard binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val   = val
        self.left  = left
        self.right = right


def inorder(root):
    """Inorder traversal: Left → Root → Right. O(n).
    For BST, this gives nodes in SORTED order."""
    if not root: return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def preorder(root):
    """Preorder: Root → Left → Right. O(n). Good for copying a tree."""
    if not root: return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def postorder(root):
    """Postorder: Left → Right → Root. O(n). Good for deleting a tree."""
    if not root: return []
    return postorder(root.left) + postorder(root.right) + [root.val]


def max_depth(root):
    """Maximum depth of binary tree. O(n).
    Key insight: depth = 1 + max(left depth, right depth)."""
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def is_balanced(root):
    """Check if tree is height-balanced. O(n).
    Key insight: check height AND balance simultaneously."""
    def check(node):
        if not node: return 0                     # base case: height 0
        left  = check(node.left)
        right = check(node.right)
        if left == -1 or right == -1:             # subtree already unbalanced
            return -1
        if abs(left - right) > 1:                 # this node is unbalanced
            return -1
        return 1 + max(left, right)               # return height

    return check(root) != -1


def level_order(root):
    """BFS level-order traversal. O(n). Returns list of levels."""
    if not root: return []
    result = []
    queue  = deque([root])    # start with root in queue

    while queue:
        level_size = len(queue)    # number of nodes at current level
        level      = []

        for _ in range(level_size):
            node = queue.popleft()          # process node
            level.append(node.val)
            if node.left:  queue.append(node.left)   # enqueue children
            if node.right: queue.append(node.right)

        result.append(level)    # save this level's values

    return result


def lowest_common_ancestor(root, p, q):
    """Find LCA of two nodes in a BST. O(log n) for BST, O(n) general.
    Key insight: if both p and q are less than root, go left. Both greater, go right.
    Otherwise, root IS the LCA."""
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left     # both nodes in left subtree
        elif p.val > root.val and q.val > root.val:
            root = root.right    # both nodes in right subtree
        else:
            return root          # they split here — root is LCA
    return None


def validate_bst(root):
    """Check if binary tree is a valid BST. O(n).
    Key insight: each node has a valid range (min, max) it must fall within."""
    def validate(node, min_val, max_val):
        if not node: return True                         # empty tree is valid BST
        if node.val <= min_val or node.val >= max_val:   # violates BST property
            return False
        return (validate(node.left,  min_val,  node.val) and   # left must be < current
                validate(node.right, node.val, max_val))        # right must be > current

    return validate(root, float('-inf'), float('inf'))


# ------------------------------------------------------------
# 8. GRAPHS
# ------------------------------------------------------------

def bfs(graph, start):
    """Breadth-First Search — visit nodes level by level. O(V+E).
    Use for: shortest path in unweighted graph, level-order problems."""
    visited = set([start])    # track visited nodes to avoid revisiting
    queue   = deque([start])  # FIFO — process nodes in order added
    order   = []

    while queue:
        node = queue.popleft()    # process next node
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def dfs(graph, start, visited=None):
    """Depth-First Search — explore as deep as possible first. O(V+E).
    Use for: detecting cycles, topological sort, connected components."""
    if visited is None: visited = set()
    visited.add(start)
    result = [start]
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result.extend(dfs(graph, neighbor, visited))
    return result


def num_islands(grid):
    """Count number of islands (connected 1s) in a 2D grid. O(m*n).
    Key insight: DFS/BFS from each unvisited '1', mark all connected as visited."""
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return    # out of bounds or water or already visited
        grid[r][c] = '0'         # mark as visited (sink the island)
        dfs(r+1, c)              # explore all 4 directions
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1       # found a new island
                dfs(r, c)        # sink the whole island

    return count

grid = [
    ['1','1','0','0','0'],
    ['1','1','0','0','0'],
    ['0','0','1','0','0'],
    ['0','0','0','1','1'],
]
print(num_islands(grid))    # 3


# ------------------------------------------------------------
# 9. DYNAMIC PROGRAMMING
# ------------------------------------------------------------
# DP = break problem into overlapping subproblems, cache results.
# Two approaches:
#   Top-down (memoization): recursion + cache
#   Bottom-up (tabulation): fill a table iteratively

def fibonacci_dp(n):
    """Fibonacci with memoization. O(n) time O(n) space."""
    memo = {}    # cache: n → fib(n)

    def fib(n):
        if n <= 1: return n
        if n in memo: return memo[n]    # return cached result
        memo[n] = fib(n-1) + fib(n-2)  # compute and cache
        return memo[n]

    return fib(n)

print(fibonacci_dp(40))    # 102334155 — fast with memoization


def climb_stairs(n):
    """Count ways to climb n stairs (1 or 2 steps at a time). O(n) O(1).
    Key insight: ways(n) = ways(n-1) + ways(n-2) — it's Fibonacci!"""
    if n <= 2: return n
    prev2, prev1 = 1, 2    # base cases: 1 stair = 1 way, 2 stairs = 2 ways

    for _ in range(3, n+1):
        curr  = prev1 + prev2    # ways to reach stair i
        prev2 = prev1            # slide the window
        prev1 = curr

    return prev1

print(climb_stairs(5))    # 8


def coin_change(coins, amount):
    """Minimum coins needed to make amount. O(amount * len(coins)).
    Key insight: dp[i] = min coins to make amount i.
    For each amount, try every coin and take the minimum."""
    dp = [float('inf')] * (amount + 1)    # dp[i] = min coins for amount i
    dp[0] = 0                              # 0 coins needed to make amount 0

    for amt in range(1, amount + 1):
        for coin in coins:
            if coin <= amt:    # coin can contribute to this amount
                dp[amt] = min(dp[amt], dp[amt - coin] + 1)
                # dp[amt-coin] + 1 means: use one of this coin,
                # plus whatever it takes to make the remaining amount

    return dp[amount] if dp[amount] != float('inf') else -1

print(coin_change([1,5,10,25], 36))    # 3  (25+10+1)
print(coin_change([2], 3))             # -1 (impossible)


def longest_common_subsequence(s1, s2):
    """LCS of two strings. O(m*n) time O(m*n) space.
    Key insight: if chars match, extend LCS; otherwise take best of two options."""
    m, n = len(s1), len(s2)
    dp   = [[0] * (n+1) for _ in range(m+1)]    # dp[i][j] = LCS of s1[:i], s2[:j]

    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:              # chars match — extend LCS
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # take best without one char

    return dp[m][n]

print(longest_common_subsequence("abcde", "ace"))    # 3 → "ace"


def knapsack_01(weights, values, capacity):
    """0/1 Knapsack — max value within weight capacity. O(n*W).
    Key insight: for each item, either take it or leave it."""
    n  = len(weights)
    dp = [[0] * (capacity+1) for _ in range(n+1)]
    # dp[i][w] = max value using first i items with weight limit w

    for i in range(1, n+1):
        for w in range(capacity+1):
            # Option 1: skip item i
            dp[i][w] = dp[i-1][w]
            # Option 2: take item i (if it fits)
            if weights[i-1] <= w:
                take = values[i-1] + dp[i-1][w - weights[i-1]]
                dp[i][w] = max(dp[i][w], take)

    return dp[n][capacity]

print(knapsack_01([2,3,4,5], [3,4,5,6], 5))    # 7 (items 0+1: weight 5, value 7)


# ------------------------------------------------------------
# 10. SORTING ALGORITHMS
# ------------------------------------------------------------

def merge_sort(arr):
    """Divide and conquer. O(n log n) time O(n) space. Stable sort."""
    if len(arr) <= 1: return arr

    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid])     # sort left half recursively
    right = merge_sort(arr[mid:])     # sort right half recursively

    # Merge two sorted halves
    result = []
    i = j  = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1

    result.extend(left[i:])     # append remaining left elements
    result.extend(right[j:])    # append remaining right elements
    return result

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))    # [3, 9, 10, 27, 38, 43, 82]


def quick_sort(arr, low=0, high=None):
    """Divide and conquer. O(n log n) avg, O(n²) worst. In-place."""
    if high is None: high = len(arr) - 1

    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)     # sort left of pivot
        quick_sort(arr, pivot_idx + 1, high)    # sort right of pivot

def partition(arr, low, high):
    """Place pivot in correct position, smaller left, larger right."""
    pivot = arr[high]    # choose last element as pivot
    i     = low - 1      # index of smaller element

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]    # swap smaller to left side

    arr[i+1], arr[high] = arr[high], arr[i+1]  # place pivot in correct spot
    return i + 1    # return pivot's final index

arr = [10, 7, 8, 9, 1, 5]
quick_sort(arr)
print(arr)    # [1, 5, 7, 8, 9, 10]


# ------------------------------------------------------------
# 11. COMMON INTERVIEW PATTERNS — cheat sheet
# ------------------------------------------------------------

# Pattern: FREQUENCY COUNTER — use dict/Counter to count occurrences
from collections import Counter

def is_anagram(s, t):
    """O(n) — character frequency comparison."""
    return Counter(s) == Counter(t)

def top_k_frequent(nums, k):
    """Return k most frequent elements. O(n log k)."""
    return [val for val, _ in Counter(nums).most_common(k)]

print(top_k_frequent([1,1,1,2,2,3], 2))    # [1, 2]


# Pattern: FAST & SLOW POINTERS — detect cycles, find middle
def find_duplicate(nums):
    """Find duplicate in array of n+1 nums in range [1,n]. O(n) O(1).
    Treat array as linked list — duplicate = cycle entry point."""
    slow = fast = nums[0]

    while True:
        slow = nums[slow]            # slow: 1 step
        fast = nums[nums[fast]]      # fast: 2 steps
        if slow == fast: break       # cycle detected

    slow = nums[0]                   # reset slow to start
    while slow != fast:
        slow = nums[slow]            # both move 1 step
        fast = nums[fast]            # they meet at cycle entry = duplicate

    return slow

print(find_duplicate([1,3,4,2,2]))    # 2


# Pattern: MERGE INTERVALS
def merge_intervals(intervals):
    """Merge overlapping intervals. O(n log n).
    Key: sort by start, then merge if current start <= prev end."""
    intervals.sort(key=lambda x: x[0])    # sort by start time
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:         # overlaps with last merged interval
            merged[-1][1] = max(merged[-1][1], end)   # extend end if needed
        else:
            merged.append([start, end])    # no overlap — add new interval

    return merged

print(merge_intervals([[1,3],[2,6],[8,10],[15,18]]))    # [[1,6],[8,10],[15,18]]


# Pattern: BACKTRACKING — explore all possibilities, undo if wrong
def generate_subsets(nums):
    """Generate all subsets (power set). O(2^n)."""
    result = []

    def backtrack(start, current):
        result.append(current[:])    # add copy of current subset to results

        for i in range(start, len(nums)):
            current.append(nums[i])          # CHOOSE: include nums[i]
            backtrack(i + 1, current)         # EXPLORE: recurse with nums[i] included
            current.pop()                     # UNCHOOSE: remove nums[i] (backtrack)

    backtrack(0, [])
    return result

print(generate_subsets([1, 2, 3]))
# [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]


def permutations(nums):
    """Generate all permutations. O(n!)."""
    result = []

    def backtrack(current, remaining):
        if not remaining:                    # no more elements to place
            result.append(current[:])        # found a complete permutation
            return
        for i in range(len(remaining)):
            current.append(remaining[i])     # choose element i
            backtrack(current, remaining[:i] + remaining[i+1:])   # explore without i
            current.pop()                    # unchoose

    backtrack([], nums)
    return result

print(permutations([1,2,3]))    # all 6 permutations


# ============================================================
# SUMMARY — Interview Pattern Cheat Sheet
# ============================================================
# Two Pointers      → sorted array, palindrome, pair sum
# Sliding Window    → subarray/substring with constraint
# Hash Map/Set      → O(1) lookup, frequency count, seen before
# Binary Search     → sorted array, O(log n) search
# BFS               → shortest path, level-order, unweighted graph
# DFS               → path finding, cycle detection, tree traversal
# Backtracking      → all combinations/permutations/subsets
# Dynamic Programming→ overlapping subproblems, optimal substructure
# Fast & Slow       → cycle detection, find middle
# Merge Intervals   → overlapping ranges, schedule conflicts
# Monotonic Stack   → next greater/smaller element
# Top K Elements    → use heap (heapq) or Counter.most_common
# Trie              → prefix matching, autocomplete
#
# Space-Time tradeoff:
#   Can't optimize time?  Use more space (dict, set, dp table)
#   Can't optimize space? Accept slower time (O(n²) → O(n log n))
# ============================================================