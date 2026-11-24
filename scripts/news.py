import json,urllib.request,urllib.parse,xml.etree.ElementTree as ET,datetime,email.utils
Q={'trending':'India travel tourism trending','know':'travel advisory OR visa rules OR new rules for travellers India',
 'travel':'India travel tourism','visa':'visa rules Indian travellers OR visa on arrival Indians OR e-visa India','flights':'flights India fares OR new flight routes India OR DGCA','airlines':'IndiGo OR Air India OR Akasa Air OR SpiceJet airline news'}
out={'updated':datetime.datetime.now(datetime.timezone.utc).isoformat()}
for k,q in Q.items():
    u='https://news.google.com/rss/search?'+urllib.parse.urlencode({'q':q+' when:3d','hl':'en-IN','gl':'IN','ceid':'IN:en'})
    x=ET.fromstring(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read())
    items=[]
    for it in x.iter('item'):
        t=it.findtext('title') or '';s=it.find('source');src=s.text if s is not None else ''
        if src and t.endswith(' - '+src): t=t[:-len(src)-3]
        d=it.findtext('pubDate');d=email.utils.parsedate_to_datetime(d).isoformat() if d else ''
        items.append({'title':t,'link':it.findtext('link'),'source':src,'date':d})
    items.sort(key=lambda i:i['date'],reverse=True);out[k]=items[:12]
json.dump(out,open('data/news.json','w'),ensure_ascii=False,indent=1)
print({k:len(v) for k,v in out.items() if k!='updated'})
