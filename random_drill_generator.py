import pandas as pd
from collections import namedtuple
from itertools import permutations
import random
from random import sample

def pref_to_rank(pref):
    return {
        a: {b: idx for idx, b in enumerate(a_pref)}
        for a, a_pref in pref.items()
    }


Pair = namedtuple("Pair", ["student", "hospital"])

def stable_matching_bf(
        *, students, hospitals, student_pref, hospital_pref
):
    """Solve the 'Stable Matching' problem using brute force.

    students -- set[str]. Set of students.
    hospitals -- set[str]. Set of hospitals.
    student_pref -- dict[str, list[str]]. Student preferences.
    hospital_pref -- dict[str, list[str]]. Hospital preferences.
    """
    s_rank = pref_to_rank(student_pref)
    f_rank = pref_to_rank(hospital_pref)
    #
    s_seq = tuple(students)
    perm = permutations(s_seq)
    list_s_seq=[]
    for item in list(perm):
        list_s_seq.append(item)
    rnd = random.randint(0, len(list_s_seq)-1)
    s_seq=list_s_seq[rnd]
    matchings = (
        [
            Pair(student=s, hospital=f)
            for s, f in zip(s_seq, f_seq)
        ]
        for f_seq in permutations(hospitals)
    )
    flag=True
    for matching in matchings:
        if flag:
            first_pair=matching
            flag=False
        match_s = {pair.student: pair for pair in matching}
        match_f = {pair.hospital: pair for pair in matching}
        unstable1 = (
            (
                    s_rank[s][f] < s_rank[s][match_s[s].hospital] and
                    f_rank[f][s] < f_rank[f][match_f[f].student]
            )
            for s in students
            for f in hospitals
            if s != match_f[f].student
            if f != match_s[s].hospital
        )
        unstable= any(unstable1)
        list_s_seq1 = []
        for item in list(unstable1):
            list_s_seq1.append(item)
        #print(list_s_seq1)
        unstb=not any(list_s_seq1)
        if not unstable:
            return [matching,first_pair]
        elif unstb:
            #print("unstable_matches: ",matching)
            pass

hospitals={"X", "Y", "Z","W", "V"}
students={"A", "B", "C","D","E"}
l_hospitals=list(hospitals)
l_students=list(students)
hospitals_perms = [''.join(p) for p in permutations(l_hospitals)]
students_perms = [''.join(p) for p in permutations(l_students)]

samples_h=sample(range(0,len(hospitals_perms)), 5)
samples_s=sample(range(0,len(students_perms)), 5)
test=list(students_perms[samples_s[0]])
hospital_pref={
    "X": list(students_perms[samples_s[0]]),
    "Y": list(students_perms[samples_s[1]]),
    "Z": list(students_perms[samples_s[2]]),
    "W": list(students_perms[samples_s[3]]),
    "V": list(students_perms[samples_s[4]]),
}
student_pref={
    "A": list(hospitals_perms[samples_h[0]]),
    "B": list(hospitals_perms[samples_h[1]]),
    "C": list(hospitals_perms[samples_h[2]]),
    "D": list(hospitals_perms[samples_h[3]]),
    "E": list(hospitals_perms[samples_h[4]]),

}
flag=True
flag_match=True
unstables=[]
while flag:
    output=stable_matching_bf(
        hospitals=hospitals,
        students=students,
        hospital_pref=hospital_pref,
        student_pref=student_pref,
    )

    match_l=[]
    for item in output[0]:
        match_l.append(item.student+"-"+ item.hospital)
    match_p = []
    for item in output[1]:
        match_p.append(item.student+"-"+ item.hospital)
    unstables.extend(match_l)
    set_len=len(set(unstables))
    # if set_len>5:
    #     flag=False

    if flag_match:
        if len(list(set(match_l) & set(match_p)))==0:
            first_best_match=match_l
            flag_match=False

    if len(list(set(unstables) & set(match_p)))<1 and set_len>5:
        flag=False
        title=match_p
        #unstables=match_l



print(title)
print(set(unstables))
unstables=list(set(unstables))
samples_h=sample(range(0,4), 2)


stable=[]
l_hospitals=list(hospitals)
l_students=list(students)
stable.append(l_hospitals[samples_h[0]]+'-'+l_hospitals[samples_h[1]])
stable.append(l_students[samples_h[0]]+'-'+l_students[samples_h[1]])

flag=True
while flag:
    rnd1 = random.randint(0, 4)
    rnd2 = random.randint(0, 4)
    pair=l_students[rnd1]+'-'+l_hospitals[rnd2]
    title_unstables=title+unstables
    if pair in title_unstables :
        pass
    else:
        flag=False
        stable.append(pair)

flag=True
while flag:
    first=str(l_students[random.randint(0, 4)])
    pair=first + '-' + student_pref[first][4]
    title_unstables=title_unstables+stable
    if pair in title_unstables :
        pass
    else:
        flag=False
        stable.append(pair)

print(stable)

csv_file = pd.read_csv("drill.csv", header=None)
data=csv_file
question=data[1][5]
text=''
for item in title:
    text=text+str(item)+', '
text=text[:-2]
text1=''
for key, value in student_pref.items():
    text1=text1+ str(key)+":"
    for item in value:
        text1=text1 + item+','
    text1=text1+ '<br />'
text2=''
for key, value in hospital_pref.items():
    text2=text2+ str(key)+":"
    for item in value:
        text2=text2 + item+','
    text2=text2+ '<br />'
new_question="<p>Consider an instance of Stable Matching with the following preference lists. Suppose that the matching is " \
             + '{'+ text + '}' + ". Select<strong> all</strong> pairs that are unstable with respect to this matching.</p>" \
            + "<p>" + text1 + "</p>" + "<p>" + text2 +"</p>"

data[1][5]=new_question

samples_unstables=sample(range(0,4), 4)
samples_question_uns=sample(range(9,15), 4)
data[2][samples_question_uns[0]]=first_best_match[samples_unstables[0]]
data[2][samples_question_uns[1]]=first_best_match[samples_unstables[1]]
data[2][samples_question_uns[2]]=first_best_match[samples_unstables[2]]
data[2][samples_question_uns[3]]=first_best_match[samples_unstables[3]]

data[1][samples_question_uns[0]]=1
data[1][samples_question_uns[1]]=1
data[1][samples_question_uns[2]]=1
data[1][samples_question_uns[3]]=1

data[4][samples_question_uns[0]]="Unstable: both prefer each other to their match"
data[4][samples_question_uns[1]]="Unstable: both prefer each other to their match"
data[4][samples_question_uns[2]]="Unstable: both prefer each other to their match"
data[4][samples_question_uns[3]]="Unstable: both prefer each other to their match"

diff = list(set([9,10,11,12,13,14,15]) - set(samples_question_uns))

data[2][diff[0]]=stable[random.randint(0, 1)]
data[1][diff[0]]=0
data[4][diff[0]]="Every pair should consist of one hospital and one student"


data[2][diff[1]]=stable[2]
data[1][diff[1]]=0
data[4][diff[1]]="A pair in a matching is always stable"

data[2][diff[2]]=stable[3]
data[1][diff[2]]=0
data[4][diff[2]]="Stable: the hospital would not want to switch"

data.to_csv("2_new.csv",index=False,header=None)
