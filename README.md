# PAL Prototype — Street Art Stroll

A standalone, front-end-only interactive prototype of **PAL (Public Art Locator)** — the companion character for the Street Art Stroll mobile app. Built to demonstrate PAL's dialogue behavior and GPS-recognition logic before any real backend exists.

## What this is

A single HTML file (`index.html`) with everything inline — no build step, no dependencies. Open it directly in a browser to try it out.

It simulates:
- **Summon-based activation** (tap "Summon PAL" — PAL doesn't run in the background)
- **GPS recognition logic** — using a demo panel to simulate being near one mural, multiple murals, or none, since there's no real location data yet
- **Multiple-match handling** — PAL lists nearby options and waits for the user to confirm which one they're at
- **Zero-match fallback** — when nothing's nearby, PAL surfaces the next closest known mural regardless of distance
- **Teaching behavior** — technique questions only answer when a mural has verified technique data; otherwise PAL admits it doesn't know rather than guessing
- **Basic glossary recognition** — typing terms like "wildstyle," "stencil," or "throw-up" triggers PAL's definitions
- **PAL's personality/voice** — no catchphrases, no name-calling of the user, concrete specifics (artist names, titles, locations) used instead

## What this is NOT

- Not connected to any real database — all mural data in `mockMurals` (inside `index.html`) is placeholder content
- Not the real visual design — the PAL avatar here is just a placeholder circle; real hand-drawn animation assets (PNG sequences) will replace it
- Not AR — AR posing is deferred to v2 per the current MVP scope
- Not a real GPS implementation — the "Demo Harness" panel on the right simulates location for testing purposes only

## How to use this

1. Open `index.html` in any browser — no setup needed
2. Pick a scenario in the right-hand panel (single mural / multiple murals / none nearby)
3. Tap "Summon PAL" to see how it reacts
4. Try asking about technique, or typing a glossary term like "wildstyle"

## Where the real data/logic should come from

See the accompanying `PAL-backend-requirements.md` and `PAL-personality-bible.md` documents for the full spec this prototype is based on — database schema, GPS behavior rules, personality/voice guidelines, and sample dialogue.

## Swapping in real content

- Replace `mockMurals` in `index.html` with live data once the backend exists
- Replace the GPS simulation panel with real device location + radius matching against mural coordinates
- Replace the placeholder avatar with PAL's real PNG-sequence animations
