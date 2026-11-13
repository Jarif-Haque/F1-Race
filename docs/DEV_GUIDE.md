# F1-Race — Developer Guide & Game Reference Document

**Project:** F1-Race
**Repository:** `Jarif-Haque/F1-Race`
**Document version:** 1.0
**Status:** Reference specification — repo is currently a fresh placeholder (no code yet). This document is the source of truth for what the game is and how it should be built.

---

## 1. Project Overview

### 1.1 What is F1-Race?

F1-Race is a **Formula 1 racing game** — a fast-paced, precision-driving racing experience built around real Formula 1-style teams, cars, and circuits. The game targets the "arcade-sim" sweet spot: accessible enough for casual players to pick up and enjoy, with enough depth (tire strategy, pit stops, aerodynamics, qualifying) to satisfy racing fans and hardcore players.

### 1.2 Repository State (Important)

As of this document's creation, the repository contains:

- A single `README.md` with the title `# F1-Race`
- One `Initial commit` on `main`
- **No source code, assets, configuration, or tests yet**

This means **everything in this document is a design target, not a description of existing code**. Developers should treat this document as the blueprint: use it to plan the architecture, estimate work, and implement the game from scratch.

### 1.3 Design References

The game is inspired by the mainstream F1 video game genre (e.g., the EA SPORTS F1 series). Key reference points developers should study:

| Reference | What to learn from it |
|---|---|
| EA SPORTS F1 series (F1 22–F1 25) | Official licensing presentation, realistic circuits, team/driver roster, career mode structure, telemetry |
| F1 arcade titles (F1 Race Stars, F1 2010-era arcade modes) | Pick-up-and-play controls, simplified physics, casual fun factor |
| Generic kart/arcade racers | Item systems, drift mechanics, AI rubber-banding tuning |
| Racing sims (Assetto Corsa, iRacing) | Advanced tire/aero modeling, input fidelity, telemetry concepts |

**Goal:** "The feel of a real F1 broadcast, the accessibility of an arcade racer."

---

## 2. Game Vision

### 2.1 Core Fantasy

> *"Get in the car, hit 300 km/h down a straight, out-brake your rivals into the corner, and cross the line first — with the full spectacle of a Grand Prix weekend."*

### 2.2 Player Experience Goals

1. **Speed** — authentic F1 car velocity, sense of scale, and momentum.
2. **Skill expression** — braking points, apexes, tire management, and pit strategy matter.
3. **Spectacle** — cinematic camera, on-screen race direction, tire smoke, sparks from kerbs.
4. **Accessibility** — assists for beginners (traction control, auto-gear, drift assist), full control for veterans (all assists off).
5. **Authenticity** — real team names/liveries, real-world-style circuits, F1 rulebook (flags, penalties, pit lane rules).

### 2.3 Target Platforms

| Priority | Platform | Notes |
|---|---|---|
| Primary | **PC** (Windows/macOS/Linux) | Primary development and launch target |
| Stretch | **Consoles** (PlayStation / Xbox) | Engine choice must support porting (see §5.1) |
| Stretch | **Mobile** (later, simplified build) | Only after core PC experience is solid |

---

## 3. Core Gameplay

### 3.1 The Core Loop

```
Race Weekend
  └── Practice → Setup/Telemetry tuning
  └── Qualifying → Grid position battle
  └── Race
        ├── Lap loop: Start → Throttle → Brake → Corner → Accelerate → Repeat
        ├── Tire degradation → Pit stop decision
        ├── Battle with AI/rivals → Positions update
        └── Lap finish → Checkered flag → Results
  └── Championship points → Next event
```

A single match is **one Grand Prix weekend** (Practice → Qualifying → Race), which is the atomic gameplay unit.

### 3.2 Controls (Baseline)

| Input | Action |
|---|---|
| `W` / Up | Throttle |
| `S` / Down | Brake / Reverse |
| `A` / Left, `D` / Right | Steer |
| `Space` | Drift / handbrake |
| `Shift` (or auto) | Gear shift |
| `C` | Change camera view |
| `M` | Map / lap timing info |
| `ESC` | Pause menu |
| Gamepad (optional) | Button mapping: right trigger = throttle, left trigger = brake |

All controls must be **remappable** in settings.

### 3.3 Physics & Driving Model

The driving model is the heart of the game. Target an **arcade-sim hybrid**:

