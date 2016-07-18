import argparse
import os
import time
import urlparse
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup



def get_people_links(page):
    '''
    in this method we are passing in a web page. The firs for loop looks for all the url's on a web page. if the url
    contains 'profile/view?id=' it is a user url and we add it to the array of user URLs

    :param page: this is a web page wew are searching for user links
    :return: we are returning an array of user links
    '''
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if 'profile/view?id=' in url:
                links.append(url)
    return links


'''
    ADD A METHOD THAT GOES TO THE PEOPLE YOU MAY KNOW PAGE TO GET MORE PEOPLE TO LOOK AT
'''

def get_ppl_may_know(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if '/people/pymk' in url:
                links.append(url)
    return links


def get_job_links(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if '/jobs' in url:
                links.append(url)
    return links


def get_ID(url):
    '''
    this method takes in the url of the person we are looking at and and first first parses the URL. then we query the
    elements of the URL and return the ID.

    :param url: the URL of the user we are looking at
    :return: the ID of the user whose url we are looking at
    '''
    parsed_url = urlparse.urlparse(url)
    return urlparse.parse_qs(parsed_url.query)['id'][0]


def view_bot(browser):
    visited = {}
    visit_plan = []
    visit_count = 0

    while True:
        #sleep for a bit to make sure everything load
        # we will add a random amount of time to make us look human

        time.sleep(random.uniform(3, 9))
        page = BeautifulSoup(browser.page_source)
        people = get_people_links(page)
        if people:
            for person in people:
                ID = get_ID(person)
                if ID not in visited:
                    visit_plan.append(person)
                    visited[ID] = 1
        if visit_plan: #if there are people to visit, then look at them
            person = visit_plan.pop()
            browser.get(person)
            visit_count += 1
            # gat all people on this page and add them to the to visit list
        else: # otherwise find people to visit
            # here we should call the method that goes to the people you may know page
            pymk = '/people/pymk'
            pymk_page = 'https://www.linkedin.com'+pymk
            browser.get(pymk_page)
            page_source = BeautifulSoup(browser.page_source)
            people.extend(get_people_links(page_source))


            if people:
                for person in people:
                    ID = get_ID(person)
                    if ID not in visited:
                        visit_plan.append(person)
                        visited[ID] = 1

        print "[+] " + browser.title +  " visited \n (" + str(visit_count) + '/'+str(len(visit_plan)) + ")visited/queue"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("email", help='linkedin email')
    parser.add_argument("password", help='linkedin password')
    args = parser.parse_args()

    browser = webdriver.Firefox()
    print "here"
    browser.get('https://www.linkedin.com/uas/login')
    print 'there'

    email_element = browser.find_element_by_id('session_key-login')
    email_element.send_keys(args.email)
    pass_element =  browser.find_element_by_id('session_password-login')
    pass_element.send_keys(args.password)
    pass_element.submit()

    os.system('clear')
    print '[+] successfully logged in! Bot is starting'

    view_bot(browser)
    browser.close()


print 'hey'
main()
