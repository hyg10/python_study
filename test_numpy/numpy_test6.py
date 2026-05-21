# path = numpy_test6.py

import numpy as np

# 기술 통계 (descriptive staticstatics) : 통계 계산용 함수를 말함
# 데이터 갯수(count), 평균(mean, average), 분산(variance), 표준편차(standard deviation)
# 최대값(maximum), 최소값(minimum), 중앙(간)값(median), 사분위(quartile)

x = np.random.randint(-10, 50, size=30)

# 데이터 갯수 : len()
print(len(x))

# 평균 : np.mean(배열변수)
print('mean :', np.mean(x))

# 표본 분산 (sample varience) : 데이터와 평균 간의 거리의 제곱의 평균
print('Var : ', np.var(x))
print('Var ddof=1 : ', np.var(x, ddof=1))

# 표준 편차 : 표본 분산의 양의 제곱근, ss라고 표시함
print('ss :', np.std(x))

# 최대값, 최소값, 중앙값(중간값)
print('max :', 'np.max(x)')
print('min :', np.min(x))
print('median :', np.median(x))

# 사분위수
# 데이터를 오름차순정렬했을 때, 1/4, 2/4(== 중앙값), 3/4, 4/4(==최대값) 위치의 값을 말함
# 1사분위, 2사분위, 3사분위, 4사분위 
# 데이터 갯수가 100개이면, 1사분위는 25번째 값이 됨
print(np.percentile(x, 0)) # 최소값이 됨
print(np.percentile(x, 25)) # 1/4
print(np.percentile(x, 50)) # 2/4
print(np.percentile(x, 75)) # 3/4
print(np.percentile(x, 100)) # 4/4, 최대값이 됨

# 난수 발생과 카운팅
# 난수 (random number) : 프로세스가 임의로 발생하는 수 
# numpy 의 random 서브 패키지에서 함수들이 제공됨

# np.random.seed(인수)
# seed : 난수의 시작값
# 인수 : 정수 >= 0 사용함
np.random.seed (0) #  난수의 시작값 지정과 랜덤값 고정
# 설정 이후 한 번 발생된 랜덤값이 계속 동일한 값이 발생됨 확인함


print(np.random.rand(5)) # 0.0 <= 난수 < 1.0 실수형 숫자 5개 발생
# [0.73215189 0.74434728 0.19670668 0.81698382 0.07325328]
# [0.9493899  0.52470335 0.08276056 0.49313408 0.32455998]
# [0.5488135  0.71518937 0.60276338 0.54488318 0.4236548 ]
# [0.5488135  0.71518937 0.60276338 0.54488318 0.4236548 ]


# 데이터 섞기 : suffle()
x = np.arange(10)
print(x)
np.random.shuffle(x)
print(x)
