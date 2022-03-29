"""Count the words in a certain text.

Steps for use:
1) Open this folder in a terminal (or open a terminal in your code editor of choice after cloning this repository).
2) Change the two file paths immediately below this docstring as necessary.
3) Run `pip install -r requirements.txt`
4) Run `python -m simple_word_counter`
5) Save the resulting visualization, if desired.
"""
# Change these file paths as necessary.
INPUT_FILE_PATH: str = "sample.txt"
OUTPUT_FILE_PATH: str = "outputData.txt"
# End edit


import nltk
from nltk.corpus import stopwords

## Add ssl to requirements.txt, reinstall requirements, and uncomment the following 7 lines if nltk download does not work.
# import ssl
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
nltk.download('punkt')
from matplotlib import pyplot
import operator


READ_MODE = "r"


def main() -> None:
    """Entrypoint to our program."""
    number_words_wanted: int = int(input("How many words do you want charted? "))
    all_word_counts: dict[str, int] = read_character_data(INPUT_FILE_PATH)
    top_word_counts: dict[str, int] = find_top_word_counts(all_word_counts, number_words_wanted)
    write_data_to_file(top_word_counts)
    chart_data(top_word_counts, number_words_wanted)


def read_character_data(file: str) -> dict[str, int]:
    """Given a filename, read its contents and count its characters."""
    counts: dict[str, int] = {}
    file_handle = open(file, READ_MODE, encoding='utf-8')
    for line in file_handle:
        line = line.lower()
        current_word: str = ""
        for char in line:
            if (char != " ") and char.isalpha():
                current_word += char
            else:
                if current_word in counts:
                    counts[current_word] += 1
                elif (current_word not in stopwords.words('english')) and (current_word != ""):
                    counts[current_word] = 1
                current_word = ""
    file_handle.close()  # Done working with file, close it!
    print("Total Unique Words Found: " + str(len(counts)))
    return counts


def find_top_word_counts(complete_dictionary: dict[str, int], bars_wanted: int) -> dict[str, int]:
    """Return a dictionary with only the key-value pairs for words with the most hits.
    
    Length of returned dictionary is specified in arguments.
    """
    results: dict[str, int] = {}
    alphabetized_complete = dict(sorted(complete_dictionary.items(), key=operator.itemgetter(0)))
    sort_counts_complete = dict(sorted(alphabetized_complete.items(), key=operator.itemgetter(1),reverse=True))
    all_words: list[int] = list(sort_counts_complete.keys())
    all_counts: list[int] = list(sort_counts_complete.values())
    i: int = 0
    if bars_wanted > len(all_words):
        bars_wanted = len(all_words)
    while (i < bars_wanted):
        results[all_words[i]] = all_counts[i]
        i += 1
    return results


def write_data_to_file(data: dict[str, int]) -> None:
    """Write data to txt file."""
    outF = open(OUTPUT_FILE_PATH, "w")
    for item in data:
        outF.write(item + ": " + str(data[item]))
        outF.write("\n")
    outF.close()


def chart_data(word_counts: dict[str, int], bars_wanted: int) -> None:
    """Plot the results of our textual analysis."""
    pyplot.title("Counts of the Top " + str(bars_wanted) + " Words in " + INPUT_FILE_PATH)
    pyplot.xlabel("Count")
    pyplot.ylabel("Words")
    labels: list[str] = list(word_counts.keys())
    values: list[int] = list(word_counts.values())
    barchart = pyplot.barh(labels, values)
    pyplot.gca().invert_yaxis()
    for rect in barchart:
        width = rect.get_width()
        pyplot.annotate('{}'.format(width),
                    xy=(width, (rect.get_y() + rect.get_height())),
                    xytext=(12, 0),  # 12 points horizontal offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    # pyplot.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
    pyplot.show()


if __name__ == "__main__":
    main()