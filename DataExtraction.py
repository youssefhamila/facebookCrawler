import bson
import re
from dateparser import parse
from Post import *
from dataBase import *


# Get page name from HTML (Meta)
def getPagename(html):
    return html.find("h1",{"class":"gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl"}).text.replace('"',"")

# Get text from post
def getText(post):
    try:
        return post.find("div",{"class":"ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a"}).text
    except:
        return ""

# Convert string to number 
def extractNumber(text):
    # If text contains "," (like 1,2k) the "K" must be replaced by 00 and the "," must be removed
    if "," in text:
         return  re.sub("[^0-9]", "", text.strip().replace(",","").replace("K","00"))
    else:
         return  re.sub("[^0-9]", "", text.strip().replace("K","000"))

# Get the number of likes
def getNumberLikes(post):
    try:
        
        number= post.find("span",{"class":"pcp91wgn"}).text
        return bson.int64.Int64(extractNumber(number))
    except:
        return 0

# Get the number of comments
def getNumberComments(post):
    try:
        
        number= post.find("div",{"class":"gtad4xkn"}).text
        return bson.int64.Int64(extractNumber(number))
    except:
        return 0

# Get the number of comments
def getNumberShares(post):
    try:
        
        number= post.findAll("div",{"class":"gtad4xkn"})[1].text
        return bson.int64.Int64(extractNumber(number))
    except:
        return 0

#Get link from post
def getLink(post):
    try:
       return post.find("span",{"class":"tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41"}).find('a')["href"].split("?")[0]  
    except:
        return ""
#Get post's date
def getDate(post):
    try:
       return parse(post.find("span",{"class":"tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41"}).text)  
    except:
        return None

#Get media type of post (Image,Video or Text)
def getMediatype(post):        
    frame=post.find("div",{"class":"bp9cbjyn cwj9ozl2 j83agx80 cbu4d94t ni8dbmo4 stjgntxs l9j0dhe7 k4urcfbm"})
    if frame is not None:
        if frame.find("img") is not None:
            return "image"
          
    frame=post.find("div",{"class":"l9j0dhe7 stjgntxs ni8dbmo4 cbu4d94t j83agx80"})
     
    if frame is not None:
        return "video"

    return "text"


     
# Get post contnent from html
def retrieve(post,page_name):
    text=getText(post)
    nb_likes=getNumberLikes(post)
    nb_comments=getNumberComments(post)
    nb_shares=getNumberShares(post)
    link=getLink(post)
    date=getDate(post)
    data_type=getMediatype(post)
    collected_post=Post(page_name=page_name,link=link,text=text,number_comments=nb_comments,number_shares=nb_shares,date=date,number_reactions=nb_likes,data_type=data_type)
    return collected_post




#Get posts from HTML
def Posts(html):
    page_name=getPagename(html)

    posts=html.findAll("div",{"class":"du4w35lb l9j0dhe7"})
    mycol=connection('posts')
    for post in posts:
        collected_post=retrieve(page_name=page_name,post=post)
        if mycol.count_documents({"link":collected_post.link})==0:
           insert_database(collected_post.__dict__,mycol)

