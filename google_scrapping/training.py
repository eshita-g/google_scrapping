import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB


df1 = pd.read_csv("/home/thebrain-eshita/Documents/training.txt", sep=',').sample(n=301)

arr = zip(df1['n12'].values.tolist(), df1['n21'].values.tolist(), df1['p12'].values.tolist(), df1['p21'].values.tolist(), df1['a12'].values.tolist(), df1['a21'].values.tolist(), df1['bin'].values.tolist())
# print(arr)

list1 = []
for i in arr:
    list1.append(list(i))

train_x = [i[:6] for i in list1[:300]]
# print(train_x)
train_y = [i[6] for i in list1[:300]]
# print(train_y)

test_x = [i[:6] for i in list1[300:]]
test_y = [i[6] for i in list1[300:]]


classifier = SVC()
classifier2 = DecisionTreeClassifier()
classifier3 = BernoulliNB()
classifier4 = GaussianNB()


classifier.fit(train_x, train_y)
classifier2.fit(train_x, train_y)
classifier3.fit(train_x, train_y)
classifier4.fit(train_x, train_y)


prediction = classifier.predict(test_x)
prediction2 = classifier2.predict(test_x)
prediction3 = classifier3.predict(test_x)
prediction4 = classifier4.predict(test_x)


score1 = accuracy_score(test_y, prediction)
score2 = accuracy_score(test_y, prediction2)
score3 = accuracy_score(test_y, prediction3)
score4 = accuracy_score(test_y, prediction4)

score1 = score1*100
print(str(test_y).replace(',', ''))
print(prediction)
print(prediction2)
print(prediction3)
print(prediction4)
print(score1, score2, score3, score4)