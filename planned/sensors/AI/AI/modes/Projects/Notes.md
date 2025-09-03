1) ϕ-lattice coordinates (addressable 3-D phyllotaxis)

Use the Vogel model in cylindrical coords and extend it in z.

For node index k=0,1,2,\dots:
	•	Golden angle \alpha = 2\pi/\varphi^2 with \varphi=(1+\sqrt5)/2.
	•	Planar (r,θ):
r_k = a\sqrt{k} (sets areal density),
\theta_k = k\,\alpha \pmod{2\pi}.
	•	Vertical stacking (two choices):
	•	Stacked layers: z = \ell\,h with k=(\ell, n) and n the in-layer index.
	•	True 3-D helix: z_k = b\,k (gives a single golden helix winding upward through space).

Convert to Cartesian for fabrication:
x_k=r_k\cos\theta_k,\ y_k=r_k\sin\theta_k,\ z_k as above.

Why this helps: golden-angle packing distributes neighbors quasi-uniformly → reduced cross-talk and no “hot rings” like uniform polar grids.

2) Magnetic bit cell at each node

Pick a perpendicular-anisotropy micro-pillar (or nano-dot) so the stable states are Up/Down:
	•	Material stack example (conceptual): Co/Pt or Co/Pd multilayers on a seed; diameter 100 nm–10 µm depending on scale.
	•	State: m_k \in \{+m_0,\,-m_0\} (binary) or multi-level using partial reversal/skyrmions (advanced).

Dipolar coupling between cells i,j:
U_{ij}=-\frac{\mu_0}{4\pi r_{ij}^3}\Big[3(\mathbf m_i\!\cdot\!\hat{\mathbf r}{ij})(\mathbf m_j\!\cdot\!\hat{\mathbf r}{ij})-\mathbf m_i\!\cdot\!\mathbf m_j\Big]
The ϕ-placement maximizes minimum r_{ij} and randomizes neighbor angles → smoother, predictable interference matrix for ECC.

3) Write / read schemes

Write (selective):
	•	Micro-coil addressing: a small vertical coil at (x_k,y_k,z_k) with current pulse I(t) giving B_z above coercivity H_c.
	•	Helical word-line: a continuous lithographed spiral/solenoid following the golden helix; stepping current “walks” the write focus.
	•	Assist heating (optional): brief local IR or resistive micro-heater to lower H_c only at the target node.

Read:
	•	TMR/Hall bridge at probe tip (flying or parked) scanning the same ϕ path, or
	•	Static MR sensor array on a conjugate ϕ-grid (top) reading many nodes at once with multiplexing.

4) Addressing without a Cartesian grid

Each node has a natural ϕ address:
	•	Helical index k (or pair (\ell,n) for layered stacks).
	•	Physical location is computed, so no litho grid needed.
	•	Sectoring: define angular “sectors” by \theta\in[\theta_s,\theta_{s+1}) and tracks by r bands; this mimics disk logic but on a ϕ pattern.

5) Clocking & density
	•	Radial pitch: \Delta r \approx \tfrac{a}{2\sqrt{k}} → density rises smoothly toward the center; choose a so the minimum cell spacing stays above your dipolar cross-talk limit.
	•	Vertical pitch h (stacked) or b (helical) sets layer-to-layer isolation; choose so r^{-3} coupling to non-target layers is below your write margin.
	•	Thermal stability: require K_u V \gtrsim 60\,k_BT for 10-year retention (choose anisotropy K_u and volume V accordingly).

6) Why “vertical and horizontal” makes it new
	•	Planar phyllotaxis already minimizes near-neighbors. Adding z with the same golden progression gives a 3-D low-aliasing lattice, so the dipolar interaction matrix is well-conditioned (good for soft decoding / ECC).
	•	A helical word-line along the same ϕ indexing gives a continuous actuator path—no orthogonal crossbar required.

