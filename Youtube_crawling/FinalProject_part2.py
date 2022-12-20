import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from operator import add

text_neck = pd.read_csv("./data/거북목.csv")
round_shoulder = pd.read_csv("./data/라운드숄더.csv")
back_pain = pd.read_csv("./data/허리 통증.csv")

# Use the statistics of diseases
stat_text_neck = [2050633, 2111697, 2241679, 2216519, 2387401]
stat_round_shoulder = [938964, 962912, 1014185, 973574, 993477]
stat_back_pain = [1951257,1978525,2063806,1952061,1975853]

# print(len(text_neck))
# print(text_neck.to_string())
translation_table = dict.fromkeys(map(ord, '[]"()/|｜#'), ' ')
translation_table[ord('!')] = ''
translation_table[ord('?')] = ''

text_neck['title'] = text_neck['title'].apply(lambda x: x.translate(translation_table))
text_neck['title'] = text_neck['title'].apply(lambda x: x.split())
text_neck['upload_date'] = text_neck['upload_date'].apply(lambda x: x.replace('스트리밍 시간: ', ''))

round_shoulder['title'] = round_shoulder['title'].apply(lambda x: x.translate(translation_table))
round_shoulder['title'] = round_shoulder['title'].apply(lambda x: x.split())
round_shoulder['upload_date'] = round_shoulder['upload_date'].apply(lambda x: x.replace('스트리밍 시간: ', ''))

back_pain['title'] = back_pain['title'].apply(lambda x: x.translate(translation_table))
back_pain['title'] = back_pain['title'].apply(lambda x: x.split())
back_pain['upload_date'] = back_pain['upload_date'].apply(lambda x: x.replace('스트리밍 시간: ', ''))


# print(text_neck.iloc[0].to_string())

text_neck = text_neck.drop(columns=["Unnamed: 0"])
round_shoulder = round_shoulder.drop(columns=["Unnamed: 0"])
back_pain = back_pain.drop(columns=["Unnamed: 0"])


remove_table_tn = ["아는형님", "짐승친구들", "두턱", "병맛노래", "반려동물", "작살", "키우기", "짤툰", "Vlog", "TURTLE", "Bengal", "자는", "귀여운"]
remove_table_rs = []
remove_table_bp = ["하복부", "복근", "데드리프트"]

# print('아는형님' in text_neck.iloc[1].title)
# print(list(text_neck.iloc[3].title)[0])

# text_neck = text_neck[text_neck['title'].apply(lambda x: remove_table_tn[0] not in x)].head(10)
# print(text_neck.head(10))

for word in remove_table_tn:
    # print(text_neck[text_neck['title'].apply(lambda x: word in x)].to_string())
    text_neck = text_neck[text_neck['title'].apply(lambda x: word not in x)]

for word in remove_table_rs:
    # print(text_neck[text_neck['title'].apply(lambda x: word in x)].to_string())
    round_shoulder = round_shoulder[round_shoulder['title'].apply(lambda x: word not in x)]

for word in remove_table_bp:
    # print(text_neck[text_neck['title'].apply(lambda x: word in x)].to_string())
    back_pain = back_pain[back_pain['title'].apply(lambda x: word not in x)]
    

# Check the shape of data
text_neck.to_csv('after_remove.csv')

tn_transition = []
rs_transition = []
bp_transition = []

years = ['8년','7년','6년', '5년', '4년', '3년', '2년', '1년', '개월', '주', '일', '시간']
for year in years:
    tn_transition.append(len(text_neck[text_neck['upload_date'].apply(lambda x: year in x)]))
    rs_transition.append(len(round_shoulder[round_shoulder['upload_date'].apply(lambda x: year in x)]))
    bp_transition.append(len(back_pain[back_pain['upload_date'].apply(lambda x: year in x)]))
    
    # if year == years[0]:
    #     print(text_neck[text_neck['upload_date'].apply(lambda x: year in x)])


# print the number of videos per year
in_year_tn = 0
in_year_rs = 0
in_year_bp = 0

for i in range(4):
    in_year_tn += tn_transition.pop()
    in_year_rs += rs_transition.pop()
    in_year_bp += bp_transition.pop()
    
tn_transition.append(in_year_tn)
rs_transition.append(in_year_rs)
bp_transition.append(in_year_bp)

yrs = ["2017", "2018", "2019", "2020", "2021", "2022"]

fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)

line1, = ax1.plot(yrs, tn_transition[3:], color = 'red')
line2, = ax2.plot(yrs, rs_transition[3:], color = 'green')
line3, = ax3.plot(yrs, bp_transition[3:], color='blue')