- **Vehicle dynamics:** mass, center of gravity, wheel grip, load transfer (lateral + longitudinal), downforce scaling with speed.
- **Tires:** four independent contact patches with grip curves; grip drops as tire temperature/wear rises; different compounds (soft/medium/hard) with different wear rates and top speeds.
- **Aerodynamics:** drag increases with speed; downforce increases with speed (more grip at high speed, less under braking).
- **Assists (player-configurable):**
  - Traction control (TC)
  - Stability control / anti-spin
  - Auto-gear
  - Braking assist (auto-brake to corner)
  - Drift assist / auto-counter-steer
  - Ideal line ghost/guide (offline practice only)
- **Damage model:** cosmetic + performance-affecting damage (wing deformation reduces downforce, tire punctures reduce grip, engine damage limits speed).

### 3.4 Circuits

Each track is a **closed-loop street/circuit** defined by:

- **Spline-based centerline** with width, elevation profile, and surface type (asphalt/kerbs/grass).
- **Checkpoints / sectors** for lap timing, progress tracking, and anti-cutting.
- **Pit lane** (entry, gantry, lane speed limit, exit) — pitting is gated by rules.
- **Corner data** for AI: corner entry/exit points, difficulty rating, recommended gears.
- **Track surface grip** variations (wet/dry weather affects grip per surface).

Minimum initial roster: **4–6 real-world-inspired circuits** (mix of high-speed, technical, and street tracks).

### 3.5 AI Racers

- **Skill rating** per AI driver (determines throttle confidence, braking point variance, mistake rate).
- **Personality traits:** aggressive vs. conservative overtaking, defensive lines, pit strategy aggressiveness.
- **Rubber-banding:** subtle catch-up to keep races close without making AI artificially fast (bounded so leaders still earn their position).
- **Collision behavior:** AI avoids contact where possible; takes alternate lines when blocked.

### 3.6 Race Rules & Penalties (F1 Authenticity)

- **Lap counting:** race is N laps (configurable per track, e.g., 3–5 laps for accessibility).
- **Cutting the track:** crossing outside allowed boundaries → sector time invalidated / penalty.
- **Pit lane rules:** speed limit in pit lane, overtaking prohibited; illegal pit exits penalized.
- **Flags:**
  - Yellow (no overtaking, hazard)
  - Green (resume racing)
  - Red (full neutralization / safety car)
  - Blue (lapped car must yield)
  - Checkered (finish)
- **Penalties:** time penalties / drive-throughs for collisions caused, pit infractions, ignoring flags.
- **Safety car / restarts:** pack-up behind safety car, rolling restart.
- **Weather:** dry/light rain/heavy rain with dynamic track grip, visibility, and wet tires.

---

## 4. Game Modes

| Mode | Description |
|---|---|
| **Quick Race** | Pick a circuit, pick difficulty, race immediately. The core demo experience. |
| **Championship / Career** | Multi-weekend season: accumulate points across events, car development, rival progression. |
| **Time Trial** | Solo, no AI; aim for best lap, ghost replays, leaderboards. |
| **Split / Multiplayer (later)** | Local or online races with up to N cars; netcode and anti-cheat are post-MVP scope. |
| **Free Run / Drift Challenge** | Open track, no rules; score-based drift modes (stretch goal). |

**Recommended MVP scope:** Quick Race + Time Trial + a lightweight Championship mode.

---

## 5. Technical Architecture

### 5.1 Engine Selection

Since the repo has no code, engine choice is the first technical decision. Recommended options (ranked):

1. **Unity (URP/HDRP)** — best for a small team: mature racing sample assets, C#, cross-platform to consoles/mobile, strong 2D/3D tooling, large asset pipeline. **Recommended default.**
2. **Unreal Engine** — best visual fidelity and free for revenue thresholds; heavier for a small team; C++ or Blueprints.
3. **Godot** — lightweight, open-source, great for 2D-style or stylized 3D racing; lowest tooling cost, weaker for AAA-style 3D fidelity.

Decision criteria: team size/skill, visual target, platform targets, licensing cost, and availability of vehicle/physics samples.

### 5.2 High-Level Architecture

