"""
Creates unique element-by-element animations for each icon.
Each icon gets a custom animation that matches its identity.

Row 1 is NEVER touched.
"""
import pathlib, re

ASSETS = pathlib.Path("assets/icons")
ORIG = pathlib.Path("assets/icons")

def read_orig(name):
    return (ORIG / f"_orig_{name}.svg").read_text(encoding="utf-8", errors="replace")

def write_anim(name, content):
    out = ASSETS / f"{name}-animated.svg"
    out.write_text(content, encoding="utf-8")
    print(f"  {name}: {len(content)} bytes")


# ── ROW 2 ──────────────────────────────────────────────────────────

def anim_git():
    """Git: Draw the branch lines, then pulse the center node."""
    svg = read_orig("git")
    svg = svg.replace('xmlns="http://www.w3.org/2000/svg"',
                       'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"')
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes draw-branch {
      0% { stroke-dasharray: 0 1000; stroke-dashoffset: 0; opacity: 1; }
      40% { stroke-dasharray: 1000 0; stroke-dashoffset: 0; opacity: 1; }
      60% { stroke-dasharray: 1000 0; stroke-dashoffset: 0; opacity: 1; }
      100% { stroke-dasharray: 1000 0; stroke-dashoffset: 0; opacity: 1; }
    }
    @keyframes pulse-dot {
      0%, 40% { transform: scale(0); opacity: 0; }
      50% { transform: scale(1.4); opacity: 1; }
      60%, 100% { transform: scale(1); opacity: 1; }
    }
    #git-path {
      fill: none;
      stroke: currentColor;
      stroke-width: 1.5;
      stroke-linecap: round;
      stroke-linejoin: round;
      animation: draw-branch 3s ease-in-out infinite;
    }
    #git-dot {
      fill: currentColor;
      transform-origin: 12.19px 13.09px;
      animation: pulse-dot 3s ease-in-out infinite;
    }
  </style>
  <path id="git-path" d="M13.09 23.549a1.54 1.54 0 0 1-2.18 0L.451 13.089a1.54 1.54 0 0 1 0-2.179l7.191-7.19 2.733 2.733a1.85 1.85 0 0 0 .964 2.326v6.66a1.849 1.849 0 1 0 1.54 0V8.957l2.508 2.508a1.85 1.85 0 1 0 1.09-1.09l-2.634-2.634a1.85 1.85 0 0 0-2.378-2.377L8.73 2.63 10.91.451a1.54 1.54 0 0 1 2.179 0l10.459 10.46a1.54 1.54 0 0 1 0 2.179z"/>
  <circle id="git-dot" cx="12.19" cy="13.09" r="2.5"/>
</svg>""")
    write_anim("git", anim_svg)


def anim_php():
    """PHP: Elephant body rocks gently, tail wags."""
    svg = read_orig("php")
    # Wrap in a group and add a gentle rocking SMIL animation
    svg = svg.replace("<svg ", '<svg id="php-root" ')
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes php-rock {
      0%, 100% { transform: rotate(0deg); }
      25% { transform: rotate(-1.5deg); }
      75% { transform: rotate(1.5deg); }
    }
    #php-root {
      animation: php-rock 4s ease-in-out infinite;
      transform-origin: 64px 64px;
    }
  </style>
</svg>""")
    write_anim("php", anim_svg)


def anim_html():
    """HTML: Shield with light sweep effect."""
    svg = read_orig("html")
    # Add a light sweep overlay using a mask + animated gradient
    anim_svg = svg.replace("</svg>", """
  <defs>
    <linearGradient id="html-sweep" x1="-0.5" y1="0" x2="0.5" y2="0">
      <stop offset="0" stop-color="white" stop-opacity="0"/>
      <stop offset="0.4" stop-color="white" stop-opacity="0.35"/>
      <stop offset="0.5" stop-color="white" stop-opacity="0.5"/>
      <stop offset="0.6" stop-color="white" stop-opacity="0.35"/>
      <stop offset="1" stop-color="white" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate"
        values="-1 0; 2 0" dur="3s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="128" height="128" fill="url(#html-sweep)" style="mix-blend-mode:overlay;pointer-events:none"/>
</svg>""")
    write_anim("html", anim_svg)


