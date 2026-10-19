import json,sys,re,collections
S=sys.argv[1]
P=json.load(open(f'{S}/parsed.json'))
days=P['days']
# add Fri-Sun 16-18 from my data (same variant structure as team columns)
def V(label,sl,p1,d,c,orr,v,o,r): return dict(label=label,SL=sl,P1=p1,**{'Delivered Volume':f'{d:,}','Unique Clicks':str(c),'Open Rate':f'{orr:.2f}%','Visitors':str(v),'Orders':str(o),'Revenue':f'£{r:,.2f}'})
extra={
 'Friday 16th October 2026':{'AM':[V('Whole Audience','Don’t take our word for it… 🏡','Real reviews, real homes – plus bundle & save up to 47%',243503,822,40.09,491,81,3911.36),V('Test A','What over 1 million happy customers already know ⭐','Their favourite reed diffusers are now up to 47% off when you bundle.',5022,13,40.20,9,0,0),V('Test B','Everyone’s talking about these diffusers 🗣️','See why – then bundle & save up to 47% and grab your FREE gift.',5172,16,39.42,16,0,0)],
   'PM':[V('Whole Audience','Bundle & save up to 47% – the reviews are in 🏡','Mix & match reed diffusers from £9.99 each – plus Friday’s FREE gift',242601,925,33.73,602,92,4305.91),V('Test A','Your new favourite scent might be in here 👀','Bundle & save up to 47% on reed diffusers – plus Friday’s FREE gift.',5161,25,34.43,20,4,283.82),V('Test B','Friday’s FREE gift + up to 47% off diffusers 🎁','Find out why our customers keep coming back for more.',5014,25,32.95,17,2,99.42)],
   'Evening':[V('Whole Audience','Your FREE Diffuser is waiting 🎁','Use FREESCENT + get up to 44% off',62899,493,28.78,371,67,2252.95)]},
 'Saturday 17th October 2026':{'AM':[V('Whole Audience','A diffuser for every room 🍂','Bundle & save up to 47% on reed diffusers',243521,1563,45.12,1104,168,8265.65),V('Test A','Bundle up, save more – up to 47% off reed diffusers 🛋️','Hallway, bedroom, bathroom… which room are you scenting first?',5035,26,44.49,15,1,37.96),V('Test B','Which room in your home needs a little love? 🕯️','Mix & match reed diffusers from £9.99 each in a bundle of 10.',5097,26,44.97,21,3,133.87)],
   'PM':[V('Whole Audience','Autumn scenting made easy 🍂','Bundle & save on reed diffusers + Get a FREE gift',242597,1123,43.89,654,79,3818.66),V('Test A','Up to 47% off reed diffusers + a FREE gift 🎁','The easiest way to make your home feel like autumn.',5037,25,44.83,12,4,192.84),V('Test B','The one thing your home is missing this autumn 🍁','Bundle & save – plus a FREE gift with your order.',5064,37,43.27,27,5,232.79)],
   'Evening':[V('Whole Audience','Sunday’s forecast: up to 44% off 🌤️','VIP early access to tomorrow’s deals + a FREE Diffuser',62726,692,41.63,322,41,1733.07)]},
 'Sunday 18th October 2026':{'AM':[V('Whole Audience','Bundle & save up to 47% 🍂','Your Sunday, scented',243549,1199,43.93,714,117,5636.77),V('Test A','Slow Sunday, cosy home + a FREE gift 🕯️','Save up to 47% when you mix & match reed diffuser.',5045,24,42.58,15,2,81.92),V('Test B','What’s your home smelling like this Sunday? ☕','Fill every room for less',5011,29,45.38,18,4,159.87)],
   'PM':[V('Whole Audience','Slow Sunday evenings 🍂','Bundle & save up to 47%',242616,977,40.96,388,43,2123.96),V('Test A','Your Sunday night wind-down starts here 🕯️','Bundle reed diffusers and save up to 47% – every room, sorted.',5014,20,41.88,6,2,106.90),V('Test B','Something cosy for your Sunday evening 🍂','Bundle & save up to 47% on reed diffusers – and grab your FREE gift.',5014,23,40.39,9,0,0)],
   'Evening':[V('Whole Audience','The clock is ticking… ⏰','Your FREE Diffuser disappears at midnight + tomorrow’s deals, up to 44% off',62939,401,37.52,237,61,2599.40)]}}
mine={'Friday 16th October 2026':['3458764687665720826','3458764687665720839','3458764687665720871'],'Saturday 17th October 2026':['3458764687665720900','3458764687665811966','3458764687665812004'],'Sunday 18th October 2026':['3458764687665812023','3458764687665812039','3458764687665812057']}
for d,sends in extra.items(): days[d]={'sends':sends}
# fix Friday 2nd AM labels
for v in days['Friday 2nd October 2026']['sends']['AM']:
    v['label']='New Customer' if int(v['Delivered Volume'].replace(',',''))<120000 else 'Existing Customer'
import datetime
def date_of(t):
    m=re.match(r'\w+ (\d+)\w* (\w+) 2026',t); return datetime.date(2026,datetime.datetime.strptime(m.group(2),'%B').month,int(m.group(1)))
order=sorted(days,key=date_of)
# image -> (day, send, idx)
blk={}
for d in order:
    for s,vs in days[d]['sends'].items():
        for k,v in enumerate(vs):
            if 'id' in v: blk[v['id']]=(d,s,k)
imgs=collections.defaultdict(list)   # (day,send) -> list of (idx, id)
MINE={i for v in mine.values() for i in v}
for im in P['images']:
    if im['id'] in MINE or im['day'] is None: continue
    if im['block'] in blk:
        d,s,k=blk[im['block']]; imgs[(d,s)].append((k,im['id']))
for d,ids in mine.items():
    for s,i in zip(['AM','PM','Evening'],ids): imgs[(d,s)].append((0,i))
# geometry
X0=-7400; PITCH=2120; DW=1880
def slot(d):
    dt=date_of(d); monday=datetime.date(2026,9,28)
    wk=(dt-monday).days//7; dow=dt.weekday(); return wk,dow
widths={}
plan=[]
for d in order:
    wk,dow=slot(d); sends=list(days[d]['sends'].items()); n=len(sends)
    colw=(DW-(n-1)*40)/n
    for ci,(s,vs) in enumerate(sends):
        cx=X0+dow*PITCH+ci*(colw+40)
        lst=sorted(imgs.get((d,s),[]))
        nv=len(vs)
        for k,i in lst:
            if len(lst)==1: w=min(400,colw); x=cx; slotk=0
            elif nv==3 or len(lst)==3:
                if k==0: w=colw-200; x=cx; slotk=0
                else: w=180; x=cx+colw-180; slotk=k
            else: w=(colw-20)/2; x=cx+k*(w+20); slotk=0
            plan.append(dict(id=i,day=d,send=s,k=k,w=round(w),x=round(x),wk=wk,stack=(nv==3 and k>0)))
json.dump(dict(order=order,days=days,plan=plan),open(f'{S}/plan.json','w'),indent=0,ensure_ascii=False)
print(len(plan),'images planned'); print(collections.Counter(p['w'] for p in plan))
svg='<svg xmlns="http://www.w3.org/2000/svg">'+''.join(f'<image data-miro-id="{p["id"]}" data-type="image" width="{p["w"]}" height="100" />' for p in plan)+'</svg>'
open(f'{S}/resize.svg','w').write(svg); print(len(svg))
