from selenium import webdriver #Selenium Webdriverをインポートして
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys


driver_path = "/usr/local/bin/" #driverのパス
shinjuku_url = "https://user.shinjuku-shisetsu-yoyaku.jp/regasu/reserve/gin_menu" #新宿テニス予約ページurl
usr_id = sys.argv[1] #利用者ID
password = sys.argv[2] #パスワード

driver = webdriver.Firefox(driver_path)

#menu画面
driver.get(shinjuku_url)

#actions = ActionChains(driver)

#多機能操作ボタン
meny_operation_btn = driver.find_element_by_css_selector(".second input:nth-child(2)")
#ログイン画面へ遷移
meny_operation_btn.click()

#利用者番号
driver.find_element_by_id("user").send_keys(usr_id)
#パスワード
driver.find_element_by_id("password").send_keys(password)
#ログイン
driver.find_element_by_css_selector(".buttons > input").click()

#予約申込クリック
driver.find_element_by_xpath("//a[contains(text(),'予約申込')]").click()

#屋外スポーツ施設洗濯
driver.find_element_by_css_selector("select:nth-child(1) > option:nth-child(2)").click()
#確定
driver.find_element_by_css_selector(".left > input:nth-child(4)").click()


#ブラウザー終了
#driver.quit()