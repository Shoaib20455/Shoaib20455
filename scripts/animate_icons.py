"""Offline generator for the 27 README icons. Run: python3 scripts/animate_icons.py.

Preserves artwork, adds colors and geometry-specific CSS motion, and includes a
prefers-reduced-motion fallback. No scripts or remote resources.
JS/TS badge paths: devicons/devicon icons/*/*-original.svg (MIT).
"""
from copy import deepcopy
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets/icons'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
ART = json.loads((ROOT/'scripts/icon_artwork.json').read_text())
MOTION = {}


def tag(el):
    return el.tag.rsplit('}', 1)[-1]


def node(kind, **attrs):
    return ET.Element(f'{{{NS}}}{kind}', {k.replace('_','-'):str(v) for k,v in attrs.items()})


def clean(name):
    root = ET.fromstring(ART[name])
    for parent in list(root.iter()):
        for child in list(parent):
            if tag(child) in ('style','animate','animateTransform','animateMotion','set','title','desc'):
                parent.remove(child)
    for el in root.iter():
        el.attrib.pop('style', None)
    if name == 'metamask':
        for el in root.iter():
            if el.get('class') in ('st1','st6'):
                c = '#e4761b' if el.get('class') == 'st1' else '#f6851b'
                el.set('fill', c); el.set('stroke', c)
    return root


def paths(root):
    defs = {e for d in root if tag(d) in ('defs','def') for e in d.iter()}
    return [e for e in root.iter() if tag(e)=='path' and e not in defs]


class Icon:
    def __init__(self, name, viewbox=None):
        self.name=name; self.source=clean(name); self.css=[]
        x,y,w,h=map(float,(viewbox or self.source.get('viewBox')).split())
        self.root=node('svg',viewBox='0 0 128 128',width=128,height=128,role='img',aria_label=name)
        title=node('title'); title.text=name; self.root.append(title)
        self.defs=node('defs'); self.root.append(self.defs)
        scale=108/max(w,h)
        self.art=node('g',transform=f'translate({64-(x+w/2)*scale:g} {64-(y+h/2)*scale:g}) scale({scale:g})',fill='#334155')
        self.root.append(self.art)
        for child in self.source:
            if tag(child) in ('defs','def'):
                for d in child: self.defs.append(deepcopy(d))
            else: self.art.append(deepcopy(child))

    def animate(self, el, label, frames, duration=7, delay=0, easing='ease-in-out', origin=None):
        key=f'{self.name}-{label}'
        self.css.append(f'@keyframes {key} {{{frames}}}')
        el.set('style',el.get('style','')+f'animation:{key} {duration}s {easing} {delay}s infinite;'+(f'transform-origin:{origin};' if origin else ''))

    def shape(self, kind, **attrs):
        el=node(kind,**attrs); self.art.append(el); return el

    def reset(self):
        self.art.clear()
        # clear() removes the normalization transform; restore it from saved attrs.
        self.art.attrib.update(self.normalization)
        for child in list(self.defs): self.defs.remove(child)

    @property
    def normalization(self):
        x,y,w,h=map(float,self.source.get('viewBox').split())
        if self.name in ('aws','github','ethereum','erc4337','solana'): x,y,w,h=0,0,24,24
        if self.name=='zksync': x,y,w,h=100,90,500,290
        s=108/max(w,h)
        return dict(transform=f'translate({64-(x+w/2)*s:g} {64-(y+h/2)*s:g}) scale({s:g})',fill='#334155')

    def accent(self,color):
        self.root.insert(2,node('rect',x=4,y=4,width=120,height=120,rx=25,fill=color))

    def save(self,description):
        desc=node('desc'); desc.text=description; self.root.insert(1,desc)
        style=node('style')
        style.text='\n'.join(self.css)+'\n@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } .motion-trail { opacity: 0; } }'
        self.defs.append(style)
        (ASSETS/f'{self.name}-animated.svg').write_text(ET.tostring(self.root,encoding='unicode')+'\n')
        MOTION[self.name]=description


