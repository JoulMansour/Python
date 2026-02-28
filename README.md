## Projects

### decision_tree
A simple medical **decision tree** diagnoser.
- Builds a binary tree from symptom questions.
- Can diagnose an illness from a symptom list, calculate success rate on labeled records, list illnesses in the tree, show paths to a specific illness, and minimize redundant nodes.
- Includes an `optimal_tree` function that searches for the best tree using a limited number of symptoms (depth).

### puzzle_solver
A **grid puzzle solver/generator** based on visibility constraints.
- Solves an `n x m` grid where each cell is `0/1` (and `-1` for unknown during solving).
- Each constraint `(row, col, seen)` restricts how many cells are “visible” from that cell (up/down/left/right) until a blocking `0`.
- Can solve a puzzle, count how many solutions exist, and generate constraints from a completed picture.

### word_search
A **word-search finder** for a letter matrix.
- Reads a word list and a character grid from files.
- Searches for each word in selected directions (up/down/left/right + diagonals).
- Outputs each found word with the number of occurrences to a CSV-style file (`word,count`).
