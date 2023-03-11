from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys

driver = webdriver.Chrome()
url = 'https://sugang.pusan.ac.kr/sugang/login.aspx'
driver.get(url)
driver.maximize_window()
action = ActionChains(driver)

while driver.current_url == 'https://sugang.pusan.ac.kr/sugang/login.aspx':
    driver.switch_to.active_element.find_element(By.XPATH, '//*[@id="txtid"]').send_keys("201924463")
    driver.switch_to.active_element.find_element(By.XPATH, '//*[@id="txtpassword"]').send_keys("ms38559851!")
    driver.switch_to.active_element.find_element(By.XPATH, '//*[@id="btnlogin"]').click()

sub_num = 14
checking = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]

original_window = driver.current_window_handle

while 1:
    if EC.number_of_windows_to_be(2):
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                driver.switch_to.active_element.find_element(By.XPATH, '//*[@id="txtInsChar"]').send_keys(driver.switch_to.active_element.find_element(By.XPATH, '//*[@id="txtRandom"]').get_attribute('value'))
                driver.switch_to.active_element.find_element(By.XPATH, '//*[@id="btnConfirm"]').click()
                driver.switch_to.window(original_window)
                break

    if EC.alert_is_present():
        driver.switch_to.alert.accept()

    driver.switch_to.active_element.find_element(By.XPATH, '//*[@id="dgBasket_List_ctl08_bt신청"]').click()

    # i = 0
    # while i < sub_num:
    #     if checking[i] == 1:
    #         driver.switch_to.active_element.find_element(By.XPATH, '//*[@id="dgBasket_List_ctl0{}_bt신청"]'.format(2 + i)).click()
    #     i += 1


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from multiprocessing import Process
# import sys, os, time
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *


# TRYING_WINDOWS = 4
# MAX_SUBJECTS = 13



# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)



# def thread_1(id, pw, checks):
#     chromedriver_path = resource_path("chromedriver.exe")
#     driver = webdriver.Chrome(chromedriver_path)
#     driver.maximize_window()


#     #첫번째 탭 주소 이동    
#     url = 'https://sugang.pusan.ac.kr/sugang/login.aspx'
#     driver.get(url)

#     #이후 TRYING_WINDOWS 개수만큼 추가 탭 생성
#     for i in range(TRYING_WINDOWS):
#         driver.execute_script('window.open("https://sugang.pusan.ac.kr/sugang/login.aspx", "_blank");')

#     #체크시작. 모든 탭을 순회하면서 완료된 탭이 발생하면 나머지 탭은 즉시 종료
#     done = 0
#     working_window = 0

#     while done == 0:
#         for w in driver.window_handles:
#             driver.switch_to.window(w)

#             if driver.current_url == 'https://sugang.pusan.ac.kr/sugang/sugang-insert.aspx':
#                 if EC.presence_of_element_located(By.XPATH, '//*[@id="dgBasket_List_ctl02_bt신청"]'):
#                     done = 1
#                     working_window = w
            
#             if driver.current_url == 'https://sugang.pusan.ac.kr/sugang/login.aspx':
#                 if done == 1:
#                     driver.close()
#                 else:
#                     driver.find_element(By.XPATH, '//*[@id="txtid"]').send_keys(id)
#                     driver.find_element(By.XPATH, '//*[@id="txtpassword"]').send_keys(pw)
#                     driver.find_element(By.XPATH, '//*[@id="btnlogin"]').click()

#             try:
#                 if EC.alert_is_present():
#                     driver.switch_to.alert.accept()
#                     driver.close()
#             except:
#                 pass

#             try:
#                 if driver.current_url == 'https://sugang.pusan.ac.kr/sugang/sugang-insert.aspx':
#                     if EC.presence_of_element_located(By.XPATH, '//*[@id="dgBasket_List_ctl02_bt신청"]'):
#                         done = 1
#                         working_window = w
#             except:
#                 pass
        
