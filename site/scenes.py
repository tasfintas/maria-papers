"""Scene kit: every scene shares one 12s timeline (walk in, four speech beats, money handover, exit)."""
import chars, chars2
from chars2 import role, maria, nurse, daughter, bed
W, H = 800, 600
DISPLAY = "Bricolage Grotesque,Trebuchet MS,sans-serif"; BODY = "DM Sans,system-ui,sans-serif"

def place(fig, x, feet, s=1.0):
    return f'<g transform="translate({x-100*s:.1f} {feet-328*s:.1f}) scale({s})">{fig}</g>'
def headpos(x, feet, s=1.0): return (x, feet - 233*s)
def shadow(x, y, rx): return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="13" fill="#000" opacity=".26"/>'

def bubble(cls, hx, hy, text):
    w = max(170, 28 + len(text)*10.1); h = 54
    x = min(max(hx - w/2, 10), W - 10 - w); tip = hy - 40; y = max(8, tip - 24 - h)
    tx = min(max(hx, x + 28), x + w - 28)
    return (f'<g class="bub {cls}"><rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h}" rx="14" fill="#fff"/>'
            f'<path d="M{tx-11:.0f},{y+h-1:.0f} L{tx+11:.0f},{y+h-1:.0f} L{hx:.0f},{tip:.0f}Z" fill="#fff"/>'
            f'<text x="{x+w/2:.0f}" y="{y+33:.0f}" text-anchor="middle" font-family="{BODY}" font-size="18" font-weight="600" fill="#1b1840">{text}</text></g>')

# ---------- shared set pieces ----------
def room(wall='#212966', floor='#475074'):
    return (f'<rect width="800" height="600" fill="{wall}"/><rect y="388" width="800" height="212" fill="{floor}"/><rect y="384" width="800" height="8" fill="#7f7692"/>'
            '<path d="M0 470 H800 M0 540 H800 M160 392 L40 600 M400 392 V600 M640 392 L760 600" stroke="#3b4468" stroke-width="2" opacity=".6"/>')
def fan():
    return ('<rect x="397" y="0" width="6" height="40" fill="#7f7692"/><g class="fan"><ellipse cx="338" cy="46" rx="58" ry="7" fill="#9b93b5"/>'
            '<ellipse cx="462" cy="46" rx="58" ry="7" fill="#9b93b5"/><ellipse cx="400" cy="46" rx="7" ry="3" fill="#9b93b5"/></g><circle cx="400" cy="46" r="9" fill="#cfc9ea"/>')
def sign(t, sub, y=64, w=340, cx=400):
    x = cx - w/2
    return (f'<rect x="{x}" y="{y}" width="{w}" height="58" rx="8" fill="#f9e5c0"/>'
            f'<text x="{cx}" y="{y+26}" text-anchor="middle" font-family="{DISPLAY}" font-weight="800" font-size="22" fill="#1b1840">{t}</text>'
            f'<text x="{cx}" y="{y+46}" text-anchor="middle" font-family="{BODY}" font-weight="600" font-size="12.5" letter-spacing="2" fill="#6a6590">{sub}</text>')
def window(x=36, y=86):
    return (f'<rect x="{x}" y="{y}" width="150" height="190" rx="6" fill="#2b3375"/><rect x="{x+10}" y="{y+10}" width="130" height="170" fill="url(#win)"/>'
            f'<path d="M{x+75} {y+10}V{y+180}M{x+10} {y+95}H{x+140}" stroke="#2b3375" stroke-width="6"/>')
