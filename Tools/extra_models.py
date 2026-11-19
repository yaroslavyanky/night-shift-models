# Executed by build_assets.py; shares its mesh primitives and material palette.
def loft(m,rings,mat,n=10):
    pts=[]
    for x,y,z,rx,rz in rings:
        pts.append([np.array((x+rx*math.cos(i*math.tau/n),y,z+rz*math.sin(i*math.tau/n))) for i in range(n)])
    for k in range(len(pts)-1):
        for i in range(n):
            j=(i+1)%n
            m.face([pts[k][i],pts[k+1][i],pts[k+1][j],pts[k][j]],mat,[(i/n,k/(len(pts)-1)),(i/n,(k+1)/(len(pts)-1)),((i+1)/n,(k+1)/(len(pts)-1)),((i+1)/n,k/(len(pts)-1))])
    for k,reverse in [(0,False),(len(pts)-1,True)]:
        center=np.mean(pts[k],axis=0)
        for i in range(n):
            a,b=pts[k][i],pts[k][(i+1)%n]
            m.face([center,b,a] if reverse else [center,a,b],mat,[(.5,.5),(0,0),(1,0)])
def wheel(m,c,r,width=.045,mat='rubber',spokes=8):
    x,y,z=c;m.tube((x-width/2,y,z),(x+width/2,y,z),r,mat,16)
    # Visible metal spokes on the outward side.
    for side in [-1,1]:
        xx=x+side*(width/2+.002)
        for i in range(spokes):
            a=i*math.tau/spokes;m.tube((xx,y,z),(xx,y+math.cos(a)*r*.86,z+math.sin(a)*r*.86),.006,'steel',5)
        m.tube((xx-side*.004,y,z),(xx+side*.008,y,z),r*.13,'steel',8)

m=model('Radiator')
for x in np.linspace(-.5,.5,9):
    loft(m,[(x,.08,0,.037,.075),(x,.12,0,.045,.09),(x,.64,0,.045,.09),(x,.69,0,.032,.065)],'porcelain',8)
for y in [.15,.59]:m.tube((-.61,y,0),(.61,y,0),.025,'rust',8)
m.tube((.61,.59,0),(.71,.59,0),.024,'steel',8);m.tube((.68,.59,0),(.68,.68,0),.018,'steel',8);m.box((.68,.69,0),(.11,.025,.08),'rubber')

m=model('FireExtinguisher')
loft(m,[(0,0,0,.095,.095),(0,.04,0,.11,.11),(0,.43,0,.11,.11),(0,.49,0,.05,.05),(0,.54,0,.025,.025)],'red',12)
m.box((0,.565,0),(.13,.025,.04),'steel');m.box((-.025,.6,0),(.18,.025,.035),'rubber');m.box((0,.27,.107),(.095,.18,.012),'paper')
m.tube((.04,.53,0),(.15,.48,0),.015,'rubber',8);m.tube((.15,.48,0),(.15,.16,.02),.015,'rubber',8);m.tube((.15,.16,.02),(.15,.09,.05),.022,'rubber',8)

m=model('TrashBin')
loft(m,[(0,0,0,.24,.24),(0,.04,0,.27,.27),(0,.72,0,.3,.3),(0,.76,0,.32,.32)],'paint',12)
m.tube((0,.76,0),(0,.79,0),.33,'rust',12);m.box((0,.825,0),(.16,.035,.045),'steel')
for x in [-.31,.31]:m.box((x,.6,0),(.06,.05,.15),'rust')

m=model('BrokenWindow')
for x in [-.68,.68]:m.box((x,.85,0),(.1,1.7,.14),'wood')
for y in [.05,1.65]:m.box((0,y,0),(1.46,.1,.14),'wood')
m.box((0,.85,0),(.055,1.6,.1),'paint');m.box((0,.95,0),(1.36,.055,.1),'paint');m.box((0,-.025,.09),(1.6,.08,.34),'plaster')
for p in [[(-.63,.1,.015),(-.11,.1,.015),(-.36,.45,.015),(-.63,.62,.015)],[(.06,1.59,.015),(.63,1.59,.015),(.63,1.15,.015),(.37,1.3,.015)],[(.06,.1,.015),(.63,.1,.015),(.63,.48,.015),(.32,.29,.015)]]:
    m.face(p,'glass');m.face(list(reversed(p)),'glass')

m=model('Mailboxes')
m.box((0,.52,0),(1.35,1.04,.23),'rust')
for x in [-.45,0,.45]:
    for y in [.18,.52,.86]:
        m.box((x,y,.13),(.42,.31,.025),'paint');m.box((x,y+.09,.149),(.29,.025,.008),'rubber');m.box((x,y-.025,.15),(.13,.06,.009),'paper');m.tube((x+.15,y-.075,.146),(x+.15,y-.075,.163),.015,'steel',8)

