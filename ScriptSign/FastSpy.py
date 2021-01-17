# 爬虫系统，实现自动化打卡技术
from selenium import webdriver
import wx
import time
import os
import sys
class Login_Spyder:
    def __init__(self, url, username, password, path, chrome_option):
        self.username = username
        self.url = url
        self.password = password
        self.chrome_option = chrome_option
        if chrome_option == None:
            self.browser = webdriver.Chrome(executable_path=path)
        else:
            self.browser = webdriver.Chrome(options=chrome_option, executable_path=path)

    def first_log(self):
        time.sleep(2)  # 给予浏览器时间响应
        self.browser.get(url)
        self.browser.implicitly_wait(10)
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

    def operator(self):
        self.browser.implicitly_wait(10)
        first = self.browser.find_element_by_xpath('//*[@title="我的表单"]')
        first.click()
        action = webdriver.ActionChains(self.browser)
        time.sleep(1)
        a = self.browser.find_elements_by_xpath('//*[@data-name="select_1582538939790"]')
        item = a[0]
        js = "var q=document.getElementsByClassName('container-fluid')[1].scrollTop=10000"
        self.browser.execute_script(js)  # 滑动到最底端
        time.sleep(1)
        action.move_to_element(item).perform()
        if item.text[:3] != "请选择":
            print("您已打卡！")

        else:
            action.click().perform()  # 移动到对应位置并点击，弹出“是”的对话栏
            with open('1.html', "w", encoding='utf-8') as filr:
                filr.write(self.browser.page_source)

            class_menu = self.browser.find_elements_by_xpath('//li[contains(@class,"dropdown-items")]')
            if class_menu == []:
                wx.MessageBox("您未在打卡时间内")
                self.browser.quit()

            else:
                its = class_menu[0]
                its.click()
                self.browser.find_element_by_xpath('//*[@class="form-save position-absolute"]').click()
                alert = self.browser.switch_to.alert

                alert.accept()
                self.browser.quit()
                print("打卡成功！")
                sys.exit()


if __name__ =='__main__':
    filename = '../signame.log'  # 文件存储日志
    path = r"F:\google_webdriver\chromedriver.exe"
    url = 'http://xmuxg.xmu.edu.cn/xmu/app/214'
    search = input("显示打卡界面？Y/N\n")
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
        r = input("请输入您的用户名和密码：")
        a = r.split(" ")
        username, password = a[0], a[1]
        with open(filename, 'w+') as f:
            f.write(r)

    try:
        browser = Login_Spyder(url, username, password, path, chrome_opt)
        browser.first_log()
        browser.operator()
    except Exception as e:
        print(str(e),e.with_traceback(), "打卡异常！")