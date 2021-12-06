from contextlib import nullcontext
from warnings import catch_warnings
import scrapy
from scrapy.loader import ItemLoader

from fiverr.items import FiverrItem

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FiverrSpider(scrapy.Spider):
    name = "fiverr"
    allowed_domains = ["fiverr.com"]
    start_urls = ['https://www.fiverr.com/categories/programming-tech/wordpress-services?source=pagination&pos=2&name=wordpress-services&page=1']

    def parse(self, response):

        self.logger.info('Parse function called on {}'.format(response.url))

        # getting all the companies on the page
        freelancers = response.css('#main-wrapper > div.main-content > div.search_perseus > div > div > div.logo-design-flow > div.layout-row.content-row > div > div > div > div > div > div > div.seller-info.text-body-2 > div > div > div > div > a')

        self.logger.info('CYCLING FREELANCERS ON THE PAGE')

        for freelancer in freelancers:

            # get freelancer url
            freelancer_fiverr_url = freelancer.css('a::attr(href)').get().split("?", 1)[0]

            # go to the freelancer page
            yield response.follow(freelancer_fiverr_url, self.parse_freelancer)

        # go to Next page with freelancers
        for a in response.css('#pagination > li:nth-child(12) > aa'):
            url = a[0].get_attribute('href')
            yield response.follow(url, self.parse)

    def parse_freelancer(self, response):

        #DRIVER START
        path = 'fiverr\driver\chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument("-headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(executable_path=path, desired_capabilities=desired_capabilities)
        driver.get(response.request.url)
        # Implicit wait
        driver.implicitly_wait(10)
        # Explicit wait
        wait = WebDriverWait(driver, 10)
        #DRIVER
        
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.username-line > a")))
            username = driver.find_elements_by_css_selector("div.username-line > a")
            username = username[0].get_attribute('outerText')
        except:
            username = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.user-profile-label > div.oneliner-wrapper > div.liner-and-pen > span")))
            oneliner = driver.find_elements_by_css_selector("div.user-profile-label > div.oneliner-wrapper > div.liner-and-pen > span")
            oneliner = oneliner[0].get_attribute('outerText')
        except:
            oneliner = ''
        
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ratings-wrapper > div > div > b")))
            rating = driver.find_elements_by_css_selector("div.ratings-wrapper > div > div > b")
            rating = rating[0].get_attribute('outerText')
        except:
            rating = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.location > b")))
            location = driver.find_elements_by_css_selector("li.location > b")
            location = location[0].get_attribute('outerText')
        except:
            location = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.member-since > b")))
            member_since = driver.find_elements_by_css_selector("li.member-since > b")
            member_since = member_since[0].get_attribute('outerText')
        except:
            member_since = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.response-time > b")))
            response_time_average = driver.find_elements_by_css_selector("li.response-time > b")
            response_time_average = response_time_average[0].get_attribute('outerText')
        except:
            response_time_average = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.recent-delivery > strong")))
            recent_delivery_time = driver.find_elements_by_css_selector("li.recent-delivery > strong")
            recent_delivery_time = recent_delivery_time[0].get_attribute('outerText')
        except:
            recent_delivery_time = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.description > p")))
            description = driver.find_elements_by_css_selector("div.description > p")
            description = description[0].get_attribute('outerText')
        except:
            description = ''
        
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.languages > ul > li")))
            lenguages = driver.find_elements_by_css_selector("div.languages > ul > li")
            for l in lenguages:
                user_lenguages = ",".join(l[0].get_attribute('outerText'))
        except:
            user_lenguages = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.skills > ul > li")))
            skills = driver.find_elements_by_css_selector("div.skills > ul > li")
            for s in skills:
                user_skills = ",".join(s[0].get_attribute('outerText'))
        except:
            user_skills = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.education-list.list > ul > li > p:nth-child(1)")))
            education_highest = driver.find_elements_by_css_selector("div.education-list.list > ul > li > p:nth-child(1)")
            education_highest = education_highest[0].get_attribute('outerText')
        except:
            education_highest = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div:nth-child(7) > ul > li > p:nth-child(1)")))
            certifications = driver.find_elements_by_css_selector("div:nth-child(7) > ul > li > p:nth-child(1)")
            user_certifications = ",".join(certifications.get_attribute('outerText'))
        except:
            user_certifications = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "footer > a > span")))
            prices = driver.find_elements_by_css_selector("footer > a > span")
            average = 0
            for p in prices:
                average += p[0].get_attribute('outerText')[1:]
            avg_price = average / len(prices)
        except:
            avg_price = ''

        
        

        loader = ItemLoader(item=FiverrItem(), response=response)
        loader.add_value('username', username)
        loader.add_value('oneliner', oneliner)
        loader.add_value('rating', rating)
        loader.add_value('location', location)
        loader.add_value('member_since', member_since)
        loader.add_value('response_time_average', response_time_average)
        loader.add_value('recent_delivery_time', recent_delivery_time)
        loader.add_value('user_lenguages', user_lenguages)
        loader.add_value('user_skills', user_skills)
        loader.add_value('education_highest', education_highest)
        loader.add_value('user_certifications', user_certifications)
        loader.add_value('avg_price', avg_price)
        yield loader.load_item()