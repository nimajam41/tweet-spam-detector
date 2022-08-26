import csv

tweets = []
with open('ExtractedTweets.csv', mode='r', encoding="utf8") as file:
    all = csv.reader(file, delimiter=',')
    for x in all:
        tweets += [x]
train = []
test = []
r = 30
for i in range(1, len(tweets)):
    if i % 70 == r:
        test += [tweets[i]]
    else:
        train += [tweets[i]]
train_words = dict()
label_1 = []
label_0 = []
c = 0
for i in range(len(train)):
    tweet_words = train[i][1].lower().split(" ")
    for x in tweet_words:
        if x.startswith("http"):
            continue
        if x == ',' or x == '.' or x == '?' or x == ';' or x == '!':
            continue
        if x == "the" or x == "am" or x == "is" or x == "are" or x == "with" or x == "in" or x == "I" or x == "as" or \
                x == "of" or x == "to" or x == "that" or x == "this" or x == "on":
            continue
        if x.endswith(',') or x.endswith('?') or x.endswith(';') or x.endswith('!') or x.endswith('.'):
            x = x[0:len(x) - 1]
        if x.startswith('@') or x.startswith('#'):
            x = x[1:]
        if x not in train_words:
            train_words[x] = c
            label_1 += [1]
            label_0 += [1]
            c += 1
            if train[i][0] == '1':
                label_1[-1] += 1
            else:
                label_0[-1] += 1
        else:
            index = train_words.get(x)
            if train[i][0] == '1':
                label_1[index] += 1
            else:
                label_0[index] += 1
sum_of_label1 = sum(label_1)
sum_of_label0 = sum(label_0)

results = []
for t in test:
    if t[0] == '1':
        num = 1
    else:
        num = 0
    str = t[1]
    proper_words = []
    whole_words = str.lower().split(" ")
    for word in whole_words:
        if word.startswith("http"):
            continue
        if word == ',' or word == '.' or word == '?' or word == ';' or word == '!':
            continue
        if word == "the" or word == "am" or word == "is" or word == "are" or word == "with" or word == "in" or \
                word == "I" or word == "as" or word == "of" or word == "to" or word == "that" or word == "this" \
                or word == "on":
            continue
        if word.endswith(',') or word.endswith('?') or word.endswith(';') or word.endswith('!') or word.endswith('.'):
            word = word[0:len(word) - 1]
        if word.startswith('@') or word.startswith('#'):
            word = word[1:]
        proper_words += [word]
    p1 = 1
    p0 = 1
    for word in proper_words:
        if train_words.get(word):
            p1 *= (label_1[train_words.get(word)] / sum_of_label1)
            p0 *= (label_0[train_words.get(word)] / sum_of_label0)
        else:
            p1 *= (1 / sum_of_label1)
            p0 *= (1 / sum_of_label0)
    if p1 >= p0:
        res = 1
    else:
        res = 0
    if num == res:
        results += [1]
    else:
        results += [0]
print(f'accuracy is: {sum(results) / len(results)}')
