import csv,re,json,sys,collections
S=sys.argv[1]
rows=[l.rstrip('\n').split('\t') for l in open(f'{S}/items.tsv')]
T=[];B=[];L=[];I=[]
for r in rows:
    typ,i,x,y,w,h,fs,grp,ln,t=r
    if i.startswith('34587646876662771') or i.startswith('34587646875202629') : continue  # my new-layout items
    if typ=='textArea':
        x,y,w=float(x),float(y),float(w)
        if y>4000: continue  # copied test block
        if re.match(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) \d+',t): T.append(dict(id=i,x=x,y=y,w=w,t=t.replace('\\n','').strip()))
        elif 'Delivered Volume' in t: B.append(dict(id=i,x=x,y=y,w=w,t=t))
        else: L.append(dict(id=i,x=x,y=y,w=w,t=t.replace('\\n',' ').strip()))
    elif typ=='image': I.append(dict(id=i,x=float(x),y=float(y)))
def day_of(x,y):
    above=[t for t in T if t['y']<y+5]
    ry=max(t['y'] for t in above); cands=[t for t in above if abs(t['y']-ry)<60]
    return min(cands,key=lambda t:abs(t['x']+t['w']/2-x))
def field(t,k):
    m=re.search(k+r':\s*(.*?)\s*(?:\\n|$)',t); return m.group(1).strip() if m else ''
out=collections.OrderedDict()
SENDS=('AM','PM','Evening')
for b in B:
    d=day_of(b['x']+b['w']/2,b['y'])
    hdr=[l for l in L if l['t'].split(' ')[0] in SENDS and b['y']-160<l['y']<b['y'] and l['x']-40<=b['x']+b['w']/2<=l['x']+l['w']+40]
    hdr=min(hdr,key=lambda l:b['y']-l['y'])['t'] if hdr else '?'
    lab=[l for l in L if b['y']-70<l['y']<b['y'] and abs(l['x']-b['x'])<40 and l['t'].split(' ')[0] not in SENDS]
    lab=lab[0]['t'] if lab else 'Whole Audience'
    f={k:field(b['t'],k) for k in ['SL','P1','Delivered Volume','Unique Clicks','Open Rate','CTR','Visitors','Orders','Conv. Rate','AOV','Revenue']}
    out.setdefault(d['t'],{'title_id':d['id'],'x':d['x'],'y':d['y'],'sends':collections.OrderedDict()})['sends'].setdefault(hdr,[]).append(dict(label=lab,bx=b['x'],id=b['id'],**f))
for d in out.values():
    for s in d['sends'].values(): s.sort(key=lambda v:v['bx'])
    d['sends']=collections.OrderedDict(sorted(d['sends'].items(),key=lambda kv:kv[1][0]['bx']))
# images -> nearest block column in same row
blocks=[(b,day_of(b['x']+b['w']/2,b['y'])) for b in B]
img=[]
for im in I:
    # row = day titles above image centre
    cand=[(b,d) for b,d in blocks if b['y']<im['y'] and im['y']-b['y']<3500]
    if not cand:
        img.append(dict(id=im['id'],x=im['x'],y=im['y'],block=None,day=None)); continue
    b,d=min(cand,key=lambda bd:abs(bd[0]['x']+bd[0]['w']/2-im['x'])+0.1*abs(bd[0]['y']-im['y']))
    img.append(dict(id=im['id'],x=im['x'],y=im['y'],block=b['id'],day=d['t']))
json.dump({'days':out,'images':img,'old_ids':[t['id'] for t in T]+[b['id'] for b in B]+[l['id'] for l in L]},open(f'{S}/parsed.json','w'),indent=1)
for k,d in out.items():
    print('##',k)
    for h,vs in d['sends'].items():
        print('  ',h,'|',' ; '.join(f"{v['label']}: {v['SL'][:30]!r} del={v['Delivered Volume']} or={v['Open Rate']} rev={v['Revenue']}" for v in vs))
print('images',len(img), collections.Counter(i['day'] for i in img))
print('old ids',len(json.load(open(f'{S}/parsed.json'))['old_ids']))
