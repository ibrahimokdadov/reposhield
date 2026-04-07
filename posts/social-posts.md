# Social Posts — RepoShield

---

## LinkedIn

### Technical
RepoShield runs four scanners on any Git repo and outputs one report.

Secrets first. The scanner has 30+ compiled regex patterns -> AWS AKIA keys, GitHub tokens, Stripe live keys, OpenAI/Anthropic API keys, JWT strings, PEM private key blocks, database URLs with passwords embedded. Actual values are redacted in the output: first four characters show, rest becomes `***REDACTED***`. Fast enough to not be the bottleneck.

Dependencies get checked against the OSV API at osv.dev in a batch call covering npm, pip, RubyGems, Cargo, Maven, NuGet, Composer, and Go modules simultaneously. CVSS scores map to critical/high/medium/low. Built-in fallback list covers the highest-severity packages when the API is unreachable.

Static analysis is about 30 OWASP rules across eight languages: SQL injection via f-strings, shell=True subprocess calls, innerHTML assignments, pickle.loads, yaml.load without SafeLoader, MD5/SHA1 usage, SSRF, XXE, path traversal. Language-filtered, so Python rules don't fire on JavaScript files.

Then there's the history pass. A secret added in commit A and removed in commit B is still fully readable in the git object store. The fourth scanner walks up to 200 commits, finds it, and tells you exactly which commit it first appeared in.

All four are local. No data leaves the machine. Add an OpenAI, Anthropic, or Gemini key and a fifth pass runs, picking the 20 most security-relevant files by name and content patterns -> auth, routes, database models, middleware -> and sending them for context-aware review. Provider auto-detected from key format.

Stack: Python FastAPI, React + Vite, WebSocket progress updates.

---

### ELI5
You wrote a secret on paper, then crossed it out.

Anyone can hold the paper to the light and read it.

Security tools usually check what's still written. RepoShield also reads the crossed-out parts -> meaning it walks your git history, not just your current files.

---

### Why we built it
The pattern I kept running into: someone pushes to GitHub, there's an API key in the history from three months back, they removed it two commits later and figured that was it. Doesn't work that way. The key sits in the git objects indefinitely.

Finding these issues meant running three or four separate tools -> different configs, different formats, different terminal windows. No single view of severity. No fix suggestions. Just a pile of output to sort through.

I wanted one tool: current files, dependencies, code patterns, commit history, all ranked by how bad the finding is. That's what this is.

---

### What makes it different
Git history scanning is where most tools cut corners or skip entirely.

RepoShield walks up to 200 commits, flags any secret that appeared at any point, shows the commit hash, and includes the exact removal command (BFG Repo Cleaner or git-filter-repo). Specific enough to act on immediately.

The dependency check covers eight ecosystems via a single OSV batch API call. No stitching together npm audit, pip-audit, and bundler-audit results separately.

And the AI pass is a fifth option, not a first requirement. You get real findings from four local scanners before you ever touch an API key.

---

### Story
A friend was about to make his Django project public. I checked the commit history before he pushed.

Six weeks earlier, he'd put a Stripe secret key directly in settings.py. He removed it two commits later and never thought about it again. The current code was clean. But the git history had the full key, right there.

The repo had been accessible for six weeks -> plenty of time for any automated scanner crawling GitHub for exposed keys to find it and try it.

History scanning is on by default partly because of that conversation.

---

## Twitter / X

### Technical
Built RepoShield: secrets (30+ patterns), CVEs via OSV, OWASP static analysis, git history. Python FastAPI + React. Runs locally, no config. Add your own AI key for a fifth pass. #security

### ELI5
You deleted the API key from the file. It's still in git history. RepoShield checks that.

### Why we built it
Running four separate security tools and manually merging the output got old enough that I just built one thing that does all of it.

### What makes it different
Most scanners don't touch git history. Deleting a secret from a file doesn't remove it from git objects. RepoShield walks up to 200 commits and finds what got "deleted."

### Story
Friend had a Stripe key in his git history for 6 weeks. He'd removed it in a commit and assumed that was enough. RepoShield would have caught it on the first scan.