```
F1-Race
├── Game Client (Unity/Unreal/Godot)
│   ├── Rendering layer (cars, track, HUD, cinematics)
│   ├── Gameplay layer
│   │   ├── Vehicle controller (physics, input, assists)
│   │   ├── AI driver (state machine + skill model)
│   │   ├── Race director (lap counting, flags, penalties)
│   │   ├── Pit stop manager
│   │   └── Weather manager
│   ├── Input system (keyboard/gamepad, remapping)
│   ├── Debug & telemetry tools
│   └── Asset pipeline imports (tracks, cars, audio)
├── Shared Data / Config
│   ├── Track definitions (splines, sectors, pit lane)
│   ├── Car definitions (stats, liveries, parts)
│   └── Game config (difficulty, assists, rules)
└── Backend (Phase 2+)
    ├── Auth & profiles
    ├── Leaderboards / ghost replays
    ├── Championship state
    └── Matchmaking (multiplayer)
```

### 5.3 Core Systems & Interfaces

| System | Responsibility | Key interfaces |
|---|---|---|
| `VehicleController` | Handles input → physics, assists, gear, damage | `Update(input), GetState()` |
| `TireModel` | Grip, temp, wear, compound | `Update(dt), GetGrip()` |
| `AeroModel` | Drag/downforce vs. speed | `GetForces(speed)` |
| `TrackController` | Spline, checkpoint collision, sector timing | `GetProgress()`, `CheckCheckpoint()` |
| `RaceDirector` | State machine: start grid → racing → finished; flags, penalties | `Update(dt)`, `ApplyPenalty()` |
| `AIDriver` | Steering/braking decision per AI car | `Decide(state)` |
| `PitManager` | Pit entry/exit, service time, strategy | `RequestPitStop()` |
| `WeatherManager` | Condition, rain intensity, grip modifiers | `GetGripMultiplier()` |
| `HUDManager` | Lap time, positions, minimap, tire info, flags | `Update(raceState)` |
| `InputManager` | Remapping, deadzones, device abstraction | `GetAxis()`, `GetButton()` |

### 5.4 Data Model (Conceptual)

```
Car
  - id, name, team
  - baseStats: topSpeed, acceleration, grip, braking, downforce
  - livery, parts (wing level, tire compound, brake setup)

Track
  - id, name, country
  - centerlineSpline, width, elevationProfile
  - sectors[] (checkpoint ids, timing gates)
  - pitLane { entry, exit, speedLimit }
  - cornerData[] { entry, exit, difficulty }

RaceConfig
  - laps, difficulty, assists, weather, aiCount, playerCarId

RaceState
  - cars[N] { position, lap, distance, tire, damage, pitState, time }
  - currentLap, racePhase (formation, green, yellow, finished)
  - events[] (penalties, overtakes, sectors)
```

### 5.5 Key Technical Concerns

- **Fixed timestep physics** (e.g., 60–120 Hz) with interpolation for rendering — deterministic and stable.
- **Deterministic simulation** where possible (replays, ghost comparisons).
- **Performance:** target stable 60 FPS; frustum culling, LOD for tracks, limited dynamic shadows on low-end.
- **Save system:** profile data, best laps, championship progress, settings (local + later cloud).
- **Telemetry:** log speed, RPM, gear, throttle/brake, G-forces for replay, debug, and (later) ghost/leaderboard comparison.
- **Replays:** record inputs + state snapshots (not video) for small, shareable ghost replays.

---

## 6. Art, Audio & Content

### 6.1 Art Style

- **3D, semi-realistic** — clean, high-contrast F1 aesthetic: glossy car bodies, real-world team-style liveries, vivid trackside branding.
- **Cars:** ~1:1 scale F1-style chassis; multiple liveries per car; wheel and wing detail.
- **Tracks:** hand-crafted, recognizable real-world-inspired circuits with grandstands, pit buildings, tire barriers, kerbs, and trackside objects.
- **VFX:** tire smoke, water spray, sparks, brake glow, exhaust, dynamic weather.

### 6.2 Audio

- **Engine audio:** real-engine-inspired samples with RPM-synced layering (idle → redline), gear shifts, release.
- **Environment:** tire/kerb noise, wind, ambient crowd, pit crew radio chatter.
- **UI:** menu, countdown beeps (qualifying/race start), penalty chimes, results music.
- **Radio:** pit crew voice lines for strategy, tire, and damage calls (nice-to-have).

### 6.3 Content Checklist

- [ ] 4–6 circuits
- [ ] 8–12 cars with team liveries
- [ ] 3 tire compounds × 3 weather conditions
- [ ] 10+ AI driver profiles
- [ ] HUD, menus, results screens, settings
- [ ] ~50–100 engine/environment audio assets

