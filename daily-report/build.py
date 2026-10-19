import json,sys,re,datetime,html
S=sys.argv[1]
J=json.load(open(f'{S}/plan.json')); days=J['days']; order=J['order']; plan=J['plan']
dims={}
for l in open(f'{S}/dims.txt'):
    i,w,h=l.split(); dims[i]=(int(w),int(h))
mine_px={'3458764687665720826':8524,'3458764687665720839':6886,'3458764687665720871':8088,'3458764687665720900':7584,'3458764687665811966':9416,'3458764687665812004':7478,'3458764687665812023':8448,'3458764687665812039':10106,'3458764687665812057':7294}
for i,h in mine_px.items(): dims[i]=(1280,h)
X0=-7400; PITCH=2120; DW=1880
def date_of(t):
    m=re.match(r'\w+ (\d+)\w* (\w+) 2026',t); return datetime.date(2026,datetime.datetime.strptime(m.group(2),'%B').month,int(m.group(1)))
def wk(d): return (date_of(d)-datetime.date(2026,9,28)).days//7
HDR={'AM':'AM - 7am','PM':'PM - 3pm','Evening':'Evening - 6pm','PM - 1am':'PM - 1am','PM - 3pm':'PM - 3pm'}
def num(s):
    s=(s or '').replace(',','').replace('£','').replace('%','').strip()
    return float(s) if s else None
e=lambda t: html.escape(t,quote=False)
# actual rendered sizes (team images can't be resized); my click maps -> 180 wide to match
rend={l.split()[0]:(int(l.split()[1]),int(l.split()[2])) for l in open(f'{S}/rendered.txt')}
for p in plan:
    if p['id'] in mine_px: p['w']=180; p['h']=round(180*mine_px[p['id']]/1280)
    else: p['w'],p['h']=rend[p['id']]
stack={}
for p in plan: stack.setdefault((p['day'],p['send']),[]).append(p)
def send_h(key):
    ps=stack.get(key,[])
    if not ps: return 0
    side=sum(p['h']+20 for p in ps if p['stack'])-20
    return max([p['h'] for p in ps if not p['stack']]+[side])
IMG=600
rows=sorted({wk(d) for d in order})
rowh={}
for r in rows:
    hs=[send_h((d,s)) for d in order if wk(d)==r for s in days[d]['sends']]
    rowh[r]=IMG+(max(hs) if max(hs+[0]) else 1500)+300
y=-6200; rowy={}
for r in rows: rowy[r]=y; y+=rowh[r]+250
out=[]; moves=[]
def T(x,y,w,fs,txt,align='left',fill='#1a1a1a'):
    out.append(f'<textArea x="{round(x)}" y="{round(y)}" width="{round(w)}" font-size="{fs}" text-align="{align}" fill="{fill}">{txt}</textArea>')
def fmt_money(v): return f'£{v:,.2f}'
def stats(vs,with_sl):
    D=[num(v['Delivered Volume']) for v in vs]
    blank=any(x is None for x in D)
    L=[]
    if with_sl:
        L+= [f'<b>SL:</b> {e(vs[0]["SL"])}', f'<b>P1:</b> {e(vs[0]["P1"])}', '']
    if blank:
        vals=dict.fromkeys(['Delivered Volume','Unique Clicks','Open Rate','CTR','Visitors','Orders','Conv. Rate','AOV','Revenue'],'')
    elif len(vs)==1:
        vals={k:vs[0].get(k,'') for k in ['Delivered Volume','Unique Clicks','Open Rate','CTR','Visitors','Orders','Conv. Rate','AOV','Revenue']}
        d,c,v,o,rv=[num(vs[0][k]) for k in ['Delivered Volume','Unique Clicks','Visitors','Orders','Revenue']]
        vals['CTR']=f'{c/d*100:.2f}%'; vals['Conv. Rate']=f'{o/v*100:.2f}%' if v else '0.00%'; vals['AOV']=fmt_money(rv/o) if o else '£0.00'; vals['Revenue']=fmt_money(rv)
    else:
        s=lambda k: sum(num(v[k]) or 0 for v in vs)
        d,c,v,o,rv=s('Delivered Volume'),s('Unique Clicks'),s('Visitors'),s('Orders'),s('Revenue')
        orr=sum(num(x['Open Rate'])*num(x['Delivered Volume']) for x in vs)/d
        vals={'Delivered Volume':f'{int(d):,}','Unique Clicks':f'{int(c):,}','Open Rate':f'{orr:.2f}%','CTR':f'{c/d*100:.2f}%','Visitors':f'{int(v):,}','Orders':f'{int(o):,}','Conv. Rate':f'{o/v*100:.2f}%' if v else '0.00%','AOV':fmt_money(rv/o) if o else '£0.00','Revenue':fmt_money(rv)}
    for grp in (['Delivered Volume','Unique Clicks','Open Rate','CTR'],['Visitors','Orders','Conv. Rate','AOV','Revenue']):
        L+=[f'<b>{k}:</b> {vals[k]}' for k in grp]+['']
    return '<br/>'.join(L[:-1])
