'''
Created on 2012-6-5

@author: luogaoqi
'''
from  BeautifulSoup import BeautifulSoup
import urllib2
import httplib
from Trip.models import Hotel as Trip_Hotel,User as Trip_User ,Hotel_User as Trip_Hotel_User
from Orbit.models import Hotel as Orbit_Hotel,User as Orbit_User,Hotel_User as Orbit_Hotel_User
from Priceline.models import Hotel as Priceline_Hotel,User as Priceline_User,Hotel_User as Priceline_Hotel_User
from hotel.models import Orbit_URL,Trip_URL,Priceline_URL


def read_urls(filename):
    url_file = open(filename)
    url_list = url_file.read()
    url_list = url_list.split()
    return url_list
 
def open_url_get_review(sub_url,user_pattern,user_tag,review_pattern,review_tag):
    
    response = urllib2.urlopen(sub_url)
    soup = BeautifulSoup(response.read())
    user_names = soup.findAll(user_tag, {'class':user_pattern})
    reviews = soup.findAll(review_tag, {'class':review_pattern})
    return user_names, reviews, soup

def get_trip_review_num_addr(url):
    response = urllib2.urlopen(url)
    parser = BeautifulSoup(response.read())
    review_num = parser.find('h3', {'class':'reviews_header'})
    if not review_num:
        review_num = 0
    else:
        review_num = int((review_num.string.split())[0])
    addr = parser.find('span',{'rel':'v:address'}).getText()
    return review_num,addr

def get_orbit_review_num_addr(url):
    response = urllib2.urlopen(url)
    parser = BeautifulSoup(response.read())
    review_num = parser.findAll('a', {'href':'#reviews'})
    if not review_num:
        review_num = 0
    else:
        review_num = int(((review_num)[1].string.split())[0])
    addr = parser.find('address').getText()
    return review_num, addr

def get_priceline_review_num_addr(url):
    response = urllib2.urlopen(url)
    parser = BeautifulSoup(response.read())
    review_num = parser.find('div', {'class':'review_paganation_left'})
    if not review_num:
        review_num = 0
    else:
        review_num = int((review_num.contents[2].string.split())[4])
    addr = parser.find('div',{'class':'address'}).getText()
    content = parser.find('div',{'class':'address'}).find('a',{'title':'Hotel Guest Rating'})
    if not content:
        addr = addr.replace('\t','').replace('\r','').replace('\n','')
    else:
        content = content.getText()
        addr = addr.replace(content,'').replace('\t','').replace('\r','').replace('\n','')
    return review_num, addr

def save_hotel(page, address):
    '''save in db'''
    if cmp(page,"trip") == 0:
        result_list = Trip_Hotel.objects.filter(addr=address)
        if  result_list:
            p = Trip_Hotel.objects.get(addr = address) 
            return p    
        else:
            p = Trip_Hotel.objects.create(addr = address)   
            return p 
    elif cmp(page,"orbit") == 0:
        result_list = Orbit_Hotel.objects.filter(addr=address)
        if  result_list:
            p = Orbit_Hotel.objects.get(addr = address) 
            return p    
        else:
            p = Orbit_Hotel.objects.create(addr = address)   
            return p
    elif cmp(page,"priceline") == 0:
        result_list = Priceline_Hotel.objects.filter(addr=address)
        if  result_list:
            p = Priceline_Hotel.objects.get(addr = address) 
            return p    
        else:
            p = Priceline_Hotel.objects.create(addr = address)   
            return p 

def save_user(page,name):
    '''save in db'''
    if cmp(page,"trip") == 0:
        result_list = Trip_User.objects.filter(name=name)
        if  result_list:
            p = Trip_User.objects.get(name = name)  
            return p    
        else:
            p = Trip_User.objects.create(name = name)  
            return p 
    elif cmp(page,"orbit") == 0:
        result_list = Orbit_User.objects.filter(name=name)
        if  result_list:
            p = Orbit_User.objects.get(name = name)  
            return p    
        else:
            p = Orbit_User.objects.create(name = name)  
            return p
    elif cmp(page,"priceline") == 0:
        result_list = Priceline_User.objects.filter(name=name)
        if  result_list:
            p = Priceline_User.objects.get(name = name)  
            return p    
        else:
            p = Priceline_User.objects.create(name = name)  
            return p