ax1.legend([line1], ['Text neck'])
ax2.legend([line2], ['Round shoulder'])
ax3.legend([line3], ['Back pain'])

ax1.set_ylabel('Number of Videos')
ax2.set_ylabel('Number of Videos')
ax3.set_ylabel('Number of Videos')

ax1_s = ax1.twinx()
ax2_s = ax2.twinx()
ax3_s = ax3.twinx()
line_1, = ax1_s.plot(yrs[:5], stat_text_neck, color = 'red', linestyle = '--')
line_2, = ax2_s.plot(yrs[:5], stat_round_shoulder, color = 'green', linestyle = '--')
line_3, = ax3_s.plot(yrs[:5], stat_back_pain, color = 'blue', linestyle = '--')

ax1_s.legend([line_1], ['Stats Text neck'])
ax2_s.legend([line_2], ['Stats Round shoulder'])
ax3_s.legend([line_3], ['Stats Back pain'])

ax1_s.set_ylabel('Number of Patients')
ax2_s.set_ylabel('Number of Patients')
ax3_s.set_ylabel('Number of Patients')

plt.show()

# 조회수 상위 50개의 동영상의 코로나 이전과 이후 수 비교(2년전까지 vs 나머지)
rank50_tn = text_neck.head(50)
rank50_rs = round_shoulder.head(50)
rank50_bp = back_pain.head(50)

corona_tn = 0
corona_rs = 0
corona_bp = 0
corona_years = ['2년', '1년', '개월', '주', '일', '시간']
for year in corona_years:
    corona_tn += len(rank50_tn[rank50_tn['upload_date'].apply(lambda x: year in x)])
    corona_rs += len(rank50_rs[rank50_rs['upload_date'].apply(lambda x: year in x)])
    corona_bp += len(rank50_bp[rank50_bp['upload_date'].apply(lambda x: year in x)])

print(corona_bp)

# Plot bar graph
disease_name = ["Text Neck", "Round Shoulder", "Back Pain"]
bar_width = 0.4
before_data = [50 - corona_tn, 50 - corona_rs, 50 - corona_bp]
after_data = [corona_tn, corona_rs, corona_bp]
index = np.arange(len(disease_name))

plt.bar(index, before_data, color = 'r', align='edge', width=bar_width, label='before')
plt.bar(index+bar_width, after_data, color = 'b', align = 'edge', width=bar_width, label='after')
plt.xticks(index + bar_width, disease_name)
plt.legend()
plt.ylabel('Number of related videos')
plt.show()

# 댓글 분석
comment_tn = []
comment_tn.append(pd.read_csv('./data_comment/거북목/거북목 교정 루틴.csv',lineterminator='\n'))
comment_tn.append(pd.read_csv('./data_comment/거북목/거북목 일자목 교정 영상.csv', lineterminator='\n'))
comment_tn.append(pd.read_csv('./data_comment/거북목/목 어깨 통증 완화를 위한.csv', lineterminator='\n'))
comment_tn.append(pd.read_csv('./data_comment/거북목/예쁜 일자 어깨.csv', lineterminator='\n'))
comment_tn.append(pd.read_csv('./data_comment/거북목/거북목 교정! 화제의 200만뷰! .csv', lineterminator='\n'))

comment_rs = []
comment_rs.append(pd.read_csv('./data_comment/라운드숄더/50만명이 효과를 본 라운드숄더 교정루틴 A (by 호주물리치료사).csv',lineterminator='\n'))
comment_rs.append(pd.read_csv('./data_comment/라운드숄더/거북목(Forward Head) & 라운드숄더(Round Shoulder) 교정 방법.csv', lineterminator='\n'))
comment_rs.append(pd.read_csv('./data_comment/라운드숄더/굽은등,라운드숄더? 이 스트레칭은 정말 엄청 시원합니다..csv', lineterminator='\n'))
comment_rs.append(pd.read_csv('./data_comment/라운드숄더/굽은어깨 교정, 어깨비대칭, 오십견예방, 어깨결림 스트레칭!.csv',lineterminator='\n'))
comment_rs.append(pd.read_csv('./data_comment/라운드숄더/한 번만 해도 바로 효과보는 승모근, 어깨스트레칭 ! 라운드숄더 교정.csv', lineterminator='\n'))

comment_bp = []
comment_bp.append(pd.read_csv('./data_comment/허리 통증/건강한 척추를 위한 요가.csv',lineterminator='\n'))
comment_bp.append(pd.read_csv('./data_comment/허리 통증/골반교정 허리통증에 직방! .csv', lineterminator='\n'))
comment_bp.append(pd.read_csv('./data_comment/허리 통증/허리 좋아지는 스트레칭 BEST모음.csv', lineterminator='\n'))
comment_bp.append(pd.read_csv('./data_comment/허리 통증/허리 통증 완화 복근운동.csv',lineterminator='\n'))
comment_bp.append(pd.read_csv('./data_comment/허리 통증/허리통증의 진단과 치료.csv', lineterminator='\n'))

