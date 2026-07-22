import os, pathlib, re, time, urllib.request, urllib.error

ASSETS = pathlib.Path("assets/icons")
ASSETS.mkdir(parents=True, exist_ok=True)

# All table icons: (name, url, animation_type)
# animation_type: "pulse", "float", "fade", "spin", "bounce", "skip" (PNG/no-animatable)
ICONS = [
    # Row 1 - techstack-generator (SVG)
    ("react",       "https://techstack-generator.vercel.app/react-icon.svg",       "pulse"),
    ("python",      "https://techstack-generator.vercel.app/python-icon.svg",      "pulse"),
    ("javascript",  "https://techstack-generator.vercel.app/js-icon.svg",          "pulse"),
    ("typescript",  "https://techstack-generator.vercel.app/ts-icon.svg",          "pulse"),
    ("cpp",         "https://techstack-generator.vercel.app/cpp-icon.svg",         "float"),
    ("csharp",      "https://techstack-generator.vercel.app/csharp-icon.svg",      "float"),
    ("aws",         "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/amazonwebservices.svg", "spin"),
    ("mysql",       "https://techstack-generator.vercel.app/mysql-icon.svg",       "float"),
    ("github",      "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/github.svg", "spin"),
    # Row 2 - mix
    ("git",         "https://user-images.githubusercontent.com/25181517/192108372-f71d70ac-7ae6-4c0d-8395-51d8870c2ef0.png", "skip"),
    ("php",         "https://skillicons.dev/icons?i=php",         "float"),
    ("html",        "https://skillicons.dev/icons?i=html",        "fade"),
    ("css",         "https://skillicons.dev/icons?i=css",         "fade"),
    ("bootstrap",   "https://skillicons.dev/icons?i=bootstrap",   "float"),
    ("tailwind",    "https://skillicons.dev/icons?i=tailwind",    "float"),
    ("nodejs",      "https://skillicons.dev/icons?i=nodejs",      "pulse"),
    ("mongodb",     "https://skillicons.dev/icons?i=mongodb",     "float"),
    ("postgres",    "https://skillicons.dev/icons?i=postgres",    "float"),
    # Row 3
    ("vscode",      "https://skillicons.dev/icons?i=vscode",      "float"),
    ("docker",      "https://skillicons.dev/icons?i=docker",      "bounce"),
    ("graphql",     "https://skillicons.dev/icons?i=graphql",     "pulse"),
    ("redis",       "https://skillicons.dev/icons?i=redis",       "float"),
    ("polygon",     "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/polygon.svg", "pulse"),
    ("stellar",     "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/stellar.svg", "spin"),
    ("payload",     "https://raw.githubusercontent.com/payloadcms/payload/main/packages/ui/src/assets/payload-favicon.svg", "float"),
    ("motion",      "assets/icons/motion-favicon.svg", "pulse"),  # already local
    ("passenger",   None, "skip"),  # PNG, already local
    # Row 4
    ("solidity",    "https://skillicons.dev/icons?i=solidity",    "pulse"),
    ("rust",        "https://skillicons.dev/icons?i=rust",        "float"),
    ("ethereum",    "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/ethereum.svg", "pulse"),
    ("solana",      "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/solana.svg", "spin"),
    ("hardhat",     "assets/icons/hardhat.svg", "bounce"),  # already local
    ("foundry",     "https://raw.githubusercontent.com/sambacha/foundry-badge/master/foundry-logo.svg", "float"),
    ("web3js",      "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/web3js/web3js-original.svg", "pulse"),
    ("aztec",       None, "skip"),  # PNG, already local
    ("zksync",      "https://raw.githubusercontent.com/matter-labs/zksync/master/zkSyncLogo.svg", "spin"),
    # Row 5
    ("erc4337",     "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/ethereum.svg", "pulse"),
    ("metamask",    "https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg", "bounce"),
    ("uniswap",     "https://upload.wikimedia.org/wikipedia/commons/e/e7/Uniswap_Logo.svg", "spin"),
]