def save_rating_comment(page,hotel_object,user_object,rating,review):
    '''save in db'''
    if cmp(page,"trip") == 0:
        result_list = Trip_Hotel_User.objects.filter(hotel = hotel_object,user = user_object)
        if not result_list:
            Trip_Hotel_User.objects.create(hotel = hotel_object,user = user_object,rating = rating,comments = review)
    elif cmp(page,"orbit") == 0:
        result_list = Orbit_Hotel_User.objects.filter(hotel = hotel_object,user = user_object)
        if not result_list:
            Orbit_Hotel_User.objects.create(hotel = hotel_object,user = user_object,rating = rating,comments = review)
    elif cmp(page,"priceline") == 0:
        result_list = Priceline_Hotel_User.objects.filter(hotel = hotel_object,user = user_object)
        if not result_list:
            Priceline_Hotel_User.objects.create(hotel = hotel_object,user = user_object,rating = rating,comments = review)
            
'''get comment from google translate'''        
def trip_comment_google_translate(tag):   
    onclick = tag.span.get('onclick')
    google_addr = (onclick.split('/'))[1].replace('amp;','').replace("\'",'').replace(")",'')
    conn = httplib.HTTPConnection("www.tripadvisor.com")
    conn.request(method = "GET",url = "/"+google_addr,headers = {'Cookie':'TASession=%1%V2ID.DED129DC762C0E3345C12E96058F232C'})
    response = conn.getresponse()
    soup = BeautifulSoup(response.read())
    comment = soup.find('div',{'class':'padded_6'}).find('div').getText().encode('utf-8')
    return comment

def Crawl_Hotel_Trip(url_list):
    "Crawl information from tripadvisor.com"
    print "trip:"
    user_pattern,review_pattern="username mo","rating reviewItemInline"
    #primary_reviews = "PrimaryReviews"
    for i in url_list:
        obj = i
        i=i.url
        '''new url for extracting whole comment conveniently'''
        review_url = i.replace("Hotel_Review","ShowUserReviews")
        print review_url
        '''get review number'''
        review_num,address = get_trip_review_num_addr(review_url)
        print address
        hotel_object = save_hotel("trip",address)       
        '''get addr and phone information'''
        #no phone number
        
        '''deal with first page'''
        user_names, reviews, soup = open_url_get_review(review_url,user_pattern,'div',review_pattern,'div')
        comment = soup.findAll('div',{'class':'entry'})
        #comment = soup.findAll('p', {'class':'partial_entry'})
        cut = len(user_names)-len(reviews)
        if not user_names:
            obj.is_save = True
            obj.save()
            continue
        #there are primary_reviews in this page,so actually only len(reviews) reviews here
        for j in range(len(reviews)):
            user_comment = ""
            user_name = user_names[j+cut].span.string.strip().encode('utf-8')
            user_object = save_user("trip",user_name)
            print user_name
            user_rating = reviews[j].img.get('alt').encode('utf-8')
            print user_rating
            ''''comment'''
            if comment[j]:
                tag = comment[j].findPreviousSibling('div')
                if tag.get('class') == "googleTranslation reviewItem":
                    user_comment = trip_comment_google_translate(tag)
                else:
                    user_comment = comment[j].getText().encode('utf-8')
                print user_comment
            save_rating_comment("trip",hotel_object,user_object,user_rating,user_comment)

        '''deal with rest pages'''
        if review_num > 5:
            if review_num%5 == 0:
                pages = review_num/5
            else:
                pages = review_num/5 +1
            while True:
                next_page = soup.find('div',{'class':'pgLinks'}).find('a',{'class':'guiArw sprite-pageNext '})
                next_url = next_page.get('href')
                next_url = "http://www.tripadvisor.com"+next_url
                print next_url
                user_names, reviews,new_soup = open_url_get_review(next_url,user_pattern,'div',review_pattern,'div')
                comment = new_soup.findAll('div',{'class':'entry'})
                cut = len(user_names)-len(reviews)
                if not user_names: return
                for k in range(len(reviews)):
                    user_comment = ""
                    user_name = user_names[k+cut].span.string.strip().encode('utf-8')
                    user_object = save_user("trip",user_name)
                    print user_name
                    user_rating = reviews[k].img.get('alt').encode('utf-8')
                    print user_rating
                    ''''comment'''
                    if comment[k]:
                        tag = comment[k].findPreviousSibling('div')
                        if tag.get('class') == "googleTranslation reviewItem":
                            user_comment = trip_comment_google_translate(tag)
                        else:
                            user_comment = comment[k].getText().encode('utf-8')
                        print user_comment
                    save_rating_comment("trip",hotel_object,user_object,user_rating,user_comment)
                cur_page = int(new_soup.find('span',{'class':'paging pageDisplay'}).getText())
                if cur_page == pages:
                    break
                else:
                    soup = new_soup
                    
        obj.is_save = True
        obj.save()
                
        
            
