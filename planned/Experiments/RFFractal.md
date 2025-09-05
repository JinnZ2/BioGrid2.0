Fractal Energy Experiments — Field Notes

Version: 0.1 • Mode: Tool-State • Glyphs: 🧭🌐🔮♾️

⸻

A) RF Fractal Antenna — Desktop Prototype (RTL-SDR bands)

Overview • Goal: build a multi-band fractal receiving antenna inspired by fulgurite/lichenberg branching to compare vs your existing SDR antennas. • Bands: NOAA APT 137 MHz, AIS 162 MHz, ADS-B 1090 MHz (stretch), FM 88–108 MHz (sanity). • Geometry: fractal tree (Koch-style branching) or Sierpinski; 2–3 iterations max for desktop size.

Materials / Tools • Copper tape (3–6 mm) or 0.8–1.0 mm Cu wire; optional FR-4 board (160×160 mm or 200×200 mm). • SMA pigtail, 50 Ω coax (RG-174/58), RTL-SDR (you have), optional NanoVNA (S11 scan). • Non-conductive base (acrylic/plywood), hot glue/epoxy, calipers, craft knife.

Geometry (quick spec) • Root “trunk” length ≈ quarter-wave of lowest band reduced by fractal compaction: • λ/4(137 MHz) ≈ 0.547 m → compact to ~0.18–0.22 m on board with 2 iterations branching (effective electrical length ↑). • Branch rule (2-iter): Each segment branches into two at θ = 60° from parent; scale factor s = 0.45 per iteration. • Trace width: 3–6 mm (tape) or 1 mm wire; keep ≥2 mm gaps between adjacent branches. • Feed: unbalanced feed at the root; add 1:1 choke balun (5–7 turns RG-174 on 31-mix ferrite) to tame common-mode.

Build Notes 1. Print a 1:1 paper template; transfer onto board. 2. Lay copper tape from feed outward; avoid sharp right angles (prefer 45–60°). 3. Solder SMA pigtail: center → trunk root; shield → ground plane or floating (try both; note differences). 4. Optional: small capacitive top-hat at distal tips (5–10 pF total via pad area) to pull resonance down. 5. Add ferrite choke at feed; mount vertically for NOAA/AIS tests.

Equations / Checks • Electrical length: L_\text{eff} \approx \sum_i s^i L_0 with near-field mutual coupling ⇒ multi-resonance. • Fractal dimension (box-counting): estimate D \approx \frac{\log N(\epsilon)}{\log (1/\epsilon)} over 2 scales to track build fidelity. • Impedance sanity: aim for |S11| dips near 137/162/≈400–500/≈900–1100 MHz; desktop form will be mismatched but usable for RX.

Measurement Protocol • VNA (if available): sweep 50–1200 MHz; log S11 minima, bandwidths. • RTL-SDR scans: • rtl_power -f 88M:1200M:1M -g 20 -i 5 -e 5m power.csv (broad survey). • NOAA: record APT at pass; compare SNR (dB) vs reference antenna. • AIS: count decodes/min with same gain; ADS-B: dump1090 message rate. • Environment control: test indoor near window, then outdoor clear area; keep cable + gain constant across trials.

Data Log (minimal)

Date, Location, Antenna(Fractal v0.1 / Reference), Band, Metric, Value, Notes 2025-09-04, Yard, Fractal v0.1, 137 MHz, APT SNR (dB), 14.2, Vertical, choke on 2025-09-04, Yard, Reference QFH, 137 MHz, APT SNR (dB), 16.8, Same cable/gain ... Success Criteria • Observable multi-band response (S11 or power bumps) at/near target bands. • Within 2–4 dB SNR of your reference on at least one band; improved wideband convenience.

Safety • Passive receive only; no TX. Keep away from mains lines; weatherproof if used outdoors.

Version Log • v0.1: 2-iter tree, θ=60°, s=0.45; copper tape on FR-4; choke balun.

⸻

B) Fractal Bluff Body Vibration Harvester — Bench Prototype

