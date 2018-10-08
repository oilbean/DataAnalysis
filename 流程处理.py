# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import loginOa
import os
import traceback
import td
import utils

#设置自定义浏览器
profile_dir='C:\\Users\\Think\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\gppwwoo0.default'
profile = webdriver.FirefoxProfile(profile_dir)

#登陆系统
brower=webdriver.Firefox(profile)
utils.Util.env['driver']= brower
url='http://172.32.0.132/middlecenter/index.jsp'
brower.get(url)
loginOa.login('sysadmin','1')
time.sleep(3)
brower.get(url)
time.sleep(3)
#流程节点名称
processname = []
#存在执行结果
dict={}
#期望结果
expect=['用人部门负责人','部门负责人','分管负责人','人力资源副总裁','HRBP确认']
dict1={'2170':expect}

#流程操作
def roll(employ_id,logger,basedir):
        logger.write("############")
        brower.find_element_by_xpath("//span[contains(text(),'流程引擎')]").click()
        time.sleep(1)
        brower.find_element_by_xpath("//li[contains(text(),'路径管理')]").click()
        time.sleep(1)
        brower.find_element_by_xpath("//span[contains(text(),'流程测试')]").click()
        brower.find_element_by_xpath("//span[contains(text(),'新建测试流程')]").click()
        time.sleep(2)
        brower.switch_to.frame('mainFrame')
        brower.find_element_by_xpath("//form//div/a[contains(text(),'离职流程')]").click()
        time.sleep(1)
        # 离职申请
        brower.switch_to.default_content();
        frama = brower.find_element_by_xpath("//iframe[contains(@id,'Dialog')]")
        brower.switch_to.frame(frama)
        time.sleep(1)
        brower.execute_script('document.getElementById("createrid").value='+employ_id)

        brower.find_element_by_xpath("//input[@title='确定']").click()

        #调转至离职理由frome
        time.sleep(3)

        td.switch_to('mainFrame','jd_iframe','bodyiframe')

        time.sleep(3)

        brower.find_element_by_xpath("//textarea[@ temptitle='离职理由']").send_keys('hahahah')

        td.switch_to('mainFrame','jd_iframe')

        time.sleep(1)
        brower.find_element_by_xpath("//input[@title='提交']").click()
        print('提交')
        brower.implicitly_wait(15)
        time.sleep(5)

        # 用人部门负责人
        # brower.switch_to.default_content();
        # 填写签字意见
        # brower.switch_to.frame('mainFrame')
        # print('mainframe')
        # brower.switch_to.frame('jd_iframe')
        # print('jd_iframe')
        # brower.switch_to.frame('bodyiframe')
        # print('bodyiframe')
        #
        # # qianzi= brower.find_element_by_xpath("//iframe[contains(@id,'ueditor')]")
        # # brower.find_element_by_id('remarkShadowDivInnerDiv').click()
        # #
        # # brower.switch_to.frame('ueditor_0')
        # #
        # # brower.execute_script('document.getElementsByTagName("span").innerText="大大大大"')

        # # brower.find_element_by_xpath("//div[@title='签字意见']").send_keys('ddd')
        # print('签字意见')
        brower.implicitly_wait(10)

        td.switch_to("mainFrame","jd_iframe")

        brower.implicitly_wait(10)
        time.sleep(1)

        #点击批准按钮至批准结束
        while True:
            #获取按钮名称
            a = brower.find_element_by_xpath("//input[@class='e8_btn_top_first']").get_attribute('title')
            #验证流程是否报错
            td.switch_to("mainFrame","jd_iframe","bodyiframe")

            b = brower.page_source.find('流程提交失败')
            print(b)

            td.switch_to("mainFrame", "jd_iframe")

            nodename = brower.find_element_by_id("objName").text[15:]

            processname.append(nodename)

            brower.implicitly_wait(10)
            time.sleep(1)

            if a=="批准" and b==-1:

                # print("###########" +brower.find_element_by_class_name("e8_btn_top_first").get_attribute('title'))
                brower.find_element_by_xpath("//input[@class='e8_btn_top_first']").click()

                time.sleep(5)
            elif b!=-1:

                td.switch_to("mainFrame")

                js = "document.documentElement.scrollLeft=0"
                brower.execute_script(js)
                brower.get_screenshot_as_file(basedir + "/" + str(int(time.time())) + ".png")
                break
            else:
                print('结束')

                # 跳转至流程状态页面截图
                brower.find_element_by_xpath("//span[contains(text(),'流程状态')]").click()

                time.sleep(3)

                td.switch_to("mainFrame", "jd_iframe","statiframe")
                m = brower.find_element_by_xpath('//iframe[@class="flowFrame"]').get_attribute('src')

                #打开新窗口并截图
                nowhandle = brower.current_window_handle
                js = 'window.open();'
                brower.execute_script(js)

                for handler in brower.window_handles:
                    if handler != nowhandle:
                        brower.switch_to_window(handler)
                        break

                brower.get(m)

                time.sleep(2)
                brower.get_screenshot_as_file(basedir + "/" + str(int(time.time())) + ".png")
                brower.close()
                brower.switch_to_window(nowhandle)
                break
#读取文件
data = open('aa','r')

#已时间戳命名文件名
file_name =str(int(time.time()))
os.mkdir(file_name)

while True:
    id = data.readline().strip()
    dict[id]=None
    print(dict)
    print("########################" + id)
    if id:
        os.mkdir(file_name + "/" + id)
        base_path = file_name + "/" + id
        log_handler = open(base_path + "/" + "log", 'w')
        try:
            brower.switch_to_default_content()
            roll(id,log_handler,base_path)
        except:
            f=log_handler
            traceback.print_exc(file=f)
            traceback.print_exc()
        finally:
            dict[id] = processname
            if id in dict1.keys():
                print(dict[id])
                td.compare(dict[id], dict1[id])
    else:
        break
    log_handler.flush()
    log_handler.close()

data.close()
