"""Original low-poly environment kit. Python 3 + Pillow + NumPy. Units: metres, Y up."""
from pathlib import Path
import math, json, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'Assets'/'NightShift'
R=random.Random(1704)
N=np.random.default_rng(1704)
COLORS={'plaster':(139,142,123),'paint':(72,94,82),'rust':(101,66,45),'wood':(102,77,52),'rubber':(33,37,36),'steel':(135,145,139),'glass':(191,204,164),'tile':(114,115,99),'warning':(184,155,67),'number':(185,179,150)}
TEXTURES={}
font_path='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(n):
    try:return ImageFont.truetype(font_path,n)
    except OSError:return ImageFont.load_default()
for name,color in COLORS.items():
    s=512
    small=Image.fromarray(N.integers(0,255,(16,16),dtype=np.uint8)).resize((s,s),Image.Resampling.BICUBIC)
    broad=(np.array(small).astype(float)-128)/12
    noise=N.normal(0,5,(s,s))
    a=np.clip(np.array(color)[None,None,:]+(broad+noise)[:,:,None],0,255).astype('uint8')
    im=Image.fromarray(a); d=ImageDraw.Draw(im)
    if name in ['paint','rust','plaster','wood']:
        for i in range(270 if name!='plaster' else 95):
            x,y=R.randrange(s),R.randrange(s); w,h=R.randrange(2,14),R.randrange(2,20)
            c=R.choice([(76,60,43),(110,78,48),(47,59,51)]) if name!='plaster' else (111,111,94)
            d.polygon([(x,y),(x+w,y+2),(x+w-3,y+h),(x+2,y+h-2)],fill=c)
        for i in range(75):
            x,y=R.randrange(s),R.randrange(s)
            d.line([(x,y),(x+R.randrange(-2,3),y+R.randrange(8,65))],fill=tuple(max(0,v-22) for v in color),width=1)
    if name=='tile':
        for y in range(0,s,128):
            for x in range(0,s,128):
                d.rectangle((x,y,x+127,y+127),outline=(48,53,48),width=5)
                d.line((x+6,y+6,x+121,y+6),fill=(145,145,124),width=2)
        d.line([(128,250),(165,271),(170,310),(207,333)],fill=(52,55,46),width=2)
    if name=='wood':
        for x in range(10,s,35):d.line((x,0,x+R.randint(-10,10),s),fill=(64,53,39),width=2)
    if name=='rubber':
        for y in range(0,s,32):d.line((0,y,s,y),fill=(18,22,21),width=4)
    if name=='warning':
        d.polygon([(256,42),(460,432),(52,432)],fill=(27,30,24))
        d.polygon([(256,83),(426,410),(85,410)],fill=(197,168,75))
        d.polygon([(273,150),(195,288),(249,280),(230,360),(326,230),(268,241)],fill=(24,27,23))
    if name=='number':
        d.rectangle((10,10,501,501),outline=(56,61,52),width=12)
        d.text((256,255),'17',font=font(270),anchor='mm',fill=(36,43,36))
    im.save(ASSETS/'Textures'/f'{name}.png');TEXTURES[name]=np.array(im)

