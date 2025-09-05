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