def Crawl_Hotel_Priceline(url_list):
    "Crawl hotel from priceline.com"
    print "priceline:"
    user_pattern,review_pattern="reviewer_info","review"
    for i in url_list:
        obj = i
        i=i.url
        print i
        '''get review number'''
        review_num,address = get_priceline_review_num_addr(i)
        hotel_object = save_hotel("priceline",address)
        print address
        if review_num ==0:
            obj.is_save = True
            obj.save()
            continue
        '''deal with first page'''
        user_names, reviews, soup = open_url_get_review(i,user_pattern,'div',review_pattern,'div')
        for j in range(len(user_names)):
            review_positive,review_negative,overall_review = "","",""
            user_name = user_names[j].contents[0].string.strip().encode('utf-8')
            user_object = save_user("priceline",user_name)
            print user_name
            '''rating'''
            user_rating = reviews[j].find('div', {'class':'reviewer_score'})
            if user_rating == None:
                user_rating = "none"
                print "none"
            else:
                user_rating = user_rating.string.strip().encode('utf-8')
                print user_rating
            '''comment'''
            comment_positive = reviews[j].find('div',{'class':'review_positive'})
            comment_negative = reviews[j].find('div',{'class':'review_negative'})
            overall_comment = reviews[j].p
            if comment_positive != None:
                review_positive = review_positive + comment_positive.getText()
            if comment_negative != None:
                review_negative = review_negative + comment_negative.getText()
            if overall_comment != None:
                overall_review = overall_review+overall_comment.getText()
            comment = "review_positive:\n" + review_positive +"\n"+"review_negative:\n"+review_negative+"\n"+ "overall_comment:\n"+overall_review
            print comment
            save_rating_comment("priceline",hotel_object,user_object,user_rating,comment)
            
        '''deal with rest pages'''
        if review_num > 10:
            if review_num%10 == 0:
                pages = (review_num-10)/10
            else:
                pages = (review_num-10)/10 +1
            for j in range(pages):
                rest_page = i+"&pg="+str(j+2)+"#reviews_start"
                #print rest_page
                user_names, reviews, soup = open_url_get_review(rest_page,user_pattern,'div',review_pattern,'div')
                for k in range(len(user_names)):
                    review_positive,review_negative,overall_review = "","",""
                    user_name = user_names[k].contents[0].string.strip().encode('utf-8')
                    user_object = save_user("priceline",user_name)
                    print user_name
                    user_rating = reviews[k].find('div', {'class':'reviewer_score'})
                    if user_rating == None:
                        user_rating = "none"
                        print "none"
                    else:
                        user_rating = user_rating.string.strip().encode('utf-8')
                        print user_rating
                    '''comment'''
                    comment_positive = reviews[k].find('div',{'class':'review_positive'})
                    comment_negative = reviews[k].find('div',{'class':'review_negative'})
                    overall_comment = reviews[k].p
                    if comment_positive != None:
                        review_positive = review_positive + comment_positive.getText()
                    if comment_negative != None:
                        review_negative = review_negative + comment_negative.getText()
                    if overall_comment != None:
                        overall_review = overall_review+overall_comment.getText()
                    comment = "review_positive:\n" + review_positive +"\n"+"review_negative:\n"+review_negative+"\n"+ "overall_comment:\n"+overall_review
                    print comment
                    save_rating_comment("priceline",hotel_object,user_object,user_rating,comment)
        obj.is_save = True
        obj.save()
                    
