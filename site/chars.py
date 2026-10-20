# Original flat-style character kit (Maria at 5 ages + 4 officials). Pure SVG strings.
SKIN=['#b8794a','#c58a5b','#a96b40','#cf9768']
INK='#2b1f1a'
def eyes(cx=100,cy=98,glasses=False,old=False):
    s=f'<ellipse cx="{cx-13}" cy="{cy}" rx="3" ry="3.6" fill="{INK}"/><ellipse cx="{cx+13}" cy="{cy}" rx="3" ry="3.6" fill="{INK}"/>'
    s+=f'<path d="M{cx-19},{cy-9} q6,-4 12,0 M{cx+7},{cy-9} q6,-4 12,0" stroke="{INK}" stroke-width="2" fill="none" stroke-linecap="round"/>'
    s+=f'<path d="M{cx},{cy+3} q-3,8 2,9" stroke="#00000033" stroke-width="2" fill="none" stroke-linecap="round"/>'
    s+=f'<circle cx="{cx-21}" cy="{cy+10}" r="6" fill="#e0705a" opacity=".3"/><circle cx="{cx+21}" cy="{cy+10}" r="6" fill="#e0705a" opacity=".3"/>'
    if old: s+=f'<path d="M{cx-20},{cy+3} l-3,2 M{cx+20},{cy+3} l3,2 M{cx-9},{cy+19} q9,5 18,0" stroke="#00000030" stroke-width="1.6" fill="none"/>'
    if glasses: s+=f'<circle cx="{cx-13}" cy="{cy}" r="9" fill="none" stroke="#3a3a48" stroke-width="2.2"/><circle cx="{cx+13}" cy="{cy}" r="9" fill="none" stroke="#3a3a48" stroke-width="2.2"/><path d="M{cx-4},{cy} h8" stroke="#3a3a48" stroke-width="2.2"/>'
    return s
def mouth(kind='smile',cx=100,cy=116):
    if kind=='flat': return f'<path d="M{cx-8},{cy} h16" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>'
    return f'<path d="M{cx-9},{cy-1} q9,9 18,0" stroke="{INK}" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
def head(skin,hairc,style,glasses=False,old=False,mood='smile',moustache=False,beard=False):
    s=''
    if style in('braid','bun','oldbun'): s+=f'<ellipse cx="100" cy="94" rx="36" ry="38" fill="{hairc}"/>'
    s+=f'<rect x="90" y="118" width="20" height="26" rx="8" fill="{skin}"/>'
    s+=f'<ellipse cx="66" cy="102" rx="5" ry="8" fill="{skin}"/><ellipse cx="134" cy="102" rx="5" ry="8" fill="{skin}"/>'
    s+=f'<circle cx="100" cy="95" r="34" fill="{skin}"/>'
    s+=eyes(glasses=glasses,old=old)+mouth(mood)
    if style=='braid':
        s+=f'<path d="M66,92 Q66,58 100,57 Q134,58 134,92 Q122,72 100,72 Q80,72 66,92Z" fill="{hairc}"/>'
        s+=f'<path d="M100,60 L100,72" stroke="#00000040" stroke-width="2"/>'
        for i,y in enumerate(range(118,196,16)): s+=f'<ellipse cx="{132+ (i%2)*3}" cy="{y}" rx="9" ry="12" fill="{hairc}"/>'
        s+='<circle cx="133" cy="200" r="6" fill="#d94f4f"/>'
    elif style in('bun','oldbun'):
        s+=f'<path d="M66,94 Q64,56 100,55 Q136,56 134,94 Q120,70 100,72 Q80,70 66,94Z" fill="{hairc}"/><circle cx="124" cy="58" r="13" fill="{hairc}"/>'
    elif style=='crop':
        s+=f'<path d="M67,92 Q64,58 100,58 Q136,58 133,92 Q128,72 100,70 Q72,72 67,92Z" fill="{hairc}"/>'
    elif style=='bald':
        s+=f'<path d="M70,80 Q72,62 100,61 Q128,62 130,80 Q118,68 100,68 Q82,68 70,80Z" fill="{hairc}" opacity=".9"/>'
    if moustache: s+=f'<path d="M86,110 q14,-8 28,0 q-14,4 -28,0Z" fill="{INK}"/>'
    if beard: s+=f'<path d="M72,108 q28,50 56,0 q-4,24 -28,28 q-24,-4 -28,-28Z" fill="{INK}" opacity=".75"/>'
    return s
def kameez(top,pants,orna,trim,skin):
    return f'''<path d="M64,252 L98,252 L94,324 L66,324Z M102,252 L136,252 L134,324 L106,324Z" fill="{pants}"/>
    <path d="M64,138 Q100,128 136,138 L152,266 L48,266Z" fill="{top}"/>
    <path d="M49,254 L151,254 L152,266 L48,266Z" fill="{trim}"/>
    <rect x="44" y="150" width="15" height="74" rx="7" fill="{top}"/><rect x="141" y="150" width="15" height="74" rx="7" fill="{top}"/>
    <rect x="44" y="214" width="15" height="9" fill="{trim}"/><rect x="141" y="214" width="15" height="9" fill="{trim}"/>
    <circle cx="51.5" cy="228" r="7.5" fill="{skin}"/><circle cx="148.5" cy="228" r="7.5" fill="{skin}"/>
    <path d="M60,140 Q100,200 140,140 L152,150 Q100,226 48,152Z" fill="{orna}"/>
    <path d="M140,142 L158,152 L164,276 L146,276Z" fill="{orna}" opacity=".95"/>
    <path d="M146,276 L164,276" stroke="{trim}" stroke-width="5"/>'''
def maria(age):
    skin=SKIN[1]; tilt=0; extra=''
    if age in (16,27,48):
        cfg={16:('#f6f2ea','#2f3f8f','#6f86d8','#2f3f8f',INK,'braid',.88),
             27:('#c9356f','#7d1f4a','#f2b84b','#f2b84b',INK,'braid',1.0),
             48:('#2f8f7a','#1d5f52','#f4d58d','#f4d58d',INK,'bun',1.0)}
        top,pants,orna,trim,hc,st,sc=cfg[age]
        body=kameez(top,pants,orna,trim,skin); h=head(skin,hc,st)
        if age==16: extra='<rect x="146" y="214" width="30" height="40" rx="4" fill="#d9674f"/><rect x="146" y="214" width="30" height="8" rx="3" fill="#a94434"/>'
        feet='<ellipse cx="80" cy="328" rx="13" ry="5" fill="#3a2f2a"/><ellipse cx="120" cy="328" rx="13" ry="5" fill="#3a2f2a"/>'
    else:
        cfg={66:('#7a6aa8','#f1d58a','#c9c9d0',2,1.0,'#fff1dc'),75:('#7f8798','#e7e0c9','#e6e6ee',6,.92,'#fff1dc')}
        sr,bd,hc,tilt,sc,bl=cfg[age]
        dk='#00000026'
        body=f'''
        <path d="M120,140 L158,160 L166,296 L136,300Z" fill="{sr}"/><path d="M158,160 L166,296" stroke="{bd}" stroke-width="5"/>
        <path d="M60,206 Q50,270 44,326 L156,326 Q150,270 140,206Z" fill="{sr}"/>
        <path d="M82,206 L118,206 L132,326 L68,326Z" fill="#ffffff" opacity=".12"/>
        <path d="M86,208 L78,326 M94,208 L90,326 M102,208 L101,326 M110,208 L112,326 M116,208 L124,326" stroke="{dk}" stroke-width="2.4"/>
        <path d="M44,326 L156,326 L155,308 L45,308Z" fill="{bd}"/><path d="M45,308 L155,308" stroke="{sr}" stroke-width="3"/>
        <path d="M66,170 L134,170 L136,208 L64,208Z" fill="{skin}"/>
        <path d="M66,138 Q100,128 134,138 L131,176 L69,176Z" fill="{bl}"/>
        <rect x="46" y="148" width="17" height="38" rx="8" fill="{bl}"/><rect x="137" y="148" width="17" height="38" rx="8" fill="{bl}"/>
        <rect x="48" y="180" width="13" height="42" rx="6.5" fill="{skin}"/><rect x="139" y="180" width="13" height="42" rx="6.5" fill="{skin}"/>
        <circle cx="54.5" cy="226" r="7.5" fill="{skin}"/><circle cx="145.5" cy="226" r="7.5" fill="{skin}"/>
        <path d="M64,140 L92,131 L148,214 L148,244 L110,238 L74,176Z" fill="{sr}"/>
        <path d="M92,131 L148,214" stroke="{bd}" stroke-width="7"/><path d="M74,176 L110,238" stroke="{bd}" stroke-width="7"/>
        <path d="M148,214 L148,244" stroke="{bd}" stroke-width="6"/>'''
        h=head(skin,hc,'crop',glasses=True,old=True)
        hood=f'''<path fill-rule="evenodd" d="M54,152 Q46,96 60,68 Q78,38 100,38 Q124,38 140,68 Q154,96 146,152 Q100,140 54,152Z M69,100 Q69,64 100,62 Q131,64 131,100 Q131,136 100,136 Q69,136 69,100Z" fill="{sr}"/>
        <path d="M69,100 Q69,64 100,62 Q131,64 131,100 Q131,136 100,136 Q69,136 69,100Z" fill="none" stroke="{bd}" stroke-width="4.5"/>'''
        extra=hood
        if age==75: extra+='<path d="M164,236 v92" stroke="#7a5230" stroke-width="5" stroke-linecap="round"/><path d="M164,236 q-12,-4 -14,8" stroke="#7a5230" stroke-width="5" fill="none" stroke-linecap="round"/>'
        feet='<ellipse cx="82" cy="330" rx="13" ry="5" fill="#3a2f2a"/><ellipse cx="118" cy="330" rx="13" ry="5" fill="#3a2f2a"/>'
    return f'<g transform="translate(100 340) scale({sc}) rotate({tilt}) translate(-100 -340)">{feet}{body}{h}{extra}</g>'
def man(kind):
    skin={'clerk':SKIN[0],'peon':SKIN[2],'dalal':SKIN[3],'police':SKIN[1]}[kind]
    legs=lambda c:f'<rect x="64" y="236" width="30" height="86" rx="6" fill="{c}"/><rect x="106" y="236" width="30" height="86" rx="6" fill="{c}"/>'
    shoes='<ellipse cx="78" cy="326" rx="16" ry="6" fill="#222"/><ellipse cx="122" cy="326" rx="16" ry="6" fill="#222"/>'
    arms=lambda c:f'<rect x="42" y="148" width="18" height="70" rx="8" fill="{c}"/><rect x="140" y="148" width="18" height="70" rx="8" fill="{c}"/><circle cx="51" cy="222" r="8" fill="{skin}"/><circle cx="149" cy="222" r="8" fill="{skin}"/>'
    if kind=='clerk':
        b=legs('#33384a')+f'<path d="M60,138 Q100,126 140,138 L146,246 L54,246Z" fill="#8fc3e8"/><path d="M92,130 L100,150 L108,130Z" fill="#fff"/><rect x="118" y="168" width="14" height="12" fill="#6aa5d1"/>'+arms('#8fc3e8')+'<rect x="156" y="204" width="34" height="42" rx="3" fill="#e8dcc0"/><rect x="156" y="204" width="34" height="8" fill="#b44"/>'
        h=head(skin,INK,'crop',glasses=True,moustache=True)
    elif kind=='peon':
        b=f'<rect x="60" y="234" width="80" height="92" rx="8" fill="#6b7fd0"/><path d="M60,260 h80 M60,290 h80 M80,234 v92 M100,234 v92 M120,234 v92" stroke="#fff" stroke-width="2.5" opacity=".55"/>'+f'<path d="M60,138 Q100,126 140,138 L146,244 L54,244Z" fill="#c98a2f"/>'+arms('#c98a2f')+'<path d="M64,140 Q100,200 150,150 L150,168 Q100,222 60,160Z" fill="#e8e0cf"/>'
        h=head(skin,INK,'crop',moustache=True)
    elif kind=='dalal':
        b=legs('#efe6d2')+f'<path d="M58,138 Q100,126 142,138 L150,262 L50,262Z" fill="#f3ead4"/><path d="M62,142 L88,134 L96,250 L58,250Z M138,142 L112,134 L104,250 L142,250Z" fill="#7a4b2a"/>'+arms('#f3ead4')+'<rect x="154" y="206" width="22" height="36" rx="4" fill="#26262e"/><rect x="157" y="210" width="16" height="26" rx="2" fill="#7fd1c7"/>'
        h=head(skin,INK,'crop',beard=True)
    else:
        b=legs('#4b4f3a')+f'<path d="M60,138 Q100,126 140,138 L146,246 L54,246Z" fill="#b9a46a"/><rect x="44" y="244" width="112" height="9" fill="#2a2a2a"/><rect x="92" y="244" width="16" height="9" fill="#d4b24a"/><rect x="116" y="162" width="16" height="10" fill="#d94f4f"/>'+arms('#b9a46a')
        h=head(skin,INK,'crop',moustache=True)+'<path d="M64,70 Q100,40 136,70 L136,78 Q100,64 64,78Z" fill="#4b4f3a"/><rect x="70" y="72" width="60" height="8" fill="#2a2a2a"/><circle cx="100" cy="66" r="5" fill="#d4b24a"/>'
    return f'<g>{b}{shoes}{h}</g>'

def mother():
    skin=SKIN[3]
    body=f'''<path d="M64,252 L98,252 L94,324 L66,324Z M102,252 L136,252 L134,324 L106,324Z" fill="#7a3b1e"/>
    <path d="M64,138 Q100,128 136,138 L152,266 L48,266Z" fill="#d98a3d"/><path d="M49,254 L151,254 L152,266 L48,266Z" fill="#f4d58d"/>
    <path d="M60,140 Q100,200 140,140 L152,150 Q100,226 48,152Z" fill="#f4d58d"/><path d="M140,142 L158,152 L164,276 L146,276Z" fill="#f4d58d"/>
    <g transform="rotate(-8 100 212)"><ellipse cx="100" cy="212" rx="38" ry="21" fill="#fff1dc"/><path d="M64,220 q36,16 72,0" stroke="#f0a0b8" stroke-width="7" fill="none"/></g>
    <circle cx="128" cy="196" r="14" fill="#d9a074"/><path d="M116,190 q12,-14 24,0" stroke="#2b1f1a" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M122,198 q3,2 6,0 M131,198 q3,2 6,0" stroke="#2b1f1a" stroke-width="1.6" fill="none"/>
    <path d="M62,150 L84,214" stroke="#d98a3d" stroke-width="16" stroke-linecap="round"/><path d="M138,150 L112,224" stroke="#d98a3d" stroke-width="16" stroke-linecap="round"/>
    <circle cx="86" cy="218" r="8" fill="{skin}"/><circle cx="110" cy="228" r="8" fill="{skin}"/>'''
    feet='<ellipse cx="80" cy="328" rx="13" ry="5" fill="#3a2f2a"/><ellipse cx="120" cy="328" rx="13" ry="5" fill="#3a2f2a"/>'
    return f'<g>{feet}{body}{head(skin,INK,"bun")}</g>'

if False:
    cells=[('Maria · 16',maria(16)),('Maria · 27',maria(27)),('Maria · 48',maria(48)),('Maria · 66',maria(66)),('Maria · 75',maria(75)),
           ('Clerk',man('clerk')),('Peon',man('peon')),('Dalal / broker',man('dalal')),('Police',man('police'))]
    W=210;H=400;cols=5;rows=2
    out=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*cols}" height="{H*rows+30}" viewBox="0 0 {W*cols} {H*rows+30}"><rect width="100%" height="100%" fill="#1b2150"/>'
    for i,(n,g) in enumerate(cells):
        x=(i%cols)*W;y=(i//cols)*H+10
        out+=f'<g transform="translate({x+5} {y})"><rect x="0" y="0" width="200" height="370" rx="14" fill="#2b3375"/><rect x="0" y="330" width="200" height="40" fill="#475074" opacity=".5"/>{g}<text x="100" y="392" text-anchor="middle" fill="#f9e5c0" font-family="sans-serif" font-size="15">{n}</text></g>'
    out+='</svg>'
    open('chars.svg','w').write(out)