def orbit(rx,ry,phase=0):
    return ''.join(f'{i*5}%{{transform:translate({rx*math.cos(i*math.pi/10+phase):.3f}px,{ry*math.sin(i*math.pi/10+phase):.3f}px)}}' for i in range(21))


def react():
    icon=Icon('react'); icon.reset()
    icon.shape('circle',cx=50,cy=50,r=5,fill='#61dafb')
    for i,rotation in enumerate((0,60,120)):
        ring=node('g',transform=f'rotate({rotation} 50 50)')
        ring.append(node('ellipse',cx=50,cy=50,rx=40,ry=13,fill='none',stroke='#61dafb',stroke_width=2.3,opacity='.8'))
        electron=node('circle',cx=50,cy=50,r=2.7,fill='#22d3ee')
        icon.animate(electron,f'electron-{i}',orbit(40,13,i*2*math.pi/3),6,easing='linear')
        ring.append(electron); icon.art.append(ring)
    icon.save('Electrons follow the three atom rings; the nucleus and logo stay fixed.')


def python():
    icon=Icon('python')
    for i,(p,c) in enumerate(zip(paths(icon.art),('#3776ab','#ffd343'))):
        p.set('fill',c); sign=-1 if i==0 else 1
        icon.animate(p,f'interlock-{i}',f'0%,25%,75%,100%{{transform:translate(0,0)}}50%{{transform:translate({sign*9}px,{sign*6}px)}}',6)
    icon.save('The blue and yellow snake halves gently interlock and settle back into the Python mark.')


def badges():
    for name in ('javascript','typescript'):
        icon=Icon(name)
        if name=='javascript':
            job=node('circle',cx=64,cy=64,r=2.4,fill='#c79b00',**{'class':'motion-trail'}); icon.root.append(job)
            icon.animate(job,'event-loop',orbit(60,60,-math.pi/2),8,easing='linear')
            description='A queued job follows the badge perimeter, representing the JavaScript event loop.'
        else:
            line=icon.shape('path',d='M25 112 H106',fill='none',stroke='#e0f2fe',stroke_width=3,stroke_linecap='round',pathLength=1)
            line.set('stroke-dasharray','1')
            icon.animate(line,'type-check','0%,15%,100%{stroke-dashoffset:0}35%{stroke-dashoffset:1}65%,90%{stroke-dashoffset:0}',6)
            description='A type-check underline completes beneath the stationary TypeScript letters.'
        icon.save(description)


def aws():
    icon=Icon('aws','0 0 24 24')
    text=deepcopy(next(e for e in icon.source.iter() if e.get('id')=='aws-text'))
    smile=[deepcopy(e) for e in icon.source.iter() if tag(e)=='path' and e.get('fill')=='white']
    icon.reset(); text.set('fill','#ff9900'); icon.art.append(text)
    for p in smile: p.set('fill','#ff9900'); icon.art.append(p)
    clip=node('clipPath',id='aws-smile-clip')
    for p in smile: clip.append(deepcopy(p))
    icon.defs.append(clip)
    track=icon.shape('path',d='M0 14.5 C8 20 16 20 24 15',clip_path='url(#aws-smile-clip)',fill='none',stroke='#ffcf70',stroke_width=2.5,pathLength=1)
    track.set('stroke-dasharray','.15 .85')
    icon.animate(track,'smile-route','from{stroke-dashoffset:1}to{stroke-dashoffset:-1}',6,easing='linear')
    icon.save('A highlight follows AWS’s orange smile; the wordmark stays upright.')


def github():
    icon=Icon('github','0 0 24 24'); mark=next(e for e in icon.source.iter() if e.get('class')=='github-mask')
    icon.reset(); icon.accent('#f0eaff')
    icon.shape('path',d=mark.get('d'),fill='#8957e5')
    ring=node('circle',cx=64,cy=64,r=58,fill='none',stroke='#c4b5fd',stroke_width=1.5,pathLength=1)
    ring.set('stroke-dasharray','.08 .92'); icon.root.append(ring)
    icon.animate(ring,'commit-ring','from{stroke-dashoffset:1}to{stroke-dashoffset:0}',8,easing='linear')
    icon.save('A commit highlight travels around the Octocat perimeter; a purple accent colors the monochrome mark.')