m=model('Stair_3m')
for i in range(10):
    y=(i+1)*.16;z=-1.35+i*.3
    m.box((0,y/2,z),(1.35,y,.3),'plaster');m.box((0,y+.008,z-.13),(1.35,.016,.035),'steel')
for x in [-.72,.72]:
    for i in [0,3,6,9]:
        z=-1.35+i*.3;y=(i+1)*.16;m.tube((x,y,z),(x,y+.9,z),.02,'rust',8)
    m.tube((x,1.06,-1.35),(x,2.5,1.35),.027,'paint',10)

m=model('StreetLamp')
m.tube((0,0,0),(0,.2,0),.16,'rust',12);m.tube((0,.2,0),(0,3.7,0),.065,'paint',12,.045);m.tube((0,3.7,0),(0,3.95,.26),.045,'paint',10);m.tube((0,3.95,.26),(0,3.95,.8),.045,'paint',10)
m.box((0,3.93,.82),(.32,.12,.62),'rust');m.box((0,3.858,.82),(.25,.028,.49),'glass')

m=model('RoadBarrier')
for x in [-.65,.65]:
    m.box((x,.48,0),(.065,.96,.065),'rust');m.box((x,.06,0),(.38,.08,.64),'rust')
for y in [.44,.78]:m.box((0,y,0),(1.65,.2,.075),'warningstripe')

m=model('Wheelchair')
for x in [-.32,.32]:
    wheel(m,(x,.31,-.18),.31)
    wheel(m,(x,.08,.38),.08,.035,spokes=4)
    for z in [-.2,.27]:m.tube((x*.8,.17,z),(x*.8,.59,z),.017,'steel',8)
    m.tube((x*.8,.53,-.21),(x*.8,.98,-.3),.02,'steel',8);m.tube((x*.8,.98,-.3),(x*.8,.98,-.43),.022,'rubber',8)
    m.tube((x,.57,-.18),(x,.57,.26),.025,'rubber',8);m.tube((x,.57,.24),(x,.37,.24),.018,'steel',8)
    m.tube((x*.7,.37,.25),(x*.7,.15,.5),.018,'steel',8);m.box((x*.7,.145,.54),(.19,.025,.22),'rubber')
m.box((0,.42,.03),(.55,.055,.47),'cloth');m.box((0,.71,-.25),(.53,.52,.045),'cloth')
m.tube((-.25,.22,.2),(.25,.41,-.2),.016,'steel',8);m.tube((.25,.22,.2),(-.25,.41,-.2),.016,'steel',8)

m=model('Gurney')
for x in [-.35,.35]:
    for z in [-.75,.75]:
        wheel(m,(x,.09,z),.09,.045,spokes=4);m.tube((x,.14,z),(x,.75,z),.025,'steel',8)
    m.tube((x,.65,-.91),(x,.65,.91),.025,'steel',8)
    for z in [-.6,.6]:m.tube((x,.72,z),(x,.94,z),.02,'steel',8)
    m.tube((x,.94,-.6),(x,.94,.6),.02,'steel',8)
m.box((0,.69,0),(.79,.08,1.94),'rust');m.box((0,.79,0),(.7,.15,1.85),'cloth');m.box((0,.905,-.66),(.48,.1,.34),'paper')
for z in [-.45,.4]:m.box((0,.872,z),(.71,.015,.06),'rubber')

m=model('Payphone')
m.box((0,.43,0),(.43,.86,.23),'paint');m.box((.08,.42,.13),(.2,.4,.025),'steel');m.box((.08,.74,.13),(.19,.06,.012),'rubber')
for x in [.025,.08,.135]:
    for y in [.33,.39,.45,.51]:m.box((x,y,.154),(.035,.038,.016),'rubber')
m.box((-.115,.48,.19),(.075,.36,.07),'rubber')
for y in [.28,.68]:m.box((-.115,y,.2),(.13,.1,.1),'rubber')
for i in range(18):
    y=.27-i*.013;x=-.115+math.sin(i*1.9)*.012
    m.tube((x,y,.14),(x+.008,y-.013,.14),.008,'rubber',6)
m.box((.09,.16,.131),(.15,.045,.018),'rubber')

m=model('SecurityCamera')
m.box((0,0,0),(.16,.24,.035),'rust');m.tube((0,0,.02),(0,-.06,.22),.025,'steel',8);m.box((0,.01,.33),(.16,.13,.32),'porcelain');m.box((0,.085,.35),(.21,.024,.4),'paint');m.tube((0,.01,.49),(0,.01,.52),.048,'rubber',12);m.tube((0,.01,.521),(0,.01,.525),.031,'glass',12)

m=model('VentCover')
m.box((0,.25,0),(.65,.5,.045),'rust');m.box((0,.25,.027),(.56,.41,.015),'rubber')
for y in np.linspace(.085,.415,9):m.box((0,y,.05),(.55,.018,.04),'steel')
for x in [-.295,.295]:
    for y in [.04,.46]:m.tube((x,y,.025),(x,y,.035),.011,'steel',8)

