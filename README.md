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
- Not the real visual design — PAL's frames are generated placeholder shapes (see below); real hand-drawn PNG sequences replace them 1:1
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


## PAL animation assets (PNG sequences)

PAL plays PNG frame sequences from `assets/pal/`. One subfolder per animation state:

```
assets/pal/<state>/frame_01.png
assets/pal/<state>/frame_02.png
...
```

**Naming rules:** lowercase state folder names exactly as listed below; frames numbered with two digits starting at `01`, no gaps.

| State folder | Used for | Loops? | Wired in prototype? |
|---|---|---|---|
| `idle` | resting loop (fidgets play every few loops) | yes | yes |
| `idle_fidget_1`, `idle_fidget_2` | small idle variations | no | yes |
| `wake` | summon entrance | no | yes |
| `sleep` | dismiss / "zzz" button (holds last frame) | no | yes |
| `listening` | user is typing | yes | yes |
| `thinking` | processing / looking something up | yes | yes |
| `alert` | multiple murals nearby | no | yes |
| `found` | matched a mural | no | yes |
| `searching` | no murals in range, fallback | yes | yes |
| `teaching` | sharing a verified fact/technique | no | yes |
| `defining_term` | explaining slang/terminology | no | yes |
| `uncertain` | honest "I don't know" | no | yes |
| `welcome_back_short`, `welcome_back_long` | returning user | no | not yet (needs accounts) |
| `warm_recognition` | revisiting a favorite artist/piece | no | not yet (needs memory) |
| `mural_changed` | flagging a changed/repainted mural | no | not yet (needs flag flow) |
| `error` | no GPS / lookup failed | no | not yet |

### Swapping in real art
1. Export each animation from Callipeg as a PNG sequence (transparent background).
2. Name the files `frame_01.png`, `frame_02.png`, ... and drop them into the matching state folder, replacing the placeholders.
3. If a state has a different number of frames than 6, update `frames` (and `fps` if desired) for that state in the `palManifest` object near the top of the script in `index.html`.

The placeholder generator (`generate_placeholder_assets.py`, needs Python + Pillow) can be re-run to restore the placeholders, but it will overwrite any real frames in those folders, so don't run it after adding real art.

### Why the manifest is hardcoded
`palManifest` lives in `index.html` rather than a JSON file because browsers block `fetch()` of local files when a page is opened directly from disk. Plain `<img>` loading works fine, so this keeps the prototype double-click-to-open. A real app can load this from anywhere.
