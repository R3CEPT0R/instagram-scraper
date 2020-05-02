import requests
import textwrap
import urllib.request
import time
import json
import bs4
import os

class ig_download:
    def __init__(self):
        self.downloads=0

    def clear_downloads(self):
        self.downloads=0

    def download(self,url):
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        image=False
        for tag in soup.find_all("meta"):
            if tag.get("property", None) == "og:image":
                media = str(tag.get("content", None))
                image=True
            elif tag.get("property",None)=="og:video":
                media = str(tag.get("content", None))
        data = requests.get(media).content

        # want image quality to remain the same so png (lossless compression)
        ext='.png' if image else '.mp4'
        with open('media'+ext, 'wb') as handler:
            handler.write(data)

        #download posts with multiple media
    def download_sidecar(self,url,shortcode=None,directory=None):
        page=requests.get(url+'?__a=1') if shortcode==None else requests.get(f"https://www.instagram.com/p/{shortcode}/?__a=1")
        edges=[]
        for edge in page.json()['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
            edges.append(edge)
            #print(edge)

        #begin downloading
        self.clear_downloads()
        for i in edges:
            print(i)
            if i['node']['is_video']==True:
                ext='.mp4'
                media_src=i['node']['video_url']
            else:
                ext='.png'
                media_src=i['node']['display_url']
            data = requests.get(media_src).content      # actually download
            path='media'+str(self.downloads)+ext if directory==None else os.path.join(directory,i['node']['id']+ext)
            with open(path, 'wb') as handler:
                handler.write(data)
            self.downloads+=1

    def download_all(self,username,directory,likes=None):
        "Download all media from a user account"
        url='https://www.instagram.com/'+username+'/'
        directory+='\\'+username
        r = requests.get(url + '?__a=1')
        user_id=r.json()['graphql']['user']['id']
        end_cursor=''
        next_page=True
        if not os.path.exists(directory):
            os.makedirs(directory)
        while next_page:
            r = requests.get('https://www.instagram.com/graphql/query/',
                             params={
                                 'query_id' : '17880160963012870',
                                 'id' : user_id,
                                 'first' : 12,
                                 'after' : end_cursor })
            graphql=r.json()['data']
            for edge in graphql['user']['edge_owner_to_timeline_media']['edges']:
                file_name = edge['node']['taken_at_timestamp']
                download_path = f"{directory}\\{file_name}.png"
                type=edge['node']['__typename']
                print(edge)
                if type=='GraphImage':
                    if likes!=None:
                        if edge['node']['edge_liked_by']['count']>=likes:
                            urllib.request.urlretrieve(edge['node']['display_url'],download_path)
                    else:
                        urllib.request.urlretrieve(edge['node']['display_url'], download_path)
                elif type=='GraphVideo':
                    shortcode=edge['node']['shortcode']
                    videos = requests.get(f"https://www.instagram.com/p/{shortcode}/?__a=1")
                    video_url = videos.json()['graphql']['shortcode_media']['video_url']
                    file_name = videos.json()['graphql']['shortcode_media']['taken_at_timestamp']
                    download_path = f"{directory}\\{file_name}.mp4"
                    if likes!=None:
                        if edge['node']['video_view_count'] >= likes:
                            urllib.request.urlretrieve(video_url,download_path)
                    else:
                        urllib.request.urlretrieve(video_url, download_path)
                elif type=='GraphSidecar':
                    shortcode=edge['node']['shortcode']
                    if likes!=None:
                        if edge['node']['edge_liked_by']['count'] >=likes:
                            self.download_sidecar(edge['node']['display_url'],shortcode,directory)
                    else:
                        self.download_sidecar(edge['node']['display_url'], shortcode, directory)
            end_cursor=graphql['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            next_page=graphql['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            time.sleep(5)


    def get_caption(self,url):
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        l = soup.find("script", {"type": "application/ld+json"})
        r = textwrap.dedent(l.get_text())
        r = json.loads(r)
        r=r['caption'] if r['caption'] else 'N/A'
        caption= str(r).replace('\n', ' ').replace('\r', '')
        return caption


    def parse(self,url):
        page=requests.get(url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        l = soup.find("script", {"type": "application/ld+json"})
        r = textwrap.dedent(l.get_text())
        r = json.loads(r)
        return r

    def get_upload_date(self,item):
        return item['uploadDate'] if item['uploadDate'] else "N/A"

    def get_publisher(self,item):
        publisher=item['author']['alternateName']
        url=item['author']['mainEntityofPage']['@id']
        return (publisher,url)

    def comment_count(self,item):
        return item['commentCount']

    def like_count(self,item):
        return item['interactionStatistic']['userInteractionCount']

    def view_count(self,item):
        return item['video_view_count']

    def get_location(self,item):
        lst=[]
        try:
            lst.append(item['contentLocation']['name'])
        except:
            return "N/A"
        try:
            item['contentLocation']['address']
            details = item['contentLocation']['address']
            for key, val in details.items() :
                lst.append(val)
        except:
            lst.append('N/A')

        return lst

    def meta_data(self,url):
        meta={}
        obj = self.parse(url)
        print("\nCollecting Data....\n")
        time.sleep(2)
        #print("Statistics:")
        meta['Caption: ']=self.get_caption(url)
        meta['Upload Date: ']=self.get_upload_date(obj)
        meta['Publisher ID: ']=self.get_publisher(obj)[0]
        meta['Publisher URL: ']=self.get_publisher(obj)[1]
        meta['Likes: ']=self.like_count(obj)
        meta['Comments: ']=self.comment_count(obj)
        meta['Location: ']=self.get_location(obj)
        #for key,value in meta.items():
        #    print(key,value)
        return meta

    def meta_append(self,url,file_path):
        results=self.meta_data(url)
        try:
            # we just append
            f=open(file_path,"a")
            f.write("\n")
            json.dump(results, f)
            f.close()
        except:
            print("Looks like there was an error, did you specify the right path?")
            return
        print("Done")

    def meta_create(self,url,path=None):
        results=self.meta_data(url)
        if (os.path.isdir(path)):
            path=os.path.join(path,"new_data.txt")
            f=open(path,"w")
        else:
            f=open("new_data.txt","w")
        json.dump(results, f)
        f.close()



if __name__=="__main__":
    #url='https://www.instagram.com/p/B5dhCqPnJuA/'
    #url='https://www.instagram.com/p/B6dpZxjnVCx/'
    #url='https://www.instagram.com/p/BXluHy5jVxV/'
    #url='https://www.instagram.com/p/B9R6xvopnBO/'
    #url='https://www.instagram.com/p/B99qAc9Hv0D/'
    #url='https://www.instagram.com/p/B9pCxqsnrwN/'
    #url='https://www.instagram.com/p/B6bLp9GnN6A/'
    #x=ig_download()
    #x.download_sidecar(url)
    #x=ig_download()
    #x.download_all('barstoolcats','C:\\Users\\promise\\Documents\\Instagram Scraper\\Instagram Scraper')
    x=ig_download()
    #x.meta_data('https://www.instagram.com/p/B_VIRVnJMvt/')
    x.meta_create('https://www.instagram.com/p/B_VIRVnJMvt/','<enter path to create file or leave empty>')
    #x.meta_append('https://www.instagram.com/p/B_VIRVnJMvt/','<enter full file path here>')