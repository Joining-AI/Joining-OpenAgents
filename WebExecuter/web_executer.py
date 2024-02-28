import requests
from bs4 import BeautifulSoup
import webbrowser
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException

class WebSearch:
    def __init__(self, search_engine='bing'):
        self.search_engine = search_engine

    def search(self, query):
        if self.search_engine == 'google':
            url = f"https://www.google.com/search?q={query}"
        elif self.search_engine == 'bing':
            url = f"https://www.bing.com/search?q={query}"
        else:
            raise ValueError("Unsupported search engine")

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'lxml')
            print(response)
            # Google search
            if self.search_engine == 'google':
                search_results = soup.find_all('div', class_='g')
                if search_results:
                    titles, links = [], []
                    for result_ in search_results[:10]:
                        titles.append(result_.find('h3').get_text())
                        links.append(result_.find('a')['href'])
                    return titles, links

            # Bing search
            elif self.search_engine == 'bing':
                search_results = soup.find_all('li', class_='b_algo')
                if search_results:
                    titles, links = [], []
                    for result_ in search_results[:10]:
                        titles.append(result_.find('h2').get_text())
                        links.append(result_.find('a')['href'])
                    return titles, links

            return None, None

        except Exception as e:
            print("An error occurred:", e)
            return None, None

class BrowserExecute:
    def __init__(self, driver_path):
        # 初始化浏览器驱动
        self.edge_service = webdriver.EdgeService(executable_path=driver_path)
        self.browser = webdriver.Edge(service=self.edge_service)
        self.base_url = 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=%E6%81%92%E5%A4%A7'

    def open_new_tab(self, url):
        # 打开新的 Tab
        self.browser.execute_script("window.open('', '_blank');")
        # 切换到新 Tab
        self.browser.switch_to.window(self.browser.window_handles[-1])
        # 打开指定的url
        self.browser.get(url)

    def close_current_tab(self):
        # 关闭当前 Tab
        self.browser.close()
        # 切换回主 Tab
        self.browser.switch_to.window(self.browser.window_handles[0])

    def page_turn(self):
        try:
            time.sleep(1)
            next_button = self.browser.find_element(By.XPATH, '//*[@id="fulltext-search"]/div[2]/div/div/div[2]/div[4]/div[2]/div/button[2]')
            disabled_value = next_button.get_attribute("disabled")
            print(f"Disabled attribute value: {disabled_value}")
            if disabled_value:
                print("无法翻页已经达到最后一页")
                return 1
            else:
                next_button.click()
                time.sleep(1)
                data = self.browser.page_source
                print("执行翻页操作")
                return data
        except NoSuchElementException as e:
            print(f"发生异常: {e}")
            return None

    def search(self, data):
        # 解析网页标题
        p_title = r'<span[^>]*class="r-title"[^>]*>(.*?)</span>'
        titles = re.findall(p_title, data)
        
        # 解析网页网址
        p_href = r'<a target="_blank" href="(.*?)" data-id='
        hrefs = re.findall(p_href, data)
        
        # 解析发布时间
        p_time = re.compile(r'<span class="time">\s*([\d-]+\s*[\d:]*\s*)</span>')
        times = re.findall(p_time, data)
        
        for index, href in enumerate(hrefs):
            # 网址清理
            cleaned_href = 'http://www.cninfo.com.cn' + re.sub('amp;', '', href)
            
            # 解析时间，确保时间格式正确
            try:
                parsed_date = datetime.strptime(times[index].strip(), "%Y-%m-%d %H:%M")
            except ValueError:
                print(f"时间解析错误: {times[index]}")
                continue
            
            # 确认时间在设定范围内
            if parsed_date >= datetime(2024, 2, 7, 0, 0):
                print(f"正在下载: {titles[index]}")
                # 下载PDF文件，这里仅显示下载逻辑的占位符
                self.download_pdf(cleaned_href, titles[index])

    def download_pdf(self, url, title):
        # 假设的下载PDF文件的方法
        try:
            # 实际下载逻辑
            response = requests.get(url)
            filename = f"{title}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"下载成功: {filename}")
        except Exception as e:
            print(f"下载失败: {e}")

    def start_scraping(self):
        self.browser.get(self.base_url)
        time.sleep(1)
        data = self.browser.page_source
        self.search(data)
        while True:
            data = self.page_turn()
            if data == 1:
                print("爬取完毕")
                break
            self.search(data)