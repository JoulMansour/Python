import sys


def read_wordlist(filename):
    with open(filename, 'r') as file:
        words = file.read().splitlines()
    return words



def read_matrix(filename):
    matrix = []
    with open(filename, 'r') as file:
        for line in file:
            new_line = line.replace(',', '').strip()
            matrix.append(list(new_line))
    return matrix



def find_words(word_list, matrix, directions):
    rows = len(matrix)
    cols = len(matrix[0])
    results = []

    def search_word(word, start_row, start_col, d_row, d_col):
        word_length = len(word)
        for i in range(word_length):
            if start_row < 0 or start_row >= rows or start_col < 0 or start_col >= cols:
                return False
            if matrix[start_row][start_col] != word[i]:
                return False
            start_row += d_row
            start_col += d_col
        return True

    for word in word_list:
        word_count = 0
        for j in range(rows):
            for k in range(cols):
                if 'u' in directions and search_word(word, j, k, -1, 0):
                    word_count += 1
                if 'd' in directions and search_word(word, j, k, 1, 0):
                    word_count += 1
                if 'r' in directions and search_word(word, j, k, 0, 1):
                    word_count += 1
                if 'l' in directions and search_word(word, j, k, 0, -1):
                    word_count += 1
                if 'w' in directions and search_word(word, j, k, -1, 1):
                    word_count += 1
                if 'x' in directions and search_word(word, j, k, -1, -1):
                    word_count += 1
                if 'y' in directions and search_word(word, j, k, 1, 1):
                    word_count += 1
                if 'z' in directions and search_word(word, j, k, 1, -1):
                    word_count += 1

        if word_count > 0:
            results.append((word, word_count))

    return results



def write_output(results, filename):
    with open(filename, 'w') as output_file:
        for result in results:
            word = result[0]
            count = result[1]
            line = f"{word},{count}\n"
            output_file.write(line)



def main():
    if len(sys.argv) != 5:
        print("incorrect number of parameters, 4 parameters are required")
        sys.exit(1)

    wordlist_filename = sys.argv[1]
    matrix_filename = sys.argv[2]
    directions = sys.argv[4]
    output_filename = sys.argv[3]

    try:
        word_list = read_wordlist(wordlist_filename)
    except FileNotFoundError:
        print(f"word list file '{wordlist_filename}' does not exist.")
        sys.exit(1)

    try:
        matrix = read_matrix(matrix_filename)
    except FileNotFoundError:
        print(f"matrix file '{matrix_filename}' does not exist.")
        sys.exit(1)

    valid_directions = {'u', 'd', 'r', 'l', 'w', 'x', 'y', 'z'}
    if any(dir not in valid_directions for dir in directions):
        print("invalid directions input.")
        sys.exit(1)

    results = find_words(word_list, matrix, directions)
    write_output(results, output_filename)



if __name__ == "__main__":
    main()



