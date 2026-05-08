# path: ./class_oop.py
# 파이썬에서 객체 지향 프로그래밍(oop) 적용
'''
객체지향 프로그래밍에서는 클래스 멤버 구성이 중요함
field(멤버 변수), method(멤버 함수), constructor(생성자), destructor(소멸자)
--oop 에서 사용되는 기술 (3대 특징)도 적용해야 함
    encapsulation(캡슐화), inheriatance(상속), polymorphism(다양성)
'''

# oop 적용 기술 1 : 캡슐화 
# 캡슐화 : 데이터 보호가 목적임, 필드에 접근 제한을 설정함
# 필드에 접근 제한자(access modifier)를 사용함
# private(비공개 : 캡슐화), public(공개 구조체??), protected(상속시 후손에게만 공개)


# 파이썬에서는 접근 제한자 없음 (제공 안 함)
# 파이썬에서는 기본적으로 클래스 안의 모든 멤버는 public 임
# 클래스를 자료형(type)으로 만든 변수 == 레퍼런스 변수라고 함 : 클래스로 만들어진 객체의 주소를 가짐
# 레퍼런스.필드명.클래스명.필드명
# 레퍼런스.메소드명, 클래스명.메소드명()

# private : 클래스 밖에서 사용 못 함, 클래스 안에서만 사용(접근)할 수 있음
# 파이썬에서 클래스 멤버를 비공개(private) 처리하려면, 
# 필드명이나 메소드명 이름 앞에 '_'(underscore)를 2개를 붙이면 됨


class PClass: # 암묵적으로 대문자로 시작
    # field (private)
    __num = 10

    # constructor  # 추가 : # 매개변수 잇는 생성자를 작성함 (파이썬은 생성자를 1개 밖에 못 만듦)
    # def __init__(self): # 매개변수 없는 기본 생성자임 self 반드시 첫번째로 써야하는 매배변수  
    #    self.__num = 0 # 기본으로 제공 작성할 필요 없음

    def __init__(self, num):
        self.__num = num # 생성자 2개 이상 작성 오버로딩 , TypeError: PClass.__init__() missing 1 required positional argument: 'num'

    # method (public) 
    def set_num(self, num):
        self.num = num

    def get_num(self):
        return self.__num # get_num으로 확인가능하다
    
#--------------------------------------------------

# 클래스 멤버 사용 : 레퍼런스변수 = 클래스명() 또는 레퍼런스 = 글래스명(전달값), 객체 생성
# pref = PClass()  # 매개변수 없는 기본 생성자 자동 실행됨, 메모리에 객체 공간 할당하고 주소를 리턴함
# print('pref가 가진 주소 :', id(pref))
# print('인스턴스 안의 __num 값 : ', pref.get_num())


# 클래스 밖에서 필드 접근 확인
# print('인스턴스 안의 __num :', pref.__num) #
# private 이므로 접근 못함 : 에러

# 객체 인스턴스가 메모리에 할당될 때, 필드값 초기화가 목적인 함수
# 생성자가 없으면 내부에서 기본생성자(매개변수 없는) 자동 작동함
# 생성자를 직접 작성한다면, __init__로 정이해야 함
# 파이썬에서는 생성자는 오버로딩(overloading : 중복 정의)할 수 없음 : 생성자는 1개
# 주로 매개변수 있는 생성자를 추가 작성함 
pref2 = PClass(20)
print('pref2가 참조하는 인스턴스 안의 필드값 확인 :', pref2.get_num())

# destructor (소멸자 함수)
# 객체 인스턴스가 메모리에서 제거(소멸)될 때 자동 실행하는 함수임
# 클래스 안에서 직접 작성했다면, __del__ 로 정의해야 함
# 해당 객체 관련 메모리나 자원들의 공유 설정 점유 설정 등을 해제할 때 
'''
class 클래스명:
    def __del__(self):
    해당 클랙스가 객체가 소멸될 때 같이 제거 또는 해제할 내용에 대한 코드 작성
'''

class Var:
    # #field : private
    __number = 100


    # constructor
    def __init__(self, n): # self는 꼭 들어가 있어야 한다
        print('self가 전달받은 주소 확인 : ', id(self))
        self.__number = n

    # destructor
    def __del__(self):
        print('인스턴스 제거시 자동 작동됨 : ', id(self))

    # method : getter and setter
    def set_number(self, n):
        self.__number = n

    def get_number(self):
        print('self가 전달받은 주소 확인 : ', id(self))
        return self.__number

# Var ---------------------------------

# 클래스 객체 생성 : 생성자가 자동 실행됨
v1 = Var(77) # 추가된 매개변수 있는 생성자가 작동됨, 참조 변수
v2 = Var(99) # 2개의 객체가 메모리에 할당

print('v1 : ', v1.get_number(), id(v1))
print('v2 : ', v2.get_number(), id(v2))
    
# 필드값 변경 : setter 사용
v1.set_number(123)
print('v1 : ', v1.get_number(), id(v1))
# v2.set_number(int(input('v2가 참조하는 객체의 필드값 변경하세요 : ')))
# print('v2 : ', v2.get_number(), id(v2))

# 정적 메모리 프로그램 시작될 때 기록 끝나면 사라짐 - 프로그램 진행 중에는 계속 사용됨
# 정적 메소드 (static method)------------------------------------------
# 프로그램 실행시 정적 메모리(static)에 따로 기록되는 메소드를 말함
# 메소드 작성시 메소드 이름 위에 장식자(decorator == 어노테이션 : annotation)를 표시하면 됨
# @staticmethod
# self가 없는 메소드임 => 메소드 사용 : 클래스명.메소드()

class C:
    def ham(self, x, y): # self가 자동으로 주소를 전달받음
        print('instance method : ', x, y)

class D:
    @staticmethod
    def spam(x, y): # 프로그램 실행시 static (정적) 메모리에 로딩됨, self 매개변수 없음
        print('static or class method :', x, y)

# static method 는 사용시 객체 레퍼런스(인스턴스의 주소) 없이 실행함
# 클래스명 메소드(전달값) 
D.spam(100, 200)
dref = D()
dref.spam(300, 400)

# instance method 사용
# C.ham(11, 22) # static method 처럼 사용할 수 없음 => self에게 반드시 주소 전달 필요함
# 해결 방법 : self 에게 직접 주소 전달하면 됨
cref = C()
cref.ham(10, 20) # cref가 가진 주소를 self 매개변수에게 자동 전달
C.ham(cref, 77, 88) # cref가 가진 주소를 self 매개변수에게 직접 전달


