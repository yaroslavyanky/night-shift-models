# Third batch: street infrastructure and abandoned interiors.
m=model('BusShelter')
for x in [-1.45,1.45]:
    for z in [-.55,.55]:m.tube((x,0,z),(x,2.45,z),.035,'steel',8)
for y in [.15,1.25,2.3]:m.tube((-1.45,y,-.55),(1.45,y,-.55),.025,'steel',8)
m.box((0,2.46,0),(3.2,.12,1.45),'paint');m.box((0,1.2,-.565),(2.85,2.15,.025),'glass')
for z in [-.18,0,.18]:m.box((0,.47,z),(2.25,.065,.15),'wood')
for x in [-.9,.9]:m.box((x,.235,0),(.055,.47,.45),'rust')
m.box((1.15,1.48,.58),(.42,.65,.05),'paint');m.box((1.15,1.48,.61),(.34,.55,.012),'paper')

m=model('Fence_3m')
for x in [-1.5,1.5]:m.tube((x,0,0),(x,2.15,0),.045,'rust',8)
for y in [.12,2.02]:m.tube((-1.5,y,0),(1.5,y,0),.025,'steel',8)
for x in np.linspace(-1.35,1.35,16):m.tube((x,.12,0),(x,2.02,0),.012,'steel',6)
for y in np.linspace(.27,1.87,10):m.tube((-1.5,y,0),(1.5,y,0),.01,'steel',6)

m=model('IronGate')
for x in [-.7,.7]:m.box((x,1.1,0),(.07,2.2,.07),'rust')
for y in [.07,.7,1.55,2.17]:m.box((0,y,0),(1.4,.045,.045),'paint')
for x in np.linspace(-.57,.57,9):
    m.tube((x,.07,0),(x,2.1,0),.016,'steel',6);loft(m,[(x,2.1,0,.034,.025),(x,2.23,0,.002,.002)],'rust',4)
m.box((.51,1.12,.04),(.1,.16,.035),'rust');m.box((.47,1.16,.075),(.15,.025,.035),'steel')

m=model('Dumpster')
loft(m,[(0,.18,0,.66,.38),(0,1.15,0,.85,.53)],'paint',4)
m.box((0,1.17,0),(1.5,.08,.96),'rubber')
for x in [-.55,.55]:
    for z in [-.3,.3]:wheel(m,(x,.1,z),.1,.05,spokes=4)
for x in [-.57,.57]:m.box((x,1.23,.1),(.05,.045,.35),'rust')
m.box((0,.65,.47),(.34,.32,.024),'warningstripe')

m=model('TrafficCone')
m.box((0,.025,0),(.39,.05,.39),'rubber')
loft(m,[(0,.05,0,.16,.16),(0,.26,0,.105,.105)],'red',12)
loft(m,[(0,.26,0,.105,.105),(0,.38,0,.075,.075)],'porcelain',12)
loft(m,[(0,.38,0,.075,.075),(0,.57,0,.028,.028)],'red',12)

m=model('ConcreteBarrier')
# Tapered cross section extruded along X.
a=[(-.33,0),(.33,0),(.33,.13),(.13,.5),(.095,.9),(-.095,.9),(-.13,.5),(-.33,.13)]
for x,rev in [(-1,False),(1,True)]:
    pts=[(x,y,z) for z,y in a]
    # triangulate the convex cross section as a fan
    for i in range(1,len(pts)-1):m.face([pts[0],pts[i+1],pts[i]] if rev else [pts[0],pts[i],pts[i+1]],'plaster')
for i in range(len(a)):
    z,y=a[i];zz,yy=a[(i+1)%len(a)];m.face([(-1,y,z),(1,y,z),(1,yy,zz),(-1,yy,zz)],'plaster')
for x in [-.65,.65]:m.box((x,.72,.105),(.16,.12,.012),'warningstripe')

m=model('WallClock')
m.tube((0,0,0),(0,0,.055),.22,'rubber',24);m.tube((0,0,.057),(0,0,.063),.196,'porcelain',24)
for i in range(12):
    a=i*math.tau/12;m.tube((.165*math.sin(a),.165*math.cos(a),.067),(.183*math.sin(a),.183*math.cos(a),.067),.006,'rubber',4)
m.tube((0,0,.075),(.08,.07,.075),.009,'rubber',4);m.tube((0,0,.078),(-.03,.155,.078),.006,'rubber',4);m.tube((0,0,.065),(0,0,.085),.018,'rust',8)

m=model('CRTMonitor')
m.box((0,.055,-.02),(.28,.08,.26),'rubber');m.box((0,.25,0),(.48,.37,.36),'porcelain');m.box((0,.29,.189),(.41,.27,.025),'rubber');m.box((0,.29,.205),(.37,.235,.012),'screen')
for x in [.12,.17]:m.box((x,.105,.19),(.025,.02,.015),'rubber')
for y in [.17,.2,.23,.26,.29]:m.box((.245,y,-.035),(.01,.012,.2),'rubber')

m=model('Desk')
m.box((0,.76,0),(1.3,.07,.68),'wood')
for x in [-.57,.57]:
    for z in [-.27,.27]:m.box((x,.365,z),(.055,.73,.055),'rust')
m.box((-.39,.57,0),(.35,.29,.59),'paint')
for y in [.51,.65]:m.box((-.39,y,.31),(.32,.12,.025),'wood');m.box((-.39,y,.335),(.12,.022,.025),'steel')
m.box((0,.2,-.26),(1.15,.07,.035),'rust')

m=model('OfficeChair')
m.tube((0,.1,0),(0,.47,0),.03,'steel',10)
for i in range(5):
    a=i*math.tau/5;x,z=.3*math.cos(a),.3*math.sin(a);m.tube((0,.11,0),(x,.075,z),.025,'rubber',8);wheel(m,(x,.045,z),.045,.04,spokes=0)
