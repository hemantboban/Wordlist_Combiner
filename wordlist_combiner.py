import os
import argparse
from termcolor import colored

# Function to check if a string matches a target with optional case sensitivity
def match_string(partial, target, case_sensitive):
    return partial in target if case_sensitive else partial.lower() in target.lower()

# Function to search for files based on partial matches in filenames or folder names
def find_files(search_dir, partial_names, case_sensitive=False, folders_only=False):
    matched_files = []
    for root, dirs, files in os.walk(search_dir):
        if folders_only:
            for dir_ in dirs:
                if any(match_string(partial, dir_, case_sensitive) for partial in partial_names):
                    for sub_root, _, sub_files in os.walk(os.path.join(root, dir_)):
                        matched_files.extend(os.path.join(sub_root, f) for f in sub_files)
        else:
            for file in files:
                if any(match_string(partial, file, case_sensitive) for partial in partial_names):
                    matched_files.append(os.path.join(root, file))
    return matched_files

# Function to combine wordlists from file paths
def combine_wordlists(filepaths):
    combined_list = []
    for filepath in filepaths:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                combined_list.extend(file.read().splitlines())
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    return [line for line in combined_list if line.strip()]

# Function to remove duplicates and sort the list
def remove_duplicates(wordlist):
    unique_words = sorted(set(wordlist))
    return unique_words, len(wordlist) - len(unique_words)

# Function to write the combined list to an output file
def write_output(output_filepath, wordlist):
    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.write('\n'.join(wordlist))
    print(f"\nCombined wordlist saved to: {colored(output_filepath, 'cyan')}")

# Function to highlight matches in file paths
def highlight_paths(paths, search_strings, case_sensitive):
    print("\n# Matched files:")
    for idx, path in enumerate(paths):
        highlighted_path = path
        for search in search_strings:
            if case_sensitive:
                highlighted_path = highlighted_path.replace(search, colored(search, 'yellow'))
            else:
                lower_search = search.lower()
                parts = highlighted_path.split(lower_search)
                highlighted_path = parts[0]
                for part in parts[1:]:
                    highlighted_path += colored(lower_search, 'yellow') + part
        print(f"{colored(str(idx + 1) + '.', 'magenta')} {highlighted_path}")

# Function to prompt user for file selection or removal
def prompt_user_selection(file_paths):
    while True:
        print("\nModify the list:")
        print("1: Select specific entries")
        print("2: Remove specific entries")
        print("3: Proceed without changes")
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            indices = input("Enter indices to keep (comma-separated): ").strip().split(',')
            indices = [int(idx.strip()) - 1 for idx in indices]
            file_paths = [file_paths[i] for i in indices if 0 <= i < len(file_paths)]
            break
        elif choice == "2":
            indices = input("Enter indices to remove (comma-separated): ").strip().split(',')
            indices = [int(idx.strip()) - 1 for idx in indices]
            file_paths = [file_paths[i] for i in range(len(file_paths)) if i not in indices]
            break
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    return file_paths

def main():
        
    parser = argparse.ArgumentParser(description="Combine multiple wordlists by matching file or folder names.")
    parser.add_argument("-d", "--directory", required=True, help="Root directory containing the wordlists")
    parser.add_argument("-s", "--search", required=True, help="Substring(s) to search (comma-separated)")
    parser.add_argument("-o", "--output", required=True, help="Output filename for the combined wordlist")
    parser.add_argument("--folders-only", action="store_true", help="Search only in folder names")
    parser.add_argument("--case-sensitive", action="store_true", help="Case-sensitive search")
    parser.add_argument("--no-prompt", action="store_true", help="Bypass the prompt for file selection/removal")

    args = parser.parse_args()

    try:
        search_dir = args.directory
        search_strings = [s.strip() for s in args.search.split(',')]
        output_file = args.output
        case_sensitive = args.case_sensitive
        folders_only = args.folders_only
        no_prompt = args.no_prompt

        # Find files based on search criteria
        files = find_files(search_dir, search_strings, case_sensitive, folders_only)
        if not files:
            print("No matching files found.")
            return

        # Highlight matched file paths
        highlight_paths(files, search_strings, case_sensitive)

        # Optionally prompt user for file selection if no-prompt is not used
        if not no_prompt:
            files = prompt_user_selection(files)

        # Combine wordlists and write to output
        combined_wordlist = combine_wordlists(files)
        unique_wordlist, duplicates_removed = remove_duplicates(combined_wordlist)
        write_output(output_file, unique_wordlist)

        print(f"Duplicates removed: {duplicates_removed}")
        print(f"Total unique words: {len(unique_wordlist)}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
