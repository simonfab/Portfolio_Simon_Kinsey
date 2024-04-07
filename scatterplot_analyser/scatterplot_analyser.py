'''
Scatterplot analyser is just to assist understand the graphs that are output
from matplotlib.
The user is asked how many variables are included (eg 3)
The script then asks for the names (eg colours, sizes, weights)
The user has the choice of reversing the variables for the y axis

The output is a tabular view giving a unique id to each plot within a
scatterplot.

Followed by a text description of each plot pair

And an indication of whether its the first unique combination of that pair 
or whether its a distribution
first instance of unique pairs is coloured red
distribution (identity pairs) are coloured green
and non unique pairs (second instances of pairs) are coloured white

Basically its to help the user "talk to themselves" about plot pairs to retain
understanding - espeically when there are higher numbers of variables.

'''
var_count = input("Please enter the number of variables...\n")
var_count = int(var_count)

var_name_list = []
for i in range(var_count):
    var_name = input("Please enter a variable name: ")
    var_name_list.append(var_name)

# Asking the user if they want to reverse the variable list
reverse_option = input("Do you want to reverse the variable list? (y/no): ").strip().lower()

# Determine the order of the variable list based on user input
if reverse_option == 'y':
    primary_list = var_name_list
    secondary_list = var_name_list[::-1]
else:
    primary_list = secondary_list = var_name_list

# Create and print the tabular key view
print("\nTabular Key View:")
for row in range(var_count, 0, -1):
    for col in range(1, var_count + 1):
        print(f"{(row - 1) * var_count + col:2}", end=' ')
    print()
print()

# Building the list of combinations with additional information
combinations = []
seen_combinations = set()
for j, v2 in enumerate(secondary_list):
    for i, v1 in enumerate(primary_list):
        tid = j * var_count + i + 1  # Calculate the ID
        if v1 == v2:
            combination_type = "Distribution"
        elif ((v1, v2) not in seen_combinations and
              (v2, v1) not in seen_combinations):
            combination_type = "Unique"
            seen_combinations.add((v1, v2))
            seen_combinations.add((v2, v1))
        else:
            combination_type = "Not Unique"

        # Calculate the tid of the identical pair
        if reverse_option == 'y':
            pair_tid = (var_count - 1 - i) * var_count + (var_count - j)
        else:
            pair_tid = i * var_count + j + 1

        combinations.append((tid, v1, v2, combination_type, pair_tid))

# Printing the combinations with specific colors and pair tid
for combo in combinations:
    tid, v1, v2, combo_type, pair_tid = combo
    if combo_type == "Unique":
        print(f"\033[91m{tid}: {v1} vs {v2} - {combo_type}"
              f"(Pair: {pair_tid})\033[0m")  # Red color for Unique
    elif combo_type == "Distribution":
        print(f"\033[92m{tid}: {v1} vs {v2} - {combo_type}"
              f"(Pair: {pair_tid})\033[0m")  # Green color for Distribution
    else:
        print(f"{tid}: {v1} vs {v2} - {combo_type}"
              f"(Pair: {pair_tid})")  # Default color for others
        
print("test")
