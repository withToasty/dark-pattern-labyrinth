#!/usr/bin/env node
// Bumps the shared cache-busting "?v=" query string on every <link>/<script>
// tag in index.html in one shot, instead of hand-editing each tag.
//
// Usage:
//   node scripts/bump-version.js            # bumps to the current date (YYYYMMDD)
//   node scripts/bump-version.js 20260920-2 # bumps to an explicit version string

const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(indexPath, 'utf8');

const current = html.match(/\?v=([^"]+)"/);
if (!current) {
  console.error('No ?v= version string found in index.html');
  process.exit(1);
}

const next =
  process.argv[2] ||
  new Date()
    .toISOString()
    .slice(0, 10)
    .replace(/-/g, '');

const updated = html.replace(/\?v=[^"]+"/g, `?v=${next}"`);
const count = (html.match(/\?v=[^"]+"/g) || []).length;

fs.writeFileSync(indexPath, updated);
console.log(`Bumped ${count} tag(s) from ?v=${current[1]} to ?v=${next}`);