for i in range(len(comment_tn)):
    comment_tn[i]['댓글 시간'] = comment_tn[i]['댓글 시간'].apply(lambda x: x.replace('스트리밍 시간: ', ''))
    comment_tn[i]['댓글 시간'] = comment_tn[i]['댓글 시간'].apply(lambda x: x.replace('(수정됨)', ''))
    
    comment_rs[i]['댓글 시간'] = comment_rs[i]['댓글 시간'].apply(lambda x: x.replace('스트리밍 시간: ', ''))
    comment_rs[i]['댓글 시간'] = comment_rs[i]['댓글 시간'].apply(lambda x: x.replace('(수정됨)', ''))

    comment_bp[i]['댓글 시간'] = comment_bp[i]['댓글 시간'].apply(lambda x: x.replace('스트리밍 시간: ', ''))
    comment_bp[i]['댓글 시간'] = comment_bp[i]['댓글 시간'].apply(lambda x: x.replace('(수정됨)', ''))

tn_comment_transition = []
rs_comment_transition = []
bp_comment_transition = []

years = ['5년', '4년', '3년', '2년', '1년', '개월', '주', '일', '시간']
for i in range(len(comment_tn)):
    num_tn = []
    num_rs = []
    num_bp = []
    
    cmt_tn = comment_tn[i]
    cmt_rs = comment_rs[i]
    cmt_bp = comment_bp[i]
    
    for year in years:
        num_tn.append(len(cmt_tn[cmt_tn['댓글 시간'].apply(lambda x: year in x)]))
        num_rs.append(len(cmt_rs[cmt_rs['댓글 시간'].apply(lambda x: year in x)]))
        num_bp.append(len(cmt_bp[cmt_bp['댓글 시간'].apply(lambda x: year in x)]))
    
    tn_comment_transition.append(num_tn)
    rs_comment_transition.append(num_rs)
    bp_comment_transition.append(num_bp)

# print the number of videos per year
in_year_tn = 0
in_year_rs = 0
in_year_bp = 0

for i in range(5):
    for _ in range(4):
        in_year_tn += tn_comment_transition[i].pop()
        in_year_rs += rs_comment_transition[i].pop()
        in_year_bp += bp_comment_transition[i].pop()
    
    tn_comment_transition[i].append(in_year_tn)
    rs_comment_transition[i].append(in_year_rs)
    bp_comment_transition[i].append(in_year_bp)

label = ["2017", "2018", "2019", "2020", "2021", "2022"]

tn_avg_transition = []
rs_avg_transition = []
bp_avg_transition = []

tn_temp = [0]*6
rs_temp = [0]*6
bp_temp = [0]*6

for i in range(5):

    tn_temp = list(map(add, tn_temp, tn_comment_transition[i]))
    rs_temp = list(map(add, rs_temp, rs_comment_transition[i]))
    bp_temp = list(map(add, bp_temp, bp_comment_transition[i]))
    
tn_new = [x / 5 for x in tn_temp]
rs_new = [x / 5 for x in rs_temp]
bp_new = [x / 5 for x in bp_temp]

fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)

line1, = ax1.plot(label, tn_new, color = 'red')
line2, = ax2.plot(label, rs_new, color = 'green')
line3, = ax3.plot(label, bp_new, color='blue')

ax1.legend([line1], ['Text neck'])
ax2.legend([line2], ['Round shoulder'], loc='upper left')
ax3.legend([line3], ['Back pain'],)

ax1.set_ylabel('Number of Comments')
ax2.set_ylabel('Number of Comments')
ax3.set_ylabel('Number of Comments')

ax1_s = ax1.twinx()
ax2_s = ax2.twinx()
ax3_s = ax3.twinx()
line_1, = ax1_s.plot(yrs[:5], stat_text_neck, color = 'red', linestyle = '--')
line_2, = ax2_s.plot(yrs[:5], stat_round_shoulder, color = 'green', linestyle = '--')
line_3, = ax3_s.plot(yrs[:5], stat_back_pain, color = 'blue', linestyle = '--')

ax1_s.legend([line_1], ['Stats Text neck'])
ax2_s.legend([line_2], ['Stats Round shoulder'])
ax3_s.legend([line_3], ['Stats Back pain'])

ax1_s.set_ylabel('Number of Patients')
ax2_s.set_ylabel('Number of Patients')
ax3_s.set_ylabel('Number of Patients')

plt.show()