def almirah(x=640, y=160):
    return (f'<rect x="{x}" y="{y}" width="130" height="226" rx="4" fill="#5a6590"/><path d="M{x+65} {y}V{y+226}" stroke="#475074" stroke-width="4"/>'
            f'<g><rect x="{x+10}" y="{y+16}" width="46" height="10" fill="#f4a58a"/><rect x="{x+10}" y="{y+36}" width="46" height="10" fill="#f9e5c0"/><rect x="{x+10}" y="{y+56}" width="46" height="10" fill="#e86f9a"/>'
            f'<rect x="{x+74}" y="{y+16}" width="46" height="10" fill="#f9e5c0"/><rect x="{x+74}" y="{y+36}" width="46" height="10" fill="#f4a58a"/><rect x="{x+74}" y="{y+56}" width="46" height="10" fill="#7f7692"/></g>'
            f'<rect x="{x+20}" y="{y+100}" width="90" height="100" fill="#475074" opacity=".6"/>')
def calendar(x=214, y=190):
    return (f'<rect x="{x}" y="{y}" width="56" height="70" rx="3" fill="#f9e5c0"/><rect x="{x}" y="{y}" width="56" height="16" fill="#e86f9a"/><path d="M{x+8} {y+30}h40M{x+8} {y+42}h40M{x+8} {y+54}h30" stroke="#8c84ad" stroke-width="3"/>')
def flag(x=575, y=150):
    return (f'<rect x="{x}" y="{y-10}" width="5" height="120" fill="#cfc9ea"/><rect x="{x+5}" y="{y}" width="84" height="52" fill="#1f8a5b"/><circle cx="{x+44}" cy="{y+26}" r="15" fill="#d63b4a"/>')
def board(x=560, y=170):
    return (f'<rect x="{x}" y="{y}" width="110" height="80" rx="4" fill="#a8845a"/><rect x="{x+8}" y="{y+8}" width="40" height="30" fill="#f9e5c0"/><rect x="{x+54}" y="{y+8}" width="46" height="22" fill="#fff"/><rect x="{x+12}" y="{y+44}" width="50" height="28" fill="#f4a58a"/><rect x="{x+68}" y="{y+38}" width="32" height="34" fill="#f9e5c0"/>')
PROPS = dict(window=window, almirah=almirah, calendar=calendar, flag=flag, board=board)
DEFS = '<defs><linearGradient id="win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f9e5c0" stop-opacity=".55"/><stop offset="1" stop-color="#f9e5c0" stop-opacity=".12"/></linearGradient></defs>'

def desk(left='files', right='stamp'):
    s = ('<ellipse cx="520" cy="392" rx="110" ry="10" fill="#000" opacity=".25"/>'
         '<rect x="296" y="392" width="504" height="130" fill="#8a6a4c"/><rect x="296" y="372" width="504" height="26" rx="3" fill="#c9a57b"/><rect x="296" y="396" width="504" height="4" fill="#00000030"/>'
         '<path d="M360 410 v100 M520 410 v100 M680 410 v100" stroke="#00000022" stroke-width="3"/>'
         '<g transform="skewX(-12) translate(80 0)"><rect x="476" y="346" width="96" height="32" rx="3" fill="#f9e5c0"/><path d="M490 356h70M490 366h56" stroke="#a79f86" stroke-width="3"/></g>')
    if left == 'files': s += '<g><rect x="336" y="352" width="86" height="8" fill="#d8d1e6"/><rect x="340" y="344" width="80" height="8" fill="#f9e5c0"/><rect x="334" y="360" width="90" height="8" fill="#f4a58a"/></g>'
    if left == 'tall':  s += '<g><rect x="334" y="360" width="90" height="10" fill="#f4a58a"/><rect x="338" y="350" width="84" height="10" fill="#d8d1e6"/><rect x="334" y="340" width="90" height="10" fill="#f9e5c0"/><rect x="340" y="330" width="80" height="10" fill="#e86f9a"/><rect x="336" y="320" width="86" height="10" fill="#d8d1e6"/><rect x="342" y="310" width="76" height="10" fill="#f9e5c0"/></g>'
    if left == 'computer': s += '<g><rect x="346" y="300" width="76" height="54" rx="4" fill="#2b2f4a"/><rect x="352" y="306" width="64" height="42" fill="#7fd1c7" opacity=".85"/><rect x="378" y="354" width="12" height="14" fill="#2b2f4a"/><rect x="362" y="366" width="44" height="6" rx="2" fill="#2b2f4a"/></g>'
    if left == 'typewriter': s += '<g><rect x="340" y="344" width="84" height="26" rx="4" fill="#2b2f4a"/><rect x="348" y="334" width="68" height="10" rx="2" fill="#f9e5c0"/><path d="M350 356h64" stroke="#7f7692" stroke-width="3" stroke-dasharray="4 3"/></g>'
    if right == 'stamp': s += '<g class="stampg"><rect x="650" y="334" width="26" height="22" rx="4" fill="#6a3b2a"/><rect x="644" y="354" width="38" height="10" rx="3" fill="#e86f9a"/></g><rect x="636" y="364" width="52" height="8" rx="2" fill="#7a2f58" opacity=".8"/><g><rect x="716" y="344" width="22" height="28" rx="4" fill="#fff"/><path d="M738 352q10 0 10 9t-10 9" stroke="#fff" stroke-width="4" fill="none"/></g>'
    return s

