"""Retrieve visually similar local images; no Internet image reverse search or identity claim."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageOps,UnidentifiedImageError

def feature(path):
    with Image.open(path) as original:
        pixels=original.width*original.height
        if pixels>40_000_000:raise ValueError('image exceeds pixel limit')
        im=ImageOps.exif_transpose(original).convert('RGB')
        gray=im.convert('L').resize((9,8));p=list(gray.tobytes());bits=[p[y*9+x]>p[y*9+x+1] for y in range(8) for x in range(8)]
        small=im.resize((32,32));hist=[0]*64
        values=small.tobytes()
        for i in range(0,len(values),3):
            r,g,b=values[i:i+3];hist[(r//64)*16+(g//64)*4+b//64]+=1/1024
        return bits,hist

def search(query,directory,limit=10):
    if type(limit)!=int or not 1<=limit<=100:raise ValueError('limit must be 1..100')
    query=Path(query).resolve();root=Path(directory).resolve()
    if not root.is_dir():raise ValueError('candidate directory missing')
    qb,qh=feature(query);rows=[];skipped=[];count=0
    for raw in sorted(root.rglob('*')):
        if raw.suffix.lower() not in {'.png','.jpg','.jpeg','.webp','.bmp'} or not raw.is_file():continue
        if raw.is_symlink() or not raw.resolve().is_relative_to(root):continue
        path=raw.resolve()
        if path==query:continue
        count+=1
        if count>5000:raise ValueError('more than 5000 candidates; narrow the directory')
        try:bits,hist=feature(path)
        except (OSError,ValueError,UnidentifiedImageError):skipped.append(raw.relative_to(root).as_posix());continue
        shape=sum(a!=b for a,b in zip(qb,bits))/64;color=sum(min(a,b) for a,b in zip(qh,hist))
        rows.append({'file':raw.relative_to(root).as_posix(),'score':round(.5*(1-shape)+.5*color,6),
                     'dhash_distance':round(shape,6),'color_histogram_overlap':round(color,6),'identity_verified':False})
    rows.sort(key=lambda r:(-r['score'],r['file']))
    return {'results':rows[:limit],'candidates_scanned':count,'skipped':skipped,'scope':'LOCAL_IMAGE_SIMILARITY_ONLY',
            'notice':'Heuristic shape/color ranking. Different products can score highly; scene changes can lower scores. Human model and shape comparison required.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('query');p.add_argument('directory');p.add_argument('--limit',type=int,default=10);a=p.parse_args()
    try:r=search(a.query,a.directory,a.limit)
    except (OSError,ValueError) as e:p.exit(2,'Image search error: '+str(e)+'\n')
    print(json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False))
if __name__=='__main__':main()
