import pandas as pd
import nltk
from operator import add
import matplotlib.pyplot as plt
import numpy as np

total_rate = []
title = ['2번째', '3분만 늦었어도 큰일 났어요 버스기사 구한 시민들', '금메달리스트의 쓸쓸한 죽음...생활고에 고독사',
         '저수지 물 다 뺀 후에야 끝난 피라니아 소탕 작전', '화려했던 조폭 두목 조양은, 초라한 노년 ']

stats_depression = [680169, 751930, 796364, 837808, 910785]

for i in range(4):
    # NLP(Delete dirtyness in comment)
    comment = pd.read_csv('./data_comment/mental/' + title[i] + '.csv')

    translation_table = dict.fromkeys(map(ord, ',.?![]"()/|｜#^\n'), ' ')
    unnc_word = dict.fromkeys(map(ord, 'ㅋㅜ~-_ㅎㅠ:;ㅡㅇ'), ' ')

    # Remove NaN value
    comment = comment.fillna({'댓글 내용':''})
    comment['댓글 내용'] = comment['댓글 내용'].apply(lambda x: x.translate(translation_table))
    comment['댓글 내용'] = comment['댓글 내용'].apply(lambda x: x.translate(unnc_word))
    comment['댓글 내용'] = comment['댓글 내용'].apply(lambda x: nltk.word_tokenize(x))
    # comment['댓글 내용'] = comment['댓글 내용'].apply(lambda x: x.replace('\n', ' '))

    #comment.to_csv('./comment_처리.csv')

    # Check the absolutist words 
    absol = ['전적으로', '틀림없이', '전혀', '극도로', '굉장히', '절대', '전혀',
                    '모든', '최대한', '최대한의', '전부', '다', '모두', '완전히', '온통', '아주', '몹시', '너무'
                    '항상', '언제나', '늘', '언제든', '가능한', '최대의', '완벽한', '완전히', '전적으로', '계속', 
                    '변함없는', '거듭되는', '확실히', '분명히', '절대', '전부', '다', '언제나', '항상', '늘', '모든',
                    '가능한', '매', '모두', '전부', '모든 것', '가장', '제일', '젤', '가득한', '무조건', '무적권',
                    '해야', '설마', '절대', '한번도', '한 번도', '결코', '완전히', '전적으로', 'ㅈㄴ', 'ㅈㄴ게', '존나',
                    '자기만', '너만', '내가', '나', '나는', '나만', '내', '저는', '난']

    # Prepare
    comment['absol'] = [False]*len(comment)

    #comment.to_csv('./comment_처리.csv')
    comment_by_year = []

    years = ['8년','7년','6년', '5년', '4년', '3년', '2년', '1년', '개월', '주', '일', '시간']
    for year in years:
        comment_by_year.append(comment[comment['댓글 시간'].apply(lambda x: year in x)].copy())


    for com in comment_by_year:
        for item in absol: #for each item in absol list
            com['absol'] |= com['댓글 내용'].apply(lambda x: item in x)
        # print(comment['댓글 내용'].apply(lambda x: absol[0] in x))
    #  fdist = nltk.FreqDist(comment['댓글 내용'])

    # sum_l = 0
    rate_abs = []
    for com in comment_by_year:
        num_abs = com['absol'].value_counts().to_list()
        if len(num_abs) == 0 or len(num_abs) == 1:
            rate_abs.append([len(com), 0])
        else:
            rate_abs.append([len(com), num_abs[1]])

    num = [0, 0]
    for i in range(4):
        num = list(map(add, rate_abs.pop(), num))
    
    rate_abs.append(num)
    total_rate.append(rate_abs)

rate_avg = []
total_comment = []

for i in range(9):
    temp = [0,0]
    
    for elem in total_rate:
        temp = list(map(add, temp, elem[i]))
    
    if temp[0] == 0:
        rate_avg.append(0)
        total_comment.append(0)
    else:
        rate_avg.append(temp[1]/temp[0])
        total_comment.append(10 / temp[0])

label = ["2017", "2018", "2019", "2020", "2021"]

fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(1, 1, 1)
ax1_1 = ax1.twinx()


line1, = ax1.plot(label, rate_avg[3:8], color = 'purple')
line_1, = ax1_1.plot(label, stats_depression, color = 'green')
ax1.legend([line1], ['Ratio of absolute comments'])
ax1_1.legend([line_1], ['The number of depression pationts'])
ax1.set_ylabel('Ratio of absolute comments')
ax1_1.set_ylabel('The number of patients')

plt.show()

fig1 = plt.figure(figsize=(12, 8))
ax = fig1.add_subplot(1,1,1)
line = ax.plot(label,total_comment[3:8],color = 'blue', linestyle='--')
ax.legend([line], x['10 / Total comments'])
ax.set_ylabel('10 / Total comments')
plt.show()
# print(len(comment))
# print("sum: ", sum_l)


 
