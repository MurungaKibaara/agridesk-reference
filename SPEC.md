# Field Ledger — specification

## The data

`data/data.js` sets `window.DATA` with seven arrays. The same content is in `data/*.csv`
if you want to read it. All money fields are integer cents.

```
sites        site_id, site_name, district, country, country_code
groups       group_id, group_name, site_id, formed_date
farmers      farmer_id, farmer_name, phone, group_id, enrolled_date
products     product_id, product_name, category, unit_price_cents
orders       order_id, farmer_id, season, order_date, deadline,
             principal_cents, service_fee_cents, total_due_cents
order_items  order_item_id, order_id, product_id, quantity,
             unit_price_cents, line_total_cents
payments     payment_id, order_id, payment_date, amount_cents, channel
```

The chain is: country → district → site → group → farmer → order → payment.
Roughly 2,400 farmers, 4,800 orders and 21,500 payments across three seasons.

## Rules

```
MONEY
All amounts are integer cents, already in one reporting currency.
Divide by 100 only when displaying.

ORDER TOTALS
principal_cents = sum of its order_items line totals.
service_fee_cents = 12% of principal, charged when the order is placed.
total_due_cents = principal + service fee.

PAYMENT ALLOCATION
Payments apply oldest first. Ties broken by payment_id.
Each payment clears the service fee first, then principal.
Anything left over after both are cleared is excess and does not reduce
the balance below zero.

REPAYMENT RATE
For one order: paid / total_due.
For any group of orders: sum(paid) / sum(total_due).
Never the average of the rates beneath it.

BANDS
on track   rate >= 85%
at risk    60% <= rate < 85%
critical   rate < 60%

TIMING
A payment dated on the deadline is on time.
A payment dated after the deadline is late.
```

## What the page does

A single scope at a time, with a breadcrumb showing where you are.

**Portfolio** lists the three countries. **Country** lists its districts.
**District** lists its sites. **Site** lists its groups. **Group** lists its members.
**Farmer** shows their details and their orders. **Order** shows the line items and
every payment against it, with what each payment cleared and the balance afterwards.

At every level above a single order, show: repayment rate, total due, repaid,
outstanding, farmer count, order count, and how many groups in scope are below 60%.

Every list is sorted weakest repayment first, because the reason to open this page
is to find the trouble.

Clicking a row drills in. The breadcrumb goes back up.

There is a search box that finds a farmer by name or ID from anywhere and jumps
straight to them.