def git():
    icon=Icon('git','0 0 24 24'); icon.reset()
    icon.shape('rect',x=3.5,y=3.5,width=17,height=17,rx=1.7,transform='rotate(45 12 12)',fill='#f05032')
    icon.shape('path',d='M8 6 L15.5 13.5 M10 8 V17',fill='none',stroke='#fff',stroke_width=1.7,stroke_linecap='round')
    for x,y in ((10,8),(15.5,13.5),(10,17)): icon.shape('circle',cx=x,cy=y,r=1.65,fill='#fff')
    job=icon.shape('circle',cx=10,cy=8,r=.9,fill='#ffd5ca',**{'class':'motion-trail'})
    icon.animate(job,'branch-commit','0%,10%,100%{transform:translate(0,0)}35%{transform:translate(0,9px)}55%{transform:translate(0,0)}80%{transform:translate(5.5px,5.5px)}',6)
    icon.save('A commit travels to each endpoint along Git’s white branches on its orange diamond.')


def shields():
    for name,c in (('html','#ffbd98'),('css','#a5e6ff')):
        icon=Icon(name)
        for el in list(icon.art):
            if tag(el)=='rect': icon.art.remove(el)
        clip=node('clipPath',id=f'{name}-numeral')
        for p in paths(icon.art)[2:]: clip.append(deepcopy(p))
        icon.defs.append(clip)
        d='M34 31 H91 L88 58 H44 L46 86 L64 91 L83 86' if name=='html' else 'M34 31 H91 L88 58 H44 M88 58 L84 88 L64 94 L43 88'
        marker=icon.shape('path',d=d,fill='none',stroke=c,stroke_width=12,clip_path=f'url(#{name}-numeral)',pathLength=1)
        marker.set('stroke-dasharray','.2 .8')
        icon.animate(marker,'numeral-trace','from{stroke-dashoffset:1}to{stroke-dashoffset:-1}',7,easing='linear')
        icon.save(f'A colored trace follows the {name.upper()} numeral inside its stationary shield.')


def tailwind():
    icon=Icon('tailwind'); p=paths(icon.art)[0]; waves=[w for w in re.split(r'(?=[Mm])',p.get('d')) if w]; icon.art.remove(p)
    for i,d in enumerate(waves):
        wave=icon.shape('path',d=d,fill='#38bdf8')
        icon.animate(wave,f'wind-{i}','0%,100%{transform:translateX(0)}30%{transform:translateX(2px)}70%{transform:translateX(-2px)}',5,-i*.6)
    icon.save('Tailwind’s two waves drift horizontally with a phase offset, like flowing air.')


def nodejs():
    icon=Icon('nodejs'); track=icon.shape('path',d='M64 7 L113 35 V92 L64 121 L15 92 V35 Z',fill='none',stroke='#d9f99d',stroke_width=1.8,pathLength=1)
    track.set('stroke-dasharray','.06 .94'); icon.animate(track,'event-loop','from{stroke-dashoffset:0}to{stroke-dashoffset:-1}',8,easing='linear')
    icon.save('An event travels around Node.js’s green hexagon, representing its event loop.')


def postgres():
    icon=Icon('postgres')
    for i,(x,y) in enumerate(((54.7,42.3),(94.3,41.7))):
        lid=icon.shape('ellipse',cx=x,cy=y,rx=3.3,ry=2.3,fill='#336791')
        lid.set('style','transform:scaleY(0);')
        icon.animate(lid,f'eye-lid-{i}','0%,42%,48%,100%{transform:scaleY(0)}44%,46%{transform:scaleY(1)}',8,origin=f'{x}px {y}px')
    icon.save('The elephant blinks while its blue body, trunk and outline remain aligned.')


