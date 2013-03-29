'''
Created on 2012-6-1

@author: luogaoqi
'''
from  BeautifulSoup import BeautifulSoup
import urllib2
import cookielib
import httplib
from hotel.models import Trip_URL,Orbit_URL,Priceline_URL
from django.utils import timezone

def read_cities(filename):
    city_file = open(filename)
    city_list = city_file.read()
    city_list = city_list.split()
    for i in range(len(city_list)):
        city_list[i] = city_list[i].replace('_','+')
    return city_list

def url_trip(city_list):
    for i in city_list:
        '''deal with first page'''
        print i,':'
        url = "http://www.tripadvisor.com/Search?q="+i
        response = urllib2.urlopen(url)
        paser = BeautifulSoup(response.read())
        hotel_num = int(paser.find('span', {'class':'pgCount'}).contents[3].string)
        citys = i.replace('+',' ')
        firstpage = paser.findAll('div', {'class':'searchResult srLODGING'})
        for j in firstpage:     
            hotel_url = "http://www.tripadvisor.com"+j.find('a').get('href')
            hotel_db = Trip_URL(url = hotel_url,city = citys,date = timezone.now())
            hotel_db.save()
            print hotel_url
        '''deal with the rest pages'''
        if hotel_num>9:
            pages = (hotel_num - 9)/20 + 1
            for j in range(pages):
                url = "http://www.tripadvisor.com/Search?ssrc=m&exc=y&o="+str(10+j*20)+"&q="+i+"&c=local&ajax=search"
                response = urllib2.urlopen(url)
                paser = BeautifulSoup(response.read())
                restpage = paser.findAll('div', {'class':'searchResult srLODGING'})
                for k in restpage:
                    hotel_url = "http://www.tripadvisor.com"+k.find('a').get('href')
                    hotel_db = Trip_URL(url = hotel_url,city = citys,date = timezone.now())
                    hotel_db.save()
                    print hotel_url

def url_orbit(city_list):
    for i in city_list:
        citys = i.replace('+',' ')
        page = 1
        url = "http://www.orbitz.com/shop/home?type=hotel&hotel.type=keyword&hotel.coord=&hotel.keyword.key="+i+"&hotel.locId=&hotel.chkin=&hotel.chkout=&hotel.rooms[0].adlts=2&hotel.rooms[0].chlds=0&hotel.rooms[0].chldAge[0]=&hotel.rooms[0].chldAge[1]=&hotel.rooms[0].chldAge[2]=&hotel.rooms[0].chldAge[3]=&hotel.rooms[0].chldAge[4]=&hotel.rating=&hotel.chain=&hotel.hname=&hotel.couponCode=&search=Search&hsv.page="
        hotel_pattern = 'hotelName'
        response = urllib2.urlopen(url+str(page))
        parser = BeautifulSoup(response.read())
        tag = parser.fetchText(' Sorry, but we cannot find your destination. Please re-enter a city name or airport code.')
        if tag:
            print "'%s', such place cannot be found."%(i)
            return
        tag = parser.fetchText('We need more information about your trip')
        if tag:
            print "we need more information for such place '%s'."%(i)
        else:
            print "we have found '%s',let's start."%(i)
            while True:
                page_url = url+str(page)
                print url
                response = urllib2.urlopen(page_url)
                parser = BeautifulSoup(response.read())
                hotels = parser.findAll('h2', {'class':hotel_pattern})
                if not hotels: break
                for j in hotels:
                    hotel_url = j.a.get('href')
                    hotel_db = Orbit_URL(url = hotel_url,city = citys,date = timezone.now())
                    hotel_db.save()
                    print hotel_url
                page += 1         
            
def url_priceline(city_list):
    for i in city_list:
        citys = i.replace('+',' ')
        city_url,session_key = priceline_city_url(i)
        city_key = city_url.split('key=')[1]
        city_key = city_key.split('&')[0]
        hotel_pattern = 'blue2-10 retail-listing group'
        response = urllib2.urlopen(city_url)
        parser = BeautifulSoup(response.read())
        hotel_num = int((parser.find('h1', {'class':'blue5 unbold'}).string.split())[0])
        #print hotel_num
        '''deal with first page'''
        firstpage = parser.findAll('div', {'class':hotel_pattern})
        for j in firstpage:
            hotel_url = "http://travela.priceline.com"+j.a.get('href')
            hotel_db = Priceline_URL(url = hotel_url,city = citys,date = timezone.now())
            hotel_db.save()
            print hotel_url
        '''deal with the rest pages'''
        if hotel_num>40:
            pages = (hotel_num - 40)/40 + 1
            for j in range(pages):
                url = "http://travela.priceline.com/hotel/listings.do?key="+city_key+"&jsk="+session_key+"&plf=PCLN&pn="+str(j+2)      
                response = urllib2.urlopen(url)
                parser = BeautifulSoup(response.read())
                restpage = parser.findAll('div', {'class':hotel_pattern})
                for k in restpage:
                    hotel_url = "http://travela.priceline.com"+k.a.get('href')
                    hotel_db = Priceline_URL(url = hotel_url,city = citys,date = timezone.now())
                    hotel_db.save()
                    print hotel_url
                
                
