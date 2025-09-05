Low-Freq Acoustic Fractals — Hex + ϕ Array (40/60 Hz)

Version: 0.1 • Mode: Tool-State • Glyphs: 🌐🔮 🌀✍♾️

⸻

1) Context / Goal
	•	You tested 40 Hz / 60 Hz using a hex array with golden-ratio (ϕ) placements → interesting interference results.
	•	Need a larger/portable test space with neighbor-safe SPL.

⸻

2) Physics quick refs
	•	Speed of sound c \approx 343\ \mathrm{m/s} (20 °C).
	•	Wavelengths:
	•	\lambda_{40} = c/40 \approx 8.575\ \mathrm{m}
	•	\lambda_{60} = c/60 \approx 5.717\ \mathrm{m}
	•	Array spacing to avoid strong grating lobes: d \lesssim \lambda/2
	•	d_{40} \lesssim 4.29\ \mathrm{m}, d_{60} \lesssim 2.86\ \mathrm{m}

Array factor (planar) for element positions \mathbf{r}n and observation direction \hat{\mathbf{u}}:
AF(\hat{\mathbf{u}}, f)=\sum{n=1}^{N} a_n\, e^{j(2\pi f/c)\,\hat{\mathbf{u}}\cdot \mathbf{r}_n + j\phi_n}
Use amplitude weights a_n and phase offsets \phi_n for beam-shaping / lobe control.

⸻

3) Geometries you can A/B

A. Hexagonal 7-pack (center + 6)
	•	Lattice vectors: \mathbf{v}_1=(d,0),\ \mathbf{v}_2=(d/2,\ d\sqrt{3}/2)
	•	Positions: center at (0,0), ring at multiples of \mathbf{v}_{1,2}.
	•	Start with d= \min(2.8\ \mathrm{m},\ \text{your space}) to cover 60 Hz safely; increase toward 40 Hz when outdoors.

B. Phyllotaxis (ϕ layout) — broadband diffusion
	•	Golden angle \theta = 137.507764^\circ
	•	Radial law r_n = a\sqrt{n} (choose a for footprint);
	•	Cartesian: x_n=r_n\cos(n\theta),\ y_n=r_n\sin(n\theta).
	•	Choose a so nearest-neighbor spacing \ge 0.6\text{–}0.8\ \mathrm{m} (indoor), scale up outdoors.
	•	Expect softer lobes, richer interference (good for “fractal” response).

⸻

4) Signal design (clean comparisons)
	•	Two-tone steady: 40 Hz + 60 Hz (check IM artifacts).
	•	Log sweep (ESS): 20–120 Hz, 30–60 s duration → deconvolve room/array response.
	•	Phase scripts: center = 0°, ring = {0°, 90°, 180°, 270°} patterns to steer/null.
	•	Amplitude taper (Dolph–Chebyshev-like at LF): outer ring gain = 0.7–0.8 to suppress sidelobes.

⸻

5) Transducers / rigs that won’t anger neighbors
	•	Tactile shakers (butt-kickers) bolted to massive platforms → minimal airborne LF, mostly structure-borne into the rig.
	•	Force-cancelling subs (back-to-back drivers on a single brace) → net reaction force ≈ 0 → less floor/neighbor coupling.
	•	Closed-box LF sources (Qtc ≈ 0.7) for tight control; keep ports out (ports leak LF far).

Mounting: 18 mm plywood tiles on sorbothane feet (isolation), each tile hosts one driver/shaker; wire tiles as nodes in your hex/ϕ grid.

⸻

6) Portable test spaces (ranked)
	1.	Open field (early hours) — best ground-truth, mark array with tape/rope; bring inverter.
	2.	Vehicle cabin (parked van/semi) — sealed cavity; good for controlled sweeps; use low power.
	3.	Inflatable/event tent with mass-loaded vinyl (MLV) skirt — temporary LF attenuation; lay EVA mats inside.
	4.	Basement/crawlspace with MLV curtain + limp-mass membrane absorbers (see §8).

⸻

7) Measurement protocol (compact)
	•	Grid: 7–13 mic points (center + ring), height ~1.0–1.2 m.
	•	Mics: 2× identical electret/USB mics; calibrate relative gain (1 kHz tone).
	•	Runs:
	1.	Hex/ϕ at in-phase (all 0°).
	2.	Add phase steering pattern.
	3.	Amplitude taper on outer ring.
	4.	Repeat at lower/higher spacing (move outer ring).
	•	Log: SPL vs frequency (ESS), spatial heatmap at 40/60 Hz, note power.

Room modes sanity (if indoors, room length L):
f_{n} \approx \frac{nc}{2L} \quad (n=1,2,\dots)
Keep array center away from room mode antinodes to reduce bias.

⸻

8) Neighbor-safe containment (LF focused)
	•	Limp-mass membrane panel: MLV sheet (≥2 kg/m²) loosely hung before a 100 mm mineral wool panel → LF absorption without strong re-radiation.
	•	Double-layer floor: plywood–MLV–plywood sandwich under the array.
	•	Force-cancelling pairs: mount drivers back-to-back; wire in parallel, invert polarity on one frame so cones move opposite, forces cancel.
	•	Duty cycle: long ESS sweeps at modest SPL beat steady 40 Hz drones (psychoacoustically less annoying).