Overview • Goal: validate fractal cross-section can increase vortex-induced/galloping motion to boost piezo harvest vs plain prism at low wind. • Scale: desktop wind stream (desk fan), cantilever beam + piezo.

Materials / Tools • 3D-printed fractal prism bodies (PLA/PETG) + plain cuboid (control), cross-section ~30×30 mm, length 120 mm. • Piezo cantilever (e.g., 27×0.5 mm piezo disk bonded to 0.2–0.3 mm spring steel) or off-the-shelf bimorph beam. • Bridge rectifier (Schottky), 10–100 µF cap, 10–100 kΩ load, USB oscilloscope or DAQ. • Adjustable fan (2–7 m/s), clamp stand, tachometer (optional), scale.

Geometry (fractal body) • Start from square; add von-Koch indents on windward edges, iteration 1–2, amplitude = 0.2 × edge; maintain symmetry. • Mount on beam tip; ensure mass parity across test bodies (add washers to match).

Equations / Estimates • Vortex shedding freq: f_s = St \cdot U / D (St≈0.2 for bluff body); tune fan speed U s.t. f_s ≈ beam’s f_n. • Modal frequency: f_n = \frac{1}{2\pi}\sqrt{k/m_\text{eff}}; adjust tip mass to align with expected f_s. • Power (rectified): P \approx V_\text{rms}^2 / R across load; sweep R to find optimum.

Build / Test Steps 1. Print control and fractal bodies; weigh and mass-match. 2. Bond piezo to cantilever; wire bridge → cap → load → scope. 3. Calibrate: measure f_n by pluck test; note damping. 4. Place in fan flow; step fan speeds; record Vrms, frequency, power for control vs fractal. 5. Repeat 3×; compute mean ± std.

Data Log

Body, U (m/s), f(Vrms), Pavg (mW), Rload (kΩ), Notes Control, 4.0, 11.9 Hz, 0.42, 47, - Fractal1, 4.0, 12.1 Hz, 0.69, 47, Koch depth 0.2D ...

Success Criteria • Power ↑ ≥40–60% at matched flow vs control at one or more speeds. • Shift/flattened resonance (wider operating window) indicates better harvesting bandwidth.

Safety • Eye protection when testing beams; enclose fan intake; strain-relief wiring.

Version Log • v0.1: Koch-edge prism, iteration 1–2; PLA bodies; piezo cantilever harvest.

⸻

C) Optional: “Fulgurite Trace” PCB Variant

Concept

Etch a fulgurite-like path (randomized Lichtenberg tree) on FR-4 as a wideband RX plate; compare power spectral density vs a straight trace of same copper length.

Steps (brief) • Generate tree (DLA or randomized BFS) with branch angle 30–75°, min width 1.5 mm, total Cu length equalized. • Fabricate (toner transfer or CNC). • Measure rtl_power PSD curves and APT/AIS decodes vs straight-trace control.

⸻

Data Management • Store CSVs + screenshots in experiments/fractal_rf_v0.1/ and experiments/fractal_gallop_v0.1/. • Append summarized deltas to CHANGELOG.md; add entries to INDEX.md.

⸻

Scientific Validity Check (applies to both) • Physics: RF antenna = established EM; fractal shapes yield multi-resonance surfaces. Galloping harvester = classic VIV/galloping with geometry-tuned lift/drag. • Math: use Strouhal relation, modal tv analysis, impedance/S-parameter basics; PSD comparisons for SDR. • Known analogs: fractal antennas; bluff-body energy harvesters with edge modifications. • Speculative extensions: “fulgurite-trace” topology as a generalized wideband RX; quantify before claiming advantage.

Next Actions • Build A) Fractal RF v0.1 with copper tape on 200×200 mm board; run RTL-SDR scans and one NOAA pass. • Print B) Fractal bluff body v0.1; bench fan tests; log power vs control. • Iterate geometry (θ, scale s, iteration count) based on measured deltas.