def anim_css():
    """CSS: Shield with blue light sweep."""
    svg = read_orig("css")
    anim_svg = svg.replace("</svg>", """
  <defs>
    <linearGradient id="css-sweep" x1="-0.5" y1="0" x2="0.5" y2="0">
      <stop offset="0" stop-color="#33A9DC" stop-opacity="0"/>
      <stop offset="0.4" stop-color="#33A9DC" stop-opacity="0.2"/>
      <stop offset="0.5" stop-color="#33A9DC" stop-opacity="0.4"/>
      <stop offset="0.6" stop-color="#33A9DC" stop-opacity="0.2"/>
      <stop offset="1" stop-color="#33A9DC" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate"
        values="-1 0; 2 0" dur="3.5s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="128" height="128" fill="url(#css-sweep)" style="pointer-events:none"/>
</svg>""")
    write_anim("css", anim_svg)


def anim_bootstrap():
    """Bootstrap: The B bounces with a spring effect."""
    svg = read_orig("bootstrap")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes bs-bounce {
      0%, 100% { transform: translateY(0); }
      15% { transform: translateY(-6px); }
      30% { transform: translateY(0); }
      45% { transform: translateY(-3px); }
      60% { transform: translateY(0); }
    }
    svg { animation: bs-bounce 3s ease-in-out infinite; transform-origin: center; }
  </style>
</svg>""")
    write_anim("bootstrap", anim_svg)


def anim_tailwind():
    """Tailwind: Wind waves pulse and shift."""
    svg = read_orig("tailwind")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes tw-shift {
      0%, 100% { transform: translateX(0) scale(1); }
      50% { transform: translateX(3px) scale(1.02); }
    }
    svg path { animation: tw-shift 2.5s ease-in-out infinite; transform-origin: 64px 64px; }
  </style>
</svg>""")
    write_anim("tailwind", anim_svg)


def anim_nodejs():
    """Node.js: Hexagonal breathe pulse."""
    svg = read_orig("nodejs")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes node-breathe {
      0%, 100% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.03); opacity: 0.9; }
    }
    svg { animation: node-breathe 3s ease-in-out infinite; transform-origin: 64px 64px; }
  </style>
</svg>""")
    write_anim("nodejs", anim_svg)


def anim_mongodb():
    """MongoDB: Leaf grows - each path fades in with stagger."""
    svg = read_orig("mongodb")
    # Add staggered opacity animations to each of the 7 paths
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes mongo-grow {
      0% { opacity: 0; transform: translateY(8px) scale(0.95); }
      60% { opacity: 1; transform: translateY(-2px) scale(1.01); }
      100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    svg path:nth-child(1) { animation: mongo-grow 2.5s ease-out 0s infinite; }
    svg path:nth-child(2) { animation: mongo-grow 2.5s ease-out 0.15s infinite; }
    svg path:nth-child(3) { animation: mongo-grow 2.5s ease-out 0.3s infinite; }
    svg path:nth-child(4) { animation: mongo-grow 2.5s ease-out 0.45s infinite; }
    svg path:nth-child(5) { animation: mongo-grow 2.5s ease-out 0.6s infinite; }
    svg path:nth-child(6) { animation: mongo-grow 2.5s ease-out 0.75s infinite; }
    svg path:nth-child(7) { animation: mongo-grow 2.5s ease-out 0.9s infinite; }
  </style>
</svg>""")
    write_anim("mongodb", anim_svg)