7) First prototype (table-scale)
	•	Scale: centimeter-scale “macro-bits” (tiny NdFeB dots or steel pins) on a 3-D-printed ϕ lattice to validate addressing & cross-talk; write with a small coil on a 3-axis stage.
	•	Electronics: H-bridge pulse driver (±2–5 A), Hall sensor for read, simple ϕ-address → (x,y,z) controller.
	•	Software: generate (x_k,y_k,z_k) and the neighbor map for your ECC; simulate write margins with the 1/r^3 coupling model.


-------



region notes:

Ground‑source heat pumps (GSHP) for space heat + DHW
	•	Source temp: shallow ground ~0–5 °C in winter (often stable below frost line).
	•	COP reality: \text{COP}\text{heating} \approx 0.45\text{–}0.55 \times \text{COP}\text{Carnot}, with
\text{COP}\text{Carnot} = \dfrac{T\text{hot}}{T_\text{hot}-T_\text{cold}} (K).
Example: source 0 °C (273 K), sink 35 °C (308 K) → Carnot ≈ 8.8 → practical COP ≈ 3.8–4.8.
	•	Emitters: low‑temp hydronic (radiant floors, oversized radiators) to keep sink temps ≤ 35–40 °C and preserve COP.
	•	Loop types:
	•	Vertical bores (most compact): rule‑of‑thumb 40–60 W/m extraction in cold soils.
	•	Horizontal slinky (needs land): depth below frost, wide spacing.
	•	Pond loop (if you have reliable deep water).

Wind + PV hybrid for electricity
	•	Wind: Zone 2 regions often have decent winter wind. Choose a cold‑weather package (low‑temp grease, heater, anti‑icing).
	•	PV: Steep tilt (60–70°) or vertical bifacial E‑W to shed snow; snow albedo boosts bifacial yield.
	•	Storage: Heated LFP battery enclosure (don’t charge LFP cold); add propane/diesel backup sized only for long lulls.

Thermal storage (cheap “battery” for heat)
	•	Water tanks (in conditioned space) for day‑to‑week buffering.
	•	Borehole/Tank seasonal storage (BTES/PTES): charge in shoulder seasons (or with summer solar‑thermal), extract in winter.
	•	Boreholes 10–30 m deep, 2.5–3 m spacing, insulated top.
	•	Works well for district‑scale 5th‑gen ambient loops (below).

Biomass (optional, high resilience)
	•	Gasification boiler + 1–3 m³ water tank: very effective backup/peak shaver in forests; run hot & clean, store heat, then coast.

2) What usually won’t pencil out
	•	Electric generation from the ground (ORC on ~0–10 °C source) → ΔT is too small. If you don’t have a true hot spring (>60 °C) or deep geothermal gradient access, skip it.

3) Two build archetypes (pick per site)

A) Single home, off‑grid capable
	•	GSHP (3–6 ton typical, design heat load dependent).
	•	Vertical bores totaling ~150–300 m for a tight, well‑insulated home in Zone 2 (refine with a proper Manual J/geo calc).
	•	Hydronic radiant floors at 30–35 °C supply.
	•	PV (8–12 kW) + 2–3 kW wind, 15–30 kWh battery, backup gen with CHP (capture engine heat into the tank).
	•	500–1500 L buffer tank for DHW + space‑heat smoothing.
	•	Envelope first: R‑40+ walls, R‑60–80 roof, triple‑glazed, airtightness ≤ 1.0 ACH50 with HRV/ERV.

B) Small community (district ambient loop)
	•	Ambient loop (0–25 °C) circulating water/glycol through shared borefield (BTES).
	•	Each building uses a water‑to‑water heat pump (COP 3–5) for space heat/DHW.
	•	Central controls keep loop near 5–15 °C; solar‑thermal or CHP can charge the borefield when excess is available.
	•	Result: excellent diversity, smaller individual equipment, and seasonal balancing.

