"""Original post-Soviet courtyard and apartment props; fictional signage, no brands."""

def surface(name,color,kind='plain'):
    COLORS[name]=color
    rng=np.random.default_rng(sum(map(ord,name)))
    a=np.clip(np.array(color)[None,None,:]+rng.normal(0,3,(512,512,1)),0,255).astype('uint8')
    im=Image.fromarray(a);d=ImageDraw.Draw(im)
    if kind=='chips':
        rr=random.Random(name)
        for i in range(180):
            x,y=rr.randrange(512),rr.randrange(512);w,h=rr.randrange(1,10),rr.randrange(2,16)
            d.polygon([(x,y),(x+w,y+2),(x+w-2,y+h),(x,y+h-3)],fill=(97,77,59))
    if kind=='concrete':
        for y in [5,506]:d.line((0,y,512,y),fill=(108,110,100),width=4)
        for x in [5,506]:d.line((x,0,x,512),fill=(108,110,100),width=4)
    im.save(ASSETS/'Textures'/f'{name}.png');TEXTURES[name]=np.array(im)

def label(name,text,bg,fg,ratio=3,lines=None):
    COLORS[name]=bg
    w=1024;h=round(w/ratio);im=Image.new('RGB',(w,h),bg);d=ImageDraw.Draw(im)
    d.rectangle((8,8,w-9,h-9),outline=fg,width=4)
    parts=lines or [text]
    size=int(h/(len(parts)+.7))
    while max(d.textbbox((0,0),t,font=font(size))[2] for t in parts)>w-60:size-=1
    for i,t in enumerate(parts):d.text((w/2,h*(i+.5)/len(parts)),t,font=font(size),anchor='mm',fill=fg)
    im=im.resize((512,512),Image.Resampling.LANCZOS);im.save(ASSETS/'Textures'/f'{name}.png');TEXTURES[name]=np.array(im)

def front(m,x,y,z,w,h,mat):
    m.face([(x-w/2,y-h/2,z),(x+w/2,y-h/2,z),(x+w/2,y+h/2,z),(x-w/2,y+h/2,z)],mat)

surface('panel',(165,160,142),'concrete');surface('bluepaint',(57,91,113),'chips');surface('ochrepaint',(165,129,59),'chips');surface('sand',(152,135,96));surface('enamel',(184,180,152),'chips')
label('shop_sign','ПРОДУКТЫ',(31,69,80),(219,213,175),5.8)
label('address_sign','',(29,56,86),(211,219,205),2.8,['ТИХАЯ УЛИЦА','17'])
label('entrance_sign','',(188,188,163),(40,51,43),2.5,['ПОДЪЕЗД 2','КВАРТИРЫ 17–32'])
label('garage_number','27',(70,76,65),(195,194,164),1.3)
# Purpose-made paper texture with tear tabs, rather than generic decoration.
COLORS['notices']=(171,165,135)
im=Image.new('RGB',(512,512),(73,81,68));d=ImageDraw.Draw(im)
for x,y,w,h,title in [(22,28,215,210,'САНТЕХНИК'),(264,55,215,270,'РЕМОНТ'),(55,270,230,215,'ПРОПАЛ КОТ')]:
    d.rectangle((x,y,x+w,y+h),fill=(192,184,147));d.text((x+w/2,y+27),title,font=font(21),anchor='mm',fill=(47,48,38))
    for yy in range(y+55,y+h-40,19):d.line((x+14,yy,x+w-16,yy),fill=(95,94,73),width=2)
    for xx in range(x+20,x+w-15,23):d.line((xx,y+h-28,xx,y+h),fill=(69,72,57),width=1)
im.save(ASSETS/'Textures/notices.png');TEXTURES['notices']=np.array(im)
# Maroon geometric carpet. The texture is authored at its physical aspect ratio.
COLORS['carpet']=(93,37,32)
im=Image.new('RGB',(512,768),(93,37,32));d=ImageDraw.Draw(im)
for inset,color,width in [(12,(184,146,92),8),(30,(40,48,42),16),(53,(171,122,70),5),(66,(177,148,100),3)]:d.rectangle((inset,inset,511-inset,767-inset),outline=color,width=width)
for y in [190,384,578]:
    for rx,ry,c in [(137,154,(39,50,48)),(111,128,(177,145,92)),(88,102,(112,53,42)),(39,50,(186,161,114))]:d.polygon([(256-rx,y),(256,y-ry),(256+rx,y),(256,y+ry)],fill=c)