---

## 7. UI / UX

### 7.1 Screens

1. **Main menu** — Quick Race, Championship, Time Trial, Settings, Credits.
2. **Car select** — grid of cars with stats, liveries.
3. **Track select** — map with difficulty, lap count, weather.
4. **Race HUD**:
   - Lap counter `LAP 3/5`
   - Current lap time, best lap, sector times
   - Position `P3` + minimap with rivals
   - Tire compound + wear indicator
   - Current flag status
   - Speed / gear (optional)
5. **Pit stop screen/overlay** — service choices (tires, repairs) and timing.
6. **Results** — position list, fastest lap, points awarded, next event.
7. **Settings** — controls, assists, difficulty, graphics, audio, language.

### 7.2 UX Principles

- **Zero-load racing:** get from menu to race in under 2 minutes.
- **Readable at speed:** large, high-contrast numerals for lap/position.
- **Informative but not cluttered:** players can toggle HUD elements.
- **Clear feedback:** penalties explained on-screen; flags and warnings prominent.

---

## 8. Development Roadmap

### Phase 0 — Foundation (Weeks 1–2)
- Repo setup: license, CI, editor config, folder structure, docs.
- Engine project bootstrapped; input system + camera scaffold.
- Simple moving car on a straight track.

### Phase 1 — Core Driving (Weeks 3–6)
- Vehicle physics + input (throttle/brake/steer/gear).
- Assists system (TC, auto-gear, braking assist).
- Basic track spline, lap detection, checkpoint sectors.
- One playable circuit, 2 cars, basic AI, Quick Race loop.

### Phase 2 — Race Systems (Weeks 7–10)
- Full race director: countdown, laps, flags, penalties, pit lane + pit stops.
- Tire compounds + wear, weather (dry/rain).
- AI skill model + rubber-banding.
- HUD (lap, position, minimap, tire, flags).
- Time Trial + ghost replay.

### Phase 3 — Content & Polish (Weeks 11–14)
- Additional circuits (to reach 4–6) and cars (8–12).
- Career/Championship mode with points.
- Audio pass (engine, environment, UI, radio).
- Art polish, VFX, performance optimization, 60 FPS target.

### Phase 4 — Launch & Beyond (Weeks 15+)
- Release candidate, beta feedback loop.
- Multiplayer (split + online), leaderboards, cloud saves.
- Console porting, mobile adaptation (stretch).

### Milestone Acceptance Criteria (per phase)
- Each phase ships a **playable, internally tested build**.
- No phase begins until the previous phase's build passes a defined test checklist (e.g., "Quick Race completes a full 5-lap race without soft-locks").

---

## 9. Definition of Done (for a feature)

A feature is "done" when:

1. Implemented against this spec, with code reviewed.
2. Works on target platform at target frame rate.
3. Has test coverage for critical systems (physics, race director, pit rules).
4. Content (art/audio) integrated and matched to the design.
5. Documented (code comments + this doc updated if behavior changed).

---

## 10. Glossary

| Term | Meaning |
|---|---|
| **Apex** | The innermost point of a corner line |
| **Downforce** | Aerodynamic push pushing the car into the track, increasing grip |
| **Drive-through** | A penalty requiring the car to enter and exit the pit lane without stopping |
| **Ghost** | Recorded replay of a run used for comparison in time trial |
| **Kerb** | Raised track edge; driving over it reduces grip |
| **Pit stop** | Stopping in the pit lane for tires/repairs/setup changes |
| **Rubber-banding** | AI speed adjustment to keep races close |
| **Sector** | Track split into timing zones for lap/sector time validation |
| **Safety car** | Vehicle that paces the field at reduced speed after incidents |
| **Telemetry** | Vehicle data (speed, RPM, G-forces, inputs) captured for analysis |

---

## 11. Next Actions for the Team

1. **Confirm engine choice** (§5.1) and set up the project scaffold.
2. **Review this spec** and mark up open questions (e.g., exact car/track licensing, platform targets, visual target).
3. **Break Phase 0–1 into tasks** in the tracker (GitHub Issues recommended).
4. **Agree on MVP scope**: Quick Race + Time Trial + 1–2 tracks + 4 cars.

*Questions or change requests should be filed as issues and this document updated to stay the source of truth.*