def priceline_city_url(city):
    conn = httplib.HTTPConnection("www.priceline.com")
    conn.request(method = "GET",url = "",headers = {'Host':'www.priceline.com','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:13.0) Gecko/20100101 Firefox/13.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Cookie':'SITESERVER=ID=5c7f78bc00000137bcb7c22fd2a10017; AxData=; WT_FPC=id=29c927dba29832ef37e1338952203232:lv=1339087046004:ss=1339083334913; __utma=137358961.524310914.1338955804.1339078807.1339086935.8; __utmz=137358961.1338955804.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Stick2=ID=0%7CA%7C06%2F07%2F2012+13%3A37; SETI=D0EF0F67332820A8BBEC8D1CB77104BEDF05786CD52FBFB92EB91B5BD2E675BC438B54B6598B14913D93009317F6982E1A31C88E1E2A96738E77DBF6C86D67B09FA0736D34ECD43B727DDED35D13EE4DFF2D4D55E23A5F058830F2EB2C01BD5C; _uxm_sid=73B3EC08-A250-4402-8A36-D6DE710BC53E; CJK=5663010a5863010a20120607122017608010829226; __utmb=137358961.55.10.1339086935; vid=v2012060716585435101030; __utmc=137358961; atgPlatoStop=1; Axxd=1'})
    r1 = conn.getresponse().getheader("Set-Cookie")
    second_half = r1.split('JSessionKey=')[1]
    session_key = second_half.split(';')[0]
    #print session_key

    data1 = 'noDatesSearch=Y&PROMO_INTERNAL_REF_ID=HPSEARCHFORM&PROMO_INTERNAL_REF_CLICK_ID=HOTEL&searchType=CITY&cityID=&cityID_Name=&cityName='+city+'&poiID=&poiID_Name=&poiName=&addrLine=&addrCity=&addrState=&addrZIP=&checkInDate=mm%2Fdd%2Fyy&checkOutDate=mm%2Fdd%2Fyy&numberOfRooms=1'
    headers1 = {'Content-Type' : 'application/x-www-form-urlencoded','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:13.0) Gecko/20100101 Firefox/13.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Cookie':'SITESERVER=ID=5c7f78bc00000137bcb7c22fd2a10017; AxData=; WT_FPC=id=29c927dba29832ef37e1338952203232:lv=1339087053656:ss=1339083334913; __utma=137358961.524310914.1338955804.1339078807.1339086935.8; __utmz=137358961.1338955804.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Stick2=ID=0%7CA%7C06%2F07%2F2012+13%3A37; SETI=D0EF0F67332820A8BBEC8D1CB77104BEDF05786CD52FBFB92EB91B5BD2E675BC438B54B6598B14913D93009317F6982E1A31C88E1E2A96738E77DBF6C86D67B09FA0736D34ECD43B727DDED35D13EE4DFF2D4D55E23A5F058830F2EB2C01BD5C; CJK=5663010a5863010a20120607122017608010829226; __utmb=137358961.57.10.1339086935; vid=v2012060716585435101030; __utmc=137358961; fs_nocache_guid=FA66C4A963D0000E773E7F85207851CA; atgPlatoStop=1; Axxd=1; JSessionKey='+session_key}
    conn_url = 'travela.priceline.com'
    conn1 = httplib.HTTPConnection(conn_url)
    conn1.request("POST", '/hotel/searchHotels.do?jsk='+session_key+'&plf=PCLN&irefid=HPSEARCHFORM&irefclickid=HOTEL', data1, headers1)
    r2 = conn1.getresponse().getheader('set-cookie')
    second_half = r2.split('JSESSIONID=')[1]
    session_ID = second_half.split(';')[0]
    #print session_ID
    
    data2 = 'checkInDate=mm%2Fdd%2Fyy&checkOutDate=mm%2Fdd%2Fyy&irefid=HPSEARCHFORM&jsk='+session_key+'&cityID=&cityName='+city+'&numberOfRooms=1&addrLine=&searchType=CITY&addrState=&noDatesSearch=Y&cityID_Name=&plf=PCLN&poiID_Name=&PROMO_INTERNAL_REF_CLICK_ID=HOTEL&irefclickid=HOTEL&addrCity=&PROMO_INTERNAL_REF_ID=HPSEARCHFORM&poiID=&addrZIP=&poiName=&key=h364rom7&o_num=null'
    headers2 = {'Host':'travela.priceline.com','Referer':'http://travela.priceline.com/hotel/searchHotels.do?jsk='+session_key+'&plf=PCLN&irefid=HPSEARCHFORM&irefclickid=HOTEL','Content-Type' : 'application/x-www-form-urlencoded','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:13.0) Gecko/20100101 Firefox/13.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Cookie':'JSESSIONID='+session_ID+'; SITESERVER=ID=5c7f78bc00000137bcb7c22fd2a10017; AxData=; WT_FPC=id=29c927dba29832ef37e1338952203232:lv=1339087053656:ss=1339083334913; __utma=137358961.524310914.1338955804.1339078807.1339086935.8; __utmz=137358961.1338955804.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Stick2=ID=0%7CA%7C06%2F07%2F2012+13%3A37; SETI=D0EF0F67332820A8BBEC8D1CB77104BEDF05786CD52FBFB92EB91B5BD2E675BC438B54B6598B14913D93009317F6982E1A31C88E1E2A96738E77DBF6C86D67B09FA0736D34ECD43B727DDED35D13EE4DFF2D4D55E23A5F058830F2EB2C01BD5C; CJK=5663010a5863010a20120607122017608010829226; __utmb=137358961.58.10.1339086935; vid=v2012060716585435101030; __utmc=137358961; fs_nocache_guid=FA66C4A963D0000E773E7F85207851CA; atgPlatoStop=1; Axxd=1; JSessionKey='+session_key}
    conn_url = 'travela.priceline.com'
    conn2 = httplib.HTTPConnection(conn_url)
    conn2.request("POST", '/hotel/searchHotels_process.do?jsk='+session_key+'&plf=PCLN&toPage=http%3A%2F%2Ftravela.priceline.com%2Fhotel%2Fhtml%2FErrorPage.html%3Freason%3Dtimeout', data2, headers2)
    city_url = conn2.getresponse().getheader('location')
    #print city_url
    return city_url,session_key        
    
    
