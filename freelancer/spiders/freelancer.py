from contextlib import nullcontext
from warnings import catch_warnings
import scrapy
from scrapy.loader import ItemLoader

from freelancer.items import FreelancerItem

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time 



class FreelancerSpider(scrapy.Spider):
    name = "freelancer"
    allowed_domains = ["freelancer.com"]
    start_urls = ['https://www.freelancer.com/freelancers/skills/php-website-design-graphic-design-html']

    def parse(self, response):

        self.logger.info('Parse function called on {}'.format(response.url))

        # getting all the companies on the page
        freelancers = response.css('#freelancer_list > div > li > div > div.freelancer-details-header > h3 > a.find-freelancer-username')

        self.logger.info('CYCLING FREELANCERS ON THE PAGE')

        for freelancer in freelancers:

            # get freelancer url
            freelancers_url = freelancer.css('a::attr(href)').get()

            # go to the freelancer page
            yield response.follow(freelancers_url, self.parse_freelancer)

        # go to Next page with freelancers
        for a in response.css('#display_div > div:nth-child(10) > div > ul > li:nth-child(7) > a'):
            yield response.follow(a, self.parse)

    def parse_freelancer(self, response):

        #DRIVER START
        path = 'freelancer\driver\chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path=path, options=options)
        self.driver.get(response.request.url)
        # Implicit wait
        self.driver.implicitly_wait(1)
        # Explicit wait
        wait = WebDriverWait(self.driver, 1)
        #DRIVER
        
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "fl-username > fl-bit:nth-child(2) > fl-heading > h3")))
            username = self.driver.find_elements_by_css_selector("fl-username > fl-bit:nth-child(2) > fl-heading > h3")
            username = username[0].get_attribute('outerText')
        except:
            username = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "app-user-profile-summary-tagline > fl-heading > h2")))
            oneliner = self.driver.find_elements_by_css_selector("app-user-profile-summary-tagline > fl-heading > h2")
            oneliner = oneliner[0].get_attribute('outerText')
        except:
            oneliner = ''
        
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "app-user-profile-summary-rating > fl-bit > fl-tooltip:nth-child(1) > fl-bit > span > span > fl-rating > fl-bit > fl-bit.ValueBlock.ng-star-inserted")))
            rating = self.driver.find_elements_by_css_selector("app-user-profile-summary-rating > fl-bit > fl-tooltip:nth-child(1) > fl-bit > span > span > fl-rating > fl-bit > fl-bit.ValueBlock.ng-star-inserted")
            rating = rating[0].get_attribute('outerText')
        except:
            rating = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(2) > fl-grid > fl-col:nth-child(2) > app-user-profile-summary-information > fl-grid > fl-col > fl-text > div > fl-link > a")))
            location = self.driver.find_elements_by_css_selector("app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(2) > fl-grid > fl-col:nth-child(2) > app-user-profile-summary-information > fl-grid > fl-col > fl-text > div > fl-link > a")
            location = location[0].get_attribute('outerText')
        except:
            location = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "app-user-profile-summary-extra-info > fl-grid:nth-child(2) > fl-col:nth-child(2) > fl-text > div")))
            member_since = self.driver.find_elements_by_css_selector("app-user-profile-summary-extra-info > fl-grid:nth-child(2) > fl-col:nth-child(2) > fl-text > div")
            member_since = member_since[0].get_attribute('outerText')
        except:
            member_since = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "fl-grid > fl-col:nth-child(4) > app-user-profile-summary-reputation > fl-bit > fl-bit > fl-grid > fl-col:nth-child(1) > app-user-profile-summary-reputation-item > fl-bit > fl-text.ReputationItemAmount > div")))
            jobs_completed_rate = self.driver.find_elements_by_css_selector("fl-grid > fl-col:nth-child(4) > app-user-profile-summary-reputation > fl-bit > fl-bit > fl-grid > fl-col:nth-child(1) > app-user-profile-summary-reputation-item > fl-bit > fl-text.ReputationItemAmount > div")
            jobs_completed_rate = jobs_completed_rate[0].get_attribute('outerText')
        except:
            jobs_completed_rate = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > app-root > app-logged-out-shell > app-user-profile-wrapper > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col:nth-child(2) > app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > fl-grid > fl-col:nth-child(4) > app-user-profile-summary-reputation > fl-bit > fl-bit > fl-grid > fl-col:nth-child(2) > app-user-profile-summary-reputation-item > fl-bit > fl-text.ReputationItemAmount > div")))
            on_budget_completed_rate = self.driver.find_elements_by_css_selector("body > app-root > app-logged-out-shell > app-user-profile-wrapper > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col:nth-child(2) > app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > fl-grid > fl-col:nth-child(4) > app-user-profile-summary-reputation > fl-bit > fl-bit > fl-grid > fl-col:nth-child(2) > app-user-profile-summary-reputation-item > fl-bit > fl-text.ReputationItemAmount > div")
            on_budget_completed_rate = on_budget_completed_rate[0].get_attribute('outerText')
        except:
            on_budget_completed_rate = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "fl-col:nth-child(4) > app-user-profile-summary-reputation > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > app-user-profile-summary-reputation-item > fl-bit > fl-text.ReputationItemAmount > div")))
            on_time_rate = self.driver.find_elements_by_css_selector("fl-col:nth-child(4) > app-user-profile-summary-reputation > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > app-user-profile-summary-reputation-item > fl-bit > fl-text.ReputationItemAmount > div")
            on_time_rate = on_time_rate[0].get_attribute('outerText')
        except:
            on_time_rate = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "fl-col:nth-child(4) > app-user-profile-summary-reputation-item > fl-bit > fl-text.ReputationItemAmount > div")))
            repeat_hire_rate = self.driver.find_elements_by_css_selector("fl-col:nth-child(4) > app-user-profile-summary-reputation-item > fl-bit > fl-text.ReputationItemAmount > div")
            repeat_hire_rate = repeat_hire_rate[0].get_attribute('outerText')
        except:
            repeat_hire_rate = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "app-user-profile-summary-description > fl-text > div")))
            description = self.driver.find_elements_by_css_selector("app-user-profile-summary-description > fl-text > div")
            description = description[0].get_attribute('outerText')
        except:
            description = ''

        try:
            i=0
            # expanding list
            while i<1:
                try:
                        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col.ng-star-inserted > app-user-profile-exams > fl-card > fl-bit > fl-bit.CardBody > fl-bit > fl-link > button')))
                        element.click()
                        i = i+1
                except:
                    break

            # extracting certifications
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "app-user-profile-exams > fl-card > fl-bit > fl-bit.CardBody > fl-list > fl-list-item > fl-bit > fl-bit > fl-bit.BitsListItemHeader > fl-bit.BitsListItemContent.ng-star-inserted > fl-bit > fl-bit > fl-text > span")))
            certifications = self.driver.find_elements_by_css_selector("app-user-profile-exams > fl-card > fl-bit > fl-bit.CardBody > fl-list > fl-list-item > fl-bit > fl-bit > fl-bit.BitsListItemHeader > fl-bit.BitsListItemContent.ng-star-inserted > fl-bit > fl-bit > fl-text > span")
            user_certifications = ''
            for c in certifications:
                user_certifications = user_certifications + c.get_attribute('outerText') + ', '
        except:
            user_certifications = ''

        try:
            # expanding list
            while True:
                try:
                        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > app-root > app-logged-out-shell > app-user-profile-wrapper > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col.ng-star-inserted > app-user-profile-skills > fl-card > fl-bit > fl-bit.CardBody > fl-link > button')))
                        element.click()
                except:
                    break

            # extracting skills
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "app-user-profile-skills > fl-card > fl-bit > fl-bit.CardBody > fl-list > fl-list-item > fl-bit > fl-bit > fl-bit.BitsListItemHeader > fl-bit.BitsListItemContent.ng-star-inserted > app-user-profile-skills-item > fl-bit > fl-bit > fl-link")))
            skills = self.driver.find_elements_by_css_selector("app-user-profile-skills > fl-card > fl-bit > fl-bit.CardBody > fl-list > fl-list-item > fl-bit > fl-bit > fl-bit.BitsListItemHeader > fl-bit.BitsListItemContent.ng-star-inserted > app-user-profile-skills-item > fl-bit > fl-bit > fl-link")
            user_skills = ''
            for s in skills:
                user_skills = user_skills + s.get_attribute('outerText') + ', '
        except:
            user_skills = ''

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "fl-grid > fl-col:nth-child(2) > app-user-profile-summary-information > fl-bit:nth-child(1) > fl-bit > fl-bit > fl-text > div")))
            price_per_hour = self.driver.find_elements_by_css_selector("fl-grid > fl-col:nth-child(2) > app-user-profile-summary-information > fl-bit:nth-child(1) > fl-bit > fl-bit > fl-text > div")
            price_per_hour = price_per_hour[0].get_attribute('outerText')
        except:
            price_per_hour = ''

        
        

        loader = ItemLoader(item=FreelancerItem(), response=response)
        loader.add_value('username', username)
        loader.add_value('oneliner', oneliner)
        loader.add_value('rating', rating)
        loader.add_value('location', location)
        loader.add_value('member_since', member_since)
        loader.add_value('on_budget_completed_rate', on_budget_completed_rate)
        loader.add_value('on_time_rate', on_time_rate)
        loader.add_value('repeat_hire_rate', repeat_hire_rate)
        loader.add_value('jobs_completed_rate', jobs_completed_rate)
        loader.add_value('user_skills', user_skills)
        loader.add_value('user_certifications', user_certifications)
        loader.add_value('price_per_hour', price_per_hour)
        loader.add_value('description', description)
        yield loader.load_item()