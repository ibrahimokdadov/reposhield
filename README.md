# RepoShield — AI-Powered Security Vulnerability Scanner

> Scan any public or private Git repository for secrets, vulnerable dependencies, insecure code patterns, and buried git-history leaks — then get a deep AI analysis powered by GPT-4, Claude, or Gemini.

**Live demo:** [securitychecker.whhite.com](https://securitychecker.whhite.com) &nbsp;|&nbsp; **Install:** `npx reposhield`

![RepoShield demo](demo.gif)

---

## Features

- **Secrets Detection** — regex + entropy-based scanning for hardcoded API keys, tokens, passwords, private keys, and connection strings across all file types
- **Dependency Scanning** — checks `package.json`, `requirements.txt`, `Gemfile.lock`, `Cargo.toml`, and more against the [OSV vulnerability database](https://osv.dev)
- **Static Analysis** — OWASP Top 10 pattern matching: SQL injection, XSS, command injection, path traversal, insecure deserialization, and more
- **Git History Scanning** — walks every commit in the repository history to surface secrets that were added and later removed (still present in git objects)
- **AI Deep Analysis** — sends selected source files to GPT-4 / Claude / Gemini for context-aware, human-readable vulnerability analysis
- **Multi-Provider AI Support** — bring your own API key for OpenAI, Anthropic, or Google Gemini; keys can be entered in the UI without touching config files
- **Real-time Progress** — WebSocket-powered live updates as each scanner runs
- **Severity Levels** — findings ranked as Critical, High, Medium, Low, and Info with confidence scores
- **Export Reports** — download scan results as JSON for CI/CD integration or audit trails

---

## Quick Start

### npx (Zero install)

```bash
npx reposhield scan https://github.com/owner/repo
```

No install needed — runs directly via npm. Optionally pass an AI key:

```bash
npx reposhield scan https://github.com/owner/repo --ai-key sk-...
```

---

### Docker (Recommended)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose).

```bash
git clone https://github.com/ibrahimokdadov/reposhield.git
cd reposhield

# Optional: add AI API keys (or enter them in the UI later)
cp .env.example .env
# edit .env with your preferred editor

docker-compose up
```

Open **http://localhost:3000** in your browser.

To rebuild after a code change:

```bash
docker-compose up --build
```

To stop:

```bash
docker-compose down
```

---

### Manual Setup

#### Prerequisites

| Tool | Minimum Version |
|------|----------------|
| Python | 3.9+ |
| Node.js | 18+ |
| Git | any recent version |

#### Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server (hot-reload enabled)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at **http://localhost:8000**.  
Interactive API docs: **http://localhost:8000/docs**

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

The UI will be available at **http://localhost:5173** and will proxy `/api` and `/ws` to the backend automatically.

#### One-command startup scripts

```bash
# Unix / macOS
chmod +x start.sh && ./start.sh

# Windows (Command Prompt)
start.bat
```

Both scripts check prerequisites, set up the virtual environment, install all dependencies, and start both services with log output written to `.logs/`.

---

## How It Works

RepoShield clones the target repository into an isolated temp directory, then runs five parallel analysis passes:

### 1. Secrets Scanner

Applies 80+ regex patterns covering common secret formats (AWS keys, GitHub tokens, Stripe keys, JWT secrets, SSH private keys, database URIs, etc.) combined with Shannon entropy analysis to catch high-entropy strings that look like secrets even if they don't match a known pattern.

### 2. Dependency Scanner

Parses dependency manifests for all major package ecosystems and queries the [OSV.dev](https://osv.dev) API for known CVEs and security advisories. Returns per-package vulnerability details including CVSS score, affected version range, and fix version.

Supported ecosystems:

| Ecosystem | Manifest files |
|-----------|---------------|
| npm / Node.js | `package.json`, `package-lock.json` |
| Python / PyPI | `requirements.txt`, `Pipfile`, `pyproject.toml` |
| Ruby / RubyGems | `Gemfile`, `Gemfile.lock` |
| Rust / crates.io | `Cargo.toml`, `Cargo.lock` |
| Go modules | `go.mod` |
| PHP / Composer | `composer.json`, `composer.lock` |

### 3. Static Analysis

Pattern-based scanner (no AST required) that detects insecure coding constructs across multiple languages, mapped to OWASP Top 10 categories:

- **A01 Broken Access Control** — missing authorization checks, insecure direct object references
- **A02 Cryptographic Failures** — use of MD5/SHA1, hardcoded IVs, weak ciphers
- **A03 Injection** — SQL injection, LDAP injection, OS command injection, eval/exec on user input
- **A04 Insecure Design** — debug flags left on, stack traces exposed to users
- **A05 Security Misconfiguration** — `CORS *`, debug mode, verbose error messages
- **A07 Auth Failures** — HTTP basic auth, JWT `none` algorithm, missing token validation
- **A08 Software Integrity Failures** — `eval()`, `pickle.loads()`, `deserialize()`
- **A10 SSRF** — unvalidated URL fetching with user-supplied input

### 4. Git History Scanner

Uses GitPython to iterate over every commit object in the repository. For each diff, it re-runs the secrets patterns against the added lines. This catches credentials that were committed by mistake and later removed — they remain accessible in git objects and must be considered permanently compromised.

### 5. AI Deep Analysis

After the automated scans, you can select any source files and send them to an AI provider for a holistic code review. The AI receives the file content alongside the automated findings for that file so it can provide richer context, explain the exploitability of each issue, and suggest concrete remediation steps.

Supported models:

| Provider | Models |
|----------|--------|
| OpenAI | GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo |
| Anthropic | Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku |
| Google | Gemini 1.5 Pro, Gemini 1.5 Flash |

---

## AI Provider Support

API keys can be supplied in three ways (highest priority wins):

1. **UI** — enter the key directly in the scan configuration panel; it is used for that session only and never stored on disk.
2. **`.env` file** — copy `.env.example` to `.env` at the project root and fill in the relevant key(s).
3. **Environment variables** — set `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GEMINI_API_KEY` in your shell before starting the server.

No AI key is required to run the automated scanners — AI analysis is an optional enhancement step.

---

## Supported Languages

The static and secrets scanners work on any text-based file. Language-aware pattern sets are included for:

Python · JavaScript / TypeScript · Java · Go · Ruby · PHP · C / C++ · C# · Rust · Kotlin · Swift · Shell / Bash · Terraform · Kubernetes YAML · Dockerfile · SQL

---

## Output / Reports

### Severity Levels

| Level | Description |
|-------|-------------|
| **Critical** | Confirmed secrets or exploitable RCE / auth bypass vectors |
| **High** | High-confidence vulnerability with likely exploitability |
| **Medium** | Probable issue requiring developer review |
| **Low** | Hardening suggestion or low-likelihood finding |
| **Info** | Informational — not a vulnerability, but worth noting |

Each finding includes:
- File path and line number
- Matched pattern / rule name
- Severity and confidence score
- Description and remediation advice
- (For dependencies) CVE ID, CVSS score, affected range, fix version

### Export

Click **Export JSON** on any completed scan to download the full result set. The JSON schema is stable and suitable for ingesting into SIEM tools, GitHub Actions annotations, or custom dashboards.

---

## Screenshots

![RepoShield scan in action](demo.gif)

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Backend bind address |
| `PORT` | `8000` | Backend port |
| `MAX_CONCURRENT_SCANS` | `5` | Maximum simultaneous repository scans |
| `OPENAI_API_KEY` | — | OpenAI API key |
| `ANTHROPIC_API_KEY` | — | Anthropic API key |
| `GEMINI_API_KEY` | — | Google Gemini API key |

---

## Contributing

Contributions are welcome. Please:

1. Fork the repository and create a feature branch (`git checkout -b feat/my-feature`)
2. Make your changes with tests where applicable
3. Ensure the project starts cleanly with `start.sh` / `start.bat`
4. Open a pull request with a clear description of what was changed and why

For new scanner rules, add them to the appropriate file in `backend/scanners/` and include at least one positive and one negative test case.

For bug reports or feature requests, open a GitHub issue.

---

## License

MIT
