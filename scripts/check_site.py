#!/usr/bin/env python3
"""Check static links, anchors, metadata and image sources without external packages."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import re,json,argparse
parser=argparse.ArgumentParser();parser.add_argument('--output',default='.');args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1];D=ROOT/args.output
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.tags=[];self.feed(text)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
 def handle_startendtag(self,t,a):self.handle_starttag(t,a)
errors=[];refs=0;pages={p.name:Page(p.read_text()) for p in D.glob('*.html') if not p.name.startswith('qa-')}
for name,p in pages.items():
 ids=[a['id'] for t,a in p.tags if 'id' in a]
 if len(ids)!=len(set(ids)):errors.append(name+': duplicate ID')
 if sum(t=='h1' for t,a in p.tags)!=1:errors.append(name+': h1 count')
 for t,a in p.tags:
  if t=='img' and any(k not in a for k in ('alt','width','height')):errors.append(name+': image metadata')
  if t=='a' and a.get('target')=='_blank' and 'noopener' not in a.get('rel',''):errors.append(name+': external rel')
  paths=[a[k] for k in ('src','href','poster') if a.get(k)]
  paths += [v.strip().split()[0] for v in a.get('srcset','').split(',') if v.strip()]
  for ref in paths:
   u=urlsplit(ref)
   if u.scheme or u.netloc:continue
   refs+=1;target=D/(unquote(u.path) or name)
   if not target.is_file():errors.append(name+': missing '+ref)
   if u.fragment and target.suffix=='.html' and target.name in pages:
    if not any(a.get('id')==u.fragment for t,a in pages[target.name].tags):errors.append(name+': missing anchor '+ref)
  for key in ('aria-controls','aria-describedby','aria-labelledby'):
   for ident in a.get(key,'').split():
    if ident not in ids:errors.append(name+': missing '+key+' '+ident)
for css in (D/'css').glob('*.css'):
 for ref in re.findall(r'url\([\'\"]?([^\)\'\"]+)',css.read_text()):
  u=urlsplit(unquote(ref))
  if u.path and not u.scheme and not u.netloc and not (css.parent/unquote(u.path)).exists():errors.append(css.name+': missing '+ref)
new=(D/'featured-klyo.html').read_text()
def answers(s):
 block=re.search(r'<dl class="qa">(.*?)</dl>',s,re.S).group(1)
 return re.findall(r'<dd[^>]*>(.*?)</dd>',block,re.S)
assert len(answers(new))==5
expected=json.loads((ROOT/'scripts/interview-baseline.json').read_text())
assert answers(new)==expected, 'Interview answers changed'
assert (D/'featured.html').read_bytes()==(D/'index.html').read_bytes()
print(f'{len(pages)} pages; {refs} local references; 5 interview answers unchanged.')
if errors:raise SystemExit('\n'.join(errors))
print('No missing files, anchors, labels or duplicate IDs.')
