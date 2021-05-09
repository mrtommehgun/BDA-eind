import requests, re, time,redis,json
from pymongo import MongoClient
from bs4 import BeautifulSoup
#setting up Redis connection
conn=redis.Redis('localhost', charset="utf-8", decode_responses=True)
client = MongoClient('localhost', 27017)
db=client["Mongocoin"]
col=db["hoogst"]

#Hier aanpassen de tijd in minuten aan te passen
#aantalminuten=int(input())
aantalminuten=5
teller=0

while True:
    
    cmc = requests.get("https://www.blockchain.com/btc/unconfirmed-transactions")
    soup = BeautifulSoup(cmc.text,"html.parser")
    HASHLIST=soup.findAll("a",attrs={'class':"sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK"})
    BTCDOLLIST=soup.findAll("span",attrs={'class':"sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC"})

#variabelen declareren
#initiele lijsten
    hashlijstje=[]
    Transactielijst=[]

#iterators voor de verschillende lijsten + lijsten, dictionaries
    tijdteller=0
    bitteller=1
    usdteller=2
    tijdstip=[]
    bitcoinlijst=[]
    usdlijst=[]
    HASHDICBTC={}
    HASHDICUSD={}

#regexfilter voor html elements weg te filteren
    htmlfilter="(<)(?<=<)(.+?)(?=>)(>)"
#hashes filteren
    for HashItem in HASHLIST:
        Hashre = re.sub(htmlfilter," ", str(HashItem))
        hashlijstje.append(Hashre.strip(" "))
#Listing the parts of transaction (and appending them to seperate lists)
    for BTCINFO in BTCDOLLIST:
        BTCre = re.sub(htmlfilter," ",str(BTCINFO))
        Transactielijst.append(BTCre.rstrip(" ").lstrip(" ").lstrip("$"))
#wegens formatprobleem, heb ik de 1000-separator verwijderd
    kommafilter=","
    for i in range(int(len(Transactielijst)/3)):
        tijdstip.append(Transactielijst[tijdteller])
        bitcoinlijst.append(Transactielijst[bitteller])
        filtergetal=re.sub(kommafilter,"",Transactielijst[usdteller])
        usdlijst.append(float(filtergetal))
        try:
            tijdteller+=3
            bitteller+=3
            usdteller+=3
        except:
            break

#Assigning bitcoin and USD values to the hash so comparing is easier   
    for i in range(len(hashlijstje)):
        HASHDICBTC[hashlijstje[i]]=bitcoinlijst[i]
        HASHDICUSD[hashlijstje[i]]=usdlijst[i]
    #print(type(tijdstip[0]))
    usdlijst.sort()
    #print(usdlijst[0])
    #print(usdlijst[-1])
#comparing values to the keys (hash)
    for key, value in HASHDICUSD.items():
        #hier moet de volledige lijst met getallen enzo, ja
        mongoformat={"hash":key,"BTC":HASHDICBTC[key],"USD":str(value),"Time":tijdstip[0]}
        print(json.dumps(mongoformat))
        mongostring=str("hash:{},BTC:{},USD:{},Time:{}".format(key,HASHDICBTC[key],value,tijdstip[0]))
        conn.hmset(str(key), mongoformat)
        if usdlijst[-1]==value:
    
            #hoogste waarde apart
            Rediskey="hoogstewaarde{}".format(tijdstip[-1])
            conn.hmset(Rediskey,mongoformat)
    #for key in HASHDICUSD.keys():
    #    print(conn.get(key))
    
    time.sleep(60)
    teller+=1
    print("slaaptijd is over, let's go again!")
    if teller==aantalminuten:
        break

hoogstelijst=[]
eindlijst=[]
for key in conn.scan_iter("hoogstewaarde*"):
    hoogstelijst.append(key)
for item in hoogstelijst:
    sleutel =conn.hgetall(item)
    eindlijst.append(sleutel)
      
for item in eindlijst:
    print(item)
    x=col.insert_one(item)