def anim_postgres():
    """PostgreSQL: Elephant head bobs gently."""
    svg = read_orig("postgres")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes pg-bob {
      0%, 100% { transform: translateY(0) rotate(0deg); }
      30% { transform: translateY(-2px) rotate(-0.5deg); }
      70% { transform: translateY(1px) rotate(0.3deg); }
    }
    svg path:first-child { animation: pg-bob 4s ease-in-out infinite; transform-origin: center; }
    svg path:last-child { animation: pg-bob 4s ease-in-out 0.5s infinite; transform-origin: center; }
  </style>
</svg>""")
    write_anim("postgres", anim_svg)


def anim_vscode():
    """VS Code: Editor ribbon waves like a flag."""
    svg = read_orig("vscode")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes vscode-wave {
      0%, 100% { transform: skewX(0deg) translateX(0); }
      25% { transform: skewX(0.5deg) translateX(1px); }
      75% { transform: skewX(-0.5deg) translateX(-1px); }
    }
    svg > g { animation: vscode-wave 3s ease-in-out infinite; transform-origin: center; }
  </style>
</svg>""")
    write_anim("vscode", anim_svg)


def anim_docker():
    """Docker: Whale bobs on waves, containers slide down into whale."""
    svg = read_orig("docker")
    # The first path is the container grid, rest is the whale body
    # Add bobbing animation to whale body, containers fade in
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes docker-bob {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-3px); }
    }
    @keyframes docker-containers {
      0% { opacity: 0; transform: translateY(-8px); }
      30% { opacity: 1; transform: translateY(0); }
      100% { opacity: 1; transform: translateY(0); }
    }
    /* whale body paths (indices 2-5) bob */
    svg path:nth-child(2), svg path:nth-child(3),
    svg path:nth-child(4), svg path:nth-child(5) {
      animation: docker-bob 3s ease-in-out infinite;
    }
    /* container grid fades in */
    svg path:nth-child(6) {
      animation: docker-containers 3s ease-out infinite;
      transform-origin: 40px 50px;
    }
  </style>
</svg>""")
    write_anim("docker", anim_svg)


def anim_graphql():
    """GraphQL: Nodes light up in circular sequence, edges draw in."""
    svg = read_orig("graphql")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes gql-node-pulse {
      0% { opacity: 0.3; transform: scale(0.8); }
      15% { opacity: 1; transform: scale(1.2); }
      30% { opacity: 0.3; transform: scale(0.8); }
      100% { opacity: 0.3; transform: scale(0.8); }
    }
    @keyframes gql-edge-draw {
      0% { stroke-dasharray: 0 200; stroke-dashoffset: 0; }
      30% { stroke-dasharray: 200 0; stroke-dashoffset: 0; }
      100% { stroke-dasharray: 200 0; stroke-dashoffset: 0; }
    }
    /* vertex dots (last 4 small paths) pulse in sequence */
    svg g path:nth-child(9) { animation: gql-node-pulse 3s ease-in-out 0s infinite; }
    svg g path:nth-child(10) { animation: gql-node-pulse 3s ease-in-out 0.3s infinite; }
    svg g path:nth-child(11) { animation: gql-node-pulse 3s ease-in-out 0.6s infinite; }
    svg g path:nth-child(12) { animation: gql-node-pulse 3s ease-in-out 0.9s infinite; }
    /* hexagon body pulses */
    svg g path:nth-child(6) { animation: gql-node-pulse 3s ease-in-out 1.2s infinite; }
    /* edge lines draw in */
    svg g path:nth-child(1), svg g path:nth-child(2),
    svg g path:nth-child(3), svg g path:nth-child(4),
    svg g path:nth-child(5), svg g path:nth-child(7),
    svg g path:nth-child(8) {
      fill: none;
      stroke: #E434AA;
      stroke-width: 2;
      animation: gql-edge-draw 3s ease-in-out infinite;
    }
  </style>
</svg>""")
    write_anim("graphql", anim_svg)


