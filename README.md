# Wordlist Combiner

A smart and flexible command-line tool to search massive wordlist repositories based on keywords, and create smaller, focused wordlists.  
Ideal for penetration testers, bug bounty hunters, and CTF players looking to optimize scan times by using a targeted wordlist instead of scanning with full large sets.

---

## ✨ Features

- Search files or folders by partial string matching (e.g., "admin", "java", "cisco")
- Optionally case-sensitive search
- Folder-only search mode (include all files inside matching folders)
- Interactive selection or removal of matched files before combining
- Automatically remove duplicate entries and sort the output alphabetically
- Highlight matches with colorful output for easier review

---

## 🛠️ Requirements

- Python 3.x
- termcolor (`pip install termcolor`)

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/wordlist-subset-creator.git
cd wordlist-subset-creator
```
Install the required dependency:
```bash
pip install termcolor
```
---

## 📖 Usage
```bash
python wordlist_combiner.py -d <path_to_wordlists> -s <search_keywords> -o <output_file> [options]
Required arguments:
-d, --directory: Root directory containing the wordlists (e.g., path to SecLists).

-s, --search: Substring(s) to search for (comma-separated keywords).

-o, --output: Output filename for the combined wordlist.

Optional arguments:
--folders-only: Search only inside folder names (not filenames).

--case-sensitive: Enable case-sensitive matching.

--no-prompt: Automatically include all matched files without asking for manual selection.
```
---

## 🎯 Example Scenarios
```bash
Extract admin-related wordlists for a directory brute-forcing attack:
python wordlist_combiner.py -d ./SecLists -s admin -o admin_wordlist.txt

Extract common passwords by searching for "common" and "password" inside filenames:
python wordlist_combiner.py -d ./SecLists -s common,password -o passwords_subset.txt

Search only inside folder names (e.g., find all wordlists under folders named "fuzzing"):
python wordlist_combiner.py -d ./SecLists -s fuzzing -o fuzzing_wordlist.txt --folders-only

Case-sensitive search if you want to differentiate "Admin" from "admin":
python wordlist_combiner.py -d ./SecLists -s Admin -o admin_case_sensitive.txt --case-sensitive
```
---

## ⚡ Why Use This?

Faster scans with a smaller, targeted wordlist

Avoid wasting time scanning irrelevant entries

Stay organized by creating keyword-specific wordlists

Especially useful when dealing with huge sets like SecLists, PayloadAllTheThings, etc.
