# AGENTS.md

## What this project is

Field Ledger: a single-page dashboard over an agricultural input-credit portfolio.
Farmers in groups at sites take seasonal packages on credit and repay in instalments.
The dashboard drills from the whole portfolio down to an individual payment.

## Non-negotiables

- One file, `index.html`. No framework, no build step, no package.json, no CDN scripts.
- Load data with `<script src="data/data.js"></script>`, which sets `window.DATA`.
  Never use `fetch()` for the CSVs. The page must work opened directly from disk.
- Money is ALWAYS integer cents. Never floats, never `parseFloat` on money.
  Divide by 100 only at the moment of display.
- Dates are plain `YYYY-MM-DD` strings. Compare them as strings.
  Never construct a `Date` object for comparison.
- Pure functions for every calculation, kept separate from anything that touches the DOM.
- Build all lookups and rollups once at startup. Do not scan 21,000 payments inside a render loop.

## Conventions

- Plain modern JavaScript in one `<script>` block. No transpiling.
- Descriptive names. Comment why, never what.
- No silent catches. If something can fail, show it on the page.
- Keyboard reachable: rows that navigate are focusable and respond to Enter.

## Design

- Restrained, dense, and legible. This is a working ledger, not a marketing page.
- Colour carries meaning and nothing else. Repayment bands only:
  on track >= 85%, at risk 60-85%, critical < 60%.
- Palette: ground `#e9edf0`, surface `#fff`, ink `#16283c`, muted `#5b7185`,
  rule `#d2dae1`, on-track `#1f7a63`, at-risk `#b06a12`, critical `#98302f`.
- System font stack only. No Google Fonts, no webfonts. The venue wifi is not to be trusted.
- Tabular numerals on every figure: `font-variant-numeric: tabular-nums`.
- No gradients, no drop shadows on cards, no rounded pill badges, no emoji.

## Domain vocabulary

- **Site** — a field location. Belongs to a district, which belongs to a country.
- **Group** — a farmer group at a site. Repayment is tracked at group level.
- **Order** — one seasonal input package taken on credit by one farmer.
- **Principal** — the cost of the inputs in an order.
- **Service fee** — 12% of principal, charged upfront, cleared before principal.
- **Repayment rate** — repaid divided by owed. At every level above a single order this is
  ALWAYS weighted by value owed, never the mean of the rates below it.

## When you are unsure

Ask. Do not guess a business rule. State the ambiguity and wait.