def anim_redis():
    """Redis: Star twinkles, layers bounce up from bottom."""
    svg = read_orig("redis")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes redis-layer {
      0% { transform: translateY(6px); opacity: 0.5; }
      30% { transform: translateY(-1px); opacity: 1; }
      100% { transform: translateY(0); opacity: 1; }
    }
    @keyframes redis-star {
      0%, 100% { transform: scale(1) rotate(0deg); opacity: 1; }
      50% { transform: scale(1.15) rotate(15deg); opacity: 0.8; }
    }
    /* database layers bounce up from bottom with stagger */
    svg path:nth-child(1) { animation: redis-layer 2.5s ease-out 0s infinite; }
    svg path:nth-child(2) { animation: redis-layer 2.5s ease-out 0.1s infinite; }
    svg path:nth-child(3) { animation: redis-layer 2.5s ease-out 0.2s infinite; }
    svg path:nth-child(4) { animation: redis-layer 2.5s ease-out 0.3s infinite; }
    svg path:nth-child(5) { animation: redis-layer 2.5s ease-out 0.4s infinite; }
    svg path:nth-child(6) { animation: redis-layer 2.5s ease-out 0.5s infinite; }
    /* white star twinkles */
    svg path:nth-child(7) {
      animation: redis-star 2s ease-in-out infinite;
      transform-origin: 62px 28px;
    }
    /* bottom decoration paths */
    svg path:nth-child(8), svg path:nth-child(9),
    svg path:nth-child(10), svg path:nth-child(11) {
      animation: redis-layer 2.5s ease-out 0.6s infinite;
    }
  </style>
</svg>""")
    write_anim("redis", anim_svg)


# ── ROW 3 ──────────────────────────────────────────────────────────

def anim_polygon():
    """Polygon: Draw the interlocking hexagons, then subtle rotate."""
    svg = read_orig("polygon")
    svg = svg.replace('xmlns="http://www.w3.org/2000/svg"',
                       'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"')
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes poly-draw {
      0% { stroke-dasharray: 0 400; stroke-dashoffset: 0; fill: transparent; }
      50% { stroke-dasharray: 400 0; stroke-dashoffset: 0; fill: transparent; }
      75%, 100% { stroke-dasharray: 400 0; stroke-dashoffset: 0; fill: currentColor; }
    }
    svg path {
      fill: transparent;
      stroke: currentColor;
      stroke-width: 0.5;
      animation: poly-draw 3.5s ease-in-out infinite;
    }
  </style>
</svg>""")
    write_anim("polygon", anim_svg)


def anim_stellar():
    """Stellar: Orbital swooshes draw in, creating orbital motion."""
    svg = read_orig("stellar")
    svg = svg.replace('xmlns="http://www.w3.org/2000/svg"',
                       'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"')
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes stellar-orbit {
      0% { stroke-dasharray: 0 600; stroke-dashoffset: 0; fill: transparent; }
      45% { stroke-dasharray: 600 0; stroke-dashoffset: 0; fill: transparent; }
      70%, 100% { stroke-dasharray: 600 0; stroke-dashoffset: 0; fill: currentColor; }
    }
    svg path {
      fill: transparent;
      stroke: currentColor;
      stroke-width: 0.3;
      animation: stellar-orbit 4s ease-in-out infinite;
    }
  </style>
</svg>""")
    write_anim("stellar", anim_svg)


def anim_payload():
    """Payload: 3D cube tumbles - two faces shift to create rotation."""
    svg = read_orig("payload")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes payload-tumble {
      0%, 100% { transform: rotate(0deg) scale(1); }
      25% { transform: rotate(2deg) scale(1.02); }
      50% { transform: rotate(0deg) scale(1); }
      75% { transform: rotate(-2deg) scale(0.98); }
    }
    svg path:first-child {
      animation: payload-tumble 4s ease-in-out infinite;
      transform-origin: 51.2px 51.2px;
    }
    svg path:last-child {
      animation: payload-tumble 4s ease-in-out 0.15s infinite;
      transform-origin: 51.2px 51.2px;
    }
  </style>
</svg>""")
    write_anim("payload", anim_svg)


