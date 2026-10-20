# Summarise a newsletter scenario: send times, subject / preheader, main image alt texts per email
import json,sys,re,datetime,html
d=json.load(open(sys.argv[1]))['result']['data']
print('#',d['name'].strip(),d['status'])
for n in d['nodes']:
    if n['type']=='planned-trigger':
        t=datetime.datetime.utcfromtimestamp(n['datetime'])
        print(' trigger',n['id'],'active' if n.get('active') else 'INACTIVE',t.strftime('%a %d %b %H:%MZ'))
    if n['type']=='label': print(' label',n['id'],(n.get('text') or '').replace('\n',' ')[:80])
for n in d['nodes']:
    if n['type']!='send-email-action': continue
    dd=n['design']['data']
    def find(o,keys):
        if isinstance(o,dict):
            for k,v in o.items():
                if k in keys and isinstance(v,str): yield k,v
                yield from find(v,keys)
        elif isinstance(o,list):
            for v in o: yield from find(v,keys)
    f=dict(find(dd,{'subject','pre_header','preheader','preHeader'}))
    h=n.get('bee_free_html_output') or json.dumps(dd)
    alts=[html.unescape(a) for a in re.findall(r'alt=\\?"([^"\\]{15,})',h)]
    print('==',n['name'],'|',f.get('subject'),'|',f.get('pre_header') or f.get('preheader') or f.get('preHeader'))
    seen=[]
    for a in alts:
        if a not in seen: seen.append(a)
    for a in seen[:12]: print('    -',a[:150])