def vscode():
    icon=Icon('vscode'); line=icon.shape('path',d='M22 63 L47 43 M22 63 L47 83',fill='none',stroke='#7dd3fc',stroke_width=3,pathLength=1)
    line.set('stroke-dasharray','.25 .75'); icon.animate(line,'code-bracket','from{stroke-dashoffset:1}to{stroke-dashoffset:-1}',6,easing='linear')
    icon.save('A code trace follows the blue editor bracket; the logo facets stay fixed together.')


def docker():
    icon=Icon('docker'); ps=paths(icon.art); whale=node('g')
    for child in list(icon.art): icon.art.remove(child); whale.append(child)
    icon.art.append(whale)
    icon.animate(whale,'swim','0%,100%{transform:translate(0,0) rotate(0deg)}25%{transform:translate(1px,-1.5px) rotate(-.6deg)}75%{transform:translate(-1px,1.5px) rotate(.6deg)}',7,origin='64px 72px')
    for i,p in enumerate(ps[5:12]): icon.animate(p,f'load-container-{i}','0%,10%,100%{transform:translateY(0)}22%{transform:translateY(-6px)}42%,92%{transform:translateY(0)}',7,-i*.35)
    icon.save('Containers load onto a swimming whale; its body, eye and contours move together.')


def graphql():
    icon=Icon('graphql'); job=icon.shape('circle',cx=64,cy=9,r=3,fill='#fce7f3',**{'class':'motion-trail'})
    icon.animate(job,'query-route','0%,100%{transform:translate(0,0)}16.66%{transform:translate(44px,25px)}33.33%{transform:translate(44px,76px)}50%{transform:translate(0,101px)}66.66%{transform:translate(-44px,76px)}83.33%{transform:translate(-44px,25px)}',8,easing='linear')
    icon.save('A query travels between GraphQL’s six pink vertices along the graph edges.')


def payload():
    icon=Icon('payload'); icon.accent('#eeeaff')
    for i,p in enumerate(paths(icon.art)):
        p.set('fill','#635bba' if i==0 else '#8276d1'); sign=1 if i==0 else -1
        icon.animate(p,f'content-block-{i}',f'0%,15%,70%,100%{{transform:translate(0,0)}}40%{{transform:translate({sign*2}px,{sign*3}px)}}',7)
    icon.save('Payload’s content blocks separate slightly and assemble again, with violet accents for its monochrome mark.')


def solidity():
    icon=Icon('solidity'); icon.accent('#ede9fe')
    for i,p in enumerate(paths(icon.art)):
        p.set('fill','#5b548b'); base=p.get('opacity','1')
        icon.animate(p,f'facet-{i}',f'0%,100%{{opacity:{base}}}40%{{opacity:.95}}',8,-i*.55)
    icon.save('Light moves across Solidity’s folded facets; its gray-violet geometry stays stationary.')


def rust():
    icon=Icon('rust'); mark=deepcopy(paths(icon.art)[0]); icon.reset(); icon.accent('#fff1e8'); mark.set('fill','#b65e36')
    mask=node('mask',id='rust-gear-mask',maskUnits='userSpaceOnUse',x=0,y=0,width=128,height=128)
    mask.append(node('rect',width=128,height=128,fill='white')); mask.append(node('circle',cx=64,cy=64,r=53,fill='black')); icon.defs.append(mask)
    clip=node('clipPath',id='rust-letter-clip'); clip.append(node('circle',cx=64,cy=64,r=53)); icon.defs.append(clip)
    outer=node('g',mask='url(#rust-gear-mask)'); outer.append(deepcopy(mark)); icon.art.append(outer)
    icon.animate(outer,'gear','from{transform:rotate(0deg)}to{transform:rotate(360deg)}',24,easing='linear',origin='64px 64px')
    mark.set('clip-path','url(#rust-letter-clip)'); icon.art.append(mark)
    icon.save('Only Rust’s outer cog turns; the central R stays upright, with copper accents.')