for y in range(90,700,42):
    for x in [88,424]:d.polygon([(x-10,y),(x,y-14),(x+10,y),(x,y+14)],fill=(174,137,84))
im=im.resize((512,512));im.save(ASSETS/'Textures/carpet.png');TEXTURES['carpet']=np.array(im)

m=model('CIS_PanelFacade')
# A 3 x 2.8 metre facade bay with a real window recess.
for x in [-1.1,1.1]:m.box((x,1.4,0),(.8,2.8,.22),'panel')
m.box((0,.47,0),(1.4,.94,.22),'panel');m.box((0,2.55,0),(1.4,.5,.22),'panel')
m.box((0,1.62,-.06),(1.4,1.36,.035),'screen')
for x in [-.7,0,.7]:m.box((x,1.62,.035),(.045,1.42,.09),'enamel')
for y in [.93,2.31]:m.box((0,y,.035),(1.45,.045,.09),'enamel')
m.box((.35,1.96,.035),(.68,.035,.09),'enamel');m.box((0,.91,.12),(1.57,.045,.37),'steel')
for x in [-1.49,1.49]:m.box((x,1.4,.115),(.015,2.8,.012),'rubber')

m=model('CIS_GlazedBalcony')
m.box((0,0,.32),(2.7,.12,1.2),'panel');m.box((0,.49,.88),(2.55,.91,.07),'bluepaint')
for x in [-1.25,1.25]:m.box((x,.49,.32),(.07,.91,1.1),'bluepaint')
for x in [-1.29,-.86,-.43,0,.43,.86,1.29]:m.box((x,1.63,.88),(.045,1.37,.065),'wood')
for y in [.96,2.3]:m.box((0,y,.88),(2.62,.045,.065),'wood')
for x in [-1.075,-.645,-.215,.215,.645,1.075]:m.box((x,1.63,.85),(.39,1.29,.012),'screen')
m.box((0,2.35,.3),(2.85,.07,1.35),'steel')
# Mismatched corrugated repair plate on the lower front.
for x in np.linspace(-1.23,1.23,26):m.box((x,.46,.93),(.018,.82,.018),'steel')

m=model('CIS_EntranceCanopy')
m.box((0,.1,0),(2.35,.12,1.55),'panel')
for x in [-.94,.94]:m.tube((x,.02,-.65),(x,-.72,-.65),.025,'rust',8);m.tube((x,-.72,-.65),(x,.02,.61),.025,'rust',8)
for x in np.linspace(-1.12,1.12,17):m.box((x,.18,0),(.035,.04,1.55),'steel')
m.box((0,.15,.78),(2.4,.22,.035),'bluepaint')