#         if done == 1:
#             break

#     #최초로 로딩이 완료된 탭을 제외한 모든 탭 닫기
#     for windows in driver.window_handles:
#         if (windows != working_window):
#             driver.switch_to.window(windows)
#             driver.close()

#     original_window = driver.current_window_handle

#     while 1:
#         if EC.number_of_windows_to_be(2):
#             for window_handle in driver.window_handles:
#                 if window_handle != original_window:
#                     driver.switch_to.window(window_handle)
#                     driver.find_element(By.XPATH, '//*[@id="txtInsChar"]').send_keys(
#                         driver.find_element(By.XPATH, '//*[@id="txtRandom"]').get_attribute('value'))
#                     driver.find_element(By.XPATH, '//*[@id="btnConfirm"]').click()
#                     driver.switch_to.window(original_window)
#                     break

#         try:
#             driver.switch_to.alert.accept()
#         except:
#             pass

#         for i in range(MAX_SUBJECTS):
#             if checks[i] == 1:
#                 if i <= 7:
#                     driver.find_element(By.XPATH, '//*[@id="dgBasket_List_ctl0{}_bt신청"]'.format(2 + i)).click()
#                 else:
#                     driver.find_element(By.XPATH, '//*[@id="dgBasket_List_ctl{}_bt신청"]'.format(2 + i)).click()


# class SugangMacroApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         vbox = QVBoxLayout()

#         self.f0 = QLabel('수강신청 매크로 v1.0')
#         self.f0.setFont(QFont('Arial', 30))
#         vbox.addWidget(self.f0)
#         self.f01 = QLabel('실패해도 책임안짐 믿거나 말거나~~\n\n')
#         self.f01.setFont(QFont('Arial', 15))
#         vbox.addWidget(self.f01)

#         self.t1 = QLabel('학번을 입력하세요')
#         self.t1.setFont(QFont('Arial', 12))
#         vbox.addWidget(self.t1)

#         self.student_id = QTextEdit()
#         self.student_id.setAcceptRichText(False)
#         self.student_id.setMaximumHeight(25)
#         vbox.addWidget(self.student_id)

#         self.t2 = QLabel('\n학지시 비밀번호를 입력하세요')
#         self.t2.setFont(QFont('Arial', 12))
#         vbox.addWidget(self.t2)

#         self.student_pw = QTextEdit()
#         self.student_pw.setAcceptRichText(False)
#         self.student_pw.setMaximumHeight(25)
#         vbox.addWidget(self.student_pw)

#         self.t3 = QLabel('\n신청할 과목을 선택하세요 (최대 7과목)')
#         self.t3.setFont(QFont('Arial', 12))
#         vbox.addWidget(self.t3)

#         self.checks = []
#         for i in range(MAX_SUBJECTS):
#             self.checks.append(QCheckBox('{}번째 과목'.format(1 + i)))
#             self.checks[i].setFont(QFont('Arial', 10))
#             vbox.addWidget(self.checks[i])

#         self.t4 = QLabel('\n')
#         self.t4.setFont(QFont('Arial', 12))
#         vbox.addWidget(self.t4)

#         self.start_btn = QPushButton('Start', self)
#         self.start_btn.setMinimumHeight(40)
#         self.start_btn.clicked.connect(self.start_macro)
#         vbox.addWidget(self.start_btn)

#         self.setLayout(vbox)
#         self.setWindowTitle('Sugang Macro v1.0')
#         self.setGeometry(0, 0, 500, 350)
#         self.center()
#         self.show()

#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())

#     def start_macro(self):
#         chec = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#         for i in range(MAX_SUBJECTS):
#             if self.checks[i].isChecked():
#                 chec[i] = 1

#         t1 = Process(target=thread_1, args=(self.student_id.toPlainText(), self.student_pw.toPlainText(), chec))
#         t1.start()



# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = SugangMacroApp()
#     sys.exit(app.exec_())