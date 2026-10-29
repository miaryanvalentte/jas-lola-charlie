import json, sys, html
S='/tmp/claude-0/-home-user-jas-lola-charlie/84acea6c-1193-59d1-8e21-164804e8a510/scratchpad'
# day -> (x of AM column, image top y)
DAY={'26':(-7400,4757),'27':(-5280,4757),'28':(-3160,4757)}
OFF={'AM':0,'PM':640,'Evening':1280}
NOTES=json.load(open(sys.argv[1]))
SC=180/640; SW,SH=250,163; GAP=12
out=[]
for d,(x0,ytop) in DAY.items():
  links=json.load(open(f'{S}/d{d}/links/links.json'))
  for send in ['AM','PM','Evening']:
    name=f'{send}_Email_{d}_10_26'
    ls=links[name]; tot=sum(l['v'] for l in ls)
    boxes={b['aid']:b for b in json.load(open(f'{S}/d{d}/out/{name}.boxes.json'))['boxes']}
    items=[]
    for n in [n for n in NOTES if n['day']==d and n['send']==send]:
      cands=[l for l in ls if n['match'].lower() in (l['alt'] or l['text']).lower() and l['aid'] in boxes]
      if not cands: print('NO MATCH',d,send,n['match'],file=sys.stderr); continue
      l=max(cands,key=lambda l:l['v']); b=boxes[l['aid']]
      by=ytop+(b['top']+b['h']/2)*SC; bx=x0+OFF[send]+(b['left']+b['w'])*SC
      share=round(l['v']/tot*100)
      items.append(dict(by=by,bx=bx,share=share,**n))
    items.sort(key=lambda i:i['by'])
    last=-1e9
    for i in items:
      sy=max(i['by']-SH/2,last+GAP); last=sy+SH
      sx=x0+OFF[send]+230
      col='light_green' if i['kind']=='worked' else 'light_pink'
      lab='Worked' if i['kind']=='worked' else "Didn't work"
      content=f"<b>{lab} – {i['share']}% of clicks</b><br>{html.escape(i['why'],quote=False)}"
      out.append(f'<line data-type="divider" x1="{i["bx"]+4:.0f}" y1="{i["by"]:.0f}" x2="{sx:.0f}" y2="{sy+SH/2:.0f}" stroke="#313131" stroke-width="2" />')
      out.append(f'<rect data-type="sticky" x="{sx:.0f}" y="{sy:.0f}" width="{SW}" height="{SH}" data-color="{col}" data-content="{html.escape(content)}" />')
print('<svg xmlns="http://www.w3.org/2000/svg">\n'+'\n'.join(out)+'\n</svg>')