m=model('CIS_Intercom')
m.box((0,0,0),(.15,.3,.035),'steel');m.box((0,.085,.021),(.105,.065,.012),'rubber')
for i in range(5):m.box((0,.067+i*.009,.029),(.09,.002,.005),'steel')
for i in range(12):
    x=(i%3-1)*.035;y=.025-(i//3)*.035;m.box((x,y,.026),(.025,.023,.012),'rubber')
m.tube((0,-.125,.019),(0,-.125,.028),.015,'steel',10)

m=model('CIS_EntranceDoor')
m.box((.48,1.07,0),(.96,2.14,.085),'rust')
for y in [.3,1.11,1.9]:m.box((.48,y,.05),(.89,.035,.018),'steel')
m.box((.48,1.68,.052),(.42,.22,.018),'bluepaint');front(m,.48,1.68,.062,.4,.2,'entrance_sign')
m.tube((.83,.96,.07),(.83,.96,.14),.018,'steel',8);m.tube((.83,1.2,.07),(.83,1.2,.14),.018,'steel',8);m.tube((.83,.96,.14),(.83,1.2,.14),.018,'steel',8)
for y in [.35,1.8]:m.tube((0,y,0),(0,y+.12,0),.025,'rust',8)

m=model('CIS_Garage')
m.box((0,1.25,-2.6),(3.2,2.5,.12),'rust')
for x in [-1.6,1.6]:
    m.box((x,1.25,0),(.1,2.5,5.2),'bluepaint')
    for z in np.linspace(-2.5,2.5,25):m.box((x+(.06 if x>0 else -.06),1.25,z),(.025,2.42,.025),'steel')
m.box((0,2.53,0),(3.4,.09,5.45),'rust')
for x in [-.79,.79]:
    m.box((x,1.24,2.64),(1.56,2.48,.08),'paint')
    for y in [.12,2.36]:m.box((x,y,2.69),(1.47,.05,.025),'rust')
for x in [-.08,.08]:m.box((x,1.13,2.72),(.03,.23,.06),'steel')
front(m,0,2.15,2.691,.35,.27,'garage_number')

# Split garage version for the game: architecture stays static, the existing double door is its own mesh.
m=model('CIS_GarageShell')
m.box((0,1.25,-2.6),(3.2,2.5,.12),'rust')
for x in [-1.6,1.6]:
    m.box((x,1.25,0),(.1,2.5,5.2),'bluepaint')
    for z in np.linspace(-2.5,2.5,25):m.box((x+(.06 if x>0 else -.06),1.25,z),(.025,2.42,.025),'steel')
m.box((0,2.53,0),(3.4,.09,5.45),'rust')

m=model('CIS_GarageDoor')
for x in [-.79,.79]:
    m.box((x,1.24,0),(1.56,2.48,.08),'paint')
    for y in [.12,2.36]:m.box((x,y,.05),(1.47,.05,.025),'rust')
for x in [-.08,.08]:m.box((x,1.13,.08),(.03,.23,.06),'steel')
front(m,0,2.15,.071,.35,.27,'garage_number')

# Hinged halves: origin sits on the hinge so Godot can swing them sideways.
m=model('CIS_GarageDoorLeft')
m.box((.78,1.24,0),(1.56,2.48,.08),'paint')
for y in [.12,2.36]:m.box((.78,y,.05),(1.47,.05,.025),'rust')
m.box((1.47,1.13,.08),(.03,.23,.06),'steel')

m=model('CIS_GarageDoorRight')
m.box((-.78,1.24,0),(1.56,2.48,.08),'paint')
for y in [.12,2.36]:m.box((-.78,y,.05),(1.47,.05,.025),'rust')
m.box((-1.47,1.13,.08),(.03,.23,.06),'steel')

m=model('CIS_Kiosk')
m.box((0,1.25,0),(2.6,2.5,1.8),'bluepaint');m.box((0,2.55,0),(2.86,.16,2.08),'steel')
m.box((-.35,1.57,.918),(1.58,1.05,.05),'rubber');m.box((-.35,1.57,.95),(1.49,.96,.012),'screen')
for x in [-1.09,-.35,.39]:m.box((x,1.57,.98),(.035,1.02,.04),'enamel')
m.box((-.35,1.04,1.06),(1.76,.06,.35),'steel')
m.box((.91,1.26,.93),(.61,2.34,.055),'paint');m.box((.91,1.59,.97),(.42,.62,.012),'glass');m.box((.71,1.05,1.0),(.025,.2,.05),'steel')
m.box((0,2.3,.94),(2.45,.42,.06),'steel');front(m,0,2.3,.973,2.4,.41,'shop_sign')
for x in np.linspace(-1.25,1.25,18):m.box((x,.5,.92),(.016,.9,.025),'steel')

m=model('CIS_NoticeBoard')
m.box((0,.5,0),(.84,1,.035),'paint')
for x in [-.44,.44]:m.box((x,.5,.018),(.045,1.06,.045),'wood')
for y in [-.02,1.02]:m.box((0,y,.018),(.92,.045,.045),'wood')
front(m,0,.5,.021,.82,.98,'notices')

m=model('CIS_Rug')
m.box((0,.008,0),(1.5,.016,2.25),'cloth')
m.face([(-.75,.018,1.125),(.75,.018,1.125),(.75,.018,-1.125),(-.75,.018,-1.125)],'carpet')
for z in [-1.16,1.16]:
    for x in np.linspace(-.72,.72,35):m.box((x,.008,z),(.012,.009,.075),'paper')

m=model('CIS_GasStove')
m.box((0,.43,0),(.6,.86,.6),'enamel');m.box((0,.39,.309),(.51,.49,.025),'rubber');m.box((0,.39,.325),(.42,.37,.014),'screen')
m.box((0,.65,.347),(.45,.03,.04),'steel')
for x in [-.19,-.065,.065,.19]:m.tube((x,.76,.304),(x,.76,.33),.028,'rubber',10)
for x in [-.15,.15]:
    for z in [-.15,.15]:
        m.tube((x,.86,z),(x,.883,z),.065,'rubber',12)
        for dx in [-.085,.085]:m.box((x+dx,.901,z),(.014,.025,.22),'steel')
        for dz in [-.085,.085]:m.box((x,.901,z+dz),(.22,.025,.014),'steel')
m.box((0,1.035,-.292),(.6,.35,.025),'enamel')

m=model('CIS_EnamelKettle')
loft(m,[(0,0,0,.07,.07),(0,.025,0,.09,.09),(0,.13,0,.095,.095),(0,.19,0,.06,.06)],'enamel',12)
m.tube((0,.19,0),(0,.203,0),.065,'steel',12);m.tube((0,.203,0),(0,.23,0),.018,'rubber',10)
m.tube((.06,.055,0),(.16,.155,0),.035,'enamel',10,.022);m.tube((.16,.155,0),(.185,.185,0),.022,'steel',10)
points=[(-.075,.14,0),(-.095,.24,0),(-.065,.31,0),(.065,.31,0),(.095,.24,0),(.075,.14,0)]
for a,b in zip(points,points[1:]):m.tube(a,b,.012,'rubber',8)

m=model('CIS_KitchenStool')
m.box((0,.46,0),(.34,.04,.34),'ochrepaint')
for x in [-.13,.13]:
    for z in [-.13,.13]:m.box((x,.22,z),(.035,.44,.035),'wood')
for z in [-.13,.13]:m.box((0,.16,z),(.29,.03,.03),'wood')
for x in [-.13,.13]:m.box((x,.23,0),(.03,.03,.29),'wood')

m=model('CIS_Sideboard')
m.box((0,1.02,0),(1.6,1.95,.43),'wood')
for x in [-.75,0,.75]:m.box((x,1.46,.24),(.045,.96,.035),'wood')
for x in [-.37,.37]:
    m.box((x,1.46,.222),(.68,.87,.012),'screen');m.box((x,.54,.235),(.71,.82,.035),'wood');m.box((x+.25,.65,.267),(.025,.17,.035),'steel')
for y in [1.0,1.45,1.9]:m.box((0,y,.25),(1.52,.025,.035),'wood')
for x in [-.6,.6]:
    for z in [-.16,.16]:m.box((x,.045,z),(.07,.09,.07),'rust')

m=model('CIS_OldTelevision')
m.box((0,.29,0),(.68,.51,.4),'wood');m.box((-.07,.31,.21),(.47,.37,.025),'rubber');m.box((-.07,.31,.228),(.42,.32,.016),'screen')
for y in [.31,.43]:m.tube((.26,y,.208),(.26,y,.235),.032,'steel',12)
for y in np.linspace(.1,.21,7):m.box((.25,y,.211),(.1,.008,.014),'rubber')
for x in [-.25,.25]:m.box((x,.025,0),(.045,.05,.27),'rubber')
m.tube((-.03,.55,0),(-.31,.94,0),.004,'steel',6);m.tube((.03,.55,0),(.31,.94,0),.004,'steel',6)

m=model('CIS_Sandbox')
m.box((0,.035,0),(2.3,.07,2.3),'sand')
for x in [-1.2,1.2]:m.box((x,.17,0),(.09,.34,2.48),'bluepaint');m.box((x,.35,0),(.23,.045,2.55),'ochrepaint')
for z in [-1.2,1.2]:m.box((0,.17,z),(2.32,.34,.09),'bluepaint');m.box((0,.35,z),(2.3,.045,.23),'ochrepaint')
# Small abandoned bucket inside.
loft(m,[(.45,.07,.3,.09,.09),(.45,.23,.3,.13,.13)],'red',8)

m=model('CIS_PullUpBars')
for x,y in [(-1.2,2.25),(0,2.25),(1.2,1.65)]:m.tube((x,0,0),(x,y,0),.034,'bluepaint',10)
m.tube((-1.2,2.25,0),(0,2.25,0),.026,'steel',10);m.tube((0,1.65,0),(1.2,1.65,0),.026,'steel',10)
for x in [-1.2,0,1.2]:m.tube((x,0,0),(x,.07,0),.1,'panel',10)

m=model('CIS_ConcreteFence')
m.box((0,.95,0),(2.65,1.9,.11),'panel')
for x in [-1.4,1.4]:m.box((x,1.02,0),(.15,2.04,.22),'panel')
for y in [.1,1.8]:m.box((0,y,.075),(2.65,.12,.1),'panel')
# Cast diamond relief, not a flat decal.
for x in [-.98,-.49,0,.49,.98]:
    for y in [.48,.96,1.44]:
        edge=[(x-.23,y,.061),(x,y-.22,.061),(x+.23,y,.061),(x,y+.22,.061)]
        for i in range(4):m.face([edge[i],edge[(i+1)%4],(x,y,.15)],'panel')

m=model('CIS_TirePlanter')
# Hollow torus with a low polygon count, earth and weeds.
for i in range(16):
    a,b=i*math.tau/16,(i+1)*math.tau/16
    for j in range(6):
        c,d=j*math.tau/6,(j+1)*math.tau/6
        def pos(t,s):return ((.3+.095*math.cos(s))*math.cos(t),.1+.095*math.sin(s),(.3+.095*math.cos(s))*math.sin(t))
        m.face([pos(a,c),pos(a,d),pos(b,d),pos(b,c)],'bluepaint')
m.tube((0,0,0),(0,.1,0),.24,'sand',16)
for i in range(7):
    a=i*math.tau/7;x,z=.1*math.cos(a),.1*math.sin(a)
    m.tube((x,.1,z),(x,.4,z),.004,'paint',5)
    for side in [-1,1]:m.face([(x,.18,z),(x+side*.08,.29,z+.02),(x,.27,z+.01)],'paint');m.face([(x,.27,z+.01),(x+side*.08,.29,z+.02),(x,.18,z)],'paint')

m=model('CIS_CourtyardTable')
for x in [-.55,.55]:
    for z in [-.28,.28]:m.box((x,.36,z),(.055,.72,.055),'bluepaint')
for z in [-.24,-.08,.08,.24]:m.box((0,.75,z),(1.5,.06,.14),'wood')
for z in [-.7,.7]:
    for x in [-.55,.55]:m.box((x,.22,z),(.05,.44,.05),'bluepaint')
    m.box((0,.46,z),(1.5,.055,.3),'wood')

m=model('CIS_EntrySign')
m.box((0,0,0),(.7,.25,.025),'steel');front(m,0,0,.013,.68,.24,'address_sign')
for x in [-.32,.32]:
    for y in [-.095,.095]:m.tube((x,y,.014),(x,y,.019),.006,'steel',6)
CIS_LABELS=['Панельный фасад · 3 м','Остеклённый балкон','Подъездный козырёк','Домофон','Железная дверь подъезда','Металлический гараж','Киоск «Продукты»','Доска объявлений','Бордовый ковёр','Газовая плита','Эмалированный чайник','Кухонный табурет','Сервант','Старый телевизор','Дворовая песочница','Двойной турник','Бетонный забор с ромбами','Клумба из покрышки','Дворовый стол с лавками','Адресная табличка']
