# Python List Methods Demonstration Program

def print_section(title):
    """Helper function to print section headers"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print('='*50)

# Creating lists
print_section("1. Creating Lists")
fruits = ['apple', 'banana', 'cherry']
numbers = [1, 2, 3, 4, 5]
mixed = [1, 'hello', 3.14, True]
print(f"Fruits list: {fruits}")
print(f"Numbers list: {numbers}")
print(f"Mixed list: {mixed}")

# append() - adds element at the end
print_section("2. append() Method")
fruits.append('orange')
print(f"After append('orange'): {fruits}")

# insert() - inserts element at specific position
print_section("3. insert() Method")
fruits.insert(1, 'mango')
print(f"After insert(1, 'mango'): {fruits}")

# extend() - adds multiple elements
print_section("4. extend() Method")
more_fruits = ['grape', 'kiwi']
fruits.extend(more_fruits)
print(f"After extend({more_fruits}): {fruits}")

# remove() - removes first occurrence of value
print_section("5. remove() Method")
fruits.remove('banana')
print(f"After remove('banana'): {fruits}")

# pop() - removes and returns element at index
print_section("6. pop() Method")
popped = fruits.pop()
print(f"Popped element: {popped}")
print(f"List after pop(): {fruits}")
popped_at_index = fruits.pop(2)
print(f"Popped element at index 2: {popped_at_index}")
print(f"List after pop(2): {fruits}")

# index() - returns index of first occurrence
print_section("7. index() Method")
print(f"Current fruits list: {fruits}")
idx = fruits.index('orange')
print(f"Index of 'orange': {idx}")
# Demonstrating with a fresh list
colors = ['red', 'blue', 'green', 'blue', 'yellow']
print(f"\nColors list: {colors}")
print(f"Index of first 'blue': {colors.index('blue')}")
print(f"Index of 'yellow': {colors.index('yellow')}")

# count() - counts occurrences of element
print_section("8. count() Method")
numbers = [1, 2, 2, 3, 2, 4, 5, 2]
count_2 = numbers.count(2)
print(f"List: {numbers}")
print(f"Count of 2: {count_2}")

# sort() - sorts list in place
print_section("9. sort() Method")
unsorted = [5, 2, 8, 1, 9, 3]
print(f"Before sort: {unsorted}")
unsorted.sort()
print(f"After sort(): {unsorted}")
unsorted.sort(reverse=True)
print(f"After sort(reverse=True): {unsorted}")

# reverse() - reverses list in place
print_section("10. reverse() Method")
items = [1, 2, 3, 4, 5]
print(f"Before reverse: {items}")
items.reverse()
print(f"After reverse(): {items}")

# copy() - creates shallow copy
print_section("11. copy() Method")
original = [1, 2, 3]
copied = original.copy()
copied.append(4)
print(f"Original list: {original}")
print(f"Copied list: {copied}")

# clear() - removes all elements
print_section("12. clear() Method")
to_clear = [1, 2, 3, 4, 5]
print(f"Before clear: {to_clear}")
to_clear.clear()
print(f"After clear(): {to_clear}")

# List operations
print_section("13. Other List Operations")
list1 = [1, 2, 3]
list2 = [4, 5, 6]

# Concatenation
combined = list1 + list2
print(f"Concatenation {list1} + {list2} = {combined}")

# Repetition
repeated = list1 * 3
print(f"Repetition {list1} * 3 = {repeated}")

# Membership testing
print(f"Is 2 in {list1}? {2 in list1}")
print(f"Is 10 in {list1}? {10 in list1}")

# Length
print(f"Length of {list1}: {len(list1)}")

# Slicing
print_section("14. List Slicing")
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"Original: {nums}")
print(f"nums[2:5]: {nums[2:5]}")
print(f"nums[:4]: {nums[:4]}")
print(f"nums[6:]: {nums[6:]}")
print(f"nums[::2]: {nums[::2]}")
print(f"nums[::-1]: {nums[::-1]}")

# List comprehension
print_section("15. List Comprehension")
squares = [x**2 for x in range(1, 6)]
print(f"Squares of 1-5: {squares}")

evens = [x for x in range(20) if x % 2 == 0]
print(f"Even numbers 0-19: {evens}")

print("\n" + "="*50)
print("Program completed successfully!")
print("="*50)
