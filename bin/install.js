#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");

const SKILL_NAME = "scaffold-ai-app";
const PACKAGE_ROOT = path.resolve(__dirname, "..");
const CODEX_HOME = process.env.CODEX_HOME || path.join(os.homedir(), ".codex");
const DEFAULT_TARGET = path.join(CODEX_HOME, "skills", SKILL_NAME);

const args = process.argv.slice(2);

function usage() {
  console.log(`Usage:
  npx github:<owner>/<repo> [--target <path>] [--force]
  npx scaffold-ai-app-skill [--target <path>] [--force]

Options:
  --target <path>  Install to a custom skill directory.
  --force          Replace an existing scaffold-ai-app skill directory.
  --help           Show this help message.
`);
}

function parseArgs(values) {
  const options = { target: DEFAULT_TARGET, force: false };
  for (let i = 0; i < values.length; i += 1) {
    const value = values[i];
    if (value === "--help" || value === "-h") {
      options.help = true;
    } else if (value === "--force") {
      options.force = true;
    } else if (value === "--target") {
      const target = values[i + 1];
      if (!target) {
        throw new Error("--target requires a path");
      }
      options.target = path.resolve(target.replace(/^~(?=$|\/|\\)/, os.homedir()));
      i += 1;
    } else {
      throw new Error(`Unknown argument: ${value}`);
    }
  }
  return options;
}

function copyRecursive(source, target) {
  const stat = fs.statSync(source);
  if (stat.isDirectory()) {
    fs.mkdirSync(target, { recursive: true });
    for (const entry of fs.readdirSync(source)) {
      copyRecursive(path.join(source, entry), path.join(target, entry));
    }
    return;
  }
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(source, target);
}

function removeRecursive(target) {
  fs.rmSync(target, { recursive: true, force: true });
}

function install() {
  const options = parseArgs(args);
  if (options.help) {
    usage();
    return;
  }

  const target = path.resolve(options.target);
  if (fs.existsSync(target)) {
    if (!options.force) {
      throw new Error(`Target already exists: ${target}
Re-run with --force to replace it, or use --target <path>.`);
    }
    removeRecursive(target);
  }

  const entries = ["SKILL.md", "agents", "references", "scripts"];
  for (const entry of entries) {
    copyRecursive(path.join(PACKAGE_ROOT, entry), path.join(target, entry));
  }

  console.log(`Installed ${SKILL_NAME} to ${target}`);
  console.log("Restart your agent CLI or start a new session if the skill list has not refreshed yet.");
}

try {
  install();
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
