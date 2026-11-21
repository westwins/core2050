import math, pathlib, urllib.request, concurrent.futures, io, json
import numpy as np
from PIL import Image, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'frontend/assets'
CACHE = ROOT / '.cache/terrain-tiles'
CACHE.mkdir(exist_ok=True, parents=True)
ZOOM = 8
BBOX = [125.8, 35.7, 129.35, 37.95]
def pixel(lon, lat):
    return ((lon+180)/360*256*2**ZOOM, (1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*256*2**ZOOM)
left, top = pixel(BBOX[0], BBOX[3])
right, bottom = pixel(BBOX[2], BBOX[1])
x0,y0,x1,y1 = int(left//256),int(top//256),int(right//256),int(bottom//256)
def tile(xy):
    x,y=xy
    f=CACHE/f'{ZOOM}-{x}-{y}.png'
    if not f.exists():
        urllib.request.urlretrieve(f'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{ZOOM}/{x}/{y}.png', f)
    return x,y,Image.open(f).convert('RGB')
atlas=Image.new('RGB',((x1-x0+1)*256,(y1-y0+1)*256))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    for x,y,img in pool.map(tile,[(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1)]):
        atlas.paste(img,((x-x0)*256,(y-y0)*256))
arr=np.array(atlas).astype(float)
heights=arr[:,:,0]*256+arr[:,:,1]+arr[:,:,2]/256-32768
crop=Image.fromarray(heights.astype('float32')).crop((round(left-x0*256),round(top-y0*256),round(right-x0*256),round(bottom-y0*256))).resize((1400,1100),Image.Resampling.BILINEAR)
h=np.asarray(crop)
smooth=sum(np.roll(np.roll(h,dy,axis=0),dx,axis=1) for dy in (-1,0,1) for dx in (-1,0,1))/9
gy,gx=np.gradient(smooth)
light=np.clip(.8+(-gx*.018-gy*.021),.38,1.25)
t=np.clip(h/1500,0,1)
base=np.stack([22+t*44,43+t*47,43+t*33],axis=-1)*light[:,:,None]
sea=h<=0
base[sea]=[8,25,32]
levels=np.floor(h/180)
lines=(levels!=np.roll(levels,1,axis=0))|(levels!=np.roll(levels,1,axis=1))
lines &= h>80
base[lines]=base[lines]*.83+np.array([128,157,136])*.17
Image.fromarray(np.uint8(np.clip(base,0,255))).save(OUT/'terrain.webp',quality=90)
(OUT/'terrain.json').write_text(json.dumps({'bbox':BBOX,'projection':'Web Mercator','source':'Mapzen Terrain Tiles on AWS','zoom':ZOOM,'contour_interval_m':180,'accessed':'2026-11-21'}),encoding='utf8')
print('Terrain ready', BBOX, 'tiles', (x1-x0+1)*(y1-y0+1))