m.box((0,.49,0),(.47,.09,.43),'cloth');m.tube((0,.43,-.17),(0,.91,-.24),.027,'steel',8);m.box((0,.84,-.23),(.44,.42,.075),'cloth')

m=model('HospitalBed')
m.box((0,.51,0),(.92,.09,2.04),'rust');m.box((0,.64,0),(.86,.18,1.95),'paper')
for z in [-1,1]:
    for x in [-.46,.46]:m.tube((x,.08,z),(x,1.05,z),.025,'steel',8)
    m.tube((-.46,1.05,z),(.46,1.05,z),.025,'steel',8)
    for x in np.linspace(-.3,.3,5):m.tube((x,.55,z),(x,1.05,z),.014,'steel',8)
m.box((0,.78,-.68),(.58,.1,.35),'cloth');m.box((0,.741,.32),(.865,.022,1.17),'cloth')

m=model('ElevatorDoors')
for x in [-.76,.76]:m.box((x,1.2,0),(.12,2.4,.17),'paint')
m.box((0,2.37,0),(1.65,.12,.17),'paint')
for x in [-.36,.36]:
    m.box((x,1.13,0),(.705,2.26,.06),'steel')
    for xx in [x-.26,x+.26]:m.box((xx,1.14,.034),(.012,2.05,.008),'rubber')
m.box((.89,1.14,.04),(.14,.3,.05),'steel');m.tube((.89,1.17,.068),(.89,1.17,.079),.027,'rubber',10);m.box((0,2.41,.095),(.28,.09,.025),'screen')

m=model('Manhole')
m.tube((0,-.025,0),(0,.008,0),.36,'rust',24);m.tube((0,.009,0),(0,.016,0),.32,'steel',24)
for z in np.linspace(-.23,.23,7):
    length=2*math.sqrt(.29**2-z**2);m.box((0,.019,z),(length,.008,.015),'rubber')
for x in [-.22,.22]:m.box((x,.021,0),(.06,.008,.04),'rubber')

m=model('Bollard')
m.tube((0,0,0),(0,.62,0),.07,'paint',10);m.tube((0,.62,0),(0,.74,0),.071,'warningstripe',10);m.tube((0,.74,0),(0,.8,0),.07,'paint',10,.035);m.tube((0,0,0),(0,.05,0),.12,'rust',12)

m=model('VendingMachine')
m.box((0,.9,0),(.85,1.8,.68),'red');m.box((0,.89,.35),(.78,1.68,.025),'rubber');m.box((-.14,1.12,.37),(.45,1.06,.025),'glass')
for y in [.67,.89,1.11,1.33,1.55]:
    m.box((-.14,y,.39),(.43,.025,.025),'steel')
    for x in [-.28,-.13,.02]:m.tube((x,y+.02,.405),(x,y+.14,.405),.038,'red',8)
m.box((.25,1.4,.37),(.13,.18,.03),'screen')
for y in [1.11,1.2,1.29]:m.box((.25,y,.39),(.08,.04,.02),'steel')
m.box((0,.24,.37),(.56,.18,.03),'rubber');m.box((0,.15,.42),(.58,.025,.12),'steel')

m=model('Hydrant')
m.tube((0,0,0),(0,.08,0),.15,'rust',12);loft(m,[(0,.08,0,.095,.095),(0,.59,0,.095,.095),(0,.69,0,.055,.055),(0,.71,0,.01,.01)],'red',12)
for side in [-1,1]:m.tube((side*.08,.44,0),(side*.2,.44,0),.06,'red',10);m.tube((side*.2,.44,0),(side*.24,.44,0),.075,'steel',10)
m.tube((0,.28,.08),(0,.28,.16),.07,'steel',10)

m=model('HospitalCurtain')
for x in [-.9,.9]:
    m.tube((x,0,0),(x,1.95,0),.022,'steel',8);m.box((x,.04,0),(.09,.06,.5),'rust')
m.tube((-.9,1.95,0),(.9,1.95,0),.022,'steel',8)
for i in range(18):
    x=-.85+i*.1;z=.04 if i%2 else -.04
    m.face([(x,.25,z),(x+.1,.25,-z),(x+.1,1.85,-z),(x,1.85,z)],'cloth')
    m.face([(x,1.85,z),(x+.1,1.85,-z),(x+.1,.25,-z),(x,.25,z)],'cloth')
    m.tube((x+.05,1.85,0),(x+.05,1.95,0),.008,'steel',6)

m=model('WallSink')
m.box((0,.74,0),(.56,.12,.4),'porcelain');m.box((0,.81,.035),(.43,.016,.27),'rubber')
# Raised rim leaves a basin-like recess rather than painting a hole on a slab.
for x in [-.255,.255]:m.box((x,.82,0),(.05,.06,.4),'porcelain')
for z in [-.175,.175]:m.box((0,.82,z),(.51,.06,.05),'porcelain')
m.tube((0,.8,-.12),(0,.98,-.12),.018,'steel',8);m.tube((0,.98,-.12),(0,.98,.02),.018,'steel',8);m.tube((0,.98,.02),(0,.94,.02),.018,'steel',8)
m.tube((0,.7,0),(0,.43,0),.027,'rust',8);m.tube((0,.43,0),(0,.43,-.2),.027,'rust',8)
STREET_LABELS=['Автобусная остановка','Секция ограды · 3 м','Железная калитка','Мусорный контейнер','Дорожный конус','Бетонное ограждение','Настенные часы','ЭЛТ-монитор','Письменный стол','Офисное кресло','Больничная кровать','Двери лифта','Канализационный люк','Парковочный столбик','Торговый автомат','Пожарный гидрант','Больничная ширма','Настенная раковина']
