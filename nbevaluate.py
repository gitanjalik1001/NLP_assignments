# calculate precision, recall and F1 score
import re
import read_files_words
import sys


with open('nboutputE.txt', 'r') as f:
    data = f.read().split('\n')


# how many were classified
def count_guessed():
    g_spam = 0
    g_ham = 0
    for line in data:
        if re.search("spam\s", line):
            g_spam += 1
        elif re.search("ham\s", line):
            g_ham += 1
    return g_spam, g_ham


# how many we classified correctly
def actual_correct():
    c_spam = 0
    c_ham = 0
    for line in data:
        if re.search("spam\s", line) and re.search(".spam\.txt$", line):
            c_spam += 1
        if re.search("ham\s", line) and re.search(".ham\.txt$", line):
            c_ham += 1
    return c_spam, c_ham


def how_many_actually():
    text_files = read_files_words.search_files(directory=sys.argv[1], extension="*.txt")
    ham_files, spam_files = read_files_words.get_files(text_files, "dev")
    return len(spam_files), len(ham_files)


correct_spam = actual_correct()[0]
correct_ham = actual_correct()[1]

guessed_spam = count_guessed()[0]
guessed_ham = count_guessed()[1]

actual_spam = how_many_actually()[0]
actual_ham = how_many_actually()[1]

prec_spam = correct_spam/guessed_spam
prec_ham = correct_ham/guessed_ham

recall_spam = correct_spam/actual_spam
recall_ham = correct_ham/actual_ham

F1_spam = (2 * prec_spam * recall_spam)/(prec_spam + recall_spam)
F1_ham = (2 * prec_ham * recall_ham)/(prec_ham + recall_ham)

print("Precision of spam: ", prec_spam, "\n", "Precision of ham: ", prec_ham, "\n", "Recall of spam: ", recall_spam,
      "\n", "Recall of ham: ", recall_ham, "\n", "F1 score of Spam: ", F1_spam, "\n", "F1 score of Ham: ", F1_ham)
