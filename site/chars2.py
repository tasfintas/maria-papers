"""Extra roles for Maria's story. All characters are original flat-style SVG drawn in code."""
import chars
from chars import SKIN, INK, head, kameez

def male(skin, shirt, trou, hair=INK, style='crop', glasses=False, mous=False, beard=False,
         tie=None, hat=None, vest=None, collar='#ffffff', hands=None):
    legs = f'<rect x="64" y="236" width="30" height="86" rx="6" fill="{trou}"/><rect x="106" y="236" width="30" height="86" rx="6" fill="{trou}"/>'
    shoes = '<ellipse cx="78" cy="326" rx="16" ry="6" fill="#222"/><ellipse cx="122" cy="326" rx="16" ry="6" fill="#222"/>'
    body = f'<path d="M60,138 Q100,126 140,138 L146,246 L54,246Z" fill="{shirt}"/><path d="M90,130 L100,152 L110,130Z" fill="{collar}"/>'
    if vest: body += f'<path d="M62,142 L88,134 L96,244 L58,244Z M138,142 L112,134 L104,244 L142,244Z" fill="{vest}"/>'
    if tie: body += f'<path d="M96,148 L104,148 L108,208 L100,218 L92,208Z" fill="{tie}"/>'
    body += f'<rect x="42" y="148" width="18" height="70" rx="8" fill="{shirt}"/><rect x="140" y="148" width="18" height="70" rx="8" fill="{shirt}"/>'
    body += f'<circle cx="51" cy="222" r="8" fill="{skin}"/><circle cx="149" cy="222" r="8" fill="{skin}"/>'
    h = head(skin, hair, style, glasses=glasses, moustache=mous, beard=beard)
    if hat == 'cap':
        h += '<path d="M64,70 Q100,40 136,70 L136,78 Q100,64 64,78Z" fill="#3f5a3f"/><rect x="70" y="72" width="60" height="8" fill="#222"/><circle cx="100" cy="66" r="5" fill="#d4b24a"/>'
    elif hat == 'hard':
        h += '<path d="M66,76 Q68,44 100,42 Q132,44 134,76Z" fill="#f2c230"/><rect x="60" y="74" width="80" height="9" rx="4" fill="#d9a420"/>'
    elif hat == 'topi':
        h += '<path d="M68,70 Q100,46 132,70 L132,80 L68,80Z" fill="#f5f0e0"/><path d="M68,80 H132" stroke="#cfc8b0" stroke-width="3"/>'
    return f'<g>{legs}{shoes}{body}{h}</g>'

def role(kind):
    S = SKIN
    if kind == 'principal': return male(S[0], '#f4f4f8', '#2b2f4a', hair='#c9c9d0', glasses=True, mous=True, tie='#7a2f58')
    if kind == 'officer':   return male(S[1], '#d9d4e8', '#1f2540', mous=True, tie='#3f4f9a')
    if kind == 'registrar': return male(S[0], '#e8e2d0', '#2b2f4a', hair='#9a9aa6', glasses=True, tie='#8a2f4f')
    if kind == 'guard':     return male(S[2], '#4f7a4f', '#3a523a', mous=True, hat='cap')
    if kind == 'lineman':   return male(S[2], '#7e8aa8', '#3a3f4a', hat='hard', vest='#e8873a')
    if kind == 'aide':      return male(S[3], '#4aa38f', '#3b8a79', hair='#2b1f1a')
    if kind == 'son':       return male(S[1], '#f1ece0', '#cfc8b0', hair=INK)   # white panjabi
    if kind == 'husband':   return male(S[0], '#9bb5e0', '#33384a', hair=INK, mous=True)
    if kind == 'assistant': return male(S[3], '#c9d6a0', '#4b4f3a', glasses=True, mous=True)
    if kind == 'inspector': return male(S[1], '#bfc6d8', '#2b2f4a', hair=INK, tie='#d98a3d', glasses=True)
    if kind == 'sweeper':
        g = chars.man('peon')
        return g[:-4] + '<path d="M170,214 L186,326" stroke="#7a5230" stroke-width="5" stroke-linecap="round"/><path d="M178,320 l-10,18 h30 l-4,-18Z" fill="#c9a24a"/></g>'
    if kind == 'scribe':    return male(S[2], '#e8e0cf', '#3a3f4a', hair='#8a8a98', glasses=True, mous=True, hat='topi')
    return chars.man(kind)

KAM = {16:('#f6f2ea','#2f3f8f','#6f86d8','#2f3f8f','braid',False),
       18:('#3f9aa8','#235a63','#f4d58d','#f4d58d','braid',False),
       22:('#4f9a5f','#2d5e39','#f2c4d8','#f2c4d8','braid',False),
       24:('#e08a3a','#8a4a1b','#fff1dc','#fff1dc','braid',False),
       27:('#c9356f','#7d1f4a','#f2b84b','#f2b84b','braid',False),
       32:('#8a4fa8','#4d2a62','#f2b84b','#f2b84b','bun',False),
       40:('#c25a3a','#6b2f1f','#f4d58d','#f4d58d','bun',False),
       44:('#3f6fb8','#25406b','#f2e6c0','#f2e6c0','bun',False),
       48:('#2f8f7a','#1d5f52','#f4d58d','#f4d58d','bun',False),
       52:('#8a2f4f','#4f1a2d','#f4d58d','#f4d58d','bun',True),
       55:('#5f7a3a','#3a4a22','#f0e6c0','#f0e6c0','bun',True)}