⸻

9) Add resonant “fractal” elements (optional)

Cantor-style Helmholtz set tuned near 40/60 Hz to shape the field (absorb/redistribute):
f_H=\frac{c}{2\pi}\sqrt{\frac{A}{V L_\mathrm{eff}}},\quad L_\mathrm{eff}\approx L+1.7r
	•	Build 3–5 boxes with f_H = {38, 43, 57, 62 Hz…}; place at ϕ-ring positions between sources.
	•	Log SPL delta at target frequencies with/without boxes.

⸻

10) Quick build specs (starter)
	•	Array: 7 nodes (center + 6), tile spacing d=2.0\ \mathrm{m} indoor; d=3.0\text{–}3.5\ \mathrm{m} outdoor.
	•	Sources: small sealed 8–10″ woofers or 4–6 tactile shakers on tiles.
	•	Amp: 2-4 channels, 100–300 W/ch @ 4–8 Ω; DSP with per-channel delay/phase.
	•	Control: laptop with multi-out interface (or mini-DSP); tone/ESS generator.

⸻

11) Data schema (CSV)

Date,Site,Layout,Spacing(m),Elem,N,PhasePattern,Weighting,Freq(Hz),SPL(dB),MicX(m),MicY(m),Power(W),Notes
2025-09-06,Field,Hex,3.0,7,0/90/180,Outer0.75,40,XX.X,1.5,0.5,120,calm wind

12) What to look for
	•	Hex vs ϕ: ϕ layout should show softer lobes and smoother spatial SPL at 40/60 Hz.
	•	Phase steering: ability to move/null the 40 Hz hot-spot by 1–3 m.
	•	Tapering: sidelobe reduction ≥3–6 dB at 60 Hz.
	•	Helmholtz adjuncts: targeted dB dips at tuned frequencies without broad SPL loss.

⸻

13) Safety
	•	Hearing: limit continuous ≤85 dB at listener; use long sweeps rather than steady drones.
	•	Structural: isolate tiles; avoid exciting building modes; watch for resonance in windows/fixtures.

⸻

14) Version Log
	•	v0.1: Hex + ϕ geometries, LF array math, neighbor-safe rigs, measurement protocol.


Attempt next:

Hex/ϕ LF Array — Cut-List, DSP Presets, Helmholtz Boxes

Version: 0.1 • Mode: Tool-State • Glyphs: 🌐🔮

⸻

A) Tile Bases (7×) — Cut-List + Drill Template

Material: 18 mm plywood (void-free), M6 hardware, sorbothane feet (30–40 mm dia).
Tile size: 600 mm × 600 mm × 18 mm (Qty 7)

Drill template (origin at tile center; X right, Y up; mm)
	•	Isolation feet (4×): (±200, ±200), Ø5.5 mm pilot → M6 insert.
	•	Cable pass-through (center): (0, 0), Ø10 mm.
	•	Shaker mount (universal) (4×): (±60, ±60), Ø6.5 mm (M6 through-bolt).
	•	Optional 8″ woofer cutout: circle center (0, 0), Ø186 mm; 8 screws at radius 110 mm every 45°, Ø5 mm.
	•	Optional 10″ woofer cutout: Ø235 mm; screws at radius 130 mm every 45°, Ø5 mm.

Hardware per tile
	•	Sorbothane feet: 4×, M6 × 20 mm bolts + washers.
	•	Shaker: 4× M6 × 25–35 mm + nylocs (length per model).
	•	If woofer: 8× wood screws 4.5×25 mm or M4 T-nuts.

Notes
	•	Use either shaker or woofer pattern; do not combine on same tile.
	•	Add perimeter fillets (3–5 mm) to reduce panel ring.

⸻

B) Array Geometry (placements)

Hex 7-pack (center + 6)
	•	Ring radius R: indoor 2.0 m, outdoor 3.0 m.
	•	Ring nodes at angles: 0°, 60°, 120°, 180°, 240°, 300°.

ϕ (phyllotaxis) layout (N tiles)
	•	Golden angle θ = 137.507764°.
	•	r_n = a\sqrt{n}, x_n=r_n\cos(n\theta), y_n=r_n\sin(n\theta).
	•	Choose a so nearest-neighbor spacing ≥0.6–0.8 m indoors; 1.2–1.5 m outdoors.

⸻

C) DSP Presets — Delays & Phases (steer toward +X)

Speed of sound c=343\ \mathrm{m/s}. For a circular ring, time delay for element angle \theta_n:
\Delta t_n = \frac{R}{c}\,\bigl[\,\max(0,\cos\theta_k)\,-\cos\theta_n\,\bigr]
(Equivalent to applying the same constant offset so all channel delays ≥ 0. Reference “ring @ 0°” has 0 ms.)

Outdoor (R = 3.0 m) → R/c = 8.750\ \mathrm{ms}

