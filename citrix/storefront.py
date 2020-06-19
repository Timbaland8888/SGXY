
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://172.16.56.33/Citrix/StoreWeb")  # 打开浏览器
time.sleep(1)
driver.find_element_by_xpath('//*[@id="protocolhandler-welcome"]/div/div/div/div/a').click()
time.sleep(2)


# js = 'document.getElementById("protocolhandler-welcome").style.display="none";'
# driver.execute_script(js)

# ## 导入cookie
# driver.add_cookie({'name':'csrftoken','value':'450FFDDA6A72EF25E399DEBEF0E31634','name':'CtxsClientAlreadyInstalled','value':'true','name':'CtxsClientDetectionDone','value':'true','name':'csrftoken','value':'737E41EEC4ECD3EFB2A6611CB48F7297'})
# # driver.add_cookie({'CsrfToken':'361DF1E4B2B5E252264540DDC13D8864','CtxsClientAlreadyInstalled':'true','CtxsClientDetectionDone':'true'})
#
#
# ## 刷新页面
# driver.refresh()
#
# driver.find_element_by_link_text("登录").click()
#
#
# time.sleep(30)

#关闭浏览器
# driver.quit()