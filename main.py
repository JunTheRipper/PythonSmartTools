# 爬虫系统，实现自动化打卡技术
class LoginSpyder:
    def __init__(self, url, username, password):
        self.username = username
        self.url = url
        self.password = password

    def spy(self):
        pass

from selenium import webdriver
import wx
import time
import os
import sys
TvalueChoice = []
PvalueChoice = []
filename = 'signame.log' #文件存储日志
PATH="chromedriver.exe"

url = 'http://xmuxg.xmu.edu.cn/xmu/app/214'


def firstlog(usr, password,browser):
    #wx.MessageBox("发现用户未登录......正在自动登录状态......")
    browser.implicitly_wait(10)
    login = browser.find_elements_by_xpath('//*[@class="btn primary-btn"]')[1]
    login.click()

    browser.find_element_by_id("username").send_keys(usr)
    browser.find_element_by_id("password").send_keys(password)
    browser.implicitly_wait(20)
    browser.find_element_by_xpath('//*[@class="auth_login_btn primary full_width"]').click()
    sign = browser.find_element_by_xpath('//*[@class="grow_1 box_flex column justify_center"]')

    sign.click()
    with open("1.html", "w", encoding="utf-8") as f:
        f.write(browser.page_source)
    time.sleep(3)
    browser.switch_to.window(browser.window_handles[1])
def operator(browser):
    browser.implicitly_wait(10)
    first = browser.find_element_by_xpath('//*[@title="我的表单"]')
    first.click()
    action = webdriver.ActionChains(browser)
    time.sleep(1)
    a = browser.find_elements_by_xpath('//*[@data-name="select_1582538939790"]')
    item = a[0]
    js = "var q=document.getElementsByClassName('container-fluid')[1].scrollTop=10000"
    browser.execute_script(js)  # 滑动到最底端
    time.sleep(1)
    action.move_to_element(item).perform()
    if item.text[:3] !="请选择":
        wx.MessageBox("您已打卡！")

    else:
        action.click().perform()  # 移动到对应位置并点击，弹出“是”的对话栏
        with open('1.html', "w", encoding='utf-8') as filr:
            filr.write(browser.page_source)


        classmenu = browser.find_elements_by_xpath('//li[contains(@class,"dropdown-items")]')
        if classmenu == []:
            wx.MessageBox("您未在打卡时间内")
            browser.quit()

        else:
            its = classmenu[0]
            its.click()
            browser.find_element_by_xpath('//*[@class="form-save position-absolute"]').click()
            alert = browser.switch_to.alert

            alert.accept()
            browser.quit()
            wx.MessageBox("打卡成功！")
            sys.exit()
class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title=u"厦门大学每日打卡自动化系统",pos=(400,400),size=(530, 200))
        panel = wx.Panel(self)
        self.SetBackgroundColour(wx.Colour(128, 255, 255))

        font = wx.Font(17, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.LIGHT, underline=False)
        self.name = wx.StaticText(panel, label="账 号：", pos=(30, 13))
        self.name.SetFont(font)
        self.nameValue = wx.ComboBox(panel, wx.ID_ANY, wx.EmptyString, (120, 12), wx.Size(352, -1),
                                TvalueChoice, 0)
        self.nameValue.SetFont(font)
        #wx.StaticText(panel, label="请选择识别的图片:", pos=(10, 38))
        self.password = wx.StaticText(panel, label="密 码：", pos=(30, 60))
        self.password.SetFont(font)
        self.passValue = wx.ComboBox(panel,wx.ID_ANY, wx.EmptyString, (120, 55), wx.Size(352, -1),
                                TvalueChoice, style=wx.TEXT_ALIGNMENT_CENTER|wx.TE_PASSWORD)
        self.passValue.SetFont(font)
        self.clear = wx.Button(panel, id=wx.ID_ANY, label="清 空", pos=(70, 100), size=(100, 30))
        font2 = wx.Font(12, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.LIGHT, underline=False)
        self.clear.SetFont(font2)
        self.clear.Bind(wx.EVT_BUTTON, self.Onclickclear)

        self.sign = wx.Button(panel, id=wx.ID_ANY, label="一键打卡", pos=(210, 100), size=(100, 30),style=wx.TE_PROCESS_ENTER)
        self.sign.SetFont(font2)
        self.sign.Bind(wx.EVT_BUTTON, self.Onclicksign)
        self.searcher = wx.CheckBox(panel, id=wx.ID_ANY, label="打开浏览器", pos=(350, 100), size=(120, 30))
        font3 = wx.Font(15, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.LIGHT, underline=True)
        self.searcher.SetFont(font3)
        # self.searcher.Bind(wx.EVT_BUTTON, self.Onclickhighersearch)
        # 设计状态栏
        self.statusbar = self.CreateStatusBar()
        self.SetStatusText("打卡网址：http://xmuxg.xmu.edu.cn/xmu/app/214   仅供本网站每日打卡", 0)
        self.nameValue.SetStringSelection(self.nameValue.GetValue())
        self.nameValue.Bind(wx.EVT_TEXT_ENTER,self.Onclicksign)

        if os.path.exists(filename):
            with open(filename,'r',encoding="utf-8") as file:
                a =file.readlines()
                for i in range(len(a)):
                    p = a[i].replace("\n","").split(" ")
                    TvalueChoice.append(p[0])
                    PvalueChoice.append(p[1])
                    self.nameValue.Append(p[0])
                    self.passValue.Append(p[1])

                    self.nameValue.SetValue(p[0])
                    self.passValue.SetValue(p[1])
        self.Bind(wx.EVT_COMBOBOX,self.OnEnter,self.nameValue)
    def Onclickclear(self,event):
        self.nameValue.SetValue("")
        self.passValue.SetValue("")
    def Onclicksign(self,event):
        try:
            if self.searcher.IsChecked():
                browser = webdriver.Chrome(executable_path=PATH)
            else:
                chromeopt = webdriver.ChromeOptions()
                chromeopt.add_argument('--headless')
                browser = webdriver.Chrome(options=chromeopt,executable_path=PATH)
            time.sleep(2)  # 给予浏览器时间响应
            browser.get(url)
            # browser.maximize_window()
            #print("Cookies：", browser.get_cookies())  # 打印看一下Cookies
            usr = self.nameValue.GetValue()
            password = self.passValue.GetValue()
            if  usr not in TvalueChoice or password not in PvalueChoice:
                with open(filename,'w+',encoding="utf-8") as file:
                    st = usr+" "+password+"\n"
                    file.write(st)

            firstlog(usr, password,browser)
            operator(browser)
        except Exception as e:
            wx.MessageBox(str(e),"打卡异常！")

    def OnEnter(self,event):
        for i in range(len(TvalueChoice)):
            if TvalueChoice[i] == self.nameValue.GetValue():
                self.passValue.SetValue(PvalueChoice[i])


    # def Onclickhighersearch(self,event):
    #     pass
if __name__ =='__main__':
    app = wx.App()
    frame = MyFrame(parent=None, id=-1)
    #frame.Bind(wx.EVT_CLOSE,frame.OnclickExit)#对象中绑定关闭系统
    frame.SetMaxSize(wx.Size(680, 650))
    frame.Center()
    frame.Show()
    app.MainLoop()
