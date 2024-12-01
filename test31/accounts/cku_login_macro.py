# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import time
# from bs4 import BeautifulSoup
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options

# def cku_login(username, password):
#     url = "https://www.cku.ac.kr/sites/cku_kr/index.do#none"
#     driver = webdriver.Chrome()
#     driver.get(url)
#     time.sleep(2)

#     # 헤드리스 모드 설정, 실행
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-gpu")  
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get("https://www.cku.ac.kr/sites/cku_kr/index.do#none")
#     time.sleep(2)

#     #팝업창 재학생 버튼 클릭
#     element = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, '#menu5578_obj3712 > div > div > ul > li:nth-child(2) > button'))
#     )
#     element.click()

#     #재학생 - 종합정보 버튼 클릭
#     element = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.user-service.on > div.info > div.right > div > ul.menu-list.menu-list2.on > li:nth-child(4) > a'))
#     )
#     element.click()

#     # 4. 새로 생성된 브라우저 창으로 전환
#     original_window = driver.current_window_handle
#     all_windows = driver.window_handles

#     for window in all_windows:
#         if window != original_window:
#             driver.switch_to.window(window)
#             break

#     # 5. 새 창에서 로그인 아이디 입력
#     login_id_field = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, '#login_id'))
#     )
#     login_id_field.send_keys(username)

#     # 2. 비밀번호 입력
#     login_pw_field = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, '#login_pwd'))
#     )
#     login_pw_field.send_keys(password)

#     # 로그인 버튼 클릭
#     element = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, '#loginForm > fieldset > div.button > a.login'))
#     )
#     element.click()

#     # 종합정보 - 학적관리 클릭
#     element = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, '#AccordionContainer > div:nth-child(1) > div > span > a'))
#     )
#     element.click()

#     # 종합정보 - 학적관리 - 학적신상카드 클릭
#     element = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, '#Accordion1Content > ul > li:nth-child(1) > a'))
#     )
#     element.click()

#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     # 학번 추출
#     CrawlUserID = driver.execute_script('return document.querySelector("td.num").innerText')
#     print(CrawlUserID)

#     # 이름 추출
#     element = driver.find_element(By.CSS_SELECTOR, "#contents > div.dataArea > table > tbody > tr:nth-child(2) > td:nth-child(2)")
#     CrawlUserName = element.text
#     print(CrawlUserName)

#     # 전공 추출
#     element = driver.find_element(By.CSS_SELECTOR, "#contents > div.dataArea > table > tbody > tr:nth-child(3) > td:nth-child(4)")
#     CrawlUserMajor = element.text
#     print(CrawlUserMajor)

#     # 로그인 후 값 반환, 웹사이트 닫기
#     time.sleep(2)  # 페이지 로드 대기
#     driver.quit()
#     return CrawlUserName, CrawlUserID, CrawlUserMajor

# if __name__ == '__main__':
#     cku_login()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def cku_login(username, password):
    url = "https://info.cku.ac.kr/haksa/common/loginForm2.jsp"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)

    # 헤드리스 모드 설정, 실행
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://info.cku.ac.kr/haksa/common/loginForm2.jsp")
    time.sleep(2)

    # 통합 로그인 버튼 클릭 (이미지 맵의 링크 요소 접근)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "area[title='통합로그인']"))
    )
    element.click()

    # 4. 새로 생성된 브라우저 창으로 전환
    original_window = driver.current_window_handle
    all_windows = driver.window_handles

    for window in all_windows:
        if window != original_window:
            driver.switch_to.window(window)
            break

    # 5. 새 창에서 로그인 아이디 입력
    login_id_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#login_id'))
    )
    login_id_field.send_keys(username)

    # 2. 비밀번호 입력
    login_pw_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#login_pwd'))
    )
    login_pw_field.send_keys(password)

    # 로그인 버튼 클릭
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#loginForm > fieldset > div.button > a.login'))
    )
    element.click()

    # 종합정보 - 학적관리 클릭
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#AccordionContainer > div:nth-child(1) > div > span > a'))
    )
    element.click()

    # 종합정보 - 학적관리 - 학적신상카드 클릭
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#Accordion1Content > ul > li:nth-child(1) > a'))
    )
    element.click()

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 학번 추출
    CrawlUserID = driver.execute_script('return document.querySelector("td.num").innerText')
    print(CrawlUserID)

    # 이름 추출
    element = driver.find_element(By.CSS_SELECTOR, "#contents > div.dataArea > table > tbody > tr:nth-child(2) > td:nth-child(2)")
    CrawlUserName = element.text
    print(CrawlUserName)

    # 전공 추출
    element = driver.find_element(By.CSS_SELECTOR, "#contents > div.dataArea > table > tbody > tr:nth-child(3) > td:nth-child(4)")
    CrawlUserMajor = element.text
    print(CrawlUserMajor)

    # 로그인 후 값 반환, 웹사이트 닫기
    time.sleep(2)  # 페이지 로드 대기
    driver.quit()
    return CrawlUserName, CrawlUserID, CrawlUserMajor

if __name__ == '__main__':
    cku_login()