class Mesh:
    def __init__(self,name):self.name=name;self.faces=[]
    def face(self,p,mat,uv=None):
        if uv is None:uv=[(0,0),(1,0),(1,1),(0,1)][:len(p)]
        self.faces.append((np.array(p,dtype=float),mat,np.array(uv,dtype=float)))
    def box(self,c,size,mat):
        x,y,z=c;a,b,d=np.array(size)/2
        v=[(x-a,y-b,z-d),(x+a,y-b,z-d),(x+a,y+b,z-d),(x-a,y+b,z-d),(x-a,y-b,z+d),(x+a,y-b,z+d),(x+a,y+b,z+d),(x-a,y+b,z+d)]
        for ids in [(0,3,2,1),(4,5,6,7),(0,4,7,3),(1,2,6,5),(3,7,6,2),(0,1,5,4)]:self.face([v[i] for i in ids],mat)
    def tube(self,a,b,r,mat,n=10,r2=None):
        a,b=np.array(a,dtype=float),np.array(b,dtype=float);axis=b-a;axis/=np.linalg.norm(axis)
        u=np.cross(axis,[0,1,0] if abs(axis[1])<.9 else [1,0,0]);u/=np.linalg.norm(u);v=np.cross(axis,u)
        r2=r if r2 is None else r2
        rings=[[c+rad*(u*math.cos(t*2*math.pi/n)+v*math.sin(t*2*math.pi/n)) for t in range(n)] for c,rad in [(a,r),(b,r2)]]
        for i in range(n):
            j=(i+1)%n
            self.face([rings[0][i],rings[0][j],rings[1][j],rings[1][i]],mat)
            self.face([a,rings[0][j],rings[0][i]],mat,[(.5,.5),(0,0),(1,0)])
            self.face([b,rings[1][i],rings[1][j]],mat,[(.5,.5),(0,0),(1,0)])
    def moved(self,offset,angle=0):
        m=Mesh(self.name);t=math.radians(angle);rot=np.array([[math.cos(t),0,math.sin(t)],[0,1,0],[-math.sin(t),0,math.cos(t)]])
        m.faces=[(p@rot.T+offset,mat,uv) for p,mat,uv in self.faces];return m
    def save(self):
        out=['# NightShift original asset | metres | Y up','mtllib NightShift.mtl',f'o {self.name}'];idx=1
        for p,mat,uv in self.faces:
            normal=np.cross(p[1]-p[0],p[2]-p[0]); normal/=np.linalg.norm(normal)
            out += ['v %.6f %.6f %.6f'%tuple(v) for v in p]
            out += ['vt %.6f %.6f'%tuple(v) for v in uv]
            out += ['vn %.6f %.6f %.6f'%tuple(normal) for v in p]
            out += [f'usemtl {mat}','s off']
            for k in range(1,len(p)-1):out.append('f '+' '.join(f'{j}/{j}/{j}' for j in (idx,idx+k,idx+k+1)))
            idx+=len(p)
        (ASSETS/'Models'/f'{self.name}.obj').write_text('\n'.join(out)+'\n')
        vs=np.concatenate([p for p,_,_ in self.faces]);return dict(name=self.name,triangles=sum(len(p)-2 for p,_,_ in self.faces),bounds_m=np.round(vs.max(0)-vs.min(0),3).tolist())
models=[]
def model(name):m=Mesh(name);models.append(m);return m
m=model('Floor_3m');m.box((0,-.08,0),(3,.16,3),'tile')
m=model('Wall_3m');m.box((0,2.05,0),(3,1.5,.16),'plaster');m.box((0,.65,0),(3,1.3,.16),'paint');m.box((0,.06,.095),(3,.12,.07),'rubber');m.box((0,1.31,.087),(3,.035,.035),'wood')
m=model('DoorFrame');
for x in [-.63,.63]:m.box((x,1.12,0),(.12,2.24,.22),'wood');m.box((x,1.12,.13),(.17,2.24,.045),'paint')
m.box((0,2.2,0),(1.38,.12,.22),'wood');m.box((0,2.23,.13),(1.43,.13,.045),'paint')
m=model('Door_17');m.box((.55,1.04,0),(1.1,2.08,.065),'paint')
for y,h in [(1.54,.68),(.54,.65)]:
    m.box((.55,y,.04),(.85,h,.018),'wood')
    for x in [.105,.995]:m.box((x,y,.06),(.045,h+.06,.035),'paint')
    for yy in [y-h/2,y+h/2]:m.box((.55,yy,.06),(.93,.045,.035),'paint')
m.box((.55,1.8,.065),(.18,.13,.015),'number');m.box((.95,1.01,.055),(.075,.22,.025),'rust');m.tube((.95,1.06,.07),(.95,1.06,.13),.018,'steel',8);m.tube((.95,1.06,.13),(.82,1.06,.13),.018,'steel',8)
for y in [.3,1.8]:m.tube((0,y,0),(0,y+.12,0),.024,'rust',8)
m=model('Locker');m.box((0,.95,0),(.62,1.8,.45),'paint');m.box((0,.94,.234),(.55,1.67,.035),'rust');m.box((0,.94,.256),(.52,1.64,.025),'paint')
for y in [1.52,1.46,1.4,.38,.32,.26]:
    m.box((0,y,.272),(.34,.022,.008),'rubber');m.box((0,y+.012,.28),(.35,.012,.018),'steel')
m.box((.18,.91,.28),(.035,.19,.025),'rubber');m.box((.18,.93,.31),(.025,.12,.035),'steel')
for x in [-.23,.23]:
    for z in [-.16,.16]:m.box((x,.055,z),(.07,.11,.07),'rust')
m=model('FuseBox');m.box((0,.4,0),(.58,.8,.18),'rust');m.box((0,.4,.102),(.54,.75,.03),'paint');m.box((0,.48,.122),(.2,.23,.012),'warning');m.box((.21,.35,.135),(.025,.16,.03),'steel')
for x in [-.21,.21]:
    for y in [.08,.72]:m.tube((x,y,.118),(x,y,.13),.009,'steel',8)
for y in [.12,.15,.18]:m.box((0,y,.12),(.3,.012,.008),'rubber')
for x in [-.16,.12]:m.tube((x,0,0),(x,-.16,0),.025,'rubber',8)
m=model('Bench');
for x in [-.64,.64]:
    for z in [-.19,.19]:m.box((x,.22,z),(.045,.44,.045),'rust')
    m.box((x,.39,0),(.055,.05,.5),'rust');m.box((x,.65,-.21),(.045,.6,.045),'rust')
for z in [-.16,0,.16]:m.box((0,.46,z),(1.6,.065,.14),'wood')
for y in [.68,.86]:m.box((0,y,-.23),(1.6,.14,.06),'wood')
m=model('Pipe');m.tube((0,.08,0),(0,2.65,0),.048,'rust',10)
for y in [.27,1.36,2.45]:m.tube((0,y-.035,0),(0,y+.035,0),.067,'steel',10);m.box((0,y,-.065),(.14,.045,.1),'rust')
m.tube((0,.65,0),(0,.65,.14),.028,'rust',8)
# A valve wheel assembled from a continuous faceted ring and spokes.
for i in range(12):
    a,b=i*math.tau/12,(i+1)*math.tau/12
    m.tube((.13*math.cos(a),.65+.13*math.sin(a),.16),(.13*math.cos(b),.65+.13*math.sin(b),.16),.014,'paint',6)
for i in range(4):
    a=i*math.pi/2;m.tube((0,.65,.16),(.13*math.cos(a),.65+.13*math.sin(a),.16),.01,'steel',6)
m=model('WallLamp');m.box((0,0,0),(.48,.19,.06),'rust');m.box((0,0,.055),(.41,.125,.065),'glass')
for x in [-.2,-.1,0,.1,.2]:m.box((x,0,.097),(.012,.15,.015),'steel')
for y in [-.075,.075]:m.box((0,y,.097),(.45,.014,.015),'steel')
m=model('Flashlight');m.tube((0,0,0),(0,0,.19),.027,'rubber',12);m.tube((0,0,.19),(0,0,.25),.027,'paint',12,.048);m.tube((0,0,.25),(0,0,.275),.05,'steel',12);m.tube((0,0,.276),(0,0,.279),.041,'glass',12);m.box((0,.029,.145),(.02,.009,.033),'paint')
for z in [.025,.05,.075,.1]:m.tube((0,0,z),(0,0,z+.006),.029,'paint',12)
m=model('Fuse');m.tube((0,0,0),(0,.07,0),.013,'glass',10)
for y in [0,.055]:m.tube((0,y,0),(0,y+.015,0),.015,'steel',10)
m=model('Crate');m.box((0,.25,0),(.64,.5,.48),'wood')
for x in [-.26,.26]:
    for z in [-.25,.25]:m.box((x,.25,z),(.07,.5,.035),'wood')
for y in [.06,.44]:m.box((0,y,.26),(.64,.06,.035),'rust');m.box((0,y,-.26),(.64,.06,.035),'rust')

mtl=[]
for name in COLORS:
    mtl += [f'newmtl {name}','Ka 0.1 0.1 0.1','Kd 1 1 1','Ks 0.05 0.05 0.05','Ns 8',f'map_Kd ../Textures/{name}.png','']
(ASSETS/'Models'/'NightShift.mtl').write_text('\n'.join(mtl))
stats=[m.save() for m in models]
(ROOT/'manifest.json').write_text(json.dumps({'units':'metres','up':'Y','texture_size':512,'assets':stats},indent=2))