def lines_est(txt,w,fs):
    n=0
    for seg in re.sub('<[^>]+>','',txt.replace('<br/>','\n')).split('\n'):
        n+=max(1,-(-len(seg)*fs*0.55//w))
    return n
for d in order:
    r=wk(d); y0=rowy[r]; dx=X0+(date_of(d).weekday())*PITCH
    T(dx,y0,DW,37,f'<b>{e(d)}</b>','center')
    sends=list(days[d]['sends'].items()); n=len(sends); cw=(DW-(n-1)*40)/n
    for ci,(s,vs) in enumerate(sends):
        cx=dx+ci*(cw+40)
        T(cx,y0+70,cw,22,f'<b><u>{e(HDR[s])}</u></b>','center')
        labs=[v['label'] for v in vs]
        if 'Test A' in labs:
            lab='Total – whole audience + tests'; body=stats(vs,True)
            ors=[(num(v['Open Rate']),'Whole audience' if v['label']=='Whole Audience' else v['label']) for v in vs]
            pl=[f'<b>{e(v["label"])} – {e(v["Open Rate"])}:</b> {e(v["SL"])} / {e(v["P1"])}' if v['SL'] else f'<b>{e(v["label"])} – </b>' for v in vs if v['label']!='Whole Audience']
            if all(o for o,_ in ors):
                ors.sort(reverse=True); pl.append('<b>Winner: '+ors[0][1]+'</b>' if ors[0][0]-ors[1][0]>=1.0 else '<b>No clear winner</b>')
        elif 'New Customer' in labs:
            lab='Total – new + existing customers'; body=stats(vs,False)
            pl=[f'<b>{e(v["label"])} – {e(v["Open Rate"])}:</b> {e(v["SL"])} / {e(v["P1"])}' for v in vs]
        else:
            lab=vs[0]['label']; body=stats(vs,True); pl=None
        T(cx,y0+115,cw,14,f'<b><u>{e(lab)}</u></b>')
        T(cx,y0+142,cw,14,body)
        if pl:
            txt='<br/>'.join(pl); ph=int(lines_est(txt,cw-20,10)*14+16)
            out.append(f'<rect x="{round(cx)}" y="{y0+470}" width="{round(cw)}" height="{ph}" rx="6" fill="#f7f7f7" stroke="#e7e7e7" stroke-width="2"/>')
            T(cx+10,y0+478,cw-20,10,txt,fill='#595959')
        else:
            T(cx,y0+478,cw,11,'<i>No subject line test on this send.</i>',fill='#595959')
        ps=sorted(stack.get((d,s),[]),key=lambda p:p['k'])
        main=[p for p in ps if not p['stack']]; side=[p for p in ps if p['stack']]
        xx=cx
        for p in main:
            moves.append((p['id'],xx,y0+IMG,p['w'],p['h'])); xx+=p['w']+20
        sy=y0+IMG
        for p in side:
            moves.append((p['id'],xx,sy,p['w'],p['h'])); sy+=p['h']+20
# week labels on the left
for r in rows:
    mon=datetime.date(2026,9,28)+datetime.timedelta(weeks=r)
    T(X0-700,rowy[r],560,30,f'<b>Week commencing {mon.day} {mon.strftime("%B")}</b>','left','#1a1a1a')
T(X0-700,rowy[rows[0]]-260,2*PITCH,16,'<b>How to read this board:</b> headline figures and click maps are totals for each send (new + existing customers, or whole audience + Test A + Test B). The grey panel underneath shows each segment / test version on its own with its open rate.','left','#595959')
# separators between weeks
for r in rows[1:]:
    yy=rowy[r]-125
    out.append(f'<line x1="{X0-700}" y1="{yy}" x2="{X0+7*PITCH-240}" y2="{yy}" stroke="#d9d9d9" stroke-width="4"/>')
json.dump(dict(moves=moves,rowy=rowy,rowh=rowh),open(f'{S}/build_out.json','w'))
# split text into chunks per row
chunks=[];cur=[]
for el in out:
    cur.append(el)
    if sum(map(len,cur))>150000: chunks.append(cur);cur=[]
chunks.append(cur)
for i,c in enumerate(chunks): open(f'{S}/text_{i}.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg">'+''.join(c)+'</svg>')
mv='<svg xmlns="http://www.w3.org/2000/svg">'+''.join((f'<image data-miro-id="{i}" data-type="image" x="{round(x)}" y="{round(y)}" />' if i in mine_px else f'<image data-miro-id="{i}" data-type="image" x="{round(x+w/2)}" y="{round(y+h/2)}" />') for i,x,y,w,h in moves)+'</svg>'
open(f'{S}/move2.svg','w').write(mv)
print(len(chunks),[len(''.join(c)) for c in chunks],len(mv),rowy,rowh)

open(f'{S}/mine_resize.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg">'+''.join(f'<image data-miro-id="{i}" data-type="image" x="{round(x)}" y="{round(y)}" width="{w}" height="{h}" />' for i,x,y,w,h in moves if i in mine_px)+'</svg>')