ANIMATIONS = {
    "pulse": """
  <animateTransform attributeName="transform" type="scale" values="1;1.15;1" dur="2s" repeatCount="indefinite" additive="sum"/>
""",
    "float": """
  <animateTransform attributeName="transform" type="translate" values="0,0;0,-3;0,0" dur="2.5s" repeatCount="indefinite" additive="sum"/>
""",
    "fade": """
  <animate attributeName="opacity" values="1;0.5;1" dur="3s" repeatCount="indefinite"/>
""",
    "spin": """
  <animateTransform attributeName="transform" type="rotate" values="0 24 24;360 24 24" dur="8s" repeatCount="indefinite" additive="sum"/>
""",
    "bounce": """
  <animateTransform attributeName="transform" type="translate" values="0,0;0,-5;0,0" dur="1s" repeatCount="indefinite" additive="sum"/>
""",
}

def download(url, dest):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            dest.write_bytes(data)
            return True
    except Exception as e:
        print(f"  WARN: {e}")
        return False

def add_smil_animation(svg_bytes, anim_type):
    """Insert SMIL <g> wrapper with animation into SVG content."""
    svg = svg_bytes.decode("utf-8", errors="replace")

    # Skip if already animated or not valid SVG
    if "<svg" not in svg:
        return svg_bytes

    anim = ANIMATIONS.get(anim_type)
    if not anim:
        return svg_bytes

    # Find the opening <svg ...> tag and extract viewBox or dimensions
    # Strategy: wrap everything after <svg> in a <g> with animation
    # Insert <g> right after the opening <svg ...> tag
    match = re.search(r'(<svg[^>]*>)', svg)
    if not match:
        return svg_bytes

    svg_open = match.group(1)
    rest = svg[match.end():]
    # Remove closing </svg> if present
    rest = re.sub(r'</svg>\s*$', '', rest).rstrip()

    # Build animated SVG
    animated = f"""{svg_open}
  <g>{anim}    {rest}
  </g>
</svg>"""

    return animated.encode("utf-8")


def main():
    readme_map = {}  # name -> local path for README update

    for name, url, anim_type in ICONS:
        safe_name = re.sub(r'[^a-z0-9_\-]', '-', name.lower())
        is_png = url and url.endswith(".png") if url else False
        ext = "png" if is_png else "svg"
        local_path = ASSETS / f"{safe_name}-animated.{ext}"

        print(f"[{name}] anim={anim_type} url={'(local)' if not url else url[:60]}...")

        if anim_type == "skip":
            # Just ensure the existing local file is referenced properly
            existing = list(ASSETS.glob(f"{safe_name}*"))
            if existing:
                readme_map[name] = str(existing[0].as_posix())
                print(f"  -> using existing {existing[0]}")
            else:
                print(f"  -> SKIP (no local file)")
            continue

        if not url:
            print(f"  -> SKIP (no URL)")
            continue

        # Check if url is a local path
        if url.startswith("assets/"):
            src = pathlib.Path(url)
            if src.exists():
                svg_data = src.read_bytes()
                if anim_type != "skip" and ext == "svg":
                    svg_data = add_smil_animation(svg_data, anim_type)
                local_path.write_bytes(svg_data)
                readme_map[name] = str(local_path.as_posix())
                print(f"  -> animated local -> {local_path}")
            continue

        # Download
        if download(url, local_path):
            if ext == "svg":
                svg_data = local_path.read_bytes()
                svg_data = add_smil_animation(svg_data, anim_type)
                local_path.write_bytes(svg_data)
            readme_map[name] = str(local_path.as_posix())
            print(f"  -> saved + animated -> {local_path}")
        else:
            print(f"  -> FAILED to download")

    # Print mapping for manual README update
    print("\n\n=== README MAPPING ===")
    for name, path in readme_map.items():
        print(f"{name}: {path}")

    return readme_map


if __name__ == "__main__":
    main()
