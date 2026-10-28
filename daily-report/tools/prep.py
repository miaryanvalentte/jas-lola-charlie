# prep.py <scenario json> <click-rows json> <dayDir>: write html/, sl.json, hm/, main/ for heatmap.mjs and links.mjs
import json,sys,re,collections,shutil,os,datetime
SC,CL,D=sys.argv[1:]
for sub in ('html','hm','main','out','links'): os.makedirs(f'{D}/{sub}',exist_ok=True)
d=json.load(open(SC))['result']['data']; print(d['name'],d['status'])
sl={}
for n in d['nodes']:
    if n.get('type')=='planned-trigger': print(' trigger',n['id'],n['active'],datetime.datetime.fromtimestamp(n['datetime'],datetime.UTC))
    if n.get('type')!='send-email-action': continue
    dd=n['design']['data']; slug=re.sub(r'\W+','_',n['name'])
    open(f"{D}/html/{slug}.html",'w').write(dd['jinja_html'])
    sl[n['name']]=(dd.get('subject'),dd.get('preheader')); print(' ',n['name'],'|',dd.get('subject'),'|',dd.get('preheader'))
json.dump(sl,open(f"{D}/sl.json",'w'),ensure_ascii=False)
rows=json.load(open(CL))['data']['rows']
agg=collections.defaultdict(collections.Counter); other=collections.Counter()
for r in rows:
    h=r['headers']; v=r['values'][0]
    if not v: continue
    if h[0]['type']!='single' or h[1]['type']!='single': other[str(h[0].get('value'))]+=v; continue
    act=h[0]['value'].strip(); send=re.sub(r'\s*-\s*Title Test [AB]\s*$','',act).strip()
    url=h[2]['value'] if h[2]['type']=='single' else '*'
    if 'eng.bloomreach.com' in url: url='*'
    agg[send][(h[1]['value'],url)]+=v
print('unattributed:',dict(other))
for send,c in sorted(agg.items()):
    slug=re.sub(r'\W+','_',send)
    json.dump({"P":"","rows":[[x,u,v] for (x,u),v in c.items()]},open(f'{D}/hm/{slug}.json','w'))
    shutil.copy(f'{D}/html/{slug}.html', f'{D}/main/{slug}.html')
    print(send, slug, sum(c.values()), len(c))
