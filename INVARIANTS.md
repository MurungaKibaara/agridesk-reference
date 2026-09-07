# Invariants

Things that must be true whatever the code ends up looking like.
Write the code so these hold, then make the page check them and show the result.

```
I1  Every payment is fully accounted for.
    For each payment: cleared_fee + cleared_principal + excess == payment amount.
    No cents appear or vanish.

I2  No balance is ever negative.
    Overpaying an order leaves a balance of zero, never less.

I3  Every order's totals reconcile to its own lines.
    sum(line_total_cents) == principal_cents
    principal_cents + service_fee_cents == total_due_cents

I4  A scope equals the sum of its children.
    The total due shown for a district is exactly the sum of the totals due
    for its sites. Same for every level of the chain.

I5  Repayment rate is weighted by value owed.
    A district's rate is sum(paid) / sum(due) across all its orders.
    It is not the mean of its sites' rates. Those two numbers are different
    whenever the sites are different sizes, and the mean is the wrong one.
```

I4 and I5 are the ones worth caring about. They hold for every possible input rather
than for one example, which is what makes them useful: they catch the cases nobody
thought to test.
