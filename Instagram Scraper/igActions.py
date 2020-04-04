from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

class InstaBot:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.followers=0
        self.following=0

        #must have chromedriver installed and specify installation path (I use chrome, but could also use firefox)
        self.bot=webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver')

    def closeBot(self):
        self.bot.close()

    def login(self):
        bot=self.bot
        bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(5)
        email=bot.find_element_by_name('username')
        password=bot.find_element_by_name('password')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

    def like_hashtag(self,hashtag):
        liked=0
        bot=self.bot
        bot.get('https://www.instagram.com/explore/tags/'+hashtag+'/')
        time.sleep(2)

        #simulate scroll down
        for i in range(1,20):
            bot.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(1)

        #get the links
        hrefs=bot.find_elements_by_tag_name('a')
        pic_hrefs=[elem.get_attribute('href') for elem in hrefs]
        pic_hrefs=[href for href in pic_hrefs if 'p' in href.split('/')]

        for pic_href in pic_hrefs:
            bot.get(pic_href)
            bot.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            try:
                time.sleep(random.randint(2,5))

                #might need to find a better way to look for the Like button
                bot.find_element_by_class_name("wpO6b").click()
                time.sleep(random.randint(60,65))   #instagram ramped up its likes per hour
                liked+=1
                print("Liked: "+str(liked))
            except Exception as e:
                print("exception")
                time.sleep(2)

    def get_user_followers(self,username):
        bot=self.bot
        bot.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        sugs=self.bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
        time.sleep(1)
        scroll_box=self.bot.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        last_ht,ht=0,1
        while last_ht != ht:
            last_ht=ht
            time.sleep(1)
            ht=self.bot.execute_script("""
            arguments[0].scrollTo(0,arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """,scroll_box)

        #get actual followers
        links=scroll_box.find_elements_by_tag_name('a')
        temp=[user.text for user in links if user != '']
        followers=[]
        for i in temp:
            if i!='':
                followers.append(i)
        return followers


    def follow_followers(self,username):
        #load the followers
        followers=self.get_followers(username)
        bot = self.bot
        followed=0
        for i in followers:
            try:
                if followed<10:    #10 is the limit per hour
                    bot.get('https://www.instagram.com/' + i + '/')
                    time.sleep(3)
                    follow_link=bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]')
                    follow_link.click()
                    time.sleep(2)
                    followed+=1
                else:
                    followed=0       #reset the followed count
                    time.sleep(3600) #wait an hour before continuing to follow
            except:
                print('exception')

    def get_following(self):
        bot=self.bot
        bot.get('https://www.instagram.com/'+self.username+'/')
        time.sleep(3)
        sugs=bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
        time.sleep(1)
        scroll_box = self.bot.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            time.sleep(1)
            ht = self.bot.execute_script("""
                    arguments[0].scrollTo(0,arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, scroll_box)

        # get following
        links = scroll_box.find_elements_by_tag_name('a')
        temp = [user.text for user in links if user != '']
        following = []
        for i in temp:
            if i != '':
                following.append(i)
        self.following=following
        return following


    def unfollow(self):
        "Unfollows all followers from account"
        if self.following==0:
            following=self.get_following()
        if len(following)==0:
            print("Not following any accounts")
            return
        bot = self.bot
        unfollowed = 0
        total=0
        while len(following)!=0:
            for i in following :
                try :
                    if unfollowed < 10 :  # 10 is the limit per hour
                        bot.get('https://www.instagram.com/' + i + '/')
                        time.sleep(3)
                        unfollow_link = bot.find_element_by_xpath(
                            '/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button')
                        unfollow_link.click()
                        time.sleep(2)
                        # a new window will pop up, so click 'unfollow' on that as well
                        bot.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[1]').click()
                        time.sleep(random.randint(2, 5))
                        unfollowed += 1
                        total += 1
                        print('Unfollowed ' + str(i) + ' Total Unfollowed: ' + str(total))
                        following.remove(i)
                    else :
                        unfollowed = 0  # reset the followed count
                        print("Waiting 1 hour...")
                        time.sleep(3600)  # wait an hour before continuing to follow
                except :
                    print('exception')


    def getPostLikers(self,url):
        bot = self.bot
        bot.get(url)
        time.sleep(2)
        bot.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[2]/div/div/button').click()
        time.sleep(1)
        scroll_box = self.bot.find_element_by_xpath('/html/body/div[4]/div/div[2]/div')
        last_ht, ht = 0, 1
        x=[]
        while last_ht != ht:
            last_ht = ht
            time.sleep(1)
            links = scroll_box.find_elements_by_tag_name('a')
            for element in links:
                item=element.get_attribute('title')
                if item not in x and item!='':
                    x.append(element.get_attribute('title'))
            ht = self.bot.execute_script("""
                    arguments[0].scrollTo(0,arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, scroll_box)
            time.sleep(2)
        print(x)
        print(len(x))
        return x

    def follow_likers(self,url):
        likers=self.getPostLikers(url)
        bot = self.bot
        followed = 0
        for i in likers:
            try:
                if followed < 10:  # 10 is the limit per hour
                    bot.get('https://www.instagram.com/' + i + '/')
                    time.sleep(3)
                    #some accounts will be private, hence the ternary operator
                    follow_link = bot.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]') if bot.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]') else bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/button')
                    follow_link.click()
                    time.sleep(2)
                    followed += 1
                    print('Followed: '+str(followed)+' users')
                else:
                    followed = 0  # reset the followed count
                    time.sleep(3600)  # wait an hour before continuing to follow
            except:
                print('exception')


if __name__=="__main__":
    username=""
    password=""
    obj=InstaBot(username,password)
    obj.login()
    obj.unfollow()

