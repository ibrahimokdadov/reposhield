"""
Demo GIF: RepoShield cold-start to scan complete.
900x560px, README-friendly, target <2MB.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "posts", "demo.gif")

BG      = (8, 12, 14)
SURFACE = (13, 17, 23)
SURF2   = (17, 24, 33)
BORDER  = (30, 45, 61)
GREEN   = (0, 255, 136)
GREEN_D = (0, 180, 90)
RED     = (255, 68, 85)
ORANGE  = (255, 140, 0)
YELLOW  = (255, 215, 0)
BLUE    = (68, 136, 255)
TEXT    = (212, 220, 232)
DIM     = (90, 106, 126)
DIM2    = (30, 45, 58)

W, H = 900, 560

def fonts():
    paths = {"mono": ["C:/Windows/Fonts/consola.ttf","C:/Windows/Fonts/cour.ttf"],
             "sans": ["C:/Windows/Fonts/segoeui.ttf","C:/Windows/Fonts/calibri.ttf","C:/Windows/Fonts/arial.ttf"],
             "bold": ["C:/Windows/Fonts/segoeuib.ttf","C:/Windows/Fonts/calibrib.ttf","C:/Windows/Fonts/arialbd.ttf","C:/Windows/Fonts/courbd.ttf"]}
    def tf(key, sz):
        for p in paths[key]:
            if os.path.exists(p):
                try: return ImageFont.truetype(p, sz)
                except: pass
        return ImageFont.load_default()
    return {
        "msm": tf("mono",11), "mmm": tf("mono",14), "mlg": tf("mono",18),
        "ssm": tf("sans",12), "smd": tf("sans",15), "slg": tf("sans",20),
        "bmd": tf("bold",18), "blg": tf("bold",26), "bxl": tf("bold",36),
    }

F = fonts()

def base():
    img = Image.new("RGB", (W,H), BG)
    d = ImageDraw.Draw(img)
    for x in range(0,W,32): d.line([(x,0),(x,H)], fill=DIM2)
    for y in range(0,H,32): d.line([(0,y),(W,y)], fill=DIM2)
    d.rectangle([0,0,4,H], fill=GREEN)
    return img, d

def panel(d, x,y,w,h, fill=SURFACE, border=BORDER, r=5):
    d.rounded_rectangle([x,y,x+w,y+h], radius=r, fill=fill, outline=border)

def badge(d, x,y, label, col):
    r,g,b = col
    try: bb=d.textbbox((0,0),label,font=F["msm"]); tw=bb[2]-bb[0]
    except: tw=50
    d.rounded_rectangle([x,y,x+tw+16,y+18], radius=2, fill=(r//6,g//6,b//6), outline=(r//2,g//2,b//2))
    d.text((x+8,y+3), label, fill=col, font=F["msm"])
    return tw+16

frames = []

# ── SCENE 1: Landing state – empty input ──────────────────────────────────
for _ in range(3):
    img, d = base()
    # Nav bar
    d.rectangle([0,0,W,44], fill=(10,15,18))
    d.line([(0,44),(W,44)], fill=BORDER)
    d.text((20,12), "reposhield", fill=GREEN, font=F["mlg"])
    d.text((W-130,14), "No API key needed", fill=GREEN_D, font=F["msm"])
    # Hero
    d.text((W//2, 100), "Scan any Git repo", fill=TEXT, font=F["bxl"], anchor="mm")
    d.text((W//2, 142), "for security vulnerabilities", fill=DIM, font=F["smd"], anchor="mm")
    # Input box
    panel(d, 60, 175, W-120, 52, fill=SURF2, border=BORDER)
    d.text((76, 194), "https://github.com/", fill=DIM, font=F["mmm"])
    # Cursor blink
    d.rectangle([76+200, 192, 76+202, 210], fill=GREEN)
    # Button
    panel(d, 60, 242, W-120, 48, fill=GREEN, border=GREEN, r=4)
    d.text((W//2, 266), "Start Scan", fill=BG, font=F["bmd"], anchor="mm")
    # Chips
    chips = [("Secrets","Deps","Static","Git History")]
    cx = 60
    for label in ["No API key", "Runs locally", "4 scanners", "OWASP Top 10"]:
        try: bb=d.textbbox((0,0),label,font=F["msm"]); tw=bb[2]-bb[0]
        except: tw=70
        panel(d, cx, 310, tw+20, 28, fill=SURFACE, border=BORDER)
        d.text((cx+10, 318), label, fill=DIM, font=F["msm"])
        cx += tw+30
    frames.append(img.quantize(colors=96))

# ── SCENE 2: Typed URL ────────────────────────────────────────────────────
repo_url = "https://github.com/example/webapp"
for step in range(len(repo_url)+1):
    if step % 3 != 0 and step != len(repo_url): continue
    img, d = base()
    d.rectangle([0,0,W,44], fill=(10,15,18))
    d.line([(0,44),(W,44)], fill=BORDER)
    d.text((20,12), "reposhield", fill=GREEN, font=F["mlg"])
    d.text((W-130,14), "No API key needed", fill=GREEN_D, font=F["msm"])
    d.text((W//2, 100), "Scan any Git repo", fill=TEXT, font=F["bxl"], anchor="mm")
    d.text((W//2, 142), "for security vulnerabilities", fill=DIM, font=F["smd"], anchor="mm")
    panel(d, 60, 175, W-120, 52, fill=SURF2, border=(0,150,80))
    typed = repo_url[:step]
    d.text((76, 194), typed, fill=TEXT, font=F["mmm"])
    panel(d, 60, 242, W-120, 48, fill=GREEN, border=GREEN, r=4)
    d.text((W//2, 266), "Start Scan", fill=BG, font=F["bmd"], anchor="mm")
    frames.append(img.quantize(colors=96))

# ── SCENE 3: Cloning ──────────────────────────────────────────────────────
for _ in range(2):
    img, d = base()
    d.rectangle([0,0,W,44], fill=(10,15,18))
    d.line([(0,44),(W,44)], fill=BORDER)
    d.text((20,12), "reposhield", fill=GREEN, font=F["mlg"])
    panel(d, 20, 55, W-40, H-70, fill=SURFACE)
    d.text((40,75), "Scan: https://github.com/example/webapp", fill=DIM, font=F["msm"])
    d.line([(40,98),(W-40,98)], fill=BORDER)
    d.text((40,115), "Cloning repository...", fill=GREEN_D, font=F["mmm"])
    # Progress bar
    panel(d, 40, 150, W-80, 12, fill=SURF2, border=BORDER, r=6)
    d.rounded_rectangle([40,150, 40+int((W-80)*0.25), 162], radius=6, fill=GREEN_D)
    d.text((40,175), "Fetched 847 files", fill=DIM, font=F["msm"])
    frames.append(img.quantize(colors=96))

# ── SCENE 4: Scanning progress ────────────────────────────────────────────
steps_data = [
    (0.30, "Scanning for hardcoded secrets...",           "secrets",     None),
    (0.50, "Scanning dependencies (OSV API)...",          "dependencies",("CRITICAL","lodash CVE",RED)),
    (0.70, "Static analysis (OWASP Top 10)...",           "static",      ("HIGH","shell=True",ORANGE)),
    (0.85, "Scanning git history (200 commits)...",       "git_history", ("CRITICAL","Stripe key in history",RED)),
    (1.00, "Scan complete",                               "done",        None),
]

live_findings = []

for pct, step_label, scanner, new_find in steps_data:
    if new_find: live_findings.append(new_find)
    for _ in range(2):
        img, d = base()
        d.rectangle([0,0,W,44], fill=(10,15,18))
        d.line([(0,44),(W,44)], fill=BORDER)
        d.text((20,12), "reposhield", fill=GREEN, font=F["mlg"])

        # Progress area
        panel(d, 20, 55, W-40, 130, fill=SURFACE)
        col_pct = GREEN if pct < 1.0 else GREEN
        d.text((40, 72), step_label, fill=GREEN_D if pct<1 else GREEN, font=F["mmm"])
        panel(d, 40, 105, W-80, 14, fill=SURF2, border=BORDER, r=7)
        bar_w = int((W-80)*pct)
        if bar_w > 0:
            d.rounded_rectangle([40,105,40+bar_w,119], radius=7, fill=GREEN if pct==1.0 else GREEN_D)
        d.text((W-80, 108), f"{int(pct*100)}%", fill=GREEN_D, font=F["msm"])
        d.text((40, 130), f"github.com/example/webapp", fill=DIM, font=F["msm"])

        # Live findings
        panel(d, 20, 200, W-40, H-220, fill=SURFACE)
        d.text((40, 215), "Live findings:", fill=DIM, font=F["msm"])
        d.line([(40,234),(W-40,234)], fill=BORDER)
        fy = 245
        for sev, msg, col in live_findings[-6:]:
            bw = badge(d, 40, fy+2, sev, col)
            d.text((40+bw+10, fy), msg, fill=TEXT, font=F["msm"])
            fy += 32

        # Summary mini
        if pct >= 0.5:
            panel(d, 20, H-55, W-40, 40, fill=SURF2, border=BORDER)
            counts = [("CRITICAL",RED,str(sum(1 for s,_,_ in live_findings if s=="CRITICAL"))),
                      ("HIGH",ORANGE,str(sum(1 for s,_,_ in live_findings if s=="HIGH")))]
            cx2 = 40
            for sev,col,n in counts:
                d.text((cx2, H-43), f"{n} {sev}", fill=col, font=F["msm"])
                cx2 += 150

        frames.append(img.quantize(colors=96))

# ── SCENE 5: Full results ──────────────────────────────────────────────────
all_findings = [
    ("CRITICAL", RED,    "src/config.py:14      AWS Secret Access Key"),
    ("CRITICAL", RED,    "HISTORY (commit a3f2)  Stripe live key, 6 weeks ago"),
    ("HIGH",     ORANGE, "src/routes.py:88       subprocess.run(shell=True)"),
    ("HIGH",     ORANGE, "package.json           lodash@4.17.4 CVE-2021-23337"),
    ("HIGH",     ORANGE, "src/db.py:34           SQL injection via f-string"),
    ("MEDIUM",   YELLOW, "src/crypto.py:12       hashlib.md5() for passwords"),
    ("LOW",      BLUE,   "settings.py            DEBUG=True in production"),
]
for _ in range(5):
    img, d = base()
    d.rectangle([0,0,W,44], fill=(10,15,18))
    d.line([(0,44),(W,44)], fill=BORDER)
    d.text((20,12), "reposhield", fill=GREEN, font=F["mlg"])
    d.text((W-200,14), "Scan complete", fill=GREEN, font=F["mmm"])

    # Summary bar
    panel(d, 20, 55, W-40, 60, fill=SURF2, border=GREEN)
    counts2 = [("2 CRITICAL",RED),("3 HIGH",ORANGE),("1 MEDIUM",YELLOW),("1 LOW",BLUE)]
    cx3 = 40
    for label, col in counts2:
        d.text((cx3, 78), label, fill=col, font=F["mmm"])
        cx3 += 190

    # Findings list
    panel(d, 20, 130, W-40, H-150, fill=SURFACE)
    d.text((40,148), "Findings", fill=DIM, font=F["msm"])
    d.line([(40,168),(W-40,168)], fill=BORDER)
    fy2 = 178
    for sev,col,msg in all_findings:
        bw = badge(d, 40, fy2+2, sev, col)
        d.text((40+bw+10,fy2), msg, fill=TEXT, font=F["msm"])
        fy2 += 42

    frames.append(img.quantize(colors=96))

# ── HOLD + SAVE ────────────────────────────────────────────────────────────
frames.extend([frames[-1]]*2)
frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=400, loop=0, optimize=True)
size = os.path.getsize(OUT)
if size > 2_000_000:
    q = [f.quantize(colors=64) for f in frames]
    q[0].save(OUT, save_all=True, append_images=q[1:], duration=400, loop=0, optimize=True)
print(f"demo.gif: {os.path.getsize(OUT)//1024}KB")