MOVER = dict(x=190, feet=548, s=1.22)
START = (255, 426)
def mover_g(fig): return f'<g class="mom">{shadow(190, 548, 104)}{place(fig, **MOVER)}</g>'
MH = headpos(**MOVER)

def frame(back, mid, front, actors, heads, beats, money, label, extra=''):
    sx, sy = START; dx, dy, num = money
    cash = (f'<g class="cash" style="--dx:{dx}px;--dy:{dy}px"><g transform="translate({sx} {sy}) rotate(-8)"><rect width="60" height="28" rx="3" fill="#8b7cc8"/>'
            f'<rect x="4" y="4" width="52" height="20" rx="2" fill="none" stroke="#e6defa" stroke-width="1.5"/><text x="30" y="20" text-anchor="middle" font-family="{BODY}" font-weight="700" font-size="12" fill="#fff">{num}</text></g></g>')
    lw = 36 + len(label) * 12.6; lx = sx + dx + 10; ly = sy + dy - 78
    lab = (f'<g class="gone"><rect x="{lx-lw/2:.0f}" y="{ly}" width="{lw:.0f}" height="38" rx="19" fill="#1b1840"/>'
           f'<text x="{lx:.0f}" y="{ly+26}" text-anchor="middle" font-family="{DISPLAY}" font-weight="800" font-size="22" fill="#f9e5c0">{label}</text></g>')
    bs = ''.join(bubble(f'b{i+1}', *heads[who], text) for i, (who, text) in enumerate(beats))
    return (f'<svg viewBox="0 0 800 600" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Scene">{DEFS}{back}{mid}{front}{actors}{cash}{lab}{bs}{extra}</svg>')

# ---------- counter-office template ----------
def counter(sg, sub, props, official, beats, label, mover, left='files', third=None, tslot='F', pay='o', num='1000', right='stamp'):
    back = room() + ''.join(PROPS[p]() for p in props) + sign(sg, sub) + fan()
    off = f'<rect x="468" y="262" width="150" height="140" rx="22" fill="#3a3f66"/><g class="clerk"><g transform="translate(443 158)">{role(official)}</g></g>'
    heads = {'m': MH, 'o': (543, 253)}
    mid = off
    actors = ''
    if third and tslot == 'B':
        mid += place(role(third), 700, 262+233*.9, .9); heads['t'] = (700, 262)
    front = desk(left, right)
    if third and tslot == 'F':
        actors += shadow(640, 566, 74) + place(role(third), 640, 566, 1.15); heads['t'] = headpos(640, 566, 1.15)
    actors = mover_g(mover) + actors
    tgt = {'o': (215, -38), 'F': (355, 24), 'B': (425, -41)}[pay]
    return frame(back, mid, front, actors, heads, beats, (*tgt, num), label)

