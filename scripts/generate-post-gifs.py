"""
Generate 10 promotional GIFs for RepoShield social posts.
5 LinkedIn (1200x628) + 5 Twitter (1200x675)
"""
from PIL import Image, ImageDraw, ImageFont
import os, sys

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "posts", "gifs")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Colors (RepoShield palette) ────────────────────────────────────────────
BG       = (8, 12, 14)
SURFACE  = (13, 17, 23)
SURFACE2 = (17, 24, 33)
BORDER   = (30, 45, 61)
GREEN    = (0, 255, 136)
GREEN_DIM= (0, 180, 90)
RED      = (255, 68, 85)
ORANGE   = (255, 140, 0)
YELLOW   = (255, 215, 0)
BLUE     = (68, 136, 255)
TEXT     = (212, 220, 232)
DIM      = (90, 106, 126)
DIM2     = (40, 55, 70)

# ── Fonts ──────────────────────────────────────────────────────────────────
def load_fonts():
    paths = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cour.ttf",
        "C:/Windows/Fonts/courbd.ttf",
    ]
    mono_path = next((p for p in paths if os.path.exists(p)), None)
    sans_paths = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    sans_path = next((p for p in sans_paths if os.path.exists(p)), None)
    bold_paths = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/courbd.ttf",
    ]
    bold_path = next((p for p in bold_paths if os.path.exists(p)), None)

    def tf(path, size):
        try:
            if path: return ImageFont.truetype(path, size)
        except: pass
        return ImageFont.load_default()

    return {
        "mono_sm":  tf(mono_path, 13),
        "mono_md":  tf(mono_path, 16),
        "mono_lg":  tf(mono_path, 22),
        "mono_xl":  tf(bold_path or mono_path, 36),
        "sans_sm":  tf(sans_path, 13),
        "sans_md":  tf(sans_path, 17),
        "sans_lg":  tf(sans_path, 22),
        "sans_xl":  tf(bold_path or sans_path, 32),
        "bold_xl":  tf(bold_path, 40),
        "bold_xxl": tf(bold_path, 56),
    }

F = load_fonts()

def save_gif(frames, path, duration=600, loop=0):
    if not frames: return
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=duration, loop=loop, optimize=True)
    size = os.path.getsize(path)
    if size > 500_000:
        # re-quantize harder
        q_frames = [f.quantize(colors=64, method=Image.Quantize.MEDIANCUT) for f in frames]
        q_frames[0].save(path, save_all=True, append_images=q_frames[1:],
                         duration=duration, loop=loop, optimize=True)
    print(f"  {os.path.basename(path)}: {os.path.getsize(path)//1024}KB")

def base_frame(w, h):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    # grid
    for x in range(0, w, 40): d.line([(x,0),(x,h)], fill=DIM2, width=1)
    for y in range(0, h, 40): d.line([(0,y),(w,y)], fill=DIM2, width=1)
    # left bar
    d.rectangle([0, 0, 5, h], fill=GREEN)
    return img, d

def watermark(d, w, h):
    label = "reposhield"
    try:
        bb = d.textbbox((0,0), label, font=F["mono_sm"])
        lw = bb[2]-bb[0]
    except:
        lw = 80
    d.text((w - lw - 16, h - 22), label, fill=(0, 100, 50), font=F["mono_sm"])

def panel(d, x, y, w, h, color=SURFACE, radius=6, border=BORDER):
    d.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=color, outline=border)

