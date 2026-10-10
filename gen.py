import re, os, sys, html

BG="#0a0e14"; PANEL="#0f151d"; TILE="#121a24"; LINE="#1f2a37"
TEXT="#d0d7de"; SOFT="#9aa7b6"; DIM="#7d8a99"
TEAL="#2ee6c5"; VIOLET="#a78bfa"; AMBER="#f5c451"; GREEN="#3fb950"
MONO="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

def esc(s): return html.escape(s, quote=False)

def kf(points, T):
    pts=list(points)
    if pts[0][0]>0: pts.insert(0,(0,pts[0][1]))
    if pts[-1][0]<T: pts.append((T,pts[-1][1]))
    kt=";".join(f"{min(max(t/T,0),1):.4f}" for t,_ in pts)
    vs=";".join(str(v) if not isinstance(v,float) else f"{v:.2f}" for _,v in pts)
    return kt, vs

def anim(attr, pts, T, extra=""):
    kt,vs=kf(pts,T)
    return f'<animate attributeName="{attr}" dur="{T:.2f}s" repeatCount="indefinite" keyTimes="{kt}" values="{vs}" {extra}/>'

def svg(w,h,title,desc,body,defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">\n'
            f'<title id="t">{esc(title)}</title>\n<desc id="d">{esc(desc)}</desc>\n'
            f'<defs>{defs}</defs>\n{body}\n</svg>\n')