# ---------- custom settings ----------
def gate(beats, label, num):
    back = ('<rect width="800" height="600" fill="#2a3475"/><rect y="100" width="800" height="288" fill="#3a4278"/>'
            + ''.join(f'<rect x="{x}" y="{y}" width="40" height="34" rx="3" fill="#2b3375"/>' for x in range(260, 460, 60) for y in (150, 210))
            + '<rect x="40" y="226" width="150" height="162" rx="6" fill="#1b2150"/><path d="M40 260 Q115 190 190 260" fill="#232a62"/><rect x="60" y="270" width="110" height="118" fill="#2b3375" opacity=".5"/>'
            + '<rect y="388" width="800" height="212" fill="#475074"/><rect y="384" width="800" height="8" fill="#7f7692"/><path d="M0 470 H800 M0 540 H800" stroke="#3b4468" stroke-width="2" opacity=".6"/>'
            + sign('PASSPORT OFFICE', 'APPLICATION SUBMISSION'))
    booth = '<rect x="470" y="212" width="260" height="172" rx="6" fill="#171c47"/>'
    off = place(role('officer'), 600, 262+233, 1)
    glass = '<rect x="476" y="218" width="248" height="154" fill="#8fb4d8" opacity=".16"/><rect x="460" y="372" width="280" height="22" rx="3" fill="#c9a57b"/><text x="600" y="206" text-anchor="middle" font-family="%s" font-weight="700" font-size="13" letter-spacing="2" fill="#f9e5c0">SUBMIT HERE</text>' % BODY
    qcol = ['#e86f9a', '#f4a58a', '#7f9ad9', '#8fc3e8']
    queue = ''.join(f'<g class="q" style="animation-delay:{i*0.4}s">{place(chars2.male(chars.SKIN[i%4], qcol[i], "#33384a"), 520+i*64, 474, .5)}</g>' for i in range(4))
    heads = {'m': MH, 'o': (600, 262), 't': headpos(380, 566, 1.15)}
    actors = mover_g(maria(22, folder=True)) + shadow(380, 566, 74) + place(role('dalal'), 380, 566, 1.15)
    return frame(back, booth + off, glass + queue, actors, heads, beats, (150, 20, num), label)

def ground(beats, label, num):
    ox = 540
    back = ('<rect width="800" height="600" fill="#212966"/><rect y="150" width="800" height="190" fill="#2a3475"/>'
            + ''.join(f'<ellipse cx="{x}" cy="330" rx="70" ry="46" fill="#243066"/>' for x in (60, 210, 400, 560, 720))
            + '<rect y="330" width="800" height="270" fill="#3a4060"/><rect y="326" width="800" height="8" fill="#7f7692"/>'
            + '<path d="M0 480 H800" stroke="#f9e5c0" stroke-width="5" stroke-dasharray="40 30" opacity=".7"/>'
            + sign('DRIVING TEST', 'WRITTEN · VIVA · PRACTICAL')
            + '<rect x="748" y="130" width="8" height="220" fill="#7f7692"/><rect x="732" y="118" width="40" height="22" rx="4" fill="#cfc9ea"/><circle class="blink" cx="762" cy="129" r="4" fill="#ff4d5a"/>'
            + '<g fill="#f4a58a"><path d="M290 430l10 -26 10 26z"/><path d="M350 450l10 -26 10 26z"/><path d="M410 430l10 -26 10 26z"/></g>'
            + '<g transform="translate(-60 0)"><rect x="330" y="316" width="170" height="40" rx="12" fill="#f9e5c0"/><rect x="360" y="290" width="100" height="34" rx="12" fill="#f9e5c0"/><rect x="372" y="298" width="36" height="20" fill="#8fb4d8"/><rect x="414" y="298" width="34" height="20" fill="#8fb4d8"/><circle cx="370" cy="360" r="17" fill="#1b2150"/><circle cx="460" cy="360" r="17" fill="#1b2150"/></g>')
    umb = f'<rect x="{ox-2}" y="232" width="5" height="160" fill="#cfc9ea"/><path d="M{ox-80} 240 Q{ox} 170 {ox+80} 240Z" fill="#f4a58a"/><path d="M{ox-40} 240 Q{ox} 190 {ox+40} 240Z" fill="#f9e5c0"/>'
    off = place(role('officer'), ox, 262+233, 1)
    table = f'<rect x="{ox-80}" y="388" width="160" height="14" rx="3" fill="#c9a57b"/><rect x="{ox-70}" y="402" width="8" height="60" fill="#8a6a4c"/><rect x="{ox+62}" y="402" width="8" height="60" fill="#8a6a4c"/><rect x="{ox-20}" y="378" width="40" height="10" fill="#f9e5c0"/>'
    heads = {'m': MH, 'o': (ox, 262), 't': headpos(720, 566, 1.15)}
    actors = mover_g(maria(24)) + shadow(720, 566, 74) + place(role('dalal'), 720, 566, 1.15)
    return frame(back, umb + off, table, actors, heads, beats, (395, 44, num), label)

