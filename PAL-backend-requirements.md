# PAL — Backend & Functionality Requirements
### For the Street Art Stroll mobile app (RiNo MVP)

This document outlines what the Public Art Locator (PAL) feature needs from the backend/database to function. It's meant as a starting point for technical scoping — happy to adjust anything here based on what makes sense on the implementation side.

---

## 1. Overview

PAL is an animated, text-based companion character in the mobile app. Users summon PAL on demand (tap to activate), and it helps them discover nearby murals via GPS, learn about artists and techniques, and builds a light memory of their favorites over time. Full creative/personality spec is covered in the separate PAL Personality Bible — this document focuses on what PAL needs technically.

**MVP scope:** RiNo only. Core PAL (GPS recognition, Q&A, memory, teaching) — AR posing and games/trivia are deferred to v2.

---

## 2. Data Structure Needed

### `Murals` table
Core content, shared source of truth with the website.

| Field | Notes |
|---|---|
| `mural_id` | Unique identifier |
| `title` | |
| `location_name` | Business the mural is painted on |
| `address` | Cross-streets, for display/reference |
| `latitude`, `longitude` | **Required** — this is what GPS recognition depends on entirely |
| `image_url(s)` | Ties to the existing photo gallery |
| `year_completed` | |
| `description` | Combined artist/mural text, however it's currently structured on the site — PAL can reference this as-is |
| `artist_id` | Links to `Artists` table; may need to support multiple artists per mural |
| `techniques[]` | **New field.** Verified techniques used (e.g. stencil, freehand, wildstyle) — array, since a piece can use more than one. This must be manually verified, not inferred, since PAL will reference it directly in unprompted commentary |
| `status` | `active` / `updated` / `repainted` / `flagged-for-review` / `removed` (see section 4) |
| `previous_mural_id` | Nullable — links a `repainted` entry back to what was previously at that location, preserving history |
| `last_verified_date` | |

### `Artists` table

| Field | Notes |
|---|---|
| `artist_id` | |
| `name` | |
| `bio` | May be empty if bio is already embedded in the mural's `description` field instead |
| `links[]` | Social/website links |

### `Users` table (accounts)

| Field | Notes |
|---|---|
| `user_id`, account basics | |
| `favorite_artists[]`, `favorite_murals[]` | |
| `visited_murals[]` | Powers "welcome back" and recognition behavior |
| `last_active_date` | Drives how PAL greets a returning user (short vs. long absence) |

**Note:** PAL does **not** address users by name directly (decided against this) — no display name needs to be surfaced to PAL's dialogue layer, though the account still needs one for login/profile purposes as normal.

---

## 3. PAL-Specific Tables (separate from core site data)

These support PAL's behavior but aren't part of the website's own content — kept distinct since they evolve independently (grow from user interaction, not site content edits).

### `PALKnowledge`

| Field | Notes |
|---|---|
| `mural_id` | |
| `teachable_facts[]` | Curated list of facts PAL can bring up unprompted — this is **separate from** `techniques[]`. PAL draws from both, since some teachable facts may not fit cleanly as a "technique" |
| `open_questions[]` | Things users have asked that PAL didn't know — reviewed and answered over time, feeding back into `teachable_facts` |

### `MuralFlags` (admin review queue)

| Field | Notes |
|---|---|
| `flag_id` | |
| `mural_id` | |
| `trigger_source` | `pal_visual` or `user_report` |
| `submitted_photo_url` | Nullable |
| `timestamp` | |
| `report_count` | Increments if multiple independent reports come in before resolution |
| `resolved` (boolean), `resolved_date` | |

---

## 4. Mural Status & Change Detection

A mural's `status` field drives both PAL's behavior and the admin review flow:

- **`active`** — normal, fully usable by PAL
- **`updated`** — minor touch-up/refresh; same mural entry, fields just updated
- **`repainted`** — confirmed as a new artwork at the same location; creates a **new** `Murals` entry, linked via `previous_mural_id` to preserve the old record rather than overwriting it
- **`flagged-for-review`** — a report came in (from PAL's own visual mismatch detection or a user report), pending admin verification
- **`removed`** — mural is gone, no replacement yet

**Flow:** PAL's visual recognition or a user report → logs a `MuralFlags` entry → admin reviews (ideally seeing the submitted photo + current mural info side by side) → admin resolves by updating status accordingly → PAL's knowledge is current again automatically, since it reads live data (see section 5).

**Escalation suggestion:** 2+ independent reports on the same unresolved mural could bump it in review priority.

---

## 5. Sync Behavior

**No separate sync job is needed.** Because PAL only checks for nearby murals on-demand (when the user taps to summon it — not continuous background checking), PAL can simply query the live `Murals`/`Artists` data directly each time. As long as PAL reads from the same database the website/admin tools write to, there's nothing to keep "in sync" — it's a single source of truth by construction.

`PALKnowledge` and `Users` data are separate from this and update independently based on in-app interactions, not website content edits.

---

## 6. GPS Recognition Behavior (functional spec)

- **Trigger:** On-demand only, when the user taps to summon PAL. No continuous or periodic background location polling.
- **Matching:** Check mural coordinates against the user's current location within a radius (suggested starting point ~50–75m, pending real-world testing against actual RiNo mural density — some blocks may need tighter tuning).
- **Multiple matches:** If more than one mural is within range, PAL lists all nearby options; the user taps to confirm which one they're at (avoids misidentification risk).
- **Zero matches:** If nothing is within the normal radius, PAL falls back to surfacing the next closest known mural regardless of distance (no hard secondary radius cutoff).

---

## 7. Platform & Delivery Notes

- **Platform:** iOS only for MVP (native build), already approved for the App Store, TestFlight MVP planned.
- **PAL's character animations** (PNG sequences, originally animated as looping GIFs in Callipeg) are static assets bundled directly in the app — not pulled from the backend, since they're fixed character states, not dynamic content.
- **Mural content** (images, descriptions, metadata) is the dynamic part that needs to come from the live backend.
- Since the app will offer account sign-in, note that **Sign in with Apple** is required by App Store guidelines if any other third-party login option is offered.

---

## 8. Open Items / To Confirm

- Final confirmation of GPS radius size once real RiNo mural coordinates are available for testing
- Whether `teachable_facts` curation is managed through the same admin interface as mural edits, or a separate lightweight tool
- Exact auth/account approach (email, Apple Sign-In, etc.)
