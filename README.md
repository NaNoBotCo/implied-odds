# Implied Odds

A plain-spoken explainer of implied odds in Texas Hold'em, in a country voice, with the
arithmetic left in and a calculator you can poke.

**Live:** https://nanobotco.github.io/implied-odds/

## The whole thing, dirt simple

1. **Pot odds** is the price the pot lays you right now: what you'd win against what it costs to call.
2. A draw hits some fraction of the time. Count your outs, and that fraction has a number.
3. If the pot pays worse than the draw needs, the naked call loses money.
4. **Implied odds** count the money you'll pull off the other feller on later streets when you hit.
5. Add that future money and a losing call can turn into a winner — *if* you actually get paid.
6. Over the long run it's the average that matters, not any one hand.

## What's on it

- **The example hand** — the nut flush draw, drawn as cards.
- **A live calculator** — pick your draw (flush, straight, gutshot, custom outs), say whether
  you're on the flop or the turn, set the pot, the bet and the villain's stack, and it computes:
  the chance you hit (exact, off the real card counts), the pot odds, and whether the call is a
  call on pot odds alone, a call on implied odds, or a fold — with the arithmetic printed out.
- **An outcomes-over-time chart** — your chips over 150 plays of the same spot: the expected
  line plus five runs of pure luck. A **dial** sets how much you drag off the villain on the
  river when you hit; turn it and watch the expected line tip from going broke to getting paid.
- **The gotchas** — you gotta get paid, loud draws pay less, and reverse implied odds.
- **The outs cheat-sheet** — the common draws, their outs, and the rules of 2 and 4.

## The math

- **Hit probability.** One card to come: `outs / 47`. Two cards to come:
  `1 − C(47−outs, 2) / C(47, 2)` — the exact chance of missing both, subtracted from one.
- **Pot odds.** After a bet `B` into a pot `P`, you call `B` to win `P + B`. Break-even needs
  `p ≥ B / (P + 2B)`.
- **Implied odds.** The extra `X` you need to win on the river to break even solves
  `p · (P + B + X) = (1 − p) · B`, so `X = (1 − p)·B / p − (P + B)`.
- **Outcomes over time.** Per hand, `EV = p · (pot + payoff) − (1 − p) · call`. The chart plots
  `n · EV` against `n`, with the payoff set by the dial; the luck runs are a seeded coin-flip
  per hand so they hold still while you turn the dial.

Every figure is computed in the page. Nothing is hard-coded.

## Licensing

- **Text and the page** in `docs/` — [CC BY 4.0](LICENSE). Credit: "Nan · hongdam.net · CC BY 4.0".
- **Code** (the calculator and chart script) — [MIT](LICENSE-CODE).

See [NOTICE.txt](NOTICE.txt).