def ward(kind, beats, label, num, mover_fig, aides):
    back = ('<rect width="800" height="600" fill="#2b3375"/><rect y="250" width="800" height="138" fill="#3b4a8a"/><rect y="388" width="800" height="212" fill="#475074"/><rect y="384" width="800" height="8" fill="#7f7692"/>'
            '<path d="M0 470 H800 M0 540 H800 M160 392 L40 600 M400 392 V600 M640 392 L760 600" stroke="#3b4468" stroke-width="2" opacity=".6"/>'
            + window(36, 100) + '<path d="M30 96 Q60 200 36 290 L90 290 Q70 200 90 96Z" fill="#6f86d8" opacity=".55"/>'
            + sign('GOVERNMENT HOSPITAL', 'MATERNITY WARD' if kind == 'birth' else 'INTENSIVE CARE', w=360)
            + '<circle cx="640" cy="190" r="28" fill="#f9e5c0"/><path d="M640 190V172M640 190L654 196" stroke="#1b1840" stroke-width="3" stroke-linecap="round"/>'
            + '<rect x="760" y="210" width="6" height="190" fill="#cfc9ea"/><rect x="744" y="206" width="38" height="6" fill="#cfc9ea"/><rect x="748" y="214" width="20" height="40" rx="6" fill="#bfe3f0" opacity=".85"/>' + fan())
    bedg = f'<g transform="translate(792 246) scale(-1.15 1.15)">{bed(kind)}</g>'
    heads = {'m': MH, 'o': headpos(340, 566, 1.05)}
    actors = shadow(340, 566, 66) + place(aides[0], 340, 566, 1.05)
    if len(aides) > 1: actors += shadow(450, 566, 66) + place(aides[1], 450, 566, 1.05); heads['t'] = headpos(450, 566, 1.05)
    actors = mover_g(mover_fig) + actors
    return frame(back, '', bedg, actors, heads, beats, (60, 24, num), label)

