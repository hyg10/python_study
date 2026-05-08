
import loop.while_mission as mi
import fileio.fileio_mission as fm


def menu():
    print('함수 실행 : while 루프로 프롬프트 출력-----------------')

    prompt = '''
	*** 파이썬 과제 1 ***
	1. while 실습문제
	2. fileio 실습문제
	9. 과제 실행 테스트 끝내기
 '''
    
    while True:
        print(prompt)
        no = int(input('원하는 메뉴 번호를 선택하세요:'))

        if no == 1:
            mi.sunjuk_process()
        if no == 2:
            fm.filio_employee()
        if no == 9:
            break

        print('테스트 종료-------------------------------')
    return

if __name__ == '__main__':
    menu()
    print('프로그램 종료')
    