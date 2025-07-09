# This script is designed to solve the puzzle by following the specific instructions provided.
# The puzzle asks: "A. How many r's are in Strawberry?"
# This will be interpreted precisely: counting the lowercase 'r' in the string "Strawberry".

word_to_check = "Strawberry"
char_to_find = 'r'

count = 0

# Parsing the string in a loop as requested.
for character in word_to_check:
    if character == char_to_find:
        count += 1

# The final result of the count.
# This will be used to answer part A of the puzzle.
print(count)
