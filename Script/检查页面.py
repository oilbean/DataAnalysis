#coding:utf-8
from selenium import webdriver
import logging
import os
import shutil
import traceback
import time


logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)

#输出到屏幕
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
#输出到文件
fh = logging.FileHandler(".log")
fh.setLevel(logging.INFO)
#设置日志格式
fomatter = logging.Formatter('%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s')
ch.setFormatter(fomatter)
fh.setFormatter(fomatter)
logger.addHandler(ch)
logger.addHandler(fh)


shutil.rmtree("./screen")
os.mkdir("./screen")

browser=webdriver.Ie()
url="url"
browser.get(url)
browser.maximize_window()
browser.implicitly_wait(15)
browser.find_element_by_name("currentuserid").clear()
browser.find_element_by_name("currentuserid").send_keys('')
browser.find_element_by_name("password").send_keys('')
browser.find_element_by_id("login_bt").click()

failcount =0

data = open('menu','r',encoding="UTF-8")
logger.info("获取查询目录")

while True:
    page=data.readline().strip()
    browser.switch_to_default_content()
    if page:
        if page.startswith("#"):
            browser.find_element_by_xpath("//span[contains(text(),'" + page[1:] + "' )]").click()
            logger.info("点击主菜单："+ page[1:] +"")
            continue

        try:
            logger.info("点击菜单：" + page + "")
            browser.find_element_by_xpath("//span[contains(text(),'"+page+"' )]").click()
        except :
            logger.exception("未找到菜单："+page)
            failcount = failcount + 1
            browser.get_screenshot_as_file("./screen" + "/" + page + ".png")
            continue

        try:
            iframe= browser.find_element_by_xpath("//div[@class=' x-panel x-panel-noborder']//div[@class='x-panel-bwrap']//div[@class=' x-panel x-panel-noborder']//iframe[contains(@id,'frame_')]")
            logger.info("进入’"+page+"‘验证页面")
            browser.switch_to_frame(iframe)

            logger.info(page + "验证’查询‘按钮")
            b=browser.find_element_by_xpath("//button[contains(@id,'button_query')]").text


            if b != "查询":
                logger.error(page  +" 未查询到 ‘查询’ 按钮")
                failcount = failcount + 1
                browser.get_screenshot_as_file("./screen" + "/" + page + ".png")
        except:
            failcount = failcount +1
            logger.exception(page+"获取元素失败")
            browser.get_screenshot_as_file("./screen" + "/" + page + ".png")

    else:
        browser.quit()
        logger.info("关闭浏览器")
        break


if failcount > 0 :
    exit(1)



