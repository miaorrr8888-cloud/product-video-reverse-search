"""Search public video metadata via the official YouTube API, or normalize saved responses."""
import argparse,json,os,re
from urllib.request import Request,urlopen
from urllib.parse import urlencode

def convert(data,product):
    if not isinstance(data,dict) or not isinstance(data.get('items'),list):raise ValueError('YouTube items array required')
    candidates=[]
    for item in data['items']:
        vid=item.get('id',{}).get('videoId','');s=item.get('snippet',{})
        if not re.fullmatch(r'[A-Za-z0-9_-]{11}',vid):continue
        if not isinstance(s.get('title'),str):raise ValueError('video title required')
        candidates.append({'url':'https://www.youtube.com/watch?v='+vid,'title':s['title'],'source':'YouTube',
                           'published':s.get('publishedAt'),'views':None,'match_level':'unknown'})
    return {'product':product,'candidates':candidates,'metadata_origin':'YOUTUBE_RESPONSE','visual_identity_verified':False}

def fetch(query,limit,key):
    if not isinstance(query,str) or not query.strip() or type(limit)!=int or not 1<=limit<=50:raise ValueError('query required; limit 1..50')
    if not key:raise ValueError('Set YOUTUBE_API_KEY locally; never paste it into prompts or input files')
    url='https://www.googleapis.com/youtube/v3/search?'+urlencode({'part':'snippet','type':'video','q':query,'maxResults':limit})
    # Keep the key out of URLs and diagnostics.
    request=Request(url,headers={'X-Goog-Api-Key':key})
    with urlopen(request,timeout=20) as response:
        raw=response.read(4_000_001)
    if len(raw)>4_000_000:raise ValueError('response too large')
    return json.loads(raw)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--query',required=True);p.add_argument('--response');p.add_argument('--limit',type=int,default=10);p.add_argument('--live',action='store_true');a=p.parse_args()
    if bool(a.live)==bool(a.response):p.error('choose --response for offline use or --live for a quota-consuming official API call')
    try:
        data=json.load(open(a.response,encoding='utf-8-sig')) if a.response else fetch(a.query,a.limit,os.environ.get('YOUTUBE_API_KEY'))
        report=convert(data,{'keywords':[a.query]});report['execution']='OFFLINE_RESPONSE' if a.response else 'LIVE_API_RESPONSE'
    except (OSError,ValueError,TypeError):p.exit(2,'Search failed; check input, API access and quota. No credentials are included in this diagnostic.\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
