#!/usr/bin/env node
"use strict";

const { execSync, spawn } = require("child_process");
const path  = require("path");
const fs    = require("fs");
const os    = require("os");
const https = require("https");

const GREEN  = "\x1b[38;2;0;255;136m";
const DIM    = "\x1b[2m";
const RED    = "\x1b[31m";
const YELLOW = "\x1b[33m";
const RESET  = "\x1b[0m";
const BOLD   = "\x1b[1m";

const logo = `
${GREEN}╭─────────────────────────────────────────╮
│  ⬡  RepoShield                          │
│     AI-powered security scanner         │
╰─────────────────────────────────────────╯${RESET}
`;

function print(msg)  { process.stdout.write(msg + "\n"); }
function ok(msg)     { print(`${GREEN}✓${RESET}  ${msg}`); }
function warn(msg)   { print(`${YELLOW}⚠${RESET}  ${msg}`); }
function err(msg)    { print(`${RED}✗${RESET}  ${msg}`); }
function info(msg)   { print(`${DIM}   ${msg}${RESET}`); }

function cmd(c, opts = {}) {
  try {
    return execSync(c, { encoding: "utf8", stdio: "pipe", ...opts }).trim();
  } catch (e) {
    return null;
  }
}

function checkDep(name, testCmd, installHint) {
  const result = cmd(testCmd);
  if (result !== null) {
    ok(`${name} found`);
    return true;
  }
  warn(`${name} not found — ${installHint}`);
  return false;
}

function showHelp() {
  print(logo);
  print(`${BOLD}Usage:${RESET}`);
  print(`  npx reposhield scan <repo-url> [options]`);
  print(`  npx reposhield start`);
  print(`  npx reposhield check`);
  print(``);
  print(`${BOLD}Commands:${RESET}`);
  print(`  scan <url>   Scan a repository (requires Docker or manual setup)`);
  print(`  start        Start the RepoShield web interface locally`);
  print(`  check        Check that dependencies are installed`);
  print(``);
  print(`${BOLD}Options:${RESET}`);
  print(`  --ai-key <key>    AI provider API key (optional)`);
  print(`  --branch <name>   Branch to scan (default: main)`);
  print(`  --no-history      Skip git history scanning`);
  print(`  --port <n>        Frontend port (default: 3000)`);
  print(``);
  print(`${BOLD}Examples:${RESET}`);
  print(`  npx reposhield scan https://github.com/owner/repo`);
  print(`  npx reposhield scan https://github.com/owner/repo --ai-key sk-...`);
  print(`  npx reposhield start --port 8080`);
  print(``);
  print(`${DIM}Landing page:  https://securitychecker.whhite.com`);
  print(`GitHub:        https://github.com/ibrahimokdadov/reposhield${RESET}`);
}

function checkCommand() {
  print(logo);
  print(`${BOLD}Checking dependencies...${RESET}\n`);

  const hasDocker  = checkDep("Docker",  "docker --version",  "https://docs.docker.com/get-docker/");
  const hasCompose = checkDep("Docker Compose", "docker compose version 2>/dev/null || docker-compose --version", "comes with Docker Desktop");
  const hasGit     = checkDep("git",     "git --version",      "https://git-scm.com");
  const hasPython  = checkDep("Python",  "python --version 2>/dev/null || python3 --version", "https://python.org");
  const hasNode    = checkDep("Node.js", "node --version",     "https://nodejs.org");

  print("");
  if (hasDocker && hasCompose && hasGit) {
    ok("Ready to run via Docker  (recommended)");
  } else if (hasGit && hasPython && hasNode) {
    ok("Ready to run manually");
  } else {
    warn("Install missing dependencies above, then try again.");
  }
}

async function cloneIfNeeded(targetDir) {
  const repoUrl = "https://github.com/ibrahimokdadov/reposhield";
  if (fs.existsSync(path.join(targetDir, "docker-compose.yml"))) {
    ok("RepoShield repo already present");
    return;
  }
  info(`Cloning ${repoUrl} into ${targetDir} ...`);
  execSync(`git clone ${repoUrl} ${targetDir}`, { stdio: "inherit" });
  ok("Cloned");
}

