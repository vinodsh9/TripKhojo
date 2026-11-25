import json,urllib.request,datetime,time
C=['USD','EUR','GBP','AED','THB','SGD','IDR','MVR','VND','MYR','LKR','NPR','JPY','AUD','CAD','CHF','SAR']
H={'User-Agent':'Mozilla/5.0'}
def get(u):return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=30))
inr={};src={}
for c in C:  # live market rate: 1 unit of c in rupees
    try:
        m=get(f'https://query1.finance.yahoo.com/v8/finance/chart/{c}INR=X?interval=1h&range=1d')['chart']['result'][0]['meta']
        v=float(m['regularMarketPrice'])
        if v>0: inr[c]=v;src[c]='market'
    except Exception as e: print(c,'market failed',e)
    time.sleep(0.3)
try:  # fallback for any currency the market feed missed
    r=get('https://open.er-api.com/v6/latest/INR')['rates']
    for c in C:
        if c not in inr and r.get(c): inr[c]=1/r[c];src[c]='daily'
except Exception as e: print('fallback failed',e)
if len(inr)<10: raise SystemExit('too few rates, keeping old file')
json.dump({'updated':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inr_per_unit':inr,'source':src},open('data/rates.json','w'),indent=1)
print(len(inr),{k:round(v,3) for k,v in inr.items()})