def anim_motion():
    """Motion: M letter strokes assemble from different directions."""
    svg = read_orig("motion")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes motion-assemble {
      0% { opacity: 0; transform: translateY(12px); }
      40% { opacity: 1; transform: translateY(-2px); }
      60%, 100% { opacity: 1; transform: translateY(0); }
    }
    svg g path {
      animation: motion-assemble 2.5s ease-out infinite;
      transform-origin: center;
    }
  </style>
</svg>""")
    write_anim("motion", anim_svg)


def anim_passenger():
    """Passenger: Already has scan-line animation from PNG wrapper. Keep it."""
    pass  # Already handled by draw_icons.py


# ── ROW 4 ──────────────────────────────────────────────────────────

def anim_solidity():
    """Solidity: Light reflection sweeps across the 6 diamond facets."""
    svg = read_orig("solidity")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes sol-facet-1 { 0%,100% { opacity: 0.45; } 30% { opacity: 1; } 60% { opacity: 0.45; } }
    @keyframes sol-facet-2 { 0%,100% { opacity: 0.6; } 40% { opacity: 1; } 70% { opacity: 0.6; } }
    @keyframes sol-facet-3 { 0%,100% { opacity: 0.8; } 50% { opacity: 1; } 80% { opacity: 0.8; } }
    svg path:nth-child(1) { animation: sol-facet-1 3s ease-in-out 0s infinite; }
    svg path:nth-child(2) { animation: sol-facet-2 3s ease-in-out 0.15s infinite; }
    svg path:nth-child(3) { animation: sol-facet-3 3s ease-in-out 0.3s infinite; }
    svg path:nth-child(4) { animation: sol-facet-1 3s ease-in-out 0.5s infinite; }
    svg path:nth-child(5) { animation: sol-facet-2 3s ease-in-out 0.65s infinite; }
    svg path:nth-child(6) { animation: sol-facet-3 3s ease-in-out 0.8s infinite; }
  </style>
</svg>""")
    write_anim("solidity", anim_svg)


def anim_rust():
    """Rust: Gear rotates slowly clockwise."""
    svg = read_orig("rust")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes rust-spin {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    svg path { animation: rust-spin 8s linear infinite; transform-origin: 64px 64px; }
  </style>
</svg>""")
    write_anim("rust", anim_svg)


def anim_ethereum():
    """Ethereum: Diamond splits vertically then snaps back."""
    svg = read_orig("ethereum")
    svg = svg.replace('xmlns="http://www.w3.org/2000/svg"',
                       'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"')
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes eth-split {
      0%, 100% { transform: translateY(0); }
      30% { transform: translateY(-2px); }
      50% { transform: translateY(0); }
    }
    svg path {
      animation: eth-split 3s ease-in-out infinite;
      transform-origin: 12px 12px;
    }
  </style>
  <animateTransform attributeName="transform" type="translate" values="0,0;0,-1.5;0,0" dur="3s" repeatCount="indefinite"/>
</svg>""")
    write_anim("ethereum", anim_svg)


def anim_solana():
    """Solana: Three parallel bars cascade in from left."""
    svg = read_orig("solana")
    svg = svg.replace('xmlns="http://www.w3.org/2000/svg"',
                       'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"')
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes sol-cascade {
      0% { transform: translateX(-8px); opacity: 0; }
      40% { transform: translateX(1px); opacity: 1; }
      60%, 100% { transform: translateX(0); opacity: 1; }
    }
    svg path {
      animation: sol-cascade 3s ease-in-out infinite;
    }
  </style>
