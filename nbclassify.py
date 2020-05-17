import json
import read_files_words
import sys


text_files = read_files_words.search_files(directory=sys.argv[1], extension="*.txt")
open('nboutputE.txt', 'w').close()
ham_files, spam_files = read_files_words.get_files(text_files, "dev")
total_files = ham_files + spam_files


def get_emails():
    all_emails = dict()
    for file in total_files:
        with open(file, 'r', encoding='latin1') as f:
            emails = f.read().split()
        all_emails[file] = [word.lower() for word in emails]
    return all_emails


# function to calculate if a message is spam or not
def spam_or_ham():

    with open("nbmodelE.txt", "r") as f:
        probabilities = [json.loads(line) for line in f]

    p_spam_ham = probabilities[0]
    p_spam = float(p_spam_ham["P(spam)"])
    p_ham = float(p_spam_ham["P(ham)"])
    p_words_spam = probabilities[1]
    p_words_ham = probabilities[2]

    all_emails = get_emails()
    for path in all_emails:
        p_message_spam = 0
        p_message_ham = 0
        for word in all_emails[path]:
            if (word not in p_words_ham) and (word not in p_words_spam):
                continue
            else:
                p_message_spam = float(p_words_spam[word]) + p_message_spam
                p_message_ham = float(p_words_ham[word]) + p_message_ham
        ham = p_message_ham + p_ham
        spam = p_message_spam + p_spam

        if ham > spam:
            with open('nboutputE.txt', 'a') as f:
                output = ["ham\t", path, "\n"]
                f.writelines(output)

        elif spam > ham:
            with open('nboutputE.txt', 'a') as f:
                output = ["spam\t", path, "\n"]
                f.writelines(output)

        else:
            with open('nboutputE.txt', 'a') as f:
                output = ["spam\t", path, "\n"]
                f.writelines(output)

    return "Complete"


print(spam_or_ham())
