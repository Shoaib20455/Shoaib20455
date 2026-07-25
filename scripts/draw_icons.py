"""
Creates 'drawing' animated SVGs for rows 2-5.
Uses the same stroke-dasharray technique as techstack-generator icons.
Row 1 is NOT touched.
"""
import os, re, pathlib, urllib.request

ASSETS = pathlib.Path("assets/icons")
ASSETS.mkdir(parents=True, exist_ok=True)

ROW2_TO_5 = [
    ("git",       "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/git.svg",           24),
    ("php",       "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/php/php-original.svg",   128),
    ("html",      "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg",128),
    ("css",       "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg", 128),
    ("bootstrap", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg", 128),
    ("tailwind",  "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-original.svg", 128),
    ("nodejs",    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg", 128),
    ("mongodb",   "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg", 128),
    ("postgres",  "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg", 128),
    ("vscode",    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg", 128),
    ("docker",    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg", 128),
    ("graphql",   "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/graphql/graphql-plain.svg", 128),
    ("redis",     "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original.svg", 128),
    ("polygon",   "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/polygon.svg",        24),
    ("stellar",   "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/stellar.svg",        24),
    ("payload",   "https://raw.githubusercontent.com/payloadcms/payload/main/packages/ui/src/assets/payload-favicon.svg", None),
    ("motion",    "https://motion.dev/favicon.svg", None),
    ("passenger", None, None),
    ("solidity",  "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/solidity/solidity-original.svg", 128),
    ("rust",      "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rust/rust-original.svg",  128),
    ("ethereum",  "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/ethereum.svg",        24),
    ("solana",    "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/solana.svg",          24),
    ("hardhat",   "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/hardhat/hardhat-original.svg", 128),
    ("foundry",   "https://raw.githubusercontent.com/sambacha/foundry-badge/master/foundry-logo.svg", None),
    ("web3js",    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/web3js/web3js-original.svg", 128),
    ("aztec",     None, None),
    ("zksync",    "https://raw.githubusercontent.com/matter-labs/zksync/master/zkSyncLogo.svg", None),
    ("erc4337",   "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/ethereum.svg",        24),
    ("metamask",  "https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg",       None),
    ("uniswap",   "https://upload.wikimedia.org/wikipedia/commons/e/e7/Uniswap_Logo.svg",       None),
]


def download(url, dest):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            dest.write_bytes(resp.read())
            return True
    except Exception as e:
        print(f"  WARN: {e}")
        return False


def extract_colors(svg_text):
    """Extract all unique fill colors from SVG."""
    colors = []
    seen = set()
    for m in re.finditer(r'\bfill="([^"]+)"', svg_text):
        c = m.group(1)
        if c not in ('none', 'transparent', 'currentColor', 'inherit', '') and c not in seen:
            colors.append(c)
            seen.add(c)
    return colors


def add_class_and_stroke_to_element(elem_str, fill_val):
    """Add class='draw' and stroke to an SVG element string."""
    # Add class="draw"
    if 'class="' in elem_str:
        elem_str = re.sub(r'class="([^"]*)"', r'class="\1 draw"', elem_str, count=1)
    else:
        # Insert class="draw" right after the tag name
        tag_match = re.match(r'(<\w+)', elem_str)
        if tag_match:
            insert_pos = tag_match.end()
            elem_str = elem_str[:insert_pos] + ' class="draw"' + elem_str[insert_pos:]

    # Add stroke if not present
    if 'stroke="' not in elem_str and fill_val:
        # Insert stroke before the closing > or />
        elem_str = re.sub(r'\s*(/?>)$', f' stroke="{fill_val}" \\1', elem_str, count=1)

    return elem_str


def create_drawing_svg(svg_bytes, name, size):
    """Wrap a static SVG in a 'drawing' animation using stroke-dasharray."""
    svg = svg_bytes.decode("utf-8", errors="replace")
    if "<svg" not in svg:
        return svg_bytes

    LARGE = 2000

    # Collect all unique fill colors
    colors = extract_colors(svg)

    # Map each color to its own keyframe animation name
    color_anim = {}
    for i, c in enumerate(colors):
        color_anim[c] = f"draw-{name}-{i}"

    default_anim = f"draw-{name}-default"

    # Build CSS keyframes
    keyframes_css = ""
    for c in colors:
        anim = color_anim[c]
        keyframes_css += f"""
      @keyframes {anim} {{
        0% {{ stroke-dasharray: 0 {LARGE}; stroke-dashoffset: 0; fill: {c}; }}
        50% {{ stroke-dasharray: {LARGE} {LARGE}; stroke-dashoffset: 0; fill: transparent; }}
        75%, 100% {{ stroke-dasharray: {LARGE} {LARGE}; stroke-dashoffset: 0; fill: {c}; }}
      }}"""

    keyframes_css += f"""
      @keyframes {default_anim} {{
        0% {{ stroke-dasharray: 0 {LARGE}; stroke-dashoffset: 0; }}
        50% {{ stroke-dasharray: {LARGE} {LARGE}; stroke-dashoffset: 0; fill: transparent; }}
        75%, 100% {{ stroke-dasharray: {LARGE} {LARGE}; stroke-dashoffset: 0; }}
      }}"""

    # Build color selector overrides
    color_selectors = ""
    for c in colors:
        anim = color_anim[c]
        color_selectors += f'\n    [fill="{c}"].draw {{ animation-name: {anim}; }}'

    css = f"""  <style>
    .draw {{
      fill: transparent;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
      animation: {default_anim} 3s linear infinite;
    }}{keyframes_css}{color_selectors}
  </style>"""

    # Strip existing <style> blocks
    modified = re.sub(r'<style[^>]*>.*?</style>', '', svg, flags=re.DOTALL)
    modified = re.sub(r'<defs>\s*</defs>', '', modified, flags=re.DOTALL)

    # Process each shape element
    # We need to find each element, extract its fill color, add class and stroke
    shape_tags = r'(?:path|rect|circle|ellipse|polygon|polyline)'

    def process_element(m):
        full_match = m.group(0)
        fill_m = re.search(r'\bfill="([^"]+)"', full_match)
        if fill_m:
            fill_val = fill_m.group(1)
            if fill_val in ('none', 'transparent', 'currentColor', 'inherit'):
                return full_match
        else:
            # No fill attribute - will inherit default (black), use a reasonable default
            fill_val = ""

        return add_class_and_stroke_to_element(full_match, fill_val)

    # Match elements that may span multiple lines, up to the closing > or />
    for tag in ['path', 'rect', 'circle', 'ellipse', 'polygon', 'polyline']:
        modified = re.sub(
            rf'<{tag}[^>]*/?>',
            process_element,
            modified,
            flags=re.DOTALL
        )

    # Insert CSS after opening <svg ...> tag
    svg_open = re.search(r'(<svg[^>]*>)', modified)
    if svg_open:
        insert_pos = svg_open.end()
        modified = modified[:insert_pos] + "\n" + css + "\n" + modified[insert_pos:]

    return modified.encode("utf-8")


def create_png_drawing_svg(png_path, name):
    """For PNG icons, create a scanning-line reveal SVG."""
    import base64
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="48" height="48">
  <defs>
    <clipPath id="scan-{name}">
      <rect x="0" y="0" width="100" height="0">
        <animate attributeName="height" from="0" to="100" dur="2s" fill="freeze" repeatCount="indefinite"/>
      </rect>
    </clipPath>
  </defs>
  <g clip-path="url(#scan-{name})">
    <image href="data:image/png;base64,{b64}" x="0" y="0" width="100" height="100"/>
  </g>
  <line x1="0" y1="0" x2="100" y2="0" stroke="#61dafb" stroke-width="2">
    <animate attributeName="y1" from="0" to="100" dur="2s" fill="freeze" repeatCount="indefinite"/>
    <animate attributeName="y2" from="0" to="100" dur="2s" fill="freeze" repeatCount="indefinite"/>
  </line>
</svg>'''
    return svg.encode("utf-8")


def main():
    for name, url, size in ROW2_TO_5:
        safe = re.sub(r'[^a-z0-9_\-]', '-', name.lower())
        out = ASSETS / f"{safe}-animated.svg"

        print(f"[{name}] url={'(local)' if not url else url[:70]}...")

        if url is None:
            src = ASSETS / f"{safe}-logo.png" if name in ("aztec",) else ASSETS / "passenger.png"
            if src.exists():
                data = create_png_drawing_svg(src, name)
                out.write_bytes(data)
                print(f"  -> {out.name}")
            else:
                print(f"  -> SKIP (no source)")
            continue

        temp = ASSETS / f"_temp_{safe}"
        if download(url, temp):
            if url.endswith(".png"):
                data = create_png_drawing_svg(temp, name)
            else:
                data = create_drawing_svg(temp.read_bytes(), name, size)
            out.write_bytes(data)
            temp.unlink(missing_ok=True)
            print(f"  -> {out.name}")
        else:
            print(f"  -> FAILED")

    print("\nDone! Row 1 untouched.")


if __name__ == "__main__":
    main()
