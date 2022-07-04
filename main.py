from bs4 import BeautifulSoup
import time
# import numpy as np
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords
# import string
# from string import digits
# from math import log10

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

lemmatizer = WordNetLemmatizer()

# necessary variable declared
all_ques_a_leet = {}
all_ques_href = []
all_ques_title = []
url = "https://leetcode.com/problemset/algorithms/?page="
#
# # finding all the things what is inside an anker tag using their page url and storing it in a variable
for i in range(10):    # to store the questions in page 1
    driver.get(url+str(i))
    time.sleep(2)   # do this for 2 second or less
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # odd: bg - layer - 1
    # even: bg - overlay - 1
    # dark: odd:bg - dark - layer - bg
    # dark: even:bg - dark - fill - 4

    # all_ques_leet = soup.findAll("div", {"class": "odd:bg-layer-1 even:bg-overlay-1 dark:odd:bg-dark-layer-bgdark:even:bg-dark-fill-4"})

    all_ques_a_leet = (soup.findAll("a", {"class": "h-5 hover:text-primary-s dark:hover:text-dark-primary-s"}))
    for ques in all_ques_a_leet:
        urlp = url.replace('/problemset/algorithms/?page=', '')
        all_ques_href.append(urlp + ques["href"])
        all_ques_title.append(ques.text)
# # Now extracting the url and the title from the above declared variable
#

print(all_ques_href)
# # now writing those questions url in the file  "Leetcode_problems_link.txt"
with open("Leetcode_problems_link.txt", "w+") as f:
    f.write("\n".join(all_ques_href))

# # now writing those questions' titles in the file  "Leetcode_problems_title.txt"
with open("Leetcode_problems_title.txt", "w+") as f:
    f.write("\n".join(all_ques_title))

# now we will create the questions file in the present folder as it is not possible to create them in some other
# folder encounterung an error
valid = ['[', ']', '(', ')', '{', '}', '>', '<', '.', ' ', '\n', ",", ':', '=', '+', '-', '/', '*', '%', '^']
i = 0  # to limit the no. of questions we want to intake
f = open("Leetcode_problems_title.txt", "+r")
with open("Leetcode_problems_link.txt", "+r") as fp:
    for line in fp:
        if i > 50:
            driver.get(line)
            time.sleep(2)  # do this for 3 second or less
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            ques_text = soup.find("div", {"class": "content__u3I1 question-content__JfgR"}).get_text()
            # print(ques_text)

            title = "problem" + str(i) + ".txt"
            ques_text = str(ques_text)
            ques_text = ''.join(char for char in ques_text if char.isalnum() or char in valid)
            with open(title, "+w") as nm:
                nm.write(ques_text)
        i += 1
        if i == 501:
            break
f.close()

# Below is my tfidf implementation.
# Now we will create a new temp file for each problem.txt file which will have only the keyword of a particular problem
# text file that will be helpful when we need to get keywords for that problem and to know the no. of the keyword
# present in that problem which
# will helpful to calculate the tf matrix
# #
f = open("Leetcode_problems_title.txt", "+r")
stop_words = ["a", "an", "is", "the", "that", "they", "may", "if", "for", "return", "of", "that", "and", "are", "as", "or", "in", "", "such", "you"]

stop_words = stop_words + stopwords.words('english')
# _idf = dict()
n = []
key_words = dict()
fm = open("keywords.txt", "+w")
j = 0  # this j will store the total no. of keywords
# f.readline()

#  Lets we set the variable which will store the no. of document we gonnna read as nd
nd = 147
for i in range(1, nd):
    # title = f.readline()
    # title = title.replace(". ", "")#     # title = title.replace(" ", "_")
    # table = str.maketrans('', '', digits)
    # title = title.translate(table)
    # title.translate(None, digits)
    # title1 = title.strip() + "_imprv.txt"
    # title = title.strip() + ".txt"
    # lines = []
    title = "problem" + str(i) + ".txt"

    with open(title, 'r') as fp:
        lines = fp.readlines()
    with open("temp.txt", 'w') as fp:
        for number, line in enumerate(lines):
            if "Example" in line:
                # print(line)
                break
            else:
                # print(line)
                fp.write(line)
    text = open("temp.txt", "r")
    for line in text:
        line = line.strip()
        line = line.lower()
        line = line.translate(line.maketrans("", "", string.punctuation))

        words = line.split(" ")
        for word in words:
            if word not in stop_words:
                if word.isdecimal() is not True and word not in key_words:
                    # word = lemmatizer.lemmatize(word)
                    # if word == "given":
                    #     print("there is a keyword name given:")
                    key_words[word] = j
                    fm.write(word + ' ')
                    j += 1
    text.close()
    file = open("temp.txt", "rt")
    data = file.read()
    words = data.split()
    n.append(len(words))
    file.close()
# f.close()
fm.close()

# stop_words.append("given")
# now make tf matrix for every key_word
tfidr = [[0 for i in range(j)] for k in range(nd+1)]  # one extra raw to store the idr values for all the words
# f = open("Leetcode_problems_title.txt", "+r")
for i in range(1, nd):
    title = "problem" + str(i) + ".txt"
    with open(title, 'r') as fp:
        lines = fp.readlines()
    with open("temp.txt", 'w') as fp:
        for number, line in enumerate(lines):
            if "Example" in line:
                # print(line)
                break
            else:
                # print(line)
                fp.write(line)
    text = open("temp.txt", "r")
    for line in text:
        line = line.strip()
        line = line.lower()
        line = line.translate(line.maketrans("", "", string.punctuation))

        words = line.split(" ")

        for word in words:
            if word.isdecimal() is not True and word not in stop_words:
                ind = key_words[word]
                # ind =1
                tfidr[i][ind] += 1
    text.close()
    for k in range(j):
        # tfidr[i][k] /= n[i]
        tfidr[i][k] /= j
# f.close()

# Now we will go for making the idr array for each word in the last row of our tridr 2d array
for i in range(j):
    count = 0
    for k in range(nd):
        if tfidr[k][i] != 0:
            count += 1
    # if count != 0:
    tfidr[nd][i] = log10(nd / (count+1))
    # else:
    #     tfidr[nd][i] = 0

for i in range(nd):
    for k in range(j):
        tfidr[i][k] *= tfidr[nd][k]

# Now we will print the whole tfidr matrix
# for i in range(nd+1):
#     for k in range(j):
#         print(tfidr[i][k], end=' ')
#     print("\n")

print(j)
# Now I will show you all the key word in my file
# print(key_words.keys())

# Now we will make a file for our tfidr matrix

with open("tfidr.txt", "+w") as fm:
    for i in range(nd+1):
        for d in tfidr[i]:
            fm.write(f"{d} ")
        fm.write('\n')
