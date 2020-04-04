# instagram-scraper

![](https://instagram-brand.com/wp-content/uploads/2016/11/Instagram_AppIcon_Aug2017.png?w=300)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)


##Features

####Downloads

- Download individual, multiple, or all posts from any given instagram account (except for a private account, in which case you must be following that user)
- Specify criteria when downloading. For example, specify a like count threshold when downloading media (the tool will download all posts which have at least that amount of likes/views specified)

####Scrape Data
- Obtain from a post such as caption, upload date, publisher ID/URL, like and view count, comments, and location
- Get list of accounts that liked a certain post or are following a certain user 


####Automation (must supply account login info)
- Like posts which contain a certain hashtag(s)
- Follow users following a certain account
- Follow users that liked a certain post
- Unfollow all users from account
- Unfollow users that are not following back (soon)

Dependencies used:
Selenium, requests, textwrap, urllib, time, random, json, bs4, os

##Usage:
(Basic python knowledge and usage of chrome web browser is assumed)
First download code, open with favorite IDE, and install dependencies.
- To use downloader, simply open igdownloader.py, specify methods, and run.
- To use automator, open igActions.py, download Chrome <a href="https://chromedriver.chromium.org/downloads">Webdriver</a>, specify download path of webdriver on line 14, account login information on lines 222 and 223, which methods you want to use, and run 
####Downloader
- **download(url)** -> downloads individual post given post url
- **download_sidecar(url, shortcode=None, path=None)** -> Use if the post you want to download contains multiple media. Simply specify url (the others are optional)
- **download_all(username, path, likes (optional))** -> downloads all media from a user. If likes are specified, then all posts which have at least that amount of likes/views will be downloaded. If not specified, then all media is downloaded by default
- **meta_data(url)** -> gets metadata from a given instagram post

####Automator
- **like_hashtag(hashtag)** -> likes posts containing given hashtag
- **get_user_followers(username)** -> returns list of users following a certain account
- **follow_followers(username)** -> follows followers of a given account
- **get_following()** -> returns list of accounts you are following
- **unfollow()** -> unfollows all accounts you are following
- **getPostLikers(url)** -> return list of users that liked a certain post
- **follow_likers(url)** -> follows all users that liked a certain post