# ---------------------------------------------------------------- HERO
def hero(P):
    W,H=900,300
    phrases=["building practical, well-designed software","shipping Flutter, Node & Next.js apps",
             "learning SOC · DFIR · MITRE ATT&CK","reading logs, tracing incidents"]
    fs=24; cw=fs*0.6; x0=70
    # timeline
    t=0.4; slots=[]
    for p in phrases:
        n=len(p); ty=n*0.055; hold=2.3; er=n*0.025
        slots.append((t,ty,hold,er,n)); t+=ty+hold+er+0.35
    T=t
    clips=""; texts=""; cur=[(0,x0)]
    for i,(a,ty,hold,er,n) in enumerate(slots):
        Wd=n*cw
        if P: wattr=Wd if i==0 else 0; an=""
        else:
            wattr=0
            an=anim("width",[(0,0),(a,0),(a+ty,round(Wd,1)),(a+ty+hold,round(Wd,1)),(a+ty+hold+er,0),(T,0)],T)
        clips+=f'<clipPath id="c{i}"><rect x="{x0}" y="238" height="36" width="{wattr}">{an}</rect></clipPath>\n'
        texts+=(f'<g clip-path="url(#c{i})"><text x="{x0}" y="262" font-family="{MONO}" font-size="{fs}" '
                f'fill="{TEAL}" textLength="{n*cw:.1f}" lengthAdjust="spacing">{esc(phrases[i])}</text></g>\n')
        cur+= [(a,x0),(a+ty,round(x0+Wd,1)),(a+ty+hold,round(x0+Wd,1)),(a+ty+hold+er,x0)]
    cur_x0 = x0+len(phrases[0])*cw if P else x0
    cursor=(f'<rect x="{cur_x0}" y="242" width="11" height="26" fill="{TEAL}">'
            + ("" if P else anim("x",cur,T)+'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/>')
            + '</rect>')
    # network art
    nodes=[(650,62),(752,38),(850,92),(700,150),(806,168),(862,244),(656,236),(764,258)]
    edges=[(0,1),(1,2),(0,3),(1,3),(1,4),(2,4),(3,4),(4,5),(3,6),(6,7),(4,7),(7,5)]
    net=""
    for a,b in edges:
        (xa,ya),(xb,yb)=nodes[a],nodes[b]
        net+=f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="#243244" stroke-width="1.5"/>\n'
    packets=[(0,1,TEAL,2.6,0),(1,4,VIOLET,3.1,0.8),(3,4,TEAL,2.2,0.3),(4,5,VIOLET,2.8,1.4),
             (6,7,TEAL,2.4,0.9),(7,5,TEAL,3.0,0.2),(0,3,VIOLET,2.5,1.7),(2,4,TEAL,2.9,1.1)]
    if not P:
        for a,b,col,dur,begin in packets:
            (xa,ya),(xb,yb)=nodes[a],nodes[b]
            net+=(f'<circle r="3.2" fill="{col}"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" '
                  f'path="M{xa} {ya} L{xb} {yb}"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.85;1" '
                  f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>\n')
    for i,(x,y) in enumerate(nodes):
        pulse="" if P else (f'<animate attributeName="r" values="5;8;5" dur="{3+i*0.37:.2f}s" repeatCount="indefinite"/>'
                            f'<animate attributeName="stroke-opacity" values="1;0.35;1" dur="{3+i*0.37:.2f}s" repeatCount="indefinite"/>')
        net+=f'<circle cx="{x}" cy="{y}" r="5" fill="{PANEL}" stroke="{TEAL}" stroke-width="1.5">{pulse}</circle>\n'
    scan="" if P else (f'<rect x="0" y="-4" width="{W}" height="3" fill="{TEAL}" opacity="0.10">'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {H+8}" dur="7s" repeatCount="indefinite"/></rect>')
    blink="" if P else '<animate attributeName="opacity" values="1;0.25;1" dur="2.4s" repeatCount="indefinite"/>'
    defs=(f'<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
          f'<radialGradient id="gl1" cx="0.12" cy="0.2" r="0.6"><stop offset="0" stop-color="{TEAL}" stop-opacity="0.20"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>'
          f'<radialGradient id="gl2" cx="0.88" cy="0.85" r="0.55"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0.18"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
          f'<pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#16202c" stroke-width="1"/></pattern>'
          f'<linearGradient id="bl" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity="0"/><stop offset="0.5" stop-color="{TEAL}" stop-opacity="0.8"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>'
          + clips)
    body=(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>\n<rect width="{W}" height="{H}" rx="14" fill="url(#grid)"/>\n'
          f'<rect width="{W}" height="{H}" rx="14" fill="url(#gl1)"/><rect width="{W}" height="{H}" rx="14" fill="url(#gl2)"/>\n{scan}\n{net}'
          f'<circle cx="46" cy="44" r="4.5" fill="{GREEN}">{blink}</circle>\n'
          f'<text x="62" y="49" font-family="{MONO}" font-size="16" fill="{DIM}">firass-a@lab  ~  online</text>\n'
          f'<text x="40" y="128" font-family="{SANS}" font-size="78" font-weight="800" fill="url(#g)" textLength="500" lengthAdjust="spacingAndGlyphs">Firas Cherfa</text>\n'
          f'<text x="42" y="170" font-family="{SANS}" font-size="26" fill="{TEXT}">Systems &amp; Networks Engineer</text>\n'
          f'<text x="42" y="202" font-family="{SANS}" font-size="19" fill="{SOFT}">Software developer  ·  Blue Team in training</text>\n'
          f'<text x="40" y="262" font-family="{MONO}" font-size="{fs}" fill="{DIM}">&gt;</text>\n{texts}{cursor}\n'
          f'<rect x="0" y="297" width="{W}" height="3" fill="url(#bl)"/>')
    return svg(W,H,"Firas Cherfa — Systems and Networks Engineer",
        "Animated hero banner: a network of glowing nodes with moving packets, the name Firas Cherfa, and a typing line cycling through what I do.",body,defs)

# ---------------------------------------------------------------- TERMINAL
def terminal(P):
    W=760; pad=28; fs=18; cw=fs*0.6; lh=30; top=70
    L=[("c","whoami"),("o","firas cherfa · systems & networks engineer"),
       ("c","cat education.txt"),("o","M.Sc. Information Systems & Networks · 2024–2026"),
       ("o","Blida 1 – Saad Dahleb  ·  mention Très Bien"),
       ("c","ls ~/focus"),("o","build/   defend/   investigate/   network/"),
       ("c","status --now"),
       ("s",(TEAL,"software developer @ Proxylan (CERIST subsidiary)")),
       ("s",(AMBER,"LetsDefend · SOC Analyst path (in progress)")),
       ("s",(VIOLET,"Hack The Box · DFIR machines (2026)")),
       ("c","")]
    H=top+len(L)*lh+30
    t=0.5; rows=""; defs=""
    for i,(k,v) in enumerate(L):
        y=top+i*lh
        if k=="c": spans=[("$ ",TEAL),(v,TEXT)]; spd=0.05
        elif k=="o": spans=[(v,"#b4c0cc")]; spd=0.012
        else: spans=[("● ",v[0]),(v[1],TEXT)]; spd=0.012
        n=sum(len(s) for s,_ in spans); Wd=n*cw
        if k=="c" and i>0: t+=0.55
        d=n*spd
        wattr=Wd if P else 0
        an="" if P else "@@%d@@"%i
        defs+=f'<clipPath id="r{i}"><rect x="{pad}" y="{y-fs-2}" height="{lh}" width="{wattr}">{an}</rect></clipPath>\n'
        ts="".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s,c in spans)
        if k=="c" and v=="":
            rows+=(f'<text x="{pad}" y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve">{ts}</text>\n')
            curx=pad+n*cw
            cur=(f'<g>{"" if P else "@@CUR@@"}<rect x="{curx:.1f}" y="{y-fs+1}" width="10" height="{fs+3}" fill="{TEAL}">'
                 f'{"" if P else chr(60)+"animate attributeName=\"opacity\" values=\"1;1;0;0\" keyTimes=\"0;0.5;0.5;1\" dur=\"1s\" repeatCount=\"indefinite\"/"+chr(62)}</rect></g>')
            cur_start=t
            rows+=cur
        else:
            rows+=(f'<g clip-path="url(#r{i})"><text x="{pad}" y="{y}" font-family="{MONO}" font-size="{fs}" '
                   f'textLength="{Wd:.1f}" lengthAdjust="spacing" xml:space="preserve">{ts}</text></g>\n')
        L[i]=(k,v,t,d,Wd)
        t+=d+(0.12 if k!="c" else 0)
    T=t+7
    if not P:
        for i,(k,v,s,d,Wd) in enumerate(L):
            if k=="c" and v=="": continue
            a=anim("width",[(0,0),(s,0),(s+d,round(Wd,1)),(T,round(Wd,1))],T)
            rows=rows.replace(f"@@{i}@@","") ; defs=defs.replace(f"@@{i}@@",a)
        a=anim("opacity",[(0,0),(cur_start,0),(cur_start+0.01,1),(T,1)],T)
        rows=rows.replace("@@CUR@@",a)
    dots="".join(f'<circle cx="{28+i*20}" cy="26" r="6" fill="{c}"/>' for i,c in enumerate(["#3a4656","#3a4656","#3a4656"]))
    body=(f'<rect width="{W}" height="{H}" rx="12" fill="{PANEL}" stroke="{LINE}"/>\n'
          f'<path d="M0 12a12 12 0 0 1 12-12h{W-24}a12 12 0 0 1 12 12v32H0z" fill="#131c27"/>\n{dots}\n'
          f'<text x="{W/2}" y="31" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{DIM}">firas@lab: ~</text>\n'
          f'<line x1="0" y1="44" x2="{W}" y2="44" stroke="{LINE}"/>\n{rows}')
    return svg(W,H,"Terminal: who I am",
        "A terminal window typing out: whoami, education, focus areas, and current status — software developer at Proxylan, LetsDefend SOC path in progress, Hack The Box DFIR machines.",body,defs)

# ---------------------------------------------------------------- SECTION HEADER / DIVIDER
def header(idx,title,P):
    W,H=760,56
    glow="" if P else (f'<rect x="0" y="50" width="120" height="3" fill="url(#hg)"><animateTransform attributeName="transform" type="translate" '
                       f'values="-120 0;{W} 0" dur="5s" repeatCount="indefinite"/></rect>')
    defs=(f'<linearGradient id="hl" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity="0.55"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>'
          f'<linearGradient id="hg" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.9"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>')
    body=(f'<text x="2" y="34" font-family="{MONO}" font-size="20" fill="{TEAL}">{idx}</text>\n'
          f'<text x="38" y="34" font-family="{MONO}" font-size="20" fill="{DIM}">//</text>\n'
          f'<text x="70" y="36" font-family="{SANS}" font-size="30" font-weight="700" fill="{TEXT}">{esc(title)}</text>\n'
          f'<rect x="0" y="51" width="{W}" height="1.5" fill="url(#hl)"/>\n{glow}')
    return svg(W,H,f"Section {idx}: {title}",f"Section heading: {title}",body,defs)

def divider(P):
    W,H=760,18
    mv="" if P else (f'<rect x="0" y="7" width="220" height="4" rx="2" fill="url(#dg)"><animateTransform attributeName="transform" type="translate" '
                     f'values="-220 0;{W} 0" dur="6s" repeatCount="indefinite"/></rect>')
    defs=(f'<linearGradient id="dg" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity="0"/><stop offset="0.5" stop-color="{TEAL}"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>')
    body=(f'<rect x="0" y="8.5" width="{W}" height="1" fill="{LINE}"/>\n{mv}\n'
          f'<rect x="{W/2-5}" y="4" width="10" height="10" transform="rotate(45 {W/2} 9)" fill="{BG}" stroke="{TEAL}"/>')
    return svg(W,H,"divider","Decorative animated divider line",body,defs)

# ---------------------------------------------------------------- PROJECT CARDS
def card(cat,color,right,title,desc,chips,P,idn):
    W=560; H=118+len(desc)*21+34
    cp=f'<clipPath id="cc{idn}"><rect width="{W}" height="{H}" rx="10"/></clipPath>'
    shimmer="" if P else (f'<g clip-path="url(#cc{idn})"><rect x="-200" y="0" width="200" height="2.5" fill="url(#sh{idn})">'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;{W+200} 0" dur="{5+idn}s" repeatCount="indefinite"/></rect></g>')
    defs=(cp+f'<linearGradient id="sh{idn}" x1="0" x2="1"><stop offset="0" stop-color="{color}" stop-opacity="0"/><stop offset="0.5" stop-color="{color}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>')
    tagw=len(cat)*8.4+20
    b=(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{PANEL}" stroke="{LINE}"/>\n'
       f'<g clip-path="url(#cc{idn})"><rect width="4" height="{H}" fill="{color}"/></g>\n{shimmer}\n'
       f'<rect x="24" y="18" width="{tagw:.0f}" height="22" rx="6" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.45"/>\n'
       f'<text x="34" y="33.5" font-family="{MONO}" font-size="12.5" fill="{color}" letter-spacing="0.5">{esc(cat)}</text>\n'
       f'<text x="{W-22}" y="33.5" text-anchor="end" font-family="{MONO}" font-size="12.5" fill="{DIM}">{esc(right)}</text>\n'
       f'<text x="24" y="72" font-family="{SANS}" font-size="23" font-weight="700" fill="{TEXT}">{esc(title)}</text>\n')
    for i,l in enumerate(desc):
        b+=f'<text x="24" y="{98+i*21}" font-family="{SANS}" font-size="14.5" fill="{SOFT}">{esc(l)}</text>\n'
    x=24; y=H-40
    for c in chips:
        w=len(c)*7.6+18
        b+=(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="24" rx="6" fill="{TILE}" stroke="{LINE}"/>'
            f'<text x="{x+9:.0f}" y="{y+16.5}" font-family="{MONO}" font-size="12.5" fill="{TEAL}">{esc(c)}</text>\n')
        x+=w+8
    return svg(W,H,f"Project: {title}",f"{cat} — {' '.join(desc)} Technologies: {', '.join(chips)}.",b,defs)

CARDS={
 "card-rl-agent":("RESEARCH · AI",TEAL,"Master's thesis · 2026","Agri Decision-Support RL Agent",
   ["A multi-objective reinforcement-learning agent that supports crop","decisions on Gym-DSSAT, plus a web app to run experiments","and follow the agent's progress and performance metrics."],
   ["Python","Gymnasium","Pandas","Flask API","Next.js"]),
 "card-iespc":("SOFTWARE ENGINEERING",TEAL,"Team project · 2025–26","IESPC Enrollment Platform",
   ["Front end and the full online enrollment flow: multi-step forms","and document uploads, plus API design with the back-end team,","from the interface down to the database."],
   ["FastAPI","Express.js","PostgreSQL","Prisma"]),
 "card-sqli":("CYBERSECURITY",VIOLET,"Bachelor's thesis · 2024","SQL Injection Detection Agent",
   ["An AI agent that detects and blocks SQL injection attempts in","real time, trained on attack patterns, with behavioural query","analysis, logging, alerts and adaptive thresholds."],
   ["ML model","Behaviour analysis","Logging","Alerting"]),
 "card-momly":("MOBILE",AMBER,"Flutter app","Momly",
   ["Baby-tracking app for parents: feeding, sleep and health logs,","smart reminders and a built-in shop for baby products,","built around clean architecture."],
   ["Flutter","Dart"]),
 "card-taxing":("MOBILE · FINTECH",AMBER,"Flutter app","Smart Taxing",
   ["Tax-management app that automates tax calculations and keeps","financial data structured, as a SaaS-ready foundation for","reporting and analytics."],
   ["Flutter","Dart"]),
}

# ---------------------------------------------------------------- KILL CHAIN
def killchain(P):
    W,H=760,150; n=7; x0=62; step=106
    labels=["Recon","Weaponize","Deliver","Exploit","Install","C2","Actions"]
    xs=[x0+i*step for i in range(n)]; y=72; T=9.0; trav=6.0
    b=(f'<rect width="{W}" height="{H}" rx="12" fill="{PANEL}" stroke="{LINE}"/>\n'
       f'<text x="24" y="30" font-family="{MONO}" font-size="14" fill="{DIM}">cyber kill chain  —  the lens I use to map alerts to attacker stages</text>\n'
       f'<line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="#243244" stroke-width="2"/>\n')
    for i,x in enumerate(xs):
        flash=""
        if not P:
            ti=trav*i/(n-1)
            flash=anim("fill-opacity",[(0,0),(max(ti-0.2,0),0),(ti,0.9),(ti+0.9,0),(T,0)],T)
        col=VIOLET if i>=4 else TEAL
        b+=(f'<circle cx="{x}" cy="{y}" r="15" fill="{PANEL}" stroke="{col}" stroke-width="1.8"/>'
            f'<circle cx="{x}" cy="{y}" r="15" fill="{col}" fill-opacity="0">{flash}</circle>'
            f'<text x="{x}" y="{y+5}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{TEXT}">{i+1}</text>'
            f'<text x="{x}" y="{y+42}" text-anchor="middle" font-family="{MONO}" font-size="15" fill="{SOFT}">{labels[i]}</text>\n')
    if not P:
        kt=f"0;{trav/T:.4f};1"
        b+=(f'<circle r="5" fill="{TEAL}"><animateMotion dur="{T}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="{kt}" calcMode="linear" '
            f'path="M{xs[0]} {y} L{xs[-1]} {y}"/><animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="0;{trav/T:.4f};{trav/T+0.02:.4f};1" values="1;1;0;0"/></circle>')
    return svg(W,H,"Cyber kill chain","Seven stages of the cyber kill chain — reconnaissance, weaponization, delivery, exploitation, installation, command and control, actions on objectives — with a signal travelling through them.",b)

# ---------------------------------------------------------------- STACK
ICON_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)),"icons")
RECOLOR={"prisma":"#9aa7b6","pandas":"#9aa7b6","linux":"#d0d7de","express":"#d0d7de","flask":"#d0d7de"}
def lum(h):
    h=h.lstrip("#")
    if len(h)==3: h="".join(c*2 for c in h)
    r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]
    return (0.2126*r+0.7152*g+0.0722*b)/255
def load_icon(name,pfx):
    s=open(f"{ICON_DIR}/{name}.svg",encoding="utf-8").read()
    s=re.sub(r"<\?xml[^>]*\?>","",s)
    m=re.search(r"<svg[^>]*>",s); head=m.group(0)
    vb=re.search(r'viewBox="([^"]+)"',head); vb=vb.group(1) if vb else "0 0 128 128"
    inner=s[m.end():s.rindex("</svg>")]
    inner=re.sub(r'\bid="([^"]+)"',lambda mm:f'id="{pfx}{mm.group(1)}"',inner)
    inner=re.sub(r'url\(#([^)]+)\)',lambda mm:f'url(#{pfx}{mm.group(1)})',inner)
    inner=re.sub(r'(xlink:)?href="#([^"]+)"',lambda mm:f'{mm.group(1) or ""}href="#{pfx}{mm.group(2)}"',inner)
    if name in RECOLOR:
        def rc(mm):
            c=mm.group(1)
            try: return f'fill="{RECOLOR[name]}"' if lum(c)<0.30 else mm.group(0)
            except Exception: return mm.group(0)
        inner=re.sub(r'fill="(#[0-9a-fA-F]{3,6})"',rc,inner)
        inner=inner.replace('fill="black"',f'fill="{RECOLOR[name]}"')
        inner=f'<g fill="{RECOLOR[name]}">{inner}</g>' if name in ("express","linux") else inner
    return vb,inner

def stack(P):
    rows=[("Mobile","freelance since 2023",[("flutter","Flutter"),("dart","Dart"),("kotlin","Kotlin"),("java","Java"),("androidstudio","Android Studio")]),
          ("Web & APIs","platforms & thesis work",[("nextjs","Next.js"),("react","React"),("nodejs","Node.js"),("express","Express"),("fastapi","FastAPI"),("flask","Flask")]),
          ("Data","SQL-first, ORM when it helps",[("postgresql","PostgreSQL"),("mysql","MySQL"),("sqlite","SQLite"),("microsoftsqlserver","SQL Server"),("prisma","Prisma")]),
          ("Scripting & tools","analysis & daily tools",[("python","Python"),("javascript","JavaScript"),("pandas","Pandas"),("git","Git"),("postman","Postman"),("linux","Linux")])]
    W=760; pitch=88; tile=64; rowh=108; top=14; labx=24; tx0=212
    H=top+len(rows)*rowh+6
    defs=""
    b=f'<rect width="{W}" height="{H}" rx="12" fill="{PANEL}" stroke="{LINE}"/>\n'
    k=0
    for r,(lab,sub,items) in enumerate(rows):
        y=top+r*rowh+8
        if r>0: b+=f'<line x1="20" y1="{y-8}" x2="{W-20}" y2="{y-8}" stroke="{LINE}"/>\n'
        b+=(f'<text x="{labx}" y="{y+30}" font-family="{SANS}" font-size="19" font-weight="700" fill="{TEXT}">{esc(lab)}</text>\n'
            f'<text x="{labx}" y="{y+50}" font-family="{MONO}" font-size="11.5" fill="{DIM}">{esc(sub)}</text>\n')
        for i,(ic,name) in enumerate(items):
            x=tx0+i*pitch
            vb,inner=load_icon(ic,f"i{k}_"); k+=1
            flt=""
            b+=(f'<rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="12" fill="{TILE}" stroke="{LINE}"/>'
                f'<svg x="{x+14}" y="{y+14}" width="36" height="36" viewBox="{vb}"><g{flt}>{inner}</g></svg>'
                f'<text x="{x+tile/2}" y="{y+tile+18}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{SOFT}">{esc(name)}</text>\n')
    return svg(W,H,"Technology stack","Technologies grouped by use: mobile (Flutter, Dart, Kotlin, Java, Android Studio), web and APIs (Next.js, React, Node.js, Express, FastAPI, Flask), data (PostgreSQL, MySQL, SQLite, SQL Server, Prisma), scripting and tools (Python, JavaScript, Pandas, Git, Postman, Linux).",b,defs)

# ---------------------------------------------------------------- BUTTONS
def button(label,color,P):
    w=len(label)*9.6+44; H=44
    b=(f'<rect x="0.5" y="0.5" width="{w:.0f}" height="{H-1}" rx="10" fill="{PANEL}" stroke="{color}" stroke-opacity="0.6"/>'
       f'<circle cx="22" cy="22" r="4" fill="{color}">'
       + ("" if P else '<animate attributeName="opacity" values="1;0.3;1" dur="2.6s" repeatCount="indefinite"/>')
       + f'</circle><text x="38" y="27" font-family="{MONO}" font-size="16" fill="{TEXT}">{esc(label)}</text>')
    return svg(int(w)+1,H,f"Link: {label}",f"Button linking to {label}",b)

def build(out,P):
    os.makedirs(out,exist_ok=True)
    files={"hero.svg":hero(P),"terminal.svg":terminal(P),"divider.svg":divider(P),
           "kill-chain.svg":killchain(P),"stack.svg":stack(P),
           "btn-linkedin.svg":button("linkedin",TEAL,P),"btn-email.svg":button("email",VIOLET,P),"btn-repos.svg":button("repositories",AMBER,P)}
    for i,(idx,t) in enumerate([("01","about"),("02","projects"),("03","stack"),("04","security & forensics"),("05","activity"),("06","contact")]):
        files[f"h-{t.split()[0]}.svg"]=header(idx,t,P)
    for n,(name,(c,col,r,t,d,ch)) in enumerate(CARDS.items()):
        files[name+".svg"]=card(c,col,r,t,d,ch,P,n+1)
    for f,s in files.items(): open(os.path.join(out,f),"w",encoding="utf-8").write(s)
    return list(files)

if __name__=="__main__":
    # usage: python3 assets/src/gen.py assets final   (or: /tmp/prev preview for a static render)
    print(build(sys.argv[1], len(sys.argv)>2 and sys.argv[2]=="preview"))
