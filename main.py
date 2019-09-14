from selenium import webdriver #Selenium Webdriverをインポートして

driver_path = "/usr/local/bin/" #driverのパス

shinjuku_url = "https://user.shinjuku-shisetsu-yoyaku.jp/regasu/reserve/gin_menu" #新宿テニス予約ページurl

driver = webdriver.Firefox(driver_path)

#menu画面
driver.get(shinjuku_url)