</svg>""")
    write_anim("solana", anim_svg)


def anim_hardhat():
    """Hardhat: Construction hat bobs up and down like nodding."""
    svg = read_orig("hardhat")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes hh-nod {
      0%, 100% { transform: translateY(0) rotate(0deg); }
      20% { transform: translateY(-4px) rotate(-1deg); }
      40% { transform: translateY(0) rotate(0deg); }
      60% { transform: translateY(-2px) rotate(0.5deg); }
      80% { transform: translateY(0) rotate(0deg); }
    }
    svg > path, svg > g > path {
      animation: hh-nod 3.5s ease-in-out infinite;
      transform-origin: 64px 80px;
    }
  </style>
</svg>""")
    write_anim("hardhat", anim_svg)


def anim_foundry():
    """Foundry: PNG bitmap - add a glowing forge effect."""
    svg = read_orig("foundry")
    anim_svg = svg.replace("</svg>", """
  <defs>
    <filter id="forge-glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="1 0 0 0 0.1  0 0.5 0 0 0  0 0 0.2 0 0  0 0 0 0.6 0" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <style>
    @keyframes forge-pulse {
      0%, 100% { filter: none; opacity: 1; }
      50% { filter: url(#forge-glow); opacity: 0.95; }
    }
    svg { animation: forge-pulse 2.5s ease-in-out infinite; }
  </style>
</svg>""")
    write_anim("foundry", anim_svg)


def anim_web3js():
    """Web3.js: Isometric cube faces glow in sequence."""
    svg = read_orig("web3js")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes w3-face-glow {
      0%, 100% { opacity: 1; filter: none; }
      33% { opacity: 1; filter: brightness(1.4); }
      66% { opacity: 1; filter: none; }
    }
    svg path:nth-child(1) { animation: w3-face-glow 3s ease-in-out 0s infinite; }
    svg path:nth-child(2) { animation: w3-face-glow 3s ease-in-out 1s infinite; }
    svg path:nth-child(3) { animation: w3-face-glow 3s ease-in-out 2s infinite; }
  </style>
</svg>""")
    write_anim("web3js", anim_svg)


# ── ROW 5 ──────────────────────────────────────────────────────────

def anim_aztec():
    """Aztec: Already has scan-line animation from PNG wrapper. Keep it."""
    pass  # Already handled by draw_icons.py


def anim_zksync():
    """ZKSync: Chevrons rotate in, letters reveal left-to-right."""
    svg = read_orig("zksync")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes zks-chevron-in {
      0% { opacity: 0; transform: rotate(-30deg) scale(0.5); }
      40% { opacity: 1; transform: rotate(5deg) scale(1.05); }
      60%, 100% { opacity: 1; transform: rotate(0deg) scale(1); }
    }
    @keyframes zks-letter-in {
      0% { opacity: 0; transform: translateY(8px); }
      50% { opacity: 1; transform: translateY(-2px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    /* chevron marks */
    svg > path:nth-child(2) {
      animation: zks-chevron-in 2s ease-out 0s infinite;
      transform-origin: 450px 230px;
    }
    svg > path:nth-child(3) {
      animation: zks-chevron-in 2s ease-out 0.3s infinite;
      transform-origin: 245px 230px;
    }
    /* letters fade in with stagger */
    svg > path:nth-child(4) { animation: zks-letter-in 2s ease-out 0.6s infinite; }
    svg > path:nth-child(5) { animation: zks-letter-in 2s ease-out 0.8s infinite; }
    svg > path:nth-child(6) { animation: zks-letter-in 2s ease-out 1.0s infinite; }
    svg > path:nth-child(7) { animation: zks-letter-in 2s ease-out 1.2s infinite; }
    svg > path:nth-child(8) { animation: zks-letter-in 2s ease-out 1.4s infinite; }
    svg > path:nth-child(9) { animation: zks-letter-in 2s ease-out 1.6s infinite; }
    svg > path:nth-child(10) { animation: zks-letter-in 2s ease-out 1.8s infinite; }
    /* hide white background rect during animation */
    svg > rect { opacity: 0; }
  </style>
</svg>""")
    write_anim("zksync", anim_svg)