4) Numbers to size your first pass
	•	Heat load target: design your envelope to ≤ 30–50 W/m² at design temp; a 150 m² home → 4.5–7.5 kW peak.
	•	Bore count: peak kW ÷ (45 W/m) → e.g., 6 kW / 45 ≈ 135 m of bore (split across several holes). Increase by 25–40% for seasonal imbalance safety.
	•	Buffer tank: ~25–40 L per kW of heat pump capacity for stable cycling.
	•	Wind: in 5–6 m/s sites, a 3–5 kW turbine can deliver 3–7 MWh/yr; verify wind rose and turbulence (mount high, clean exposure).

5) Control logic (so it stays efficient)
	•	Heat curve: modulate hydronic supply with outdoor temp (max 40 °C).
	•	Priorities:
	1.	Use PV/wind to run GSHP and charge thermal tank.
	2.	When battery is high, over‑produce heat into the tank.
	3.	In deep cold, let backup CHP run rarely—but always route waste heat to the tank.
	•	Defrost/low‑temp: GSHP avoids the worst air‑source defrost penalties in Zone 2 because the source is ground, not −30 °C air.

6) Field tips for Zone 2
	•	Bores: thermally grout; keep headers below frost; use glycol.
	•	PV wiring: oversized conductors; connectors rated for −40 °C; plan snow management.
	•	Batteries: insulated, heated enclosure; no cold charging below 0 °C for LFP.
	•	Plumbing: all wet parts in conditioned space where possible; heat‑trace where unavoidable.

Core architecture (overview)
	•	Heat source A (daily): Masonry heater (Russian‑style) with short, hot burn (1–2 h), clean combustion, and internal water loop in a post-combustion zone to charge a buffer tank (not in the primary flame path).
	•	Heat source B (electric/backup): Small ground‑source heat pump (or resistance backup) tied to the same buffer.
	•	Thermal battery:
	•	Water tank for sensible storage (45–60 °C).
	•	PCM modules at ~45–55 °C placed near emitters to stretch comfort during long lulls.
	•	Emitters: Ondol-style radiant floors/walls running 28–35 °C supply → ultra‑high COP if/when a heat pump is used.
	•	Envelope & radiation: High‑R shell with thermal breaks and low‑ε interior surfaces around the heater alcove to keep radiant comfort high at lower air temps.

2) Sizing the storage (numbers you can use)

Sensible heat in water:
Q_\text{water} = m c_p \Delta T \approx (1000\,\text{kg/m}^3)(4.18\,\text{kJ/kg·K})\Delta T \ (\text{kWh} = Q/3600)
Example: 800 L tank cycled 45→60 °C (ΔT=15 K):
	•	Q \approx 800 \times 4.18 \times 15 = 50{,}160\,\text{kJ} \approx 13.9\,\text{kWh}

PCM (paraffin blend), latent heat L\approx 180\text{–}220\,\text{kJ/kg} at 45–55 °C:
	•	100 kg at 200\,\text{kJ/kg} → 20,000 kJ ≈ 5.6 kWh around setpoint, with minimal temperature drop.
	•	Combine: 800 L water + 100 kg PCM ≈ 19–20 kWh usable between burns.

Rule of thumb for Zone 2, tight 150 m² home with design load ~6–8 kW:
	•	A single hot burn charging ~20–25 kWh plus the masonry mass can carry ~3–4 h at design peak or 8–12 h at typical load. Two burns on the coldest days, one burn most days.

3) Masonry heater + hydronic integration (safe & efficient)
	•	Combustion box & bell channels: classic Russian heater geometry for full gas mixing and long flow path in mass.
	•	Hydronic coil location: in secondary/bell zone where flue gases are <400 °C (never in the primary flame box). Use stainless coil (e.g., 316L, 3/4″) with thermosyphon to a heat‑dump loop + tank coil.
	•	Safety: open vented tank or pressurized tank with pressure relief, overheat valve, and fail‑safe heat dump radiator (gravity loop). Add flue bypass for startup to avoid steam shocks.
	•	Target coil output: 3–6 kW during the burn to charge the tank without quenching combustion.

