"""Rank supplied video candidates; no crawling, visual recognition or metric verification."""
import argparse
from datetime import datetime,timezone
import json
import math
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode

MATCH_SCORE={'confirmed':1.0,'similar':0.6,'unknown':0.3}
SOURCE_CRED={'YouTube':0.90,'TikTok':0.85,'Douyin':0.90,'抖音':0.90,'TikTok Shop':0.80}

def norm(value): return str(value or '').lower()

def keyword_overlap(product,title):
    words=[norm(product.get('brand')),norm(product.get('model'))]+[norm(x) for x in product.get('keywords',[]) if x]
    words=list(dict.fromkeys(w for w in words if w)); hits=sum(w in norm(title) for w in words)
    return hits/len(words) if words else 0.0,hits,len(words)

def parse_date(value):
    dt=datetime.fromisoformat(value.replace('Z','+00:00'))
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)

def recency_score(published,as_of=None):
    if not published: return None
    try:
        date=parse_date(published); now=as_of or datetime.now(timezone.utc)
        days=(now-date).total_seconds()/86400
        return None if days<0 else 0.5**(days/180)
    except (ValueError,TypeError,AttributeError): return None

def interaction_score(value):
    if value is None or isinstance(value,bool): return None
    try: number=float(value)
    except (ValueError,TypeError): return None
    if not math.isfinite(number) or number<0: return None
    return min(1.0,math.log10(number+1)/6)

def canonical_url(value):
    try:
        p=urlsplit(value)
        if p.scheme!='https' or not p.hostname or p.username or p.password: raise ValueError('HTTPS URL required')
        query=[(k,v) for k,v in parse_qsl(p.query,keep_blank_values=True) if not k.lower().startswith('utm_') and k.lower() not in {'fbclid','gclid'}]
        return urlunsplit((p.scheme,p.netloc.lower(),p.path.rstrip('/'),urlencode(sorted(query)),''))
    except (TypeError,AttributeError): raise ValueError('URL must be text')

def rank(data,as_of=None):
    if not isinstance(data,dict) or not isinstance(data.get('product'),dict) or not isinstance(data.get('candidates'),list):
        raise ValueError('Expected product object and candidates array')
    product=data['product']
    if not isinstance(product.get('keywords',[]),list): raise ValueError('keywords must be an array')
    rows=[]; seen=set(); duplicates=0
    for candidate in data['candidates']:
        if not isinstance(candidate,dict): raise ValueError('Each candidate must be an object')
        url=canonical_url(candidate.get('url'))
        if url in seen: duplicates+=1; continue
        seen.add(url)
        title=candidate.get('title','')
        if not isinstance(title,str): raise ValueError('title must be text')
        match=candidate.get('match_level') or 'unknown'
        if match not in MATCH_SCORE: raise ValueError('match_level must be confirmed, similar or unknown')
        overlap,_,_=keyword_overlap(product,title)
        recent=recency_score(candidate.get('published'),as_of); views=interaction_score(candidate.get('views'))
        weights={'match':.40,'keywords':.20,'views':.20,'source':.10,'recency':.10}
        if views is None: weights['match']+=weights.pop('views')
        if recent is None: weights['match']+=weights.pop('recency')
        values={'match':MATCH_SCORE[match],'keywords':overlap,'views':views or 0.0,
                'source':SOURCE_CRED.get(candidate.get('source'),.70),'recency':recent or 0.0}
        parts={key:round(weight*values[key],6) for key,weight in weights.items()}
        supplied={key:candidate.get(key) for key in ('source','title','published','views','likes','comments')}
        rows.append({**supplied,'url':url,'match_level':match,'score':round(sum(parts.values()),6),
                     'weights':weights,'score_parts':parts,'keyword_overlap':overlap,
                     'interaction_known':views is not None,'recency_known':recent is not None,
                     'content_verified':False,'metrics_origin':'SUPPLIED_UNVERIFIED'})
    rows.sort(key=lambda row:(-row['score'],row['url']))
    return {'as_of':(as_of or datetime.now(timezone.utc)).isoformat(),'results':rows,'duplicates_removed':duplicates,
            'notice':'Heuristic ranking of supplied claims; URLs, identity and metrics were not independently verified.'}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('input'); p.add_argument('--json',action='store_true'); p.add_argument('--as-of')
    args=p.parse_args(argv)
    try:
        with open(args.input,encoding='utf-8-sig') as f: data=json.load(f)
        report=rank(data,parse_date(args.as_of) if args.as_of else None)
    except (OSError,ValueError,TypeError) as exc: p.exit(2,'Input error: '+str(exc)+'\n')
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)); return 0
    print('# 商品视频候选排序\n\n'+report['notice']+'\n')
    for index,row in enumerate(report['results'][:5],1):
        print(f"## {index}. {row['title']} — {row['score']}\n- URL: {row['url']}\n- 匹配由输入声明: {row['match_level']}\n- 播放量是否有效填写: {row['interaction_known']}（未独立核实）\n- 分数构成: {row['score_parts']}\n")
    print('去重数:',report['duplicates_removed']); return 0

if __name__=='__main__': raise SystemExit(main())