def ren_ren():
    data = 'checkInDate=mm%2Fdd%2Fyy&checkOutDate=mm%2Fdd%2Fyy&irefid=HPSEARCHFORM&jsk=4663010a5564010a20120607164322811021608312&cityID=&cityName=buffalo&numberOfRooms=1&addrLine=&searchType=CITY&addrState=&noDatesSearch=Y&cityID_Name=&plf=PCLN&poiID_Name=&PROMO_INTERNAL_REF_CLICK_ID=HOTEL&irefclickid=HOTEL&addrCity=&PROMO_INTERNAL_REF_ID=HPSEARCHFORM&poiID=&addrZIP=&poiName=&key=h35svk4x&o_num=null'
    myCookie = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(myCookie)
    urllib2.install_opener(opener)
    req = urllib2.Request('http://travela.priceline.com/hotel/searchHotels_process.do?jsk=4663010a5564010a20120607164322811021608312&plf=PCLN&toPage=http%3A%2F%2Ftravela.priceline.com%2Fhotel%2Fhtml%2FErrorPage.html%3Freason%3Dtimeout', data)
    html_src = opener.open(req).read()
    print myCookie.cookiejar
    #print html_src
    parser = BeautifulSoup(html_src)
    tag = parser.find('h1',{'class':'blue5 unbold'}).getText()
    print tag
    
def priceline():
    city = 'buffalo'
    conn = httplib.HTTPConnection("travela.priceline.com")
    conn.request("GET","")
    r1 = conn.getresponse().getheader("Set-Cookie")
    second_half = r1.split('JSessionKey=')[1]
    session_key = second_half.split(';')[0]
    print session_key
    
    data = "noDatesSearch=Y&PROMO_INTERNAL_REF_ID=HPSEARCHFORM&PROMO_INTERNAL_REF_CLICK_ID=HOTEL&searchType=CITY&cityID=&cityID_Name=&cityName="+city+"&poiID=&poiID_Name=&poiName=&addrLine=&addrCity=&addrState=&addrZIP=&checkInDate=mm%2Fdd%2Fyy&checkOutDate=mm%2Fdd%2Fyy&numberOfRooms=1"
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
    conn_url = "/hotel/searchHotels.do?jsk="+session_key+"&plf=PCLN&irefid=HPSEARCHFORM&irefclickid=HOTEL"
    conn1 = httplib.HTTPConnection("travela.priceline.com")
    conn1.request("POST", conn_url, data, headers)
    response = conn1.getresponse().getheaders()
    print response

        
if __name__ == '__main__':
    filename="D:/workspace/hotel_django/cities.txt"
    city_list = read_cities(filename)
    url_priceline(city_list)
    url_trip(city_list)
    url_orbit(city_list)
    