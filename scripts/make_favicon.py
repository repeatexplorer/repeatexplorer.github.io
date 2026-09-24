#!/usr/bin/env python3
"""Generate the favicon set from the site's own typeface.

The mark is RE in Space Grotesk Bold, the same face as the wordmark. Letters
are converted to outlines: a favicon cannot rely on a font being installed on
the reader's machine.

Needs fontTools and brotli, and Inkscape or ImageMagick to rasterise. These are
one-off asset tools, deliberately not in environment.yml, which is for building
the site. Run only when the mark changes.
"""
import pathlib, subprocess, sys

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT = ROOT / 'assets' / 'fonts' / 'space-grotesk-var.woff2'
STATIC = ROOT / 'static'

GROUND = '#C6F24E'   # --accent: bright, so the tab is findable on light and dark
INK = '#101311'      # --ink
BOX = 64             # SVG user units; the icon is square
RADIUS = 14


def glyph_paths(text, weight=700):
    font = TTFont(FONT)
    font = instancer.instantiateVariableFont(font, {'wght': weight})
    glyphset = font.getGlyphSet()
    cmap = font.getBestCmap()
    upem = font['head'].unitsPerEm
    out, advance = [], 0
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(glyphset)
        glyphset[name].draw(pen)
        out.append((pen.getCommands(), advance))
        advance += glyphset[name].width
    return out, advance, upem


def main():
    paths, total_advance, upem = glyph_paths('RE')

    # fit the two glyphs into the box with a margin, cap height not em box:
    # the em includes descender space the letters do not use
    margin = 7
    inner = BOX - 2 * margin
    scale = inner / total_advance
    cap = 700 * scale                      # Space Grotesk cap height, in units
    x0 = margin
    y0 = (BOX + cap) / 2                   # baseline, so the letters sit optically centred

    glyphs = '\n'.join(
        f'    <path d="{d}" transform="translate({x0 + adv * scale:.2f} {y0:.2f}) '
        f'scale({scale:.5f} {-scale:.5f})"/>'
        for d, adv in paths)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BOX} {BOX}" width="{BOX}" height="{BOX}" role="img" aria-label="RepeatExplorer">
  <rect width="{BOX}" height="{BOX}" rx="{RADIUS}" fill="{GROUND}"/>
  <g fill="{INK}">
{glyphs}
  </g>
</svg>
'''
    STATIC.mkdir(exist_ok=True)
    (STATIC / 'favicon.svg').write_text(svg)
    print(f'  favicon.svg          {len(svg)} bytes')

    # raster fallbacks: Safari and older browsers ignore SVG favicons
    for name, size in [('favicon-32.png', 32), ('favicon-180.png', 180)]:
        subprocess.run(['inkscape', str(STATIC / 'favicon.svg'),
                        f'--export-width={size}', f'--export-height={size}',
                        f'--export-filename={STATIC / name}'],
                       check=True, capture_output=True)
        print(f'  {name:20s} {(STATIC / name).stat().st_size} bytes')

    subprocess.run(['convert', str(STATIC / 'favicon-32.png'),
                    '-define', 'icon:auto-resize=32,16', str(STATIC / 'favicon.ico')],
                   check=True, capture_output=True)
    print(f'  favicon.ico          {(STATIC / "favicon.ico").stat().st_size} bytes')


if __name__ == '__main__':
    main()