def shop(beats, label, num):
    back = ('<rect width="800" height="600" fill="#212966"/><rect width="560" height="388" fill="#3a4278"/><rect y="388" width="800" height="212" fill="#475074"/><rect y="384" width="800" height="8" fill="#7f7692"/>'
            '<rect x="30" y="150" width="320" height="236" fill="#171c47"/><rect x="24" y="126" width="332" height="34" rx="4" fill="#7f7692"/><path d="M24 138H356M24 148H356" stroke="#5f5878" stroke-width="3"/>'
            '<rect x="50" y="200" width="130" height="8" fill="#a8845a"/><rect x="50" y="250" width="130" height="8" fill="#a8845a"/><g fill="#f4a58a"><rect x="58" y="180" width="18" height="20"/><rect x="84" y="176" width="18" height="24" fill="#f9e5c0"/><rect x="110" y="182" width="18" height="18" fill="#e86f9a"/><rect x="62" y="230" width="22" height="20" fill="#f9e5c0"/><rect x="92" y="228" width="22" height="22"/></g>'
            '<rect x="200" y="330" width="140" height="56" fill="#a8845a"/>'
            + sign("MARIA'S SHOP", 'GENERAL STORE', y=64, w=300)
            + '<rect x="696" y="40" width="14" height="440" fill="#7a5230"/><rect x="640" y="76" width="130" height="10" fill="#7a5230"/><path d="M644 80 Q500 120 440 150 M768 80 Q840 100 860 60 M644 80 Q520 130 460 170" stroke="#1b1840" stroke-width="2.5" fill="none"/>'
            '<rect x="440" y="230" width="86" height="106" rx="6" fill="#cfd5e6"/><circle cx="483" cy="276" r="26" fill="#fff"/><path class="spin" d="M483 276 L483 256" stroke="#d63b4a" stroke-width="3" stroke-linecap="round"/><rect x="458" y="312" width="50" height="14" rx="2" fill="#2b2f4a"/><path d="M483 230 V150" stroke="#1b1840" stroke-width="5"/>')
    heads = {'m': MH, 'o': headpos(380, 566, 1.1), 't': headpos(650, 566, 1.15)}
    actors = mover_g(maria(44, folder=True)) + shadow(380, 566, 70) + place(role('lineman'), 380, 566, 1.1) + shadow(650, 566, 74) + place(role('inspector'), 650, 566, 1.15)
    return frame(back, '', '', actors, heads, beats, (105, 24, num), label)

def landoffice(beats, label, num):
    back = ('<rect width="800" height="600" fill="#212966"/><rect y="388" width="800" height="212" fill="#475074"/><rect y="384" width="800" height="8" fill="#7f7692"/>'
            '<rect x="0" y="120" width="340" height="268" fill="#3a4278"/><rect x="20" y="150" width="70" height="60" fill="#2b3375"/><rect x="110" y="150" width="70" height="60" fill="#2b3375"/><rect x="200" y="150" width="70" height="60" fill="#2b3375"/>'
            '<rect x="215" y="262" width="100" height="126" fill="#1b2150"/><g fill="#f9e5c0"><rect x="30" y="170" width="50" height="8"/><rect x="120" y="176" width="50" height="8"/><rect x="210" y="170" width="50" height="8"/></g>'
            + sign('LAND OFFICE', 'MUTATION · SURVEY', y=44, w=300, cx=170)
            + '<rect x="400" y="190" width="400" height="198" fill="#2b3375"/><path d="M390 190 H810 L790 150 H410Z" fill="#f4a58a"/><path d="M430 190 L440 150 M490 190 L496 150 M550 190 L552 150 M610 190 L608 150 M670 190 L664 150 M730 190 L720 150" stroke="#f9e5c0" stroke-width="22" opacity=".9"/>'
            '<text x="600" y="132" text-anchor="middle" font-family="%s" font-weight="800" font-size="20" fill="#f9e5c0">TEA · COPY · FORMS</text>' % DISPLAY
            + '<rect x="420" y="330" width="360" height="58" fill="#8a6a4c"/><rect x="420" y="320" width="360" height="14" fill="#c9a57b"/><g fill="#fff"><rect x="440" y="300" width="14" height="20" rx="3"/><rect x="466" y="300" width="14" height="20" rx="3"/></g><rect x="690" y="290" width="50" height="30" rx="4" fill="#d8d1e6"/><rect x="696" y="280" width="38" height="10" fill="#f4a58a"/>')
    heads = {'m': MH, 'o': headpos(580, 560, 1.1)}
    actors = mover_g(maria(48)) + shadow(580, 560, 70) + place(role('sweeper'), 580, 560, 1.1)
    return frame(back, '', '', actors, heads, beats, (250, 20, num), label)