# CPU orthographic renderer: previews use the exported geometry and UVs, not concept art.
def render(meshes,w=640,h=600):
    faces=[f for m in meshes for f in m.faces]
    allp=np.concatenate([p for p,_,_ in faces]);center=(allp.min(0)+allp.max(0))/2
    view=np.array([.85,.6,1.35]);view/=np.linalg.norm(view)
    right=np.cross([0,1,0],view);right/=np.linalg.norm(right);up=np.cross(view,right)
    basis=np.array([right,up,view]);proj=(allp-center)@basis.T
    span=np.ptp(proj[:,:2],axis=0);scale=min((w-75)/max(span[0],.01),(h-70)/max(span[1],.01))
    pixels=np.zeros((h,w,3),dtype=np.uint8);pixels[:]=[28,33,32];depth=np.full((h,w),-np.inf)
    light=np.array([-.4,.8,1]);light/=np.linalg.norm(light)
    for p,mat,uv in faces:
        n=np.cross(p[1]-p[0],p[2]-p[0]);n/=np.linalg.norm(n)
        if np.dot(n,view)<=0:continue
        q=(p-center)@basis.T;q[:,:2]*=scale;q[:,0]+=w/2;q[:,1]=h/2-q[:,1]
        shade=.45+.55*max(0,np.dot(n,light))
        for k in range(1,len(q)-1):
            ids=[0,k,k+1];t=q[ids];tuv=uv[ids]
            x0=max(0,int(np.floor(t[:,0].min())));x1=min(w-1,int(np.ceil(t[:,0].max())))
            y0=max(0,int(np.floor(t[:,1].min())));y1=min(h-1,int(np.ceil(t[:,1].max())))
            if x1<x0 or y1<y0:continue
            yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
            den=(t[1,1]-t[2,1])*(t[0,0]-t[2,0])+(t[2,0]-t[1,0])*(t[0,1]-t[2,1])
            if abs(den)<1e-8:continue
            a=((t[1,1]-t[2,1])*(xx-t[2,0])+(t[2,0]-t[1,0])*(yy-t[2,1]))/den
            b=((t[2,1]-t[0,1])*(xx-t[2,0])+(t[0,0]-t[2,0])*(yy-t[2,1]))/den;c=1-a-b
            z=a*t[0,2]+b*t[1,2]+c*t[2,2];zbuf=depth[y0:y1+1,x0:x1+1]
            mask=(a>=0)&(b>=0)&(c>=0)&(z>zbuf)
            texuv=a[:,:,None]*tuv[0]+b[:,:,None]*tuv[1]+c[:,:,None]*tuv[2]
            tx=np.clip((texuv[:,:,0]*511).astype(int),0,511);ty=np.clip(((1-texuv[:,:,1])*511).astype(int),0,511)
            col=np.clip(TEXTURES[mat][ty,tx]*shade,0,255).astype('uint8')
            pixels[y0:y1+1,x0:x1+1][mask]=col[mask];zbuf[mask]=z[mask]
    return Image.fromarray(pixels)

labels=['Плиточный пол · 3 м','Стена · 3 м','Дверная коробка','Дверь квартиры 17','Металлический шкафчик','Электрощиток','Скамейка','Труба с вентилем','Защищённый светильник','Карманный фонарь','Предохранитель','Деревянный ящик']
sheet=Image.new('RGB',(1600,1470),(20,25,24));d=ImageDraw.Draw(sheet)
d.text((38,25),'НОЧНОЙ ОБХОД',font=font(38),fill=(218,222,204));d.text((38,75),'Набор окружения / 12 моделей / исходная геометрия',font=font(20),fill=(144,157,146))
for i,m in enumerate(models):
    x=(i%4)*400;y=130+(i//4)*440
    sheet.paste(render([m],390,350),(x+5,y));d.text((x+20,y+360),labels[i],font=font(18),fill=(212,218,202));d.text((x+20,y+390),f'{stats[i]["triangles"]} треугольников',font=font(15),fill=(137,155,143))
sheet.save(ROOT/'Preview'/'asset-sheet.jpg',quality=94)
# A small assembled corner for an immediate sense of scale.
lookup={m.name:m for m in models}
scene=[lookup['Floor_3m'],lookup['Wall_3m'].moved((0,0,-1.5)),lookup['Wall_3m'].moved((-1.5,0,0),90),lookup['Locker'].moved((-.9,0,-1.18)),lookup['FuseBox'].moved((.75,1.15,-1.29)),lookup['Bench'].moved((-.9,0,.2),90),lookup['Pipe'].moved((1.3,0,-1.25)),lookup['WallLamp'].moved((.5,2.5,-1.35)),lookup['Crate'].moved((.9,0,.7))]
render(scene,1400,1200).save(ROOT/'Preview'/'room-corner.png')
print(json.dumps({'models':len(models),'triangles':sum(s['triangles'] for s in stats),'previews':2}))