def ethereum():
    icon=Icon('ethereum','0 0 24 24'); icon.reset()
    facets=[('12,0 4.6,12.2 12,8.8','#8fa7ff'),('12,0 19.4,12.2 12,8.8','#627eea'),('4.6,12.2 12,8.8 12,16.5','#536ac5'),('19.4,12.2 12,8.8 12,16.5','#344eac'),('4.6,13.7 12,18.1 12,24','#8fa7ff'),('19.4,13.7 12,18.1 12,24','#627eea')]
    for i,(points,c) in enumerate(facets):
        p=icon.shape('polygon',points=points,fill=c); icon.animate(p,f'crystal-light-{i}','0%,100%{opacity:1}45%{opacity:.7}',9,-i*.6)
    icon.save('Blue light passes across the Ethereum crystal facets; its diamond stays fixed.')


def solana():
    icon=Icon('solana','0 0 24 24'); icon.reset()
    gradient=node('linearGradient',id='solana-brand',x1=0,y1=0,x2=1,y2=1)
    gradient.append(node('stop',offset=0,stop_color='#14f195')); gradient.append(node('stop',offset=1,stop_color='#9945ff')); icon.defs.append(gradient)
    for i,points in enumerate(('4,2 23,2 19,6 0,6','0,10 19,10 23,14 4,14','4,18 23,18 19,22 0,22')):
        p=icon.shape('polygon',points=points,fill='url(#solana-brand)'); sign=1 if i!=1 else -1
        icon.animate(p,f'transaction-{i}',f'0%,15%,65%,100%{{transform:translateX(0)}}38%{{transform:translateX({sign*.6}px)}}',6,-i*.6)
    icon.save('Solana’s gradient bars slide in sequence; the middle bar moves in the opposite direction.')


def hardhat():
    icon=Icon('hardhat'); clip=node('clipPath',id='helmet-surface')
    for p in paths(icon.art)[:4]: clip.append(deepcopy(p))
    icon.defs.append(clip)
    glint=icon.shape('path',d='M36 34 Q27 54 27 77',fill='none',stroke='#fff7b3',stroke_width=3,clip_path='url(#helmet-surface)')
    icon.animate(glint,'helmet-glint','0%,100%{opacity:.3}45%{opacity:1}',7)
    icon.save('A specular glint follows Hardhat’s curved yellow helmet surface; the helmet stays still.')


def foundry():
    icon=Icon('foundry')
    tint=node('filter',id='forge-tint',color_interpolation_filters='sRGB')
    transfer=node('feComponentTransfer')
    for channel,intercept in (('R',.74),('G',.34),('B',.14)):
        transfer.append(node('feFunc'+channel,type='linear',slope=1-intercept,intercept=intercept))
    tint.append(transfer); icon.defs.append(tint)
    image=next(e for e in icon.art.iter() if tag(e)=='image'); image.set('filter','url(#forge-tint)')
    clip=node('clipPath',id='forge-flame'); clip.append(node('rect',x=76,y=122,width=35,height=44)); icon.defs.append(clip)
    fire=node('filter',id='forge-fire',color_interpolation_filters='sRGB')
    glow=node('feComponentTransfer')
    for channel,intercept in (('R',1),('G',.65),('B',.16)):
        glow.append(node('feFunc'+channel,type='linear',slope=1-intercept,intercept=intercept))
    fire.append(glow); icon.defs.append(fire)
    flame=node('g',clip_path='url(#forge-flame)'); flame_image=deepcopy(image)
    flame_image.attrib.pop('id',None)
    flame_image.set('filter','url(#forge-fire)'); flame.append(flame_image); icon.art.append(flame)
    icon.animate(flame,'flame','0%,100%{opacity:.2}22%{opacity:.8}29%{opacity:.3}48%{opacity:.9}60%{opacity:.4}81%{opacity:1}',6)
    for i in range(3):
        spark=icon.shape('path',d=f'M{84+i*8} 120 l1 -3',fill='none',stroke='#ff9900',stroke_width=2,stroke_linecap='round',**{'class':'motion-trail'})
        icon.animate(spark,f'forge-spark-{i}',f'0%,20%,80%,100%{{opacity:0;transform:translate(0,0)}}30%{{opacity:1}}60%{{opacity:0;transform:translate({(i-1)*6}px,-10px)}}',7,-i*.25)
    icon.save('The forge flame flickers and sparks rise inside Foundry’s copper-colored tools mark.')


