import xml.etree.ElementTree as ET
import os
import re
import json
from collections import Counter

SVG_NS = "http://www.w3.org/2000/svg"
NS = {"svg": SVG_NS}

ICONS = [
    ("polygon",     "assets/icons/_orig_polygon.svg"),
    ("stellar",     "assets/icons/_orig_stellar.svg"),
    ("solidity",    "assets/icons/_orig_solidity.svg"),
    ("rust",        "assets/icons/_orig_rust.svg"),
    ("ethereum",    "assets/icons/_orig_ethereum.svg"),
    ("solana",      "assets/icons/_orig_solana.svg"),
    ("hardhat",     "assets/icons/_orig_hardhat.svg"),
    ("web3js",      "assets/icons/_orig_web3js.svg"),
    ("foundry",     "assets/icons/_orig_foundry.svg"),
    ("zksync",      "assets/icons/_orig_zksync.svg"),
    ("metamask",    "assets/icons/_orig_metamask.svg"),
    ("uniswap",     "assets/icons/_orig_uniswap.svg"),
    ("payload",     "assets/icons/_orig_payload.svg"),
    ("motion",      "assets/icons/_orig_motion.svg"),
    ("passenger-animated", "assets/icons/passenger-animated.svg"),
    ("aztec-animated",     "assets/icons/aztec-animated.svg"),
]

def strip_ns(tag):
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag

def parse_color(val):
    if not val:
        return None
    val = val.strip()
    if val == "none":
        return "none"
    return val

def analyze_svg(filepath):
    result = {}
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError as e:
        return {"error": f"Parse error: {e}"}
    except Exception as e:
        return {"error": str(e)}

    # viewBox
    vb = root.get("viewBox") or root.get("viewbox")
    width = root.get("width", "N/A")
    height = root.get("height", "N/A")
    result["viewBox"] = vb or "none"
    result["width"] = width
    result["height"] = height

    # Check for embedded images (base64)
    images = root.findall(f".//{{{SVG_NS}}}image")
    result["embedded_images"] = len(images)
    if images:
        for i, img in enumerate(images):
            href = img.get(f"{{{SVG_NS}}}href") or img.get("href") or ""
            if href.startswith("data:"):
                mime = href.split(";")[0].replace("data:", "") if ";" in href else "unknown"
                result[f"image_{i}_type"] = mime
                result[f"image_{i}_size_hint"] = f"base64 data ({len(href)} chars)"
            else:
                result[f"image_{i}_href"] = href[:120]

    # Collect all drawable elements
    elements = []
    fill_colors = Counter()

    # Direct children shape elements
    shape_tags = ["path", "circle", "rect", "ellipse", "polygon", "polyline", "line"]
    all_elements = []
    for elem in root.iter():
        tag = strip_ns(elem.tag)
        if tag in shape_tags:
            all_elements.append((tag, elem))

    for tag, elem in all_elements:
        fill = elem.get("fill") or elem.get("style", "")
        stroke = elem.get("stroke") or ""

        # Extract fill from style attribute
        style = elem.get("style", "")
        fill_match = re.search(r'(?:^|;)\s*fill\s*:\s*([^;]+)', style)
        if fill_match:
            fill_from_style = fill_match.group(1).strip()
            if fill_from_style not in ("none", "inherit"):
                fill = fill_from_style
            elif fill_from_style == "none":
                fill = "none"

        stroke_match = re.search(r'(?:^|;)\s*stroke\s*:\s*([^;]+)', style)
        if stroke_match:
            stroke = stroke_match.group(1).strip()

        parsed_fill = parse_color(fill) if fill else "inherited/default"
        fill_colors[str(parsed_fill)] += 1

        elem_info = {"tag": tag, "fill": str(parsed_fill)}

        if tag == "path":
            d = elem.get("d", "")
            elem_info["d_length"] = len(d)
            # Rough classification by d attributes
            cmds = re.findall(r'[MmZzLlHhVvCcSsQqTtAa]', d)
            elem_info["commands"] = "".join(cmds)[:80]
        elif tag == "circle":
            elem_info["cx"] = elem.get("cx", "?")
            elem_info["cy"] = elem.get("cy", "?")
            elem_info["r"] = elem.get("r", "?")
        elif tag == "rect":
            elem_info["x"] = elem.get("x", "?")
            elem_info["y"] = elem.get("y", "?")
            elem_info["w"] = elem.get("width", "?")
            elem_info["h"] = elem.get("height", "?")
            elem_info["rx"] = elem.get("rx", "")
        elif tag == "polygon":
            pts = elem.get("points", "")
            elem_info["num_points"] = len(re.findall(r'[\d.]+', pts)) // 2
        elif tag == "ellipse":
            elem_info["cx"] = elem.get("cx", "?")
            elem_info["cy"] = elem.get("cy", "?")

        elements.append(elem_info)

    # Also count groups
    groups = sum(1 for e in root.iter() if strip_ns(e.tag) == "g")
    defs = sum(1 for e in root.iter() if strip_ns(e.tag) == "defs")

    result["total_shape_elements"] = len(elements)
    result["groups"] = groups
    result["defs_blocks"] = defs
    result["fill_colors"] = dict(fill_colors.most_common(15))
    result["elements"] = elements

    # Gradient / pattern detection
    grads = sum(1 for e in root.iter() if strip_ns(e.tag) in ("linearGradient", "radialGradient"))
    result["gradients"] = grads

    # Text elements
    texts = [e for e in root.iter() if strip_ns(e.tag) == "text"]
    result["text_elements"] = len(texts)

    return result


# Run analysis
for name, path in ICONS:
    full = os.path.join(os.getcwd(), path)
    print(f"\n{'='*70}")
    print(f"ICON: {name}")
    print(f"FILE: {path}")
    print(f"{'='*70}")

    if not os.path.exists(full):
        print("  *** FILE NOT FOUND ***")
        continue

    size = os.path.getsize(full)
    print(f"  File size: {size:,} bytes")

    info = analyze_svg(full)
    if "error" in info:
        print(f"  Error: {info['error']}")
        continue

    print(f"  viewBox: {info['viewBox']}")
    print(f"  width/height: {info['width']} x {info['height']}")
    print(f"  Groups: {info['groups']}, Defs: {info['defs_blocks']}, Gradients: {info['gradients']}")
    print(f"  Text elements: {info['text_elements']}")
    print(f"  Embedded images: {info['embedded_images']}")
    for k, v in info.items():
        if k.startswith("image_"):
            print(f"    {k}: {v}")
    print(f"  Total shape elements: {info['total_shape_elements']}")
    print(f"  Fill colors: {info['fill_colors']}")

    if info["elements"]:
        print(f"\n  --- Element Breakdown ---")
        tag_counts = Counter(e["tag"] for e in info["elements"])
        print(f"  Tag distribution: {dict(tag_counts)}")

        for i, el in enumerate(info["elements"]):
            summary = f"    [{i+1}] <{el['tag']}> fill={el['fill']}"
            if el["tag"] == "path":
                summary += f" d_cmds={el.get('commands','')[:40]} d_len={el.get('d_length',0)}"
            elif el["tag"] == "circle":
                summary += f" cx={el.get('cx')} cy={el.get('cy')} r={el.get('r')}"
            elif el["tag"] == "rect":
                summary += f" x={el.get('x')} y={el.get('y')} w={el.get('w')} h={el.get('h')}"
            elif el["tag"] == "polygon":
                summary += f" points={el.get('num_points')}"
            print(summary)