m=model('Generator')
for x in [-.38,.38]:
    for z in [-.25,.25]:m.tube((x,.05,z),(x,.68,z),.025,'steel',8)
    for y in [.05,.68]:m.tube((x,y,-.25),(x,y,.25),.025,'steel',8)
for z in [-.25,.25]:
    for y in [.05,.68]:m.tube((-.38,y,z),(.38,y,z),.025,'steel',8)
m.box((0,.56,0),(.64,.17,.4),'red');m.tube((-.13,.22,0),(.24,.22,0),.16,'rust',12);m.box((-.25,.25,0),(.2,.3,.32),'rubber');m.box((.18,.34,.24),(.24,.16,.05),'paint')
for x in [.12,.23]:m.tube((x,.35,.27),(x,.35,.28),.035,'rubber',10)
m.tube((.12,.65,0),(.12,.685,0),.04,'rubber',10);m.tube((.13,.2,-.12),(.32,.43,-.12),.025,'steel',8)

m=model('Key')
for i in range(12):
    a,b=i*math.tau/12,(i+1)*math.tau/12
    m.tube((.018*math.cos(a),.065+.022*math.sin(a),0),(.018*math.cos(b),.065+.022*math.sin(b),0),.003,'steel',6)
m.box((0,.025,0),(.007,.06,.006),'steel');m.box((.007,.008,0),(.018,.006,.006),'steel');m.box((.005,.018,0),(.014,.006,.006),'steel')

m=model('Padlock')
m.box((0,.04,0),(.075,.08,.026),'rust')
points=[(-.025,.08,0),(-.025,.11,0),(-.018,.125,0),(0,.132,0),(.018,.125,0),(.025,.11,0),(.025,.08,0)]
for a,b in zip(points,points[1:]):m.tube(a,b,.006,'steel',8)
m.tube((0,.035,.014),(0,.035,.016),.008,'rubber',8);m.box((0,.024,.015),(.006,.015,.002),'rubber')

m=model('ExitSign');m.box((0,0,0),(.52,.18,.07),'rubber');m.box((0,0,.042),(.48,.145,.02),'exit')

m=model('Watcher')
# Bent silhouette, floor pivot, asymmetrical coat and long hands. Static prototype, no rig.
loft(m,[(0,.62,0,.31,.17),(.015,.86,-.015,.28,.155),(0,1.13,-.03,.24,.145),(-.02,1.45,-.065,.29,.18),(-.03,1.62,-.08,.36,.16),(-.04,1.68,-.06,.19,.13)],'cloth',10)
loft(m,[(-.03,1.65,-.055,.085,.09),(-.04,1.84,.015,.07,.08)],'bone',8)
loft(m,[(-.04,1.79,.035,.06,.065),(-.055,1.85,.045,.115,.1),(-.07,2.03,.025,.12,.1),(-.07,2.1,.005,.07,.07),(-.07,2.12,0,.005,.005)],'bone',10)
# Bandaged eye line and a dark recessed mouth; no copied character design.
m.box((-.065,1.99,.121),(.17,.033,.013),'rubber');m.box((-.065,1.9,.14),(.065,.018,.008),'rubber')
for side in [-1,1]:
    x=side*.29
    m.tube((x,1.58,-.06),(side*.43,1.21,-.02),.095,'cloth',8,.072)
    m.tube((side*.43,1.21,-.02),(side*.45,.88,.095),.075,'cloth',8,.045)
    m.tube((side*.45,.89,.095),(side*.46,.76,.14),.048,'bone',8,.035)
    for j in range(4):
        fx=side*.46+(j-1.5)*.021
        m.tube((fx,.77,.15),(fx+side*.014,.62-abs(j-1.5)*.012,.18),.01,'bone',6,.007)
    m.tube((side*.12,.73,-.02),(side*.13,.39,.045),.09,'cloth',8,.065)
    m.tube((side*.13,.39,.045),(side*.14,.12,0),.065,'cloth',8,.05)
    m.box((side*.14,.075,.065),(.15,.15,.28),'rubber')
for y in [.85,1.03,1.21,1.39,1.55]:m.tube((-.025,y,.15),(-.025,y,.167),.012,'steel',6)
# Coat seams, front split and a hanging service tag.
m.box((0,.73,.174),(.023,.22,.012),'rubber');m.box((.115,1.43,.125),(.075,.11,.025),'paper')
EXTRA_LABELS=['Чугунная батарея','Огнетушитель','Мусорный бак','Разбитое окно','Почтовые ящики','Лестничный пролёт','Уличный фонарь','Дорожное ограждение','Инвалидное кресло','Больничная каталка','Таксофон','Камера наблюдения','Вентиляционная решётка','Генератор','Ключ','Навесной замок','Указатель выхода','Смотритель · без рига']