def web3js():
    icon=Icon('web3js')
    for i,p in enumerate(paths(icon.art)): icon.animate(p,f'linked-face-{i}','0%,100%{opacity:1}45%{opacity:.6}',7,-i*.8)
    icon.save('A signal passes through Web3.js’s three linked orange and silver faces.')


def aztec():
    icon=Icon('aztec'); icon.reset()
    # Vector reconstruction of the existing purple geometric mark, with transparency.
    icon.shape('path',d='M8.3 8.3 H41.7 V25 H25 V41.7 H8.3 Z M58.3 8.3 H91.7 V41.7 H75 V25 H58.3 Z M41.7 25 H58.3 V41.7 H41.7 Z M8.3 41.7 H41.7 V91.7 H25 V58.3 H8.3 Z M58.3 41.7 H91.7 V58.3 H75 V91.7 H58.3 Z',fill='#6546d3')
    veil=icon.shape('path',d='M25 41.7 V91.7 M75 41.7 V91.7',fill='none',stroke='#b7a3f3',stroke_width=1.7,pathLength=1)
    veil.set('stroke-dasharray','.18 .82'); icon.animate(veil,'privacy-veil','from{stroke-dashoffset:1}to{stroke-dashoffset:-1}',8,easing='linear')
    icon.save('A narrow privacy veil passes through Aztec’s purple geometry; the mark remains visible throughout.')


def zksync():
    icon=Icon('zksync','100 90 500 290'); ps=paths(icon.art)[:2]; icon.reset()
    for i,p in enumerate(ps):
        p=deepcopy(p); icon.art.append(p); sign=1 if i==0 else -1
        icon.animate(p,f'rollup-arrow-{i}',f'0%,100%{{transform:translateX(0)}}45%{{transform:translateX({sign*13}px)}}',7)
    icon.save('zkSync’s purple arrows exchange a rollup signal in opposite directions, without its tiny wordmark.')


def erc4337():
    icon=Icon('erc4337','0 0 24 24'); icon.reset()
    icon.shape('rect',x=4,y=7,width=16,height=12,rx=2,fill='#627eea')
    icon.shape('rect',x=14,y=11,width=7,height=5,rx=1.5,fill='#a5b4fc'); icon.shape('circle',cx=17,cy=13.5,r=.8,fill='#fff')
    for i,x in enumerate((6,12,18)):
        icon.shape('circle',cx=x,cy=3.5,r=1.2,fill='#8b5cf6')
        route=icon.shape('path',d=f'M{x} 5 V7',fill='none',stroke='#8b5cf6',stroke_width=.65,pathLength=1); route.set('stroke-dasharray','.4 .6')
        icon.animate(route,f'user-operation-{i}','from{stroke-dashoffset:1}to{stroke-dashoffset:0}',5,-i*.65,easing='linear')
    icon.save('User-operation signals enter a smart wallet, illustrating ERC-4337 rather than repeating Ethereum’s logo.')


def metamask():
    icon=Icon('metamask'); eyes=next(p for p in paths(icon.art) if p.get('fill')=='#233447')
    icon.animate(eyes,'fox-blink','0%,40%,45%,100%{transform:scaleY(1)}42%,43%{transform:scaleY(.08)}',9,origin='159px 185px')
    icon.save('The orange MetaMask fox blinks while its ears, head and muzzle stay aligned.')


def main():
    react(); python(); badges(); aws(); github(); git(); shields(); tailwind()
    nodejs(); postgres(); vscode(); docker(); graphql(); payload(); solidity()
    rust(); ethereum(); solana(); hardhat(); foundry(); web3js(); aztec(); zksync()
    erc4337(); metamask()
    (ROOT/'scripts/icon_motion.json').write_text(json.dumps(MOTION,indent=2,ensure_ascii=False)+'\n')
    print(f'Built {len(MOTION)} individually animated, colored SVGs with reduced-motion fallbacks.')


if __name__=='__main__':
    main()
