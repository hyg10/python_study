# path : pandas_test1.py

import numpy as np
import pandas as pd

# pandas 는 데이터 분석을 위한 Series(class) 와 DataFrame 을 준비하기 위해 사용하는 패키지(모듈)
# Series (시리즈) : numpy 의 1차원배열(벡터) 또는 리스트에 인덱스 라벨을 추가 지정한 것


# 1. Series 객체 생성 
# 예 : 각 도시의 2025년 인구 데이터를 시리즈로 만든다면 
s = pd.Series([123456784, 5437689, 3445433, 2803088], index=['서울', '부산', '인천', '대구'])
print(s)

'''
서울    123456784
부산      5437689
인천      3445433
대구      2803088
'''

# Series 객체 생성시, 인덱스 라벨을 생략할 수 있음
# 자동으로 0으로 시작하는 정수가 인덱스 라벨로 표시됨
print(pd.Series(range(10)))

# 2. DataFrame (데이터프레임 : 표 -2차원배열(행렬, 매트릭스)) 만들기
# 변수 = pd.DataFrame(행렬 | 행렬변수 | 사전자료형변수, index=행인덱스라벨, columns=열인덱스라벨)
data = {
    '2022': [123446784, 5436689, 3444433, 2843088],
    '2023': [123436784, 5435689, 3443433, 2833088],
    '2024': [123426784, 5434689, 3442433, 2823088],
    '2025': [123416784, 5433689, 3441433, 2813088],
    '지역': ['수도권', '경상권', '수도권', '경상권'],
    '2015~2019 증가율':[0.0283, 0.0305, 0.0442, 0.0512]
} # dict 사전자료형

print(type(data)) # <class, 'dict'>
print(data)

# 사전(dict) 자료에 저장된 값에 대해 컬럼 나열 순서를 재배치하려 할 때 DataFrame 이용할 수 있음
# 예 : 가로 한 줄로 출력되 것을 표(table) 형태로 만들고자 한다면, 컬럼 라벨(위쪽에 가로로 표시)을 준비함
columns_lbl = ['지역', '2022', '2023', '2024', '2025', '2015~2019 증가율']
# 인덱스 라벨(행라벨, 왼쪽에 세로로 표시) 준비함 
index_lbl = ['서울', '부산', '인천', '대구']

df = pd.DataFrame(data, columns=columns_lbl, index=index_lbl)
# 사전 자료형의 key가 컬럼인덱스 라벨과 매칭되는 순서로 재배치됨
print(df)

# DataFrame 생성시 columns 라벨을 생략하면, 사전의 데이터 구성 순서대로 프레임 구성됨
df2 = pd.DataFrame(data, index=index_lbl)
print(df2)

# DataFrame 생성시 행과 열 인덱스 라벨 모두 생략할 수도 있음
df3 = pd.DataFrame(np.arange(12).reshape(3, 4))
print(df3)

# 데이터 파일 입출력 기능 제공함 
# 파일에 저장(출력) : 데이터프레임.to_파일종류
# df.to_csv('test.csv', mode='w', sep=',')

# 파일 읽어와서 DataFrame 에 저장 
# 데이터프레임변수 = pd.read_파일종류('파일명.확장자', 속성='값', .....)
# df4 = pd.read_csv('test.csv')
df4 = pd.read_csv('sample.csv')
print(df4)

