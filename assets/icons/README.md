# Profile icons

The 27 icons shown in the profile README are standalone animated SVG images.
Rebuild them from the repository root with Python 3:

```sh
python3 scripts/animate_icons.py
```

The build is offline and deterministic. `scripts/icon_artwork.json` stores the
source geometry; `scripts/icon_motion.json` describes each icon's motion.
`scripts/draw_icons.py` is a compatibility entry point for the same generator.
Unused legacy icons are not regenerated.

Each animation targets a logo part or a route related to the technology:
React electrons follow the atom rings, Git commits follow branches, Docker
containers load onto its whale, Rust's outer teeth turn around a fixed letter,
and the MetaMask fox blinks. The SVGs contain no JavaScript or external resources.
They stop animating when `prefers-reduced-motion: reduce` is active in the SVG
document. Whether an embedded image receives that preference depends on the
browser and host page.

Multicolor logos retain their recognizable colors. Originally monochrome marks
use chosen violet or copper accents, rather than claiming official multicolor
brand variants. The ERC-4337 asset is a smart-wallet illustration, not an official
logo. The former "Multisig" label now identifies the actual MetaMask artwork.

Existing artwork comes from the repository. The JavaScript and TypeScript badge
geometry comes from [Devicon](https://github.com/devicons/devicon), under the
included [MIT license](DEVICON-LICENSE.txt). Brand marks remain the property of
their respective owners.