def anim_erc4337():
    """ERC-4337: Diamond pulses with a gentle breathing glow."""
    svg = read_orig("ethereum")  # Same base as ethereum
    svg = svg.replace('xmlns="http://www.w3.org/2000/svg"',
                       'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"')
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes erc-breathe {
      0%, 100% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.08); opacity: 0.85; }
    }
    svg path {
      animation: erc-breathe 2.5s ease-in-out infinite;
      transform-origin: 12px 12px;
    }
  </style>
</svg>""")
    write_anim("erc4337", anim_svg)


def anim_metamask():
    """MetaMask: Fox eyes blink, subtle head movement."""
    svg = read_orig("metamask")
    anim_svg = svg.replace("</svg>", """
  <style>
    @keyframes mm-blink {
      0%, 42%, 58%, 100% { transform: scaleY(1); }
      48%, 52% { transform: scaleY(0.05); }
    }
    @keyframes mm-head {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-1.5px); }
    }
    /* eye paths (#233447) - index 6 */
    svg > path:nth-child(6) {
      animation: mm-blink 4s ease-in-out infinite;
      transform-origin: 159px 193px;
    }
    /* subtle head bob on the main orange body */
    svg > path:nth-child(1) {
      animation: mm-head 4s ease-in-out infinite;
    }
    svg > path:nth-child(2) {
      animation: mm-head 4s ease-in-out 0.05s infinite;
    }
  </style>
</svg>""")
    write_anim("metamask", anim_svg)


def anim_uniswap():
    """Uniswap: Unicorn logo bounces, horn sparkles."""
    svg = read_orig("uniswap")
    anim_svg = svg.replace("</svg>", """
  <defs>
    <filter id="uni-glow">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="1 0 0 0 0  0 0 0 0 0.48  0 0 0 0 0  0 0 0 0.8 0" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <style>
    @keyframes uni-bounce {
      0%, 100% { transform: translateY(0) scale(1); }
      25% { transform: translateY(-8px) scale(1.01); }
      50% { transform: translateY(0) scale(1); }
      75% { transform: translateY(-3px) scale(1); }
    }
    @keyframes uni-horn-sparkle {
      0%, 70%, 100% { filter: none; opacity: 1; }
      85% { filter: url(#uni-glow); opacity: 1; }
    }
    /* Main unicorn body bounces */
    svg path:nth-child(8) {
      animation: uni-bounce 3s ease-in-out infinite;
      transform-origin: center;
    }
    /* Horn path (path 1 is the horn/head area) sparkles */
    svg path:nth-child(1) {
      animation: uni-horn-sparkle 3s ease-in-out infinite;
    }
    /* Eye blinks */
    svg path:nth-child(9) {
      animation: mm-blink 4s ease-in-out infinite;
      transform-origin: 265px 276px;
    }
    @keyframes mm-blink {
      0%, 42%, 58%, 100% { transform: scaleY(1); }
      48%, 52% { transform: scaleY(0.05); }
    }
  </style>
</svg>""")
    write_anim("uniswap", anim_svg)


# ── MAIN ───────────────────────────────────────────────────────────

def main():
    print("=== Row 2 ===")
    anim_git()
    anim_php()
    anim_html()
    anim_css()
    anim_bootstrap()
    anim_tailwind()
    anim_nodejs()
    anim_mongodb()
    anim_postgres()
    anim_vscode()
    anim_docker()
    anim_graphql()
    anim_redis()

    print("\n=== Row 3 ===")
    anim_polygon()
    anim_stellar()
    anim_payload()
    anim_motion()
    # passenger: keep existing scan animation

    print("\n=== Row 4 ===")
    anim_solidity()
    anim_rust()
    anim_ethereum()
    anim_solana()
    anim_hardhat()
    anim_foundry()
    anim_web3js()

    print("\n=== Row 5 ===")
    # aztec: keep existing scan animation
    anim_zksync()
    anim_erc4337()
    anim_metamask()
    anim_uniswap()

    print("\nDone! Row 1 untouched.")


if __name__ == "__main__":
    main()
