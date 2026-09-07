# Field Ledger — reference build

The finished version. Keep this one to yourself until after the session, then share it
so people can compare their build against it.

Open `index.html` directly. Nothing to install, nothing to run.

## What to demo, in order

1. Land on the portfolio. Three countries, sorted weakest repayment first.
2. Open Uganda, then its weakest district, then the weakest site in it.
3. Open a group. Members are listed weakest first, so the one dragging the group
   down is at the top.
4. Open that member. Their orders across seasons.
5. Open one order. Line items, then every payment against it, showing what each
   payment cleared and the balance after it.
6. Point at the check panel in the corner, which has been recalculating at every
   level the whole way down.
7. Use the search box to jump straight to a farmer from anywhere.

## Generating the data again

`generate.py` writes the CSVs, `tojs.py` turns them into `data/data.js`. The seed is
fixed, so re-running produces byte-identical output. Do not regenerate unless you also
replace the data in the starter repo, or the numbers people see will stop matching yours.
# agridesk-reference