def Crawl_Hotel_Orbitz(url_list):  
    "Crawl hotel from orbit.com" 
    print "orbit:"
    user_pattern,review_pattern="reviewer","userReviewScore"
    for i in url_list:  
        obj = i
        i=i.url
        print i
        '''get review number'''
        review_num,address = get_orbit_review_num_addr(i) 
        hotel_object = save_hotel("orbit",address)  
        print address
        if review_num == 0:
            obj.is_save = True
            obj.save()
            continue
        num = review_num/10 +2
        all_url=i+"&reviewPage="+str(num)+"&selectedTab=reviews"     
        user_names, reviews, soup = open_url_get_review(all_url,user_pattern,'strong',review_pattern,'div')
        comment = soup.findAll('div',{'class':'review'})
        #orbitz always extract the average score in every page, so we del that
        reviews=reviews[1:]
        for j in range(len(user_names)):   
            if user_names[j].string:
                user_name = user_names[j].string.strip().encode('utf-8')
                '''comment'''
                user_review = comment[j].p.getText().encode('utf-8')
                extend_review = comment[j].find('span',{'class':'extendedReviewText noneInline'})
                if extend_review:
                    user_review = user_review + extend_review.getText().encode('utf-8')
                print user_review
                
                user_object = save_user("orbit",user_name)
                print user_name
            else:
                user_name = "anonymity"
                '''comment'''
                user_review = comment[j].p.getText().encode('utf-8')
                extend_review = comment[j].find('span',{'class':'extendedReviewText noneInline'})
                if extend_review:
                    user_review = user_review + extend_review.getText().encode('utf-8')
                print user_review
                user_object = save_user("orbit",user_name)
                print user_name
            user_rating = reviews[j].span.string.strip().encode('utf-8')+" of 5 stars"
            save_rating_comment("orbit",hotel_object,user_object,user_rating,user_review)
            print user_rating
        obj.is_save = True
        obj.save()

def sibling_test():
    url = "http://www.tripadvisor.com/ShowUserReviews-g60430-d1028308-r118897437-Holiday_Inn_Express_Buffalo-Buffalo_Wyoming.html#REVIEWS"   
    response = urllib2.urlopen(url)
    soup = BeautifulSoup(response.read())
    comment = soup.find('div',{'class':'entry'})
    tag = comment.findPreviousSibling('div')
    if tag.get('class') == "googleTranslation reviewItem":
        user_comment = trip_comment_google_translate(tag)
    print user_comment
    
def test():
    url = "/MachineTranslation?g=60442&d=101173&r=86992197&page=review&sl=de&tl=en"
    conn = httplib.HTTPConnection("www.tripadvisor.com")
    conn.request(method = "GET",url = url,headers = {'Cookie':'TASession=%1%V2ID.DED129DC762C0E3345C12E96058F232C'})
    response = conn.getresponse()
    soup = BeautifulSoup(response.read())
    comment = soup.find('div',{'class':'padded_6'}).find('div').getText().encode('utf-8')
    print comment
    
if __name__ == '__main__':
    
#    sibling_test()
#    test()
#    filename_trip="D:/workspace/hotel_django/trip.txt"
#    trip_url_list = read_urls(filename_trip)
#    Crawl_Hotel_Trip(trip_url_list)
#    
#    filename_orbit="D:/workspace/hotel_django/orbit.txt"
#    orbit_url_list = read_urls(filename_orbit)
#    Crawl_Hotel_Orbitz(orbit_url_list)
#   
#    filename_priceline="D:/workspace/hotel_django/priceline.txt"
#    priceline_url_list = read_urls(filename_priceline)
#    Crawl_Hotel_Priceline(priceline_url_list)
    
    trip_url_list = Trip_URL.objects.filter(is_save = False)
    Crawl_Hotel_Trip(trip_url_list)
    
    orbit_url_list = Orbit_URL.objects.filter(is_save = False)
    Crawl_Hotel_Orbitz(orbit_url_list)
    
    priceline_url_list = Priceline_URL.objects.filter(is_save = False)
    Crawl_Hotel_Priceline(priceline_url_list)
    
    
    
    
    
    
    
    
    
    