def maria(age, bag=False, folder=False):
    if age in (66, 75): return chars.maria(age)
    top, pants, orna, trim, st, gl = KAM[age]
    hc = {52:'#4a4a56',55:'#8a8a98'}.get(age, INK)
    skin = SKIN[1]
    sc = {16:.88,18:.94,22:.98}.get(age, 1.0)
    body = kameez(top, pants, orna, trim, skin)
    h = head(skin, hc, st, glasses=gl, old=(age>=52))
    ex = ''
    if bag: ex = '<rect x="146" y="214" width="30" height="40" rx="4" fill="#d9674f"/><rect x="146" y="214" width="30" height="8" rx="3" fill="#a94434"/>'
    if folder: ex = '<rect x="148" y="206" width="34" height="42" rx="3" fill="#f9e5c0"/><rect x="148" y="206" width="34" height="8" fill="#e86f9a"/>'
    feet = '<ellipse cx="80" cy="328" rx="13" ry="5" fill="#3a2f2a"/><ellipse cx="120" cy="328" rx="13" ry="5" fill="#3a2f2a"/>'
    return f'<g transform="translate(100 340) scale({sc}) translate(-100 -340)">{feet}{body}{h}{ex}</g>'

def daughter():
    skin = SKIN[3]
    return f'<g><ellipse cx="80" cy="328" rx="13" ry="5" fill="#3a2f2a"/><ellipse cx="120" cy="328" rx="13" ry="5" fill="#3a2f2a"/>{kameez("#e0a0c0","#7a4a6b","#f6f2ea","#f6f2ea",skin)}{head(skin,INK,"braid")}</g>'

def nurse():
    skin = SKIN[1]
    b = kameez('#f4f6fb', '#8fc3e8', '#8fc3e8', '#8fc3e8', skin)
    h = head(skin, INK, 'bun') + '<path d="M72,66 Q100,40 128,66 L128,74 Q100,60 72,74Z" fill="#fff"/><rect x="96" y="52" width="8" height="14" fill="#e86f9a"/>'
    return f'<g><ellipse cx="80" cy="328" rx="13" ry="5" fill="#3a2f2a"/><ellipse cx="120" cy="328" rx="13" ry="5" fill="#3a2f2a"/>{b}{h}</g>'

def bed(kind):
    """Hospital bed, local box 0..380 x 0..210. kind: 'birth' (Maria 27 with baby) or 'dead' (Maria 75, eyes closed)."""
    if kind == 'birth': skin, hair, st, blanket = SKIN[1], INK, 'braid', '#6fb3b8'
    else:               skin, hair, st, blanket = SKIN[1], '#e6e6ee', 'oldbun', '#e9ecf4'
    hd = head(skin, hair, st, glasses=False, old=(kind=='dead'))
    if kind == 'dead':
        hd += f'<circle cx="87" cy="98" r="6" fill="{skin}"/><circle cx="113" cy="98" r="6" fill="{skin}"/>' \
              f'<path d="M81,98 q6,5 12,0 M107,98 q6,5 12,0" stroke="{INK}" stroke-width="2" fill="none" stroke-linecap="round"/>'
    s = '<rect x="6" y="40" width="14" height="150" rx="4" fill="#5a6590"/><rect x="360" y="90" width="14" height="100" rx="4" fill="#5a6590"/>'
    s += '<rect x="14" y="120" width="352" height="44" rx="12" fill="#f0f2f8"/><rect x="26" y="164" width="10" height="34" fill="#475074"/><rect x="340" y="164" width="10" height="34" fill="#475074"/>'
    s += f'<path d="M104,102 Q220,84 366,108 L366,148 Q220,160 104,150Z" fill="{blanket}"/><path d="M104,112 Q220,96 366,118" stroke="#00000018" stroke-width="3" fill="none"/>'
    s += '<ellipse cx="62" cy="108" rx="56" ry="18" fill="#fafbff"/>'
    s += f'<path d="M30,126 Q60,100 112,112 L110,150 L34,150Z" fill="#cfd8ee"/>'
    s += f'<g transform="translate(-4 14) scale(.62)">{hd}</g>'
    if kind == 'birth':
        s += '<g transform="rotate(-6 170 104)"><ellipse cx="172" cy="104" rx="38" ry="19" fill="#fff1dc"/><path d="M136,112 q36,14 72,0" stroke="#f0a0b8" stroke-width="6" fill="none"/></g><circle cx="200" cy="96" r="13" fill="#d9a074"/><path d="M188,90 q12,-13 24,0" stroke="#2b1f1a" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M194,98 q3,2 6,0 M203,98 q3,2 6,0" stroke="#2b1f1a" stroke-width="1.6" fill="none"/>'
    return f'<g>{s}</g>'
