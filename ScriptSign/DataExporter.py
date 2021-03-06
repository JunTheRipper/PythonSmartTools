# DataExporter 辅导员打卡数据文档自动导出
from selenium import webdriver
import time
import os
import re
import datetime
import sys


class DataExportder:
    def __init__(self, url, username, password, path, chrome_option):
        self.username = username
        self.url = url
        self.password = password
        self.chrome_option = chrome_option
        if chrome_option is None:
            self.browser = webdriver.Chrome(executable_path=path)
        else:
            self.browser = webdriver.Chrome(options=chrome_option, executable_path=path)

    def first_log(self):
        time.sleep(2)  # 给予浏览器时间响应
        self.browser.get(self.url)
        self.browser.implicitly_wait(8)
        login = self.browser.find_elements_by_xpath('//*[@class="btn primary-btn"]')[1]
        login.click()

        self.browser.find_element_by_id("username").send_keys(self.username)
        self.browser.find_element_by_id("password").send_keys(self.password)
        self.browser.implicitly_wait(20)
        self.browser.find_element_by_xpath('//*[@class="auth_login_btn primary full_width"]').click()
        sign = self.browser.find_element_by_xpath('//*[@class="grow_1 box_flex column justify_center"]')
        sign.click()
        time.sleep(3)
        self.browser.switch_to.window(self.browser.window_handles[1])
        # 跳转到第二个窗口

    def operator(self):
        self.browser.implicitly_wait(8)
        first = self.browser.find_element_by_xpath('//*[@title="辅导员"]')
        first.click()
        time.sleep(1)
        logout = self.browser.find_element_by_xpath('//*[@class="pull-right operation-group export"]')
        logout.click()
        time.sleep(1)
        excel = self.browser.find_elements_by_xpath('//*[@class="btn blockBtn"]')
        excel[1].click()
        time.sleep(1)
        confirm = self.browser.find_elements_by_xpath('//*[@class="btn submit-btn clearBtnBorder"]')
        confirm[1].click()


if __name__ == '__main__':

    filename = 'admin.log'  # 文件存储日志
    path = r"F:\webdrivers\chromedriver.exe"
    url = 'http://xmuxg.xmu.edu.cn/xmu/app/214'
    download_location = r'C:\Users\admin\Downloads'

    search = input("显示打卡界面？Y/N\n")
    print("Please wait for seconds ...... ")
    chrome_opt = None
    username, password = None, None
    if search.__eq__('N') or search.__eq__('n'):
        chrome_opt = webdriver.ChromeOptions()
        chrome_opt.add_argument('--headless')
    if os.path.exists(filename):
        with open(filename, 'r', encoding="utf-8") as file:
            a = file.readlines()[0].split(" ")
            username = a[0]
            password = a[1]
        file.close()
    else:
        r = input("请输入您的用户名和密码(写一行，空格隔开)：")
        a = r.split(" ")
        username, password = a[0], a[1]
        with open(filename, 'w+') as f:
            f.write(r)

    now_time = datetime.datetime.now()
    string_date = now_time.strftime("%m") + now_time.strftime("%d") + ".xlsx"

    os.chdir(download_location)  # 这是我的默认下载路径,修正工作路径

    if os.path.exists(string_date):
        os.remove(string_date)  # 由于当日打卡数据更新，事先删除当日已经存储的打卡.xlsx 文件

    try:
        browserObj = DataExportder(url, username, password, path, chrome_opt)
        browserObj.first_log()
        browserObj.operator()
        print('获取excel文件成功！')
    except Exception as e:
        print(str(e), "打卡异常！")

    time.sleep(5)
    # 转换器： 功能：excel重命名+直接打开

    target = r'Daily Health Report (\w*)\.xlsx'
    flag = None

    for item in os.listdir(os.getcwd()):
        if re.search(target, item) is not None:
            flag = item
            print(item)
            break

    if flag is not None:
        os.rename(flag, string_date)
        os.system(string_date)