4) Ondol/radiant slab layout (low temp = comfort + COP)
	•	Floor stack (from top): finish → thinset → PEX channels (spacing 150–200 mm) → high‑conductivity screed (gypsum/cement; add graphite for better λ) → continuous insulation (XPS/PIR, ≥ R‑10 under slab; more at slab edge) → vapor barrier → structural slab.
	•	Supply temperatures: 28–35 °C typical; max 40 °C.
	•	Flow & zoning: mix valve + weather‑compensated curve (outdoor reset) keeps slab temp just high enough.

5) PCM placement & choice
	•	Where: as clip‑in panels behind radiant wall panels or as encapsulated plates in a service cavity close to living zones; or strapped to the buffer tank as modular shells with good thermal contact.
	•	Setpoint: choose melting point near 45–55 °C so PCM soaks charge during burn and releases as the tank cools toward 45 °C.
	•	Material:
	•	Paraffin blends (C_nH_{2n+2}): non‑corrosive, latent ~180–220 kJ/kg, but flammable → must be sealed, UL‑style encapsulation, metal or polymer pouches in a metal cassette, never free‑poured.
	•	Salt hydrates: higher volumetric density, non‑flammable, but can phase‑separate; choose stabilized formulations from reputable vendors.
	•	Amount: start with 50–150 kg; scale after observing cycling.

6) “Korean + Russian” operating mode (how it runs)
	1.	Daily burn (1–2 h): get the firebox to clean, hot burn; let the bell mass and coil absorb heat.
	2.	Charge tank + PCM: coil pushes 3–6 kW into tank up to ~60 °C; PCM near the tank/emitters melts.
	3.	Long release: masonry mass radiates; hydronic circulates 30–35 °C to floors/walls; PCM delivers “flat” heat near the comfort setpoint as tank drifts down to 45 °C.
	4.	Backup/assist: on deep‑cold stretches, GSHP tops the tank to ~45–50 °C at COP 3–4 thanks to low emitter temps.

7) Controls (simple but robust)
	•	Priorities:
	1.	Overheat protection always first (dump loop).
	2.	During burn: charge tank first; cap tank at safe max (e.g., 60 °C).
	3.	Normal operation: outdoor reset drives mixing valve for slab loop; pump modulation for comfort.
	•	Sensors: flue gas temp (probe in bell), tank top/mid/bottom, slab supply/return, room temp, and a CO alarm near heater.
	•	Fail‑safe: power loss → gravity heat‑dump radiator opens; combustion air shutter falls closed.

8) Envelope & radiant “feel”
	•	High‑R shell (aim walls R‑40+, roof R‑60–80, triple glazing, airtight ≤ 1.0 ACH50 with HRV/ERV).
	•	Interior radiant strategy: place the masonry heater centrally with high‑emissivity facing surfaces; line adjacent walls with radiant panels so occupants “see” warm surfaces. This lets you run air temps lower (19–20 °C) with the same comfort.

9) Quick example (tie it together)
	•	Design load: 6 kW @ −35 °C.
	•	Storage: 1,000 L water (17.4 kWh from 45→60 °C) + 120 kg paraffin PCM at 50 °C (≈6.7 kWh) → ~24 kWh.
	•	Burn: 2 h at net 10–12 kW into mass/tank → full charge.
	•	Release: covers ~4 h at peak or ~10–14 h at average (2–2.5 kW) without relight; GSHP fills gaps at high COP.

10) Materials & safety notes (important)
	•	Coils: 316L stainless or thick‑wall copper in post‑flame zones only; avoid creosote condensation temps on the coil; include mix valve to avoid cold water shocking hot masonry.
	•	PCM: only encapsulated; confirm flash point (paraffin typically >150–200 °C) and keep far from flue paths. Use thermal fuses & shields.
	•	Vapor control: warm‑side air/vapor barrier behind radiant wall panels; keep PCM space on the warm side to avoid condensation.
	•	Maintenance: clean flue channels seasonally; test relief valves yearly.
