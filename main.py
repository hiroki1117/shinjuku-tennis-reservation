from selenium import webdriver #Selenium Webdriverをインポートして
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import time
import sys
import os
import platform
import teams

SHINJUKU_URL = "https://user.shinjuku-shisetsu-yoyaku.jp/regasu/reserve/gin_menu" #新宿テニス予約ページurl

def createOptionsAndPath():
    options = webdriver.ChromeOptions()
    path = "/usr/local/bin/chromedriver"

    if(platform.system() != 'Darwin'):
        options.binary_location = "/opt/bin/headless-chromium"
        options.add_argument('-headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--single-process")
        path = "/opt/bin/chromedriver"

    return (options, path)

def scrapingOperation(driver, usr_id, password):
    #menu画面
    driver.get(SHINJUKU_URL)

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

    #分類-屋外スポーツ施設洗濯
    driver.find_element_by_css_selector("select:nth-child(1) > option:nth-child(2)").click()
    #確定
    driver.find_element_by_css_selector(".left > input:nth-child(4)").click()
    #目的-テニス
    driver.find_element_by_xpath("//select[@name='riyosmk']/option[2]").click()
    #確定
    driver.find_element_by_css_selector(".double-contents:nth-child(1) > .left > input:nth-child(3)").click()
    #施設-落合中央公園
    driver.find_element_by_css_selector("select:nth-child(1) > option:nth-child(3)").click()
    #確定
    driver.find_element_by_css_selector(".inner-block:nth-child(4) input:nth-child(3)").click()
    #部屋-落合中央公園庭球場
    driver.find_element_by_css_selector(".selector > select > option").click()
    #確定
    driver.find_element_by_css_selector(".followed > input:nth-child(2)").click()
    #検索条件-月火水木金
    driver.find_element_by_css_selector(".last > input:nth-child(3)").click()
    driver.find_element_by_css_selector(".last > input:nth-child(5)").click()
    driver.find_element_by_css_selector(".last > input:nth-child(7)").click()
    driver.find_element_by_css_selector(".last > input:nth-child(9)").click()
    driver.find_element_by_css_selector(".last > input:nth-child(11)").click()
    #検索
    driver.find_element_by_id("btnOK").click()

    #表示する日付を増やす
    driver.find_element_by_css_selector("li img").click()
    html_source = driver.page_source

    result = parseCoatStatusTable(html_source)

    #もう1月選択できる場合
    month_options = Select(driver.find_element_by_id("MM")).options
    if len(month_options) >= 2:
        #次の月を選択
        month_options[1].click()
        #検索
        driver.find_element_by_xpath("//img[@alt='検索']").click()
        html_source2 = driver.page_source
        result.update(parseCoatStatusTable(html_source2))

    return result

def parseCoatStatusTable(html):
    #Beautifulsoupでhtmlをパース
    soup = BeautifulSoup(html, "html.parser")
    #予約状況のテーブル
    resavation_table = soup.find("table")
    #日付
    day_ary = list(map(lambda x: x.string, resavation_table.find_all("strong")))

    #key-日付　value-dom要素
    dict = {}

    #1900~2100のid属性
    #base_id = "td{daynum}{col}_7"
    base_id = "td11{col}_7"

    #1900~2100の予約状況を取得
    for day, index in zip(day_ary, range(len(day_ary))):
        id = base_id.format(col=index)
        temp = resavation_table.find(id=id)
        dict[day] = temp

    return dict


def parseCoastStatusHtml(coatStatusMap):
    result = {}
    for key, value in coatStatusMap.items():
        if value.string == 'Ｘ':
            result[key] = '×'
        else:
            result[key] = '○'
    return result

def main(event, context):
    usr_id = os.environ['USR_ID']
    password = os.environ['PASSWORD']
    teams_url = os.environ['TEAMS']

    #実行環境ごとのオプション作成
    (options, exe_path) = createOptionsAndPath()

    #Driver作成
    driver = webdriver.Chrome(
        executable_path=exe_path,
        chrome_options=options
    )

    #コートの予約状況の取得
    dict = scrapingOperation(driver, usr_id, password)
    statusMap = parseCoastStatusHtml(dict)

    print(statusMap)
    teams.sendToTeams(statusMap, teams_url)

    #ブラウザー終了
    driver.quit()


if __name__ == "__main__":
    main({},{})