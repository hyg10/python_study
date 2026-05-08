# 프로젝트(어플리케이션)를 실행하는 스크립트
# CLI(Command Line interface) : 실행 시 터미널(command prompt)에 글자로 메세지가 출력되고, 키보드 입력으로 실행
# GUI(Graphic User interface) : 실행 시 윈도우 창이 열리면서, 메뉴바/툴바 등을 마우스 클릭으로 실행

import fileio_sample.fileio_module as fs # C:\python_workspace\python_fileio\fileio_sample\fileio_module
import loop.while_sample as lw
import fileio_sample.fileio_moduel2 as fs2
 
# cli 방식의 메뉴 출력용 함수
def menu():
    print('파일입출력 및 예외처리 테스트용 프로그램 시작 ----------------------------')
    
    # 파이썬에서는 여러 줄의 문자열 값을 표현할 때 3쌍의 따옴표를 이용함
    prompt = '''
    1. 파일에 저장하기 테스트 1
    2. 파일에 저장하기 테스트 2 : 경로 지정 저장
    3. 파일에 저장하기 테스트 3 : 추가쓰기 모드 확인
    4. 파일로 부터 읽어오기 4 :
    5. while 반복문 사용 테스트 1
    6. while 반복문 사용 테스트 2 : 문자 유니코드 출력
    7. os 모듈의 함수 확인 1 
    10. 파일 내용 줄단위로 리스트에 저장하기 
    11. 컬렉션 아이템들을 파일에 저장하기
    12. 이진 데이터로 파일에 저장하기 
    13. 파일로 부터 이진 데이터 읽어오기
    9. 메뉴 끝내기
'''
    
    
    while True:
        # print('1. 파일에 저장하기 테스트 1')
        # print('2. 파일로 부터 읽어오기 테스트 1')
        # print('9. 메뉴 끝내기')
        
        print(prompt)
        no = int(input('원하는 메뉴 번호 입력 :'))

        if no == 1:
            fs.test_fwrite()
        if no == 2:
            fs.test_fwrite2()
        if no == 3:
            fs.test_fwrite3()
        if no == 4:
            fs.test_fread()
        if no == 5:
            lw.test_while()
        if no == 6:
            lw.print_unicode()
        if no == 7:
            fs.test_osmodule()
        if no == 9:
            break
        if no == 10:
            fs.test_fread2()
        if no == 11:
            fs.test_writeline()
        if no == 12:
            fs2.test_binary_fileio()
        if no == 13:
            fs2.test_binary_fileio2()
    # while end -------------------------------

    print('테스트 종료!--------------------------------')
    return


if __name__ == '__main__':
    # fs.test_fwrite() 
    # lw.test_while()
    menu() # pass   # 내용 없어요 지나가세요
    print('프로그램 종료')

# 함수들만 모아둔 파일, 모듈
# 모듈 묶음, PKG

#