Element
Angle
Delay (ms)
Phase @40 Hz
Phase @60 Hz
Center
—
8.750
126°
189°
Ring@0°
0°
0.000
0°
0°
60°
60°
4.375
63°
94.5°
120°
120°
13.125
189°
283.5°
180°
180°
17.500
252°
18° (≡ 378°)
240°
240°
13.125
189°
283.5°
300°
300°
4.375
63°
94.5°


Indoor (R = 2.0 m) → R/c = 5.833\ \mathrm{ms}

Element
Angle
Delay (ms)
Phase @40 Hz
Phase @60 Hz
Center
—
5.833
84°
126°
Ring@0°
0°
0.000
0°
0°
60°
60°
2.917
42°
63°
120°
120°
8.750
126°
189°
180°
180°
11.667
168°
252°
240°
240°
8.750
126°
189°
300°
300°
2.917
42°
63°


Amplitude taper (outer ring): start at 0.75 gain (Chebyshev-like) to reduce sidelobes.
Phase steering to other angles: replace \cos\theta_n with \cos(\theta_n-\theta_\mathrm{steer}).

⸻

D) Helmholtz Boxes (absorber/field-shaper) — Dimensions

Helmholtz frequency:
f = \frac{c}{2\pi}\sqrt{\frac{A}{V\,L_\mathrm{eff}}},\quad L_\mathrm{eff}=L+1.7r
A=\pi r^2 (circular neck), r=neck radius, L=physical tube length beyond baffle, c=343\ \mathrm{m/s}.
Stuffing: 30–50% mineral wool inside cavity to broaden bandwidth; add felt in neck for resistance.

Construction: 18 mm plywood. Internal dimensions listed. Tube protrusion accounts for 18 mm baffle thickness (i.e., cut tube so protrusion = L, not counting panel).

Targets & Builds (practical combos)

38 Hz (broad, low)
	•	Volume V: 80 L (0.08 m³) — internal 400×400×500 mm
	•	Port: 75 mm ID PVC (r = 37.5 mm ⇒ A=0.004418\ \mathrm{m^2})
	•	Required L_\mathrm{eff} ≈ 0.114 m → Tube protrusion L ≈ 50 mm (since 1.7r≈63.8 mm)
	•	Cut-list (outer dims add 2×18 mm per axis):
	•	Top/Bottom: 436×536 (2×)
	•	Front/Back: 436×400 (2×) [front has 75 mm hole]
	•	Sides: 536×400 (2×)

43 Hz
	•	Volume: 60 L (0.06 m³) — internal 400×300×500 mm
	•	Port: 75 mm ID
	•	L_\mathrm{eff} ≈ 0.119 m → Tube L ≈ 55 mm
	•	Cut-list:
	•	Top/Bottom: 436×536 (2×)
	•	Front/Back: 436×300 (2×)
	•	Sides: 536×300 (2×)

57 Hz
	•	Volume: 12 L (0.012 m³) — internal 300×200×200 mm
	•	Port: 32 mm ID (r = 16 mm ⇒ A=0.000804)
	•	L_\mathrm{eff} ≈ 0.0615 m → Tube L ≈ 34 mm (since 1.7r≈27.2 mm)
	•	Cut-list:
	•	Top/Bottom: 336×236 (2×)
	•	Front/Back: 336×200 (2×)
	•	Sides: 236×200 (2×)

62 Hz
	•	Volume: 10 L (0.010 m³) — internal 250×200×200 mm
	•	Port: 32 mm ID
	•	L_\mathrm{eff} ≈ 0.0623 m → Tube L ≈ 35 mm
	•	Cut-list:
	•	Top/Bottom: 286×236 (2×)
	•	Front/Back: 286×200 (2×)
	•	Sides: 236×200 (2×)

Build notes
	•	Seal all joints (PVA + caulk).
	•	Place light scrim over port interior to prevent fiber shedding.
	•	Start with light stuffing; increase until target dip broadens ~±3–5 Hz.
	•	Place boxes at ϕ-ring interstices between tiles; vary distance 0.3–1.0 m from nearest source.

⸻

E) Quick Test Matrix

Layout
R (m)
Pattern
Outer Gain
Notes
Hex
2.0
Delays: table above
0.75
Indoor sanity
Hex
3.0
Delays: table above
0.75
Outdoor field
ϕ
a s.t. nn≈1.2 m
same delays by nearest ring angle
0.75
Softer lobes
Hex + HH @38/43
3.0
as above
0.75
Check 40 Hz/60 Hz spatial nulls
Hex + HH @57/62
3.0
as above
0.75
Shape 60 Hz field

Log SPL maps at 40/60 Hz before/after HH boxes; target ≥3–6 dB sidelobe reduction and/or localized dips at tuned spots.

⸻

F) Safety / Practical
	•	Limit continuous LF ≤ 85 dB at listener.
	•	Use force-cancelling driver pairs or shakers on tiles to minimize neighbor coupling.
	•	Isolate tiles (sorbothane); avoid exciting room modes (stay off axial antinodes).

⸻

G) Version Log
	•	v0.1: Delivered tile cut-list + drill template, DSP delay/phase tables (2 m/3 m), and four tuned Helmholtz boxes with full cut-lists.
