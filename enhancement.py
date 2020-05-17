# any enhancement tried?
# removing the word "Subject:" since it appears in all the emails: same result as with 100% data.
# Trying with Laplacian smoothing : same as with add-1 smoothing
# Trying using Lidstone and Jeffreys-Perks law : lambda = 1/2

import sys
from collections import Counter
from math import log
import json
import read_files_words
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag


text_files = read_files_words.search_files(directory=sys.argv[1], extension="*.txt")
ham_files, spam_files = read_files_words.get_files(text_files, "train")
total_emails = ham_files + spam_files


# returns the files with words in ham or spam in a list
def all_words_in_class(class_type):  # class_type is either ham or spam
    all_words_in_lists = []
    if class_type == "ham":
        type_files = ham_files
    else:
        type_files = spam_files
    for line in type_files:
        with open(line, 'r', encoding='latin1') as file:
            words = file.read().split()
            for w in words:
                if not(w == "Subject:"):
                    all_words_in_lists.append(w)
    all_words = [str(word).lower() for word in all_words_in_lists]
    return all_words


# calculates the probability of the class- ham or spam
def probability_of_class(word):
    if word == "ham":
        num_class_type = len(ham_files)
    else:
        num_class_type = len(spam_files)
    prob_class_type = log(num_class_type/len(total_emails))
    return prob_class_type


words_in_spam = all_words_in_class("spam")
words_in_ham = all_words_in_class("ham")
all_words_in_data = words_in_spam + words_in_ham


unique_words_in_data = set(all_words_in_data)

word_occurrence_in_spam = Counter(words_in_spam)
word_occurrence_in_ham = Counter(words_in_ham)

prob_of_word_in_spam = dict()
prob_of_word_in_ham = dict()


# Laplacian smoothing
# Lidstone and Jeffreys-Perks law l = 1/2


lam = 0.5


def cal_probability(class_type, w):
    if class_type == "ham":
        count_word = word_occurrence_in_ham[w] + lam
        p_word_ham = count_word / (len(words_in_ham) + len(unique_words_in_data) * lam)
        return log(p_word_ham)
    else:
        count_word = word_occurrence_in_spam[w] + lam
        p_word_spam = count_word / (len(words_in_spam) + len(unique_words_in_data) * lam)
        return log(p_word_spam)


for word in unique_words_in_data:
    prob_of_word_in_ham[word] = cal_probability("ham", word)
    prob_of_word_in_spam[word] = cal_probability("spam", word)


# function that generates a nbmodelE.txt file. Output file is ordered as - P(spam), P(ham), P(word|spam),P(word|ham)
def output():
    p_words_in_spam = prob_of_word_in_spam
    p_words_in_ham = prob_of_word_in_ham
    p_spam = probability_of_class("spam")
    p_ham = probability_of_class("ham")
    prob = {"P(spam)": str(p_spam), "P(ham)": str(p_ham)}
    with open("nbmodelE.txt", "w") as file:
        file.write(json.dumps(prob))
        file.write("\n")
        file.write(json.dumps(p_words_in_spam))
        file.write("\n")
        file.write(json.dumps(p_words_in_ham))
    return "Complete"


# calling the output() to create the file nbmodel.txt
print(output())