def sev_badge(d, x, y, label, color):
    try:
        bb = d.textbbox((0,0), label, font=F["mono_sm"])
        tw = bb[2]-bb[0]
    except:
        tw = 60
    pad = 10
    r, g, b = color
    d.rounded_rectangle([x, y, x+tw+pad*2, y+20], radius=3,
                         fill=(r//6, g//6, b//6), outline=(r//2, g//2, b//2))
    d.text((x+pad, y+3), label, fill=color, font=F["mono_sm"])
    return tw + pad*2

def txt(d, x, y, text, font=None, fill=TEXT, anchor=None):
    kw = {"font": font or F["sans_md"], "fill": fill}
    if anchor: kw["anchor"] = anchor
    d.text((x, y), text, **kw)

# ════════════════════════════════════════════════════════════════════════════
# LINKEDIN GIFs (1200x628)
# ════════════════════════════════════════════════════════════════════════════
LW, LH = 1200, 628

def linkedin_technical():
    """Architecture pipeline in motion"""
    frames = []
    stages = ["Secrets Scanner", "Dependency Check", "OWASP Analysis", "Git History", "Report Ready"]
    colors_s = [RED, ORANGE, YELLOW, BLUE, GREEN]

    for i in range(len(stages)+2):
        img, d = base_frame(LW, LH)

        # Title
        d.text((60, 45), "RepoShield", fill=GREEN, font=F["mono_xl"])
        d.text((60, 100), "Four scanners. One report.", fill=DIM, font=F["sans_md"])

        # Pipeline boxes
        box_w, box_h = 180, 70
        total_w = len(stages)*box_w + (len(stages)-1)*16
        start_x = (LW - total_w) // 2
        y = 200

        for j, (stage, col) in enumerate(zip(stages, colors_s)):
            x = start_x + j*(box_w+16)
            active = j < i
            current = j == i-1

            bg = SURFACE2 if active else SURFACE
            border = col if active else BORDER
            if current:
                bg = tuple(min(255, c//4) for c in col)

            panel(d, x, y, box_w, box_h, color=bg, border=border)

            if active:
                d.rectangle([x, y, x+box_w, y+4], fill=col)
                # checkmark
                d.text((x+box_w-24, y+8), "✓", fill=col, font=F["mono_sm"])

            # Stage label (wrap at space)
            words = stage.split()
            if len(words) == 2:
                d.text((x+10, y+14), words[0], fill=TEXT if active else DIM, font=F["mono_sm"])
                d.text((x+10, y+30), words[1], fill=TEXT if active else DIM, font=F["mono_sm"])
            else:
                d.text((x+10, y+22), stage, fill=TEXT if active else DIM, font=F["mono_sm"])

            # Arrow
            if j < len(stages)-1:
                ax = x + box_w + 4
                ay = y + box_h//2
                d.polygon([(ax, ay-6), (ax+10, ay), (ax, ay+6)], fill=GREEN_DIM if active else BORDER)

        # Stats below
        stats = [("30+ patterns", RED), ("8 ecosystems", ORANGE), ("OWASP Top 10", YELLOW), ("200 commits", BLUE)]
        sx = 60
        for stat, col in stats:
            panel(d, sx, 330, 240, 44, color=SURFACE)
            try:
                bb = d.textbbox((0,0), stat, font=F["mono_sm"])
                tw = bb[2]-bb[0]
            except:
                tw = 120
            d.text((sx + (240-tw)//2, 341), stat, fill=col, font=F["mono_sm"])
            sx += 256

        # Findings preview (last frame)
        if i >= len(stages):
            panel(d, 60, 400, LW-120, 170, color=SURFACE)
            findings = [
                ("CRITICAL", RED,    "src/config.py:14  AWS Secret Access Key"),
                ("HIGH",     ORANGE, "package.json      lodash@4.17.4  CVE-2021-23337"),
                ("HIGH",     ORANGE, "src/routes.py:88  Command injection (shell=True)"),
                ("MEDIUM",   YELLOW, "requirements.txt  PyYAML@3.13  CVE-2017-18342"),
            ]
            fy = 416
            for sev, col, msg in findings:
                x0 = 80
                bw = sev_badge(d, x0, fy+2, sev, col)
                d.text((x0+bw+12, fy), msg, fill=TEXT, font=F["mono_sm"])
                fy += 30

        watermark(d, LW, LH)
        frames.append(img.quantize(colors=96, method=Image.Quantize.MEDIANCUT))

    # Hold last frame
    frames.extend([frames[-1]] * 3)
    return frames

def linkedin_eli5():
    """Before/after: messy paper -> clean output"""
    frames = []

    # Frame 1: "Before" - the problem
    img, d = base_frame(LW, LH)
    panel(d, 60, 80, 500, 460, color=SURFACE)
    d.text((80, 100), "The problem", fill=DIM, font=F["mono_sm"])
    d.text((80, 140), "settings.py", fill=TEXT, font=F["mono_md"])
    code_lines = [
        ("SECRET_KEY = 'abc123'",          RED),
        ("STRIPE_KEY = 'sk_live_X4j...'",  RED),
        ("DB_PASS    = 'admin2024'",        RED),
        ("# removed in next commit",       DIM),
        ("# (still in git history)",       DIM),
    ]
    cy = 180
    for line, col in code_lines:
        d.text((80, cy), line, fill=col, font=F["mono_sm"])
        if col == RED:
            try:
                bb = d.textbbox((80, cy), line, font=F["mono_sm"])
                d.line([(80, cy+8), (bb[2], cy+8)], fill=(255, 68, 85, 80), width=2)
            except: pass
        cy += 28

    d.text((80, 380), "Deleted from current code.", fill=DIM, font=F["sans_sm"])
    d.text((80, 404), "Still in git history forever.", fill=RED, font=F["sans_sm"])

    d.text((700, 260), "Most scanners", fill=DIM, font=F["sans_lg"])
    d.text((700, 295), "only check this ->", fill=DIM, font=F["mono_sm"])
    d.text((700, 340), "current files", fill=TEXT, font=F["bold_xl"])
    watermark(d, LW, LH)
    frames.append(img.quantize(colors=96))

    # Frame 2: Transition flash
    img2, d2 = base_frame(LW, LH)
    d2.rectangle([0, 0, LW, LH], fill=(0, 40, 20))
    d2.text((LW//2, LH//2 - 20), "RepoShield", fill=GREEN, font=F["bold_xxl"], anchor="mm")
    d2.text((LW//2, LH//2 + 40), "checking everything...", fill=GREEN_DIM, font=F["mono_md"], anchor="mm")
    frames.append(img2.quantize(colors=96))

    # Frame 3: After - findings from history
    img3, d3 = base_frame(LW, LH)
    panel(d3, 60, 80, LW-120, 460, color=SURFACE)
    d3.text((80, 100), "Scan complete", fill=GREEN, font=F["mono_md"])
    d3.text((80, 130), "https://github.com/example/webapp", fill=DIM, font=F["mono_sm"])

    findings = [
        ("CRITICAL", RED,    "src/config.py:2      AWS Secret Access Key  (CURRENT CODE)"),
        ("CRITICAL", RED,    "HISTORY (commit a3f2d1)  Stripe live key  sk_live_X4j***REDACTED***"),
        ("CRITICAL", RED,    "HISTORY (commit b8e1c9)  DB password found, deleted 6 weeks ago"),
        ("HIGH",     ORANGE, "package.json           lodash@4.17.4  CVE-2021-23337"),
        ("HIGH",     ORANGE, "src/routes.py:88        Command injection via shell=True"),
        ("MEDIUM",   YELLOW, "src/crypto.py:12        MD5 used for password hashing"),
    ]
    fy = 175
    for sev, col, msg in findings:
        x0 = 80
        bw = sev_badge(d3, x0, fy+2, sev, col)
        d3.text((x0+bw+12, fy), msg, fill=TEXT, font=F["mono_sm"])
        fy += 36

    # Summary row
    panel(d3, 80, 420, LW-160, 48, color=SURFACE2, border=GREEN)
    d3.text((100, 432), "7 findings", fill=GREEN, font=F["mono_md"])
    counts = [("3 critical", RED), ("2 high", ORANGE), ("1 medium", YELLOW), ("1 low", BLUE)]
    cx = 280
    for label, col in counts:
        d3.text((cx, 432), label, fill=col, font=F["mono_md"])
        cx += 190

    watermark(d3, LW, LH)
    frames.extend([img3.quantize(colors=96)] * 3)
    return frames

def linkedin_why_built():
    """Pain moment -> broken state -> tool solves it"""
    frames = []

    # Frame 1: The pain - multiple terminals
    img, d = base_frame(LW, LH)
    d.text((60, 40), "Before: four tools, four terminals", fill=DIM, font=F["mono_sm"])

    terminals = [
        ("$ gitleaks detect",         ["[WARN] leaks found: 3"]),
        ("$ npm audit",               ["found 12 vulnerabilities"]),
        ("$ bandit -r .",             ["Issue: 8, Severity: HIGH"]),
        ("$ git log | grep -i key",   ["... no output ..."]),
    ]
    positions = [(60,80),(640,80),(60,320),(640,320)]
    for (cmd, output), (px, py) in zip(terminals, positions):
        panel(d, px, py, 510, 200, color=SURFACE)
        d.text((px+12, py+10), cmd, fill=GREEN, font=F["mono_sm"])
        d.line([(px+12, py+30), (px+498, py+30)], fill=BORDER, width=1)
        oy = py+44
        for line in output:
            d.text((px+12, oy), line, fill=DIM, font=F["mono_sm"])
            oy += 22

    d.text((60, 545), "No unified severity. No fix suggestions. Just raw output.", fill=DIM, font=F["sans_sm"])
    watermark(d, LW, LH)
    frames.append(img.quantize(colors=96))

    # Frame 2: Flash
    img2, d2 = base_frame(LW, LH)
    d2.rectangle([0, 0, LW, LH], fill=(20, 8, 8))
    d2.text((LW//2, LH//2), "One tool.", fill=GREEN, font=F["bold_xxl"], anchor="mm")
    frames.append(img2.quantize(colors=96))

    # Frame 3: RepoShield result
    img3, d3 = base_frame(LW, LH)
    panel(d3, 60, 60, LW-120, 500, color=SURFACE)
    d3.text((80, 80), "$ reposhield scan github.com/example/webapp", fill=GREEN, font=F["mono_sm"])
    d3.line([(80, 106), (LW-80, 106)], fill=BORDER, width=1)

    d3.text((80, 120), "Cloning...  Scanning...  Done.", fill=DIM, font=F["mono_sm"])

    steps = [
        ("Secrets scanner",    "3 findings",   RED),
        ("Dependency scanner", "4 CVEs",        ORANGE),
        ("Static analysis",    "2 issues",      YELLOW),
        ("Git history",        "1 leaked key",  RED),
    ]
    sy = 160
    for step, result, col in steps:
        d3.text((80, sy), "✓", fill=GREEN, font=F["mono_sm"])
        d3.text((104, sy), step, fill=TEXT, font=F["mono_sm"])
        d3.text((380, sy), result, fill=col, font=F["mono_sm"])
        sy += 30

    panel(d3, 80, 340, LW-160, 180, color=SURFACE2, border=GREEN)
    findings2 = [
        ("CRITICAL", RED,    "HISTORY commit a3f2d1 -> Stripe secret key (was deleted 6 weeks ago)"),
        ("CRITICAL", RED,    "src/app.py:44 -> subprocess.run(..., shell=True)"),
        ("HIGH",     ORANGE, "lodash@4.17.4 -> CVE-2021-23337 (prototype pollution)"),
        ("MEDIUM",   YELLOW, "src/crypto.py:12 -> hashlib.md5() used for password storage"),
    ]
    fy = 355
    for sev, col, msg in findings2:
        bw = sev_badge(d3, 96, fy+2, sev, col)
        d3.text((96+bw+10, fy), msg, fill=TEXT, font=F["mono_sm"])
        fy += 36

    watermark(d3, LW, LH)
    frames.extend([img3.quantize(colors=96)] * 3)
    return frames

def linkedin_unique():
    """Side-by-side: others vs RepoShield on git history"""
    frames = []

    # Frame 1: What others do
    img, d = base_frame(LW, LH)
    panel(d, 60, 60, 510, 500, color=SURFACE)
    d.text((80, 80), "Most scanners", fill=DIM, font=F["mono_md"])
    d.line([(80, 108), (550, 108)], fill=BORDER, width=1)

    checks = [
        ("✓", GREEN,  "Current source files"),
        ("✓", GREEN,  "Dependencies (sometimes)"),
        ("✗", RED,    "Git history"),
        ("✗", RED,    "Deleted secrets"),
        ("✗", RED,    "Commit-level detail"),
        ("✗", RED,    "Removal commands"),
    ]
    cy = 125
    for icon, col, label in checks:
        d.text((80, cy), icon, fill=col, font=F["mono_md"])
        d.text((110, cy), label, fill=TEXT if col==GREEN else DIM, font=F["sans_md"])
        cy += 44

    # Frame 1 right: RepoShield
    panel(d, 630, 60, 510, 500, color=SURFACE2, border=GREEN)
    d.rectangle([630, 60, 1140, 64], fill=GREEN)
    d.text((650, 80), "RepoShield", fill=GREEN, font=F["mono_md"])
    d.line([(650, 108), (1120, 108)], fill=BORDER, width=1)

    checks2 = [
        ("✓", GREEN, "Current source files"),
        ("✓", GREEN, "Dependencies (8 ecosystems)"),
        ("✓", GREEN, "Git history (200 commits)"),
        ("✓", GREEN, "Deleted secrets"),
        ("✓", GREEN, "Commit hash + date"),
        ("✓", GREEN, "BFG / git-filter-repo cmd"),
    ]
    cy = 125
    for icon, col, label in checks2:
        d.text((650, cy), icon, fill=col, font=F["mono_md"])
        d.text((680, cy), label, fill=TEXT, font=F["sans_md"])
        cy += 44

    watermark(d, LW, LH)
    frames.append(img.quantize(colors=96))

    # Frame 2: History scanner in action
    img2, d2 = base_frame(LW, LH)
    panel(d2, 60, 60, LW-120, 500, color=SURFACE)
    d2.text((80, 80), "Git history scanner -> what it actually finds", fill=GREEN, font=F["mono_sm"])
    d2.line([(80, 106), (LW-80, 106)], fill=BORDER, width=1)

    history_finds = [
        ("a3f2d1", "3 weeks ago", "CRITICAL", RED,    "Stripe secret key  sk_live_X4j***REDACTED***"),
        ("b8e1c9", "6 weeks ago", "CRITICAL", RED,    "AWS_SECRET_ACCESS_KEY = 'AKIA***REDACTED***'"),
        ("c2d4f8", "2 months ago","HIGH",     ORANGE, "DB_PASSWORD = 'prod_db_pass_2023'"),
        ("e9a1b3", "3 months ago","HIGH",     ORANGE, "SENDGRID_API_KEY = 'SG.***REDACTED***'"),
    ]
    fy = 125
    for commit, age, sev, col, msg in history_finds:
        d2.text((80, fy), commit, fill=DIM, font=F["mono_sm"])
        d2.text((160, fy), age, fill=DIM, font=F["mono_sm"])
        bw = sev_badge(d2, 290, fy+2, sev, col)
        d2.text((290+bw+10, fy), msg, fill=TEXT, font=F["mono_sm"])
        fy += 48

    panel(d2, 80, 370, LW-160, 70, color=SURFACE2, border=ORANGE)
    d2.text((100, 385), "Fix:", fill=DIM, font=F["mono_sm"])
    d2.text((140, 385), "bfg --delete-files settings.py && git push --force", fill=TEXT, font=F["mono_sm"])
    d2.text((100, 410), "or: git filter-repo --path settings.py --invert-paths", fill=DIM, font=F["mono_sm"])

    watermark(d2, LW, LH)
    frames.extend([img2.quantize(colors=96)] * 3)
    return frames

def linkedin_story():
    """The Stripe key story: repo -> discovery -> reality"""
    frames = []

    # Frame 1: The moment
    img, d = base_frame(LW, LH)
    panel(d, 60, 60, LW-120, 200, color=SURFACE)
    d.text((80, 80),  "Friend's repo", fill=DIM, font=F["mono_sm"])
    d.text((80, 110), "settings.py (current)",  fill=TEXT, font=F["mono_md"])
    d.line([(80,140),(LW-80,140)], fill=BORDER, width=1)
    d.text((80, 156), "STRIPE_KEY = os.environ.get('STRIPE_KEY')  # looks clean", fill=GREEN, font=F["mono_sm"])

    panel(d, 60, 285, LW-120, 160, color=SURFACE)
    d.text((80, 300), "git log --all (6 weeks of history)", fill=DIM, font=F["mono_sm"])
    d.line([(80,325),(LW-80,325)], fill=BORDER, width=1)
    d.text((80, 342), "commit a3f2d1  [3 months ago]  'remove hardcoded keys'", fill=DIM, font=F["mono_sm"])
    d.text((80, 368), "- STRIPE_KEY = 'sk_live_X4j9RmKpLq...'", fill=RED, font=F["mono_sm"])

    panel(d, 60, 470, LW-120, 100, color=(40,10,10), border=RED)
    d.text((80, 490), "Still in git objects. Fully readable. 6 weeks exposed.", fill=RED, font=F["mono_md"])

    watermark(d, LW, LH)
    frames.append(img.quantize(colors=96))

    # Frame 2: RepoShield catches it
    img2, d2 = base_frame(LW, LH)
    panel(d2, 60, 60, LW-120, 520, color=SURFACE)
    d2.text((80, 80), "$ reposhield scan github.com/friend/django-app", fill=GREEN, font=F["mono_sm"])
    d2.line([(80,106),(LW-80,106)], fill=BORDER, width=1)
    d2.text((80, 125), "Scanning git history (200 commits)...", fill=DIM, font=F["mono_sm"])

    panel(d2, 80, 160, LW-160, 100, color=(40,10,10), border=RED)
    d2.text((100, 175), "CRITICAL", fill=RED, font=F["mono_md"])
    d2.text((210, 175), "Stripe Secret Key found in git history", fill=TEXT, font=F["mono_md"])
    d2.text((100, 210), "Commit: a3f2d1  |  File: settings.py  |  6 weeks ago", fill=DIM, font=F["mono_sm"])
    d2.text((100, 232), "Value: sk_live_X4j***REDACTED***", fill=RED, font=F["mono_sm"])

    d2.text((80, 290), "Fix:", fill=DIM, font=F["mono_sm"])
    d2.text((120, 290), "bfg --delete-files settings.py", fill=GREEN, font=F["mono_sm"])
    d2.text((80, 316), "Then revoke this key in your Stripe dashboard.", fill=ORANGE, font=F["sans_sm"])

    panel(d2, 80, 380, LW-160, 170, color=SURFACE2, border=GREEN)
    d2.text((100, 400), "This is why history scanning is on by default.", fill=TEXT, font=F["sans_md"])
    d2.text((100, 434), "Not just what's in your code now.", fill=DIM, font=F["sans_sm"])
    d2.text((100, 458), "What was ever in your code.", fill=GREEN, font=F["sans_md"])

    watermark(d2, LW, LH)
    frames.extend([img2.quantize(colors=96)] * 3)
    return frames

# ════════════════════════════════════════════════════════════════════════════
# TWITTER GIFs (1200x675)
# ════════════════════════════════════════════════════════════════════════════
TW, TH = 1200, 675

def twitter_technical():
    frames = []
    stages = [("Secrets", RED), ("CVEs", ORANGE), ("OWASP", YELLOW), ("History", BLUE)]

    for i in range(len(stages)+2):
        img, d = base_frame(TW, TH)
        d.text((60, 50), "RepoShield", fill=GREEN, font=F["bold_xl"])
        d.text((60, 105), "$ reposhield scan github.com/your/repo", fill=DIM, font=F["mono_sm"])

        bw = 220; gap = 20
        total = len(stages)*bw + (len(stages)-1)*gap
        sx = (TW-total)//2
        by = 200

        for j, (name, col) in enumerate(stages):
            x = sx + j*(bw+gap)
            active = j < i
            panel(d, x, by, bw, 100, color=(min(col[0]//4,30), min(col[1]//4,30), min(col[2]//4,30)) if active else SURFACE,
                  border=col if active else BORDER)
            if active:
                d.rectangle([x, by, x+bw, by+4], fill=col)
            d.text((x+bw//2, by+44), name, fill=col if active else DIM, font=F["mono_md"], anchor="mm")
            if active:
                d.text((x+bw//2, by+72), "✓", fill=col, font=F["mono_sm"], anchor="mm")
            if j < len(stages)-1:
                ax = x+bw+gap//2
                d.polygon([(ax-6,by+50),(ax+6,by+44),(ax+6,by+56)], fill=GREEN_DIM if active else BORDER)

        if i >= len(stages):
            panel(d, 60, 360, TW-120, 240, color=SURFACE)
            lines = [
                ("CRITICAL", RED,    "AWS key in src/config.py"),
                ("HIGH",     ORANGE, "lodash CVE-2021-23337"),
                ("HIGH",     ORANGE, "Command injection line 88"),
                ("CRITICAL", RED,    "Stripe key in git history (commit a3f2)"),
            ]
            ly = 376
            for sev, col, msg in lines:
                bw2 = sev_badge(d, 80, ly+2, sev, col)
                d.text((80+bw2+10, ly), msg, fill=TEXT, font=F["mono_sm"])
                ly += 44

        watermark(d, TW, TH)
        frames.append(img.quantize(colors=96))

    frames.extend([frames[-1]]*2)
    return frames

def twitter_eli5():
    frames = []

    # Frame 1: crossed-out paper analogy
    img, d = base_frame(TW, TH)
    panel(d, 60, 100, 480, 460, color=SURFACE)
    d.text((80, 120), "settings.py", fill=TEXT, font=F["mono_md"])
    d.line([(80,150),(520,150)], fill=BORDER)
    lines = ["SECRET='sk_live_X4j...'", "DB_PASS='admin2024'", "# <-- deleted later"]
    ly = 168
    for line in lines:
        d.text((80, ly), line, fill=RED, font=F["mono_sm"])
        try:
            bb = d.textbbox((80,ly), line, font=F["mono_sm"])
            d.line([(80,ly+8),(bb[2],ly+8)], fill=(200,50,60), width=2)
        except: pass
        ly += 36
    d.text((80, 320), '"deleted"', fill=DIM, font=F["mono_lg"])
    d.text((80, 370), 'Still in git objects.', fill=RED, font=F["sans_md"])

    panel(d, 620, 100, 520, 460, color=SURFACE2, border=GREEN)
    d.text((640, 120), "RepoShield checks", fill=GREEN, font=F["mono_md"])
    d.line([(640,150),(1120,150)], fill=BORDER)
    d.text((640, 180), "current files   ✓", fill=GREEN, font=F["mono_sm"])
    d.text((640, 215), "dependencies   ✓", fill=GREEN, font=F["mono_sm"])
    d.text((640, 250), "OWASP rules    ✓", fill=GREEN, font=F["mono_sm"])
    d.text((640, 285), "git history    ✓", fill=GREEN, font=F["mono_sm"])
    d.text((640, 340), "Including what", fill=TEXT, font=F["sans_md"])
    d.text((640, 372), 'got "deleted."', fill=GREEN, font=F["bold_xl"])

    watermark(d, TW, TH)
    frames.extend([img.quantize(colors=96)] * 4)
    return frames

def twitter_why_built():
    frames = []

    img, d = base_frame(TW, TH)
    # Left: chaos
    panel(d, 60, 80, 480, 500, color=(20,10,10), border=RED)
    d.text((80, 100), "Before", fill=RED, font=F["mono_md"])
    tools = ["gitleaks detect", "npm audit --json", "bandit -r src/", "git log | grep key"]
    ty = 140
    for tool in tools:
        panel(d, 80, ty, 440, 50, color=SURFACE)
        d.text((96, ty+14), f"$ {tool}", fill=DIM, font=F["mono_sm"])
        ty += 66
    d.text((80, 440), "Four terminals. Four formats.", fill=DIM, font=F["sans_sm"])
    d.text((80, 465), "No shared severity ranking.", fill=DIM, font=F["sans_sm"])

    # Right: simple
    panel(d, 620, 80, 520, 500, color=(10,20,10), border=GREEN)
    d.text((640, 100), "After", fill=GREEN, font=F["mono_md"])
    panel(d, 640, 145, 480, 60, color=SURFACE2, border=GREEN)
    d.text((660, 162), "$ reposhield scan github.com/you/repo", fill=GREEN, font=F["mono_sm"])
    d.text((640, 250), "One command.", fill=GREEN, font=F["bold_xl"])
    d.text((640, 310), "All four passes.", fill=TEXT, font=F["sans_lg"])
    d.text((640, 360), "Severity ranked.", fill=TEXT, font=F["sans_lg"])
    d.text((640, 410), "Fix suggestions.", fill=TEXT, font=F["sans_lg"])

    watermark(d, TW, TH)
    frames.extend([img.quantize(colors=96)] * 4)
    return frames

def twitter_unique():
    frames = []

    img, d = base_frame(TW, TH)
    panel(d, 60, 80, LW-120, 520, color=SURFACE)
    d.text((80, 100), "What git history actually looks like", fill=GREEN, font=F["mono_sm"])
    d.line([(80,126),(TW-80,126)], fill=BORDER)

    d.text((80, 145), "$ git log --all  (200 commits scanned)", fill=DIM, font=F["mono_sm"])

    commits = [
        ("a3f2d1", "3 weeks", "settings.py", "STRIPE_KEY='sk_live_X4j...'",  RED),
        ("b8e1c9", "6 weeks", "config.py",   "AWS_SECRET='AKIA4X...'",        RED),
        ("c2d4f8", "2 months","app.py",       "DB_PASS='prod2023!'",           ORANGE),
    ]
    cy = 185
    for c, age, f, secret, col in commits:
        panel(d, 80, cy, TW-160, 55, color=(min(col[0]//5,20), 8, 8), border=col)
        d.text((96, cy+8),  c,      fill=DIM,  font=F["mono_sm"])
        d.text((200, cy+8), age,    fill=DIM,  font=F["mono_sm"])
        d.text((330, cy+8), f,      fill=TEXT, font=F["mono_sm"])
        d.text((96, cy+30), secret, fill=col,  font=F["mono_sm"])
        sev_badge(d, TW-240, cy+16, "CRITICAL", RED)
        cy += 71

    panel(d, 80, 420, TW-160, 60, color=SURFACE2, border=GREEN)
    d.text((100, 435), "Most scanners miss this.", fill=DIM, font=F["sans_sm"])
    d.text((100, 457), "RepoShield walks 200 commits by default.", fill=GREEN, font=F["sans_md"])

    watermark(d, TW, TH)
    frames.extend([img.quantize(colors=96)] * 4)
    return frames

def twitter_story():
    frames = []

    img, d = base_frame(TW, TH)
    panel(d, 60, 60, TW-120, 260, color=SURFACE)
    d.text((80, 80), "git log -- settings.py", fill=GREEN, font=F["mono_sm"])
    d.line([(80,106),(TW-80,106)], fill=BORDER)
    d.text((80, 125), "commit a3f2d1  (6 weeks ago)", fill=DIM, font=F["mono_sm"])
    d.text((80, 155), '- STRIPE_KEY = "sk_live_X4j9RmKpLq..."  # removed', fill=RED, font=F["mono_sm"])
    d.text((80, 195), "Still in git objects.", fill=TEXT, font=F["sans_md"])
    d.text((80, 225), "Fully readable.", fill=RED, font=F["sans_md"])

    panel(d, 60, 350, TW-120, 260, color=SURFACE2, border=GREEN)
    d.text((80, 375), "RepoShield scan -> 1 CRITICAL (git history)", fill=GREEN, font=F["mono_sm"])
    d.text((80, 415), "Stripe key in commit a3f2d1, 6 weeks ago.", fill=TEXT, font=F["sans_md"])
    d.text((80, 455), "Revoke it. Then:", fill=DIM, font=F["sans_sm"])
    d.text((80, 480), "bfg --delete-files settings.py", fill=GREEN, font=F["mono_sm"])
    d.text((80, 515), "History scanning is on by default for exactly this.", fill=DIM, font=F["sans_sm"])
    d.text((80, 545), "git delete != gone.", fill=GREEN, font=F["bold_xl"])

    watermark(d, TW, TH)
    frames.extend([img.quantize(colors=96)] * 4)
    return frames

# ════════════════════════════════════════════════════════════════════════════
# GENERATE ALL
# ════════════════════════════════════════════════════════════════════════════
print("Generating LinkedIn GIFs...")
save_gif(linkedin_technical(), os.path.join(OUT_DIR, "linkedin-technical.gif"), duration=700)
save_gif(linkedin_eli5(),      os.path.join(OUT_DIR, "linkedin-eli5.gif"),      duration=1200)
save_gif(linkedin_why_built(), os.path.join(OUT_DIR, "linkedin-why-built.gif"), duration=900)
save_gif(linkedin_unique(),    os.path.join(OUT_DIR, "linkedin-unique.gif"),    duration=1000)
save_gif(linkedin_story(),     os.path.join(OUT_DIR, "linkedin-story.gif"),     duration=1100)

print("Generating Twitter GIFs...")
save_gif(twitter_technical(), os.path.join(OUT_DIR, "twitter-technical.gif"), duration=500)
save_gif(twitter_eli5(),      os.path.join(OUT_DIR, "twitter-eli5.gif"),      duration=800)
save_gif(twitter_why_built(), os.path.join(OUT_DIR, "twitter-why-built.gif"), duration=700)
save_gif(twitter_unique(),    os.path.join(OUT_DIR, "twitter-unique.gif"),    duration=700)
save_gif(twitter_story(),     os.path.join(OUT_DIR, "twitter-story.gif"),     duration=800)
print("Done.")
