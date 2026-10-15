"""Draws the product pictures as SVG, so no image files are needed.

Each garment is shaded like a studio product photo: soft light, fabric
texture, folds, stitching, ribbed cuffs and a floor shadow.
"""


def _clamp(v):
    return max(0, min(255, int(round(v))))


def shade(hex_color, amount):
    """amount > 0 lightens, amount < 0 darkens (range -1 to 1)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if amount >= 0:
        r, g, b = (c + (255 - c) * amount for c in (r, g, b))
    else:
        r, g, b = (c * (1 + amount) for c in (r, g, b))
    return "#%02x%02x%02x" % (_clamp(r), _clamp(g), _clamp(b))


# ---------------------------------------------------------------- shapes
BODY = {
    "tee": ("M146 62 C132 66 116 76 100 86 L52 158 L96 184 L122 150 "
            "C120 220 118 290 118 352 Q200 360 282 352 C282 290 280 220 278 150 "
            "L304 184 L348 158 L300 86 C284 76 268 66 254 62 "
            "C244 98 156 98 146 62 Z"),
    "long": ("M146 62 C132 66 116 76 100 86 L44 292 L90 306 L122 176 "
             "C120 230 118 290 118 352 Q200 360 282 352 C282 290 280 230 278 176 "
             "L310 306 L356 292 L300 86 C284 76 268 66 254 62 "
             "C244 98 156 98 146 62 Z"),
    "tank": ("M150 52 L172 52 C176 100 224 100 228 52 L250 52 "
             "C256 100 276 130 284 158 C280 220 282 290 282 350 Q200 358 118 350 "
             "C118 290 120 220 116 158 C124 130 144 100 150 52 Z"),
    "hoodie": ("M152 84 C130 90 112 96 96 104 L48 290 L98 304 L124 190 "
               "C122 250 120 300 120 356 Q200 364 280 356 C280 300 278 250 276 190 "
               "L302 304 L352 290 L304 104 C288 96 270 90 248 84 Z"),
}
HOOD = ("M150 86 C140 30 168 10 200 10 C232 10 260 30 250 86 "
        "C240 124 222 138 200 140 C178 138 160 124 150 86 Z")
HOOD_IN = ("M166 88 C164 52 180 34 200 34 C220 34 236 52 234 88 "
           "C226 114 214 122 200 124 C186 122 174 114 166 88 Z")

FOLDS_DARK = {
    "tee": ["M124 152 C150 190 158 232 148 276", "M278 152 C252 190 244 232 252 276",
            "M146 330 C166 318 182 334 200 326 C216 320 232 334 252 328",
            "M98 92 C82 116 72 138 62 158"],
    "long": ["M124 176 C150 204 158 244 148 284", "M278 176 C252 204 244 244 252 284",
             "M146 330 C166 318 182 334 200 326 C216 320 232 334 252 328",
             "M72 210 C70 244 66 272 60 296", "M328 210 C330 244 334 272 340 296"],
    "tank": ["M120 170 C146 210 154 252 146 296", "M280 170 C254 210 246 252 254 296",
             "M146 332 C166 320 182 336 200 328 C216 322 232 336 252 330"],
    "hoodie": ["M124 192 C150 222 156 262 146 304", "M276 192 C250 222 244 262 254 304",
               "M74 150 C70 200 62 250 56 288", "M326 150 C330 200 338 250 344 288",
               "M150 340 C170 330 190 344 210 336"],
}
FOLDS_LIGHT = {
    "tee": ["M172 124 C190 144 212 144 230 124", "M168 196 C176 236 172 276 166 302"],
    "long": ["M172 124 C190 144 212 144 230 124", "M168 200 C176 240 172 280 166 304",
             "M84 140 C76 190 70 230 64 270"],
    "tank": ["M172 130 C190 150 212 150 230 130", "M168 200 C176 240 172 280 166 304"],
    "hoodie": ["M200 144 C196 204 202 254 198 304", "M170 154 C176 194 172 234 168 264",
               "M84 130 C78 190 70 240 64 280"],
}

SPECS = {
    "classic-tee": dict(kind="tee", color="#EFEDE6", bg="#FFD23F", noise=.12),
    "graphic-tee": dict(kind="tee", color="#202028", bg="#7B5CFF", noise=.16),
    "hooded-sweatshirt": dict(kind="hoodie", color="#8F929E", bg="#FF4D9D", noise=.26),
    "hoodie-shirt": dict(kind="hoodie", color="#1F2A4D", bg="#C6FF3D", noise=.2),
    "tank-top": dict(kind="tank", color="#D9493F", bg="#3DE8FF", noise=.14),
    "long-sleeve": dict(kind="long", color="#2F5D50", bg="#FF7A45", noise=.16),
}

FONT = 'font-family="Arial Black,Impact,Arial,sans-serif" font-weight="900"'


def _star(cx, cy, r, fill):
    import math
    pts = []
    for i in range(8):
        rad = r if i % 2 == 0 else r * 0.35
        a = math.pi / 4 * i - math.pi / 2
        pts.append("%.1f,%.1f" % (cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return '<polygon points="%s" fill="%s"/>' % (" ".join(pts), fill)


def _rib(color, pid):
    return (
        '<pattern id="rib-%s" width="5" height="5" patternUnits="userSpaceOnUse">'
        '<rect width="5" height="5" fill="%s"/>'
        '<rect width="1.7" height="5" fill="%s" opacity=".55"/></pattern>'
        % (pid, shade(color, -.1), shade(color, -.35))
    )


def _details(pid, spec):
    """Prints, pockets, collars and hardware for each product."""
    kind, c = spec["kind"], spec["color"]
    dark, darker = shade(c, -.3), shade(c, -.5)
    out = ""

    if kind in ("tee", "long"):
        # ribbed neckband + visible inside back of the collar
        out += ('<path d="M146 62 C156 70 244 70 254 62 C244 98 156 98 146 62 Z" '
                'fill="%s" opacity=".85"/>' % shade(c, -.45))
        out += ('<path d="M146 62 C156 98 244 98 254 62" fill="none" stroke="%s" '
                'stroke-width="9" stroke-linecap="round"/>' % shade(c, -.14))
        out += ('<path d="M148 64 C158 95 242 95 252 64" fill="none" stroke="%s" '
                'stroke-width="2" opacity=".6" stroke-linecap="round"/>' % shade(c, .25))
        out += ('<path d="M132 340 H268" stroke="%s" stroke-width="1.6" '
                'stroke-dasharray="5 4" opacity=".55"/>' % shade(c, .35))

    if kind == "tank":
        out += ('<path d="M172 52 C176 100 224 100 228 52" fill="none" stroke="%s" '
                'stroke-width="7" stroke-linecap="round"/>' % shade(c, -.16))
        out += ('<path d="M150 52 C144 100 124 130 116 158 M250 52 C256 100 276 130 284 158" '
                'fill="none" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % shade(c, -.16))
        out += ('<path d="M122 338 H278" stroke="%s" stroke-width="1.6" '
                'stroke-dasharray="5 4" opacity=".55"/>' % shade(c, .35))

    if pid == "classic-tee":
        out += ('<text x="232" y="184" text-anchor="middle" %s font-size="13" '
                'fill="#23202e" opacity=".9">spazz</text>' % FONT)

    if pid == "graphic-tee":
        out += ('<g opacity=".95">'
                '<polygon points="200,186 168,250 196,250 182,308 234,230 204,230 224,186" '
                'fill="#C6FF3D" stroke="#FF4D9D" stroke-width="3" stroke-linejoin="round"/>'
                + _star(150, 214, 10, "#FFD23F") + _star(258, 284, 12, "#3DE8FF")
                + _star(246, 200, 7, "#FF4D9D") + '</g>')

    if kind == "hoodie":
        rib = "url(#rib-%s)" % pid
        # hood opening, ribbed hem and cuffs
        out += '<path d="%s" fill="url(#hoodIn)"/>' % HOOD_IN
        out += ('<path d="%s" fill="none" stroke="%s" stroke-width="3" opacity=".7"/>'
                % (HOOD_IN, shade(c, -.55)))
        out += '<path d="M120 336 H280 V362 H120 Z" fill="%s" clip-path="url(#cut)"/>' % rib
        out += '<polygon points="52,274 101,288 98,306 46,291" fill="%s"/>' % rib
        out += '<polygon points="348,274 299,288 302,306 354,291" fill="%s"/>' % rib
        out += ('<path d="M120 336 H280" stroke="%s" stroke-width="2" opacity=".6"/>'
                % shade(c, -.5))

    if pid == "hooded-sweatshirt":
        out += ('<text x="200" y="240" text-anchor="middle" %s font-size="31" '
                'fill="#F6F5FA" opacity=".93" letter-spacing="2">SPAZZ</text>' % FONT)
        out += ('<path d="M146 252 q13 -10 26 0 t26 0 t26 0 t26 0" fill="none" '
                'stroke="#F6F5FA" stroke-width="3" stroke-linecap="round" opacity=".9"/>')
        # kangaroo pocket
        out += ('<path d="M146 276 C170 268 230 268 254 276 L274 338 L126 338 Z" '
                'fill="%s" fill-opacity=".35" stroke="%s" stroke-width="2.2" '
                'stroke-linejoin="round"/>' % (shade(c, -.2), shade(c, -.45)))
        out += ('<path d="M152 282 C172 275 228 275 248 282 M134 332 H266" fill="none" '
                'stroke="%s" stroke-width="1.4" stroke-dasharray="4 4" opacity=".6"/>' % shade(c, .4))
        # drawstrings
        out += ('<path d="M190 128 C186 156 188 180 184 204 M210 128 C214 156 212 182 216 206" '
                'fill="none" stroke="#F6F5FA" stroke-width="4.5" stroke-linecap="round"/>'
                '<rect x="181" y="202" width="6" height="14" rx="3" fill="#2a2638"/>'
                '<rect x="213" y="204" width="6" height="14" rx="3" fill="#2a2638"/>')

    if pid == "hoodie-shirt":
        out += ('<path d="M200 140 V364" stroke="%s" stroke-width="5"/>' % shade(c, -.55))
        out += ('<path d="M200 140 V364" stroke="#C9CDD6" stroke-width="3" '
                'stroke-dasharray="2.5 2.5"/>')
        out += ('<rect x="193" y="146" width="14" height="26" rx="4" fill="#DDE0E8" '
                'stroke="#7d8290" stroke-width="1.5"/>'
                '<circle cx="200" cy="164" r="3" fill="#7d8290"/>')
        out += ('<path d="M128 294 L170 330 M272 294 L230 330" stroke="%s" stroke-width="2.4" '
                'stroke-linecap="round"/>' % shade(c, -.5))
        out += ('<path d="M128 296 L168 330 M272 296 L232 330" stroke="%s" stroke-width="1.2" '
                'stroke-dasharray="4 3" opacity=".6"/>' % shade(c, .35))
        out += ('<text x="238" y="204" text-anchor="middle" %s font-size="12" '
                'fill="#EDE9DD" opacity=".92">SPAZZ</text>' % FONT)
        out += ('<path d="M190 132 C187 150 188 166 186 182 M210 132 C213 150 212 166 214 184" '
                'fill="none" stroke="#EDE9DD" stroke-width="4" stroke-linecap="round"/>')

    if pid == "tank-top":
        out += ('<circle cx="200" cy="244" r="32" fill="#FFD23F" opacity=".95"/>'
                '<circle cx="189" cy="236" r="4.5" fill="#2a1f10"/>'
                '<circle cx="211" cy="236" r="4.5" fill="#2a1f10"/>'
                '<path d="M184 252 Q200 270 216 252" fill="none" stroke="#2a1f10" '
                'stroke-width="3.5" stroke-linecap="round"/>')

    if pid == "long-sleeve":
        cream = "#EFE8D4"
        out += ('<path d="M63 222 L107 236 M60 236 L104 250 M337 222 L293 236 M340 236 L296 250" '
                'stroke="%s" stroke-width="7" stroke-linecap="round" opacity=".95"/>' % cream)
        out += ('<text x="200" y="236" text-anchor="middle" %s font-size="26" '
                'fill="%s" letter-spacing="3" opacity=".95">STREET</text>' % (FONT, cream))
        out += '<path d="M148 252 H252" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % cream
        out += _star(200, 282, 11, "#FFD23F")
        # ribbed cuffs
        out += ('<polygon points="49,276 96,290 90,307 44,293" fill="%s"/>' % shade(c, -.2))
        out += ('<polygon points="351,276 304,290 310,307 356,293" fill="%s"/>' % shade(c, -.2))
    return out


def render_svg(pid):
    spec = SPECS.get(pid)
    if spec is None:
        return None
    kind, c, bg = spec["kind"], spec["color"], spec["bg"]
    body = BODY[kind]
    clip_shapes = '<path d="%s"/>' % body + ('<path d="%s"/>' % HOOD if kind == "hoodie" else "")
    outline = '<path d="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-linejoin="round"/>' % (
        body, shade(c, -.55))
    if kind == "hoodie":
        outline += '<path d="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-linejoin="round"/>' % (
            HOOD, shade(c, -.55))

    folds = "".join(
        '<path d="%s" fill="none" stroke="#000" stroke-opacity=".2" stroke-width="7" '
        'stroke-linecap="round" filter="url(#b3)"/>' % d for d in FOLDS_DARK[kind])
    folds += "".join(
        '<path d="%s" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="9" '
        'stroke-linecap="round" filter="url(#b4)"/>' % d for d in FOLDS_LIGHT[kind])

    hood_extra = ""
    if kind == "hoodie":
        hood_extra = ('<path d="M150 86 C170 112 230 112 250 86" fill="none" stroke="#000" '
                      'stroke-opacity=".25" stroke-width="6" filter="url(#b3)"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 420" role="img" aria-label="{pid}">
<defs>
<radialGradient id="studio" cx=".5" cy=".42" r=".75">
<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="{shade(bg, .25)}"/></radialGradient>
<linearGradient id="side" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#000" stop-opacity=".34"/><stop offset=".22" stop-color="#000" stop-opacity="0"/>
<stop offset=".5" stop-color="#fff" stop-opacity=".12"/>
<stop offset=".78" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".34"/></linearGradient>
<linearGradient id="vert" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".6" stop-color="#000" stop-opacity="0"/>
<stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient>
<linearGradient id="hoodIn" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{shade(c, -.75)}"/><stop offset="1" stop-color="{shade(c, -.45)}"/></linearGradient>
<clipPath id="cut">{clip_shapes}</clipPath>
{_rib(c, pid)}
<filter id="b3" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="b4" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="4.5"/></filter>
<filter id="b8" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="noise" x="0" y="0" width="100%" height="100%">
<feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/>
<feColorMatrix type="saturate" values="0"/></filter>
</defs>

<rect width="400" height="420" fill="url(#studio)"/>
<circle cx="200" cy="215" r="170" fill="{bg}" opacity=".35"/>
<ellipse cx="200" cy="384" rx="140" ry="15" fill="#000" opacity=".28" filter="url(#b8)"/>

<g transform="translate(0 9)" opacity=".28" filter="url(#b8)"><g fill="#000">{clip_shapes}</g></g>

<g clip-path="url(#cut)">
<rect width="400" height="420" fill="{c}"/>
<rect width="400" height="420" fill="url(#side)"/>
<rect width="400" height="420" fill="url(#vert)"/>
<path d="{body}" fill="none" stroke="#000" stroke-opacity=".3" stroke-width="20" filter="url(#b3)"/>
{folds}{hood_extra}
<rect width="400" height="420" filter="url(#noise)" opacity="{spec['noise']}" style="mix-blend-mode:multiply"/>
</g>
{outline}
{_details(pid, spec)}
</svg>'''
    return svg
