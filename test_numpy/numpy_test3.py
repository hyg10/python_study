# path : numpy_test3.py
import numpy as np

# 전치연산 : T 속성 사용함 => 2차원배열명.T
# 2차배열에 행과 열을 서로 바꿀 때 사용함 => 2행 3열.T => 3행 2열이 됨
ar = np.array([[1, 2, 3], [4, 5, 6]]) # 2행 3열 배열
print(ar) # 2행 3열 배열의 요소값 출력
print(ar.shape) # (2, 3) => 2행 3열
print(ar.T) # 3행 2열로 바뀐 배열의 요소값 출력
print(ar.T.shape) # (3, 2) => 3행 2열

# 1차원배열은 전치연산 못 함
# 1차원배열을 다차원배열로 변경할 수 있음 
# reshape() 함수 사용함 => 전체 크기(갯수)는 바뀌지 않음
ar = np.arange(12) # 12 : 0 ~ 11까지 정수로 구성된 1차원 배열
print(ar) # 1차원 배열의 요소값 출력
print(type(ar)) # <class 'numpy.ndarray'>
print(ar.ndim) # 1차원 배열의 차원 : 1
print(ar.size) # 1차원 배열의 요소값 갯수 : 12

# 3행 4열 2차원 배열로 바꾸기 
br = ar.reshape(3, 4) # reshape(행, 열)
print(br) # 3행 4열로 바뀐 배열의 요소값 출력
print(br.ndim) # 2차원 배열의 차원 : 2
print(br.size) # 2차원 배열의 요소값 갯수 : 12
print(br.T) # 4행 3열로 바뀐 배열의 요소값 출력
print(np.transpose(br)) # T 속성과 동일한 결과를 리턴함
print(np.swapaxes(br, 0, 1)) # T 속성과 동일한 결과를 리턴함

# reshape() 사용시에 면, 행, 열 갯수를 지정하지 않고 , -1 로 표기할 수도 있음
# -1로 표시된 항목은 내부 계산에 의해 갯수가 자동 설정됨
br2 = ar.reshape(3, -1)
print(br2)
print(br2.shape) # (3, 4) 

# 1차원배열을 3차원배열로 바꾸기 
br3 = ar.reshape(2, 2, -1) 
print(br3)
print(br3.shape) # (2, 2, 3) => 2면 2행 3열

br4 = ar.reshape(2, -1, 3) 
print(br4)
print(br4.shape) # (2, 2, 3) => 2면 2행 3열

# flatten() 함수, ravel() 함수
# 다차원 배열을 1차원 배열로 바꿀 때 사용함
print('br :', br.shape) # (3, 4)
print(br.flatten()) # 1차원 배열로 바뀐 요소값 출력
print(br.ravel()) # 1차원 배열로 바뀐 요소값 출력

print('br3 :', br3.shape) # (2, 2, 3)
print(br3.flatten()) # 3차원배열 => 1차월배열 1차원 배열로 바뀐 요소값 출력
print(br3.ravel()) # 1차원 배열로 바뀐 요소값 출력

# newaxis 함수
# 배열의 차원을 1증가 시키는 함수 
# 1차원배열 => 2차원배열 => 3차원배열
# 예 : 값의 갯수가 5개인 1차원배열을 2차원 배열로 바꿀 때 (5, 1) | (1, 5) 
# 1차원배열 [값 5개] 과 2차원배열 [[값 5개]]은 다름
xr = np.arange(5) # 0 ~ 4까지 정수로 구성된 1차원 배열
print(xr) # 1차원 배열의 요소값 출력
print(xr.shape) # (5, ) => 1차원 배열의 요소값 갯수 : 5
print(xr.reshape(1, 5)) # 2차원 배열로 바뀐 요소값 출력
print(xr.reshape(5, 1)) # 2차원 배열로 바뀐 요소값 출력

# 총 값의 갯수가 같은 배열에 대해 차원만 1증가시키는 경우, newaxis 사용할 수 있음
print(xr[:, np.newaxis]) # [행, 열] 을 의미함
# :(콜론) 의미는 모든 값 (처음부터:끝까지 슬라이싱함)
print(xr[np.newaxis, :]) # [행, 열] 을 의미함
print(xr[:, np.newaxis].shape) # (5, 1) => 5행 1열
