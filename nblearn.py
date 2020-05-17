# the file is a local file in the Naive_Bayes project
import sys
from collections import Counter
from math import log10
import json
import read_files_words


text_files = read_files_words.search_files(directory=sys.argv[1], extension="*.txt")
ham_files, spam_files = read_files_words.get_files(text_files, "train")
total_emails = ham_files + spam_files

# # 10% data
# less_ham_files, less_spam_files = read_files_words.get_files(text_files, "less_data")
# ten_percent_data = less_ham_files + less_spam_files


# returns the files with words in ham or spam in a list
def all_words_in_class(class_type, data):  # class_type is either ham or spam
    # default runs in this clause
    if data == "all":
        # print("nothing")
        all_words_in_lists = []
        if class_type == "ham":
            type_files = ham_files
        else:
            type_files = spam_files
        for line in type_files:
            with open(line, 'r', encoding='latin1') as file:
                words = file.read().split()
                all_words_in_lists.append(words)
        all_words = [str(word).lower() for list_of_words in all_words_in_lists for word in list_of_words]
    # # for 10% data
    # else:
    #     less_data_in_lists = []
    #     if class_type == "ham":
    #         less_type_files = less_ham_files
    #     else:
    #         less_type_files = less_spam_files
    #     for l in less_type_files:
    #         with open(l, 'r', encoding='latin1') as file:
    #             w = file.read().split()
    #             less_data_in_lists.append(w)
    #     all_words = [str(w).lower() for list_of_words in less_data_in_lists for w in list_of_words]
    return all_words
# output of above class: [word, word, word]


# calculates the probability of the class- ham or spam
def probability_of_class(word, data):
    # default runs in this clause
    if data == "all":
        if word == "ham":
            num_class_type = len(ham_files)
        else:
            num_class_type = len(spam_files)
        prob_class_type = log10(num_class_type/len(total_emails))
        return prob_class_type
    # 10% of data
    # else:
    #     if word == "ham":
    #         num_class_type = len(less_ham_files)
    #     else:
    #         num_class_type = len(less_spam_files)
    #     prob_class_type = log10(num_class_type/len(ten_percent_data))
    #     return prob_class_type
# returns P(spam) or P(ham) depending on what it was invoked for


words_in_spam = all_words_in_class("spam", "all")
words_in_ham = all_words_in_class("ham", "all")


# # 10% data
# words_in_spam = all_words_in_class("spam", "less")
# words_in_ham = all_words_in_class("ham", "less")

all_words_in_data = words_in_spam + words_in_ham
unique_words_in_data = set(all_words_in_data)

word_occurrence_in_spam = Counter(words_in_spam)
word_occurrence_in_ham = Counter(words_in_ham)

prob_of_word_in_spam = dict()
prob_of_word_in_ham = dict()


def cal_probability(class_type, w):
    if class_type == "ham":
        count_word = word_occurrence_in_ham[w] + 1
        p_word_ham = count_word / (len(words_in_ham) + len(unique_words_in_data))
        return log10(p_word_ham)
    else:
        count_word = word_occurrence_in_spam[w] + 1
        p_word_spam = count_word / (len(words_in_spam) + len(unique_words_in_data))
        return log10(p_word_spam)


for word in unique_words_in_data:
    prob_of_word_in_ham[word] = cal_probability("ham", word)
    prob_of_word_in_spam[word] = cal_probability("spam", word)


# function that generates a nbmodel.txt file. Output file is ordered as - P(spam), P(ham), P(word|spam),P(word|ham)
def output():
    p_spam = probability_of_class("spam", "all")
    p_ham = probability_of_class("ham", "all")

    # # 10% data
    # p_spam = probability_of_class("spam", "less")
    # p_ham = probability_of_class("ham", "less")

    prob = {"P(spam)": str(p_spam), "P(ham)": str(p_ham)}
    with open("nbmodel.txt", "w") as file:
        file.write(json.dumps(prob))
        file.write("\n")
        file.write(json.dumps(prob_of_word_in_spam))
        file.write("\n")
        file.write(json.dumps(prob_of_word_in_ham))
    return "Complete"


# calling the output() to create the file nbmodel.txt
print(output())