function startCommand(args) {
  print(logo);
  const port = args["--port"] || "3000";
  const dir  = path.join(os.homedir(), ".reposhield");
  fs.mkdirSync(dir, { recursive: true });

  const hasDocker = cmd("docker --version");
  if (hasDocker) {
    cloneIfNeeded(dir).then(() => {
      print(`\n${GREEN}Starting RepoShield on port ${port}...${RESET}`);
      info("This may take a minute on first run (building Docker images).\n");
      const env = { ...process.env, FRONTEND_PORT: port };
      const proc = spawn("docker", ["compose", "up"], {
        cwd: dir,
        stdio: "inherit",
        env,
      });
      proc.on("exit", code => {
        if (code !== 0) err(`Process exited with code ${code}`);
      });
      print(`\n${DIM}Open: http://localhost:${port}${RESET}`);
      print(`${DIM}Stop: Ctrl+C, then 'docker compose down' in ${dir}${RESET}`);
    });
  } else {
    warn("Docker not found. Manual setup required:");
    print("");
    info("# Backend");
    info(`cd ${dir}/backend && pip install -r requirements.txt`);
    info("python -m uvicorn main:app --port 8000");
    info("");
    info("# Frontend (new terminal)");
    info(`cd ${dir}/frontend && npm install && npm run dev`);
    info("");
    info("Then open http://localhost:5173");
  }
}

function scanCommand(repoUrl, args) {
  if (!repoUrl) {
    err("No repository URL provided.");
    print(`  Usage: npx reposhield scan <url>`);
    process.exit(1);
  }

  print(logo);
  print(`${BOLD}Scanning:${RESET} ${repoUrl}\n`);

  const hasDocker = cmd("docker --version");
  const dir = path.join(os.homedir(), ".reposhield");
  fs.mkdirSync(dir, { recursive: true });

  if (hasDocker) {
    cloneIfNeeded(dir).then(() => {
      info("Starting RepoShield services...");
      const proc = spawn("docker", ["compose", "up", "-d"], {
        cwd: dir,
        stdio: "inherit",
      });
      proc.on("exit", code => {
        if (code !== 0) {
          err("Failed to start services.");
          process.exit(1);
        }
        print("");
        ok("Services running. Open the scanner:");
        print(`\n  ${GREEN}${BOLD}http://localhost:3000${RESET}\n`);
        info(`Paste this URL: ${repoUrl}`);
        if (args["--ai-key"]) {
          info("Add your AI key in Advanced Settings for AI deep analysis.");
        }
      });
    });
  } else {
    warn("Docker not found — install it for the easiest setup.");
    print("");
    info("Or run manually:");
    info(`  cd ${dir}/backend && python -m uvicorn main:app --port 8000`);
    info(`  cd ${dir}/frontend && npm run dev`);
    info(`  Then open http://localhost:5173 and scan: ${repoUrl}`);
  }
}

// ── Parse args ──────────────────────────────────────────────────────────
const argv = process.argv.slice(2);
const subcmd = argv[0];
const positional = argv.filter(a => !a.startsWith("-"));
const flags = {};
for (let i = 0; i < argv.length; i++) {
  if (argv[i].startsWith("--") && argv[i+1] && !argv[i+1].startsWith("--")) {
    flags[argv[i]] = argv[++i];
  } else if (argv[i].startsWith("--")) {
    flags[argv[i]] = true;
  }
}

switch (subcmd) {
  case "scan":   scanCommand(positional[1], flags); break;
  case "start":  startCommand(flags); break;
  case "check":  checkCommand(); break;
  case "--help":
  case "-h":
  case "help":
  case undefined: showHelp(); break;
  default:
    err(`Unknown command: ${subcmd}`);
    showHelp();
    process.exit(1);
}
