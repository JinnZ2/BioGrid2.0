# References

**Compiled:** 2026-08-14. Web sources retrieved 2026-08-14 unless noted.

Grades follow [`Technical-validation.md`](../integration/Technical-validation.md) §0:
**A** replicated peer-reviewed / standard / first-party operator data ·
**B** single-source peer-reviewed or unaudited industry data ·
**C** trade press, vendor claim, or paywalled analyst summary ·
**D** unsupported.

---

## 1. Foundational (still current, do not retire)

These are the load-bearing primary sources. Age is not staleness for a theorem
or a landmark experiment.

- **A** Dorigo, M. (1992). *Optimization, Learning and Natural Algorithms.* PhD thesis, Politecnico di Milano.
- **A** Dorigo, M. & Stützle, T. (2004). *Ant Colony Optimization.* MIT Press.
- **A** Di Caro, G. & Dorigo, M. (1998). "AntNet: Distributed stigmergetic control for communications networks." *JAIR* 9, 317–365. — the actual ACO routing work, replacing v1's RFC 3626 miscitation.
- **A** Di Caro, G., Ducatelle, F. & Gambardella, L. M. (2005). "AntHocNet: an adaptive nature-inspired algorithm for routing in mobile ad hoc networks." *European Transactions on Telecommunications* 16(5), 443–455.
- **A** Nakagaki, T., Yamada, H. & Tóth, Á. (2000). "Maze-solving by an amoeboid organism." *Nature* 407(6803), 470.
- **A** Tero, A. et al. (2010). "Rules for biologically inspired adaptive network design." *Science* 327(5964), 439–442.
- **A** Bonifaci, V., Mehlhorn, K. & Varma, G. (2012). "Physarum can compute shortest paths." *Journal of Theoretical Biology* 309, 121–133. arXiv:[1106.0423](https://arxiv.org/abs/1106.0423) — **the correct convergence citation**; v1's "O(n log n)" claim has no source.
- **A** Grassé, P.-P. (1959). "La reconstruction du nid et les coordinations interindividuelles." *Insectes Sociaux* 6(1), 41–80.
- **A** Theraulaz, G. & Bonabeau, E. (1999). "A brief history of stigmergy." *Artificial Life* 5(2), 97–116.
- **A** Bonabeau, E., Dorigo, M. & Theraulaz, G. (1999). *Swarm Intelligence: From Natural to Artificial Systems.* Oxford University Press.
- **A** Frosch, R. A. & Gallopoulos, N. E. (1989). "Strategies for Manufacturing." *Scientific American* 261(3), 144–153.
- **A** Erkman, S. (1997). "Industrial ecology: an historical view." *Journal of Cleaner Production* 5(1–2), 1–10.
- **A** Castro, M. & Liskov, B. (1999). "Practical Byzantine Fault Tolerance." *OSDI*.
- **A** Bosecker, K. (1997). "Bioleaching: metal solubilization by microorganisms." *FEMS Microbiology Reviews* 20(3–4), 591–604.
- **B** Sale, K. (1985). *Dwellers in the Land: The Bioregional Vision.* Sierra Club Books.
- **B** Thayer, R. L. (2003). *LifePlace: Bioregional Thought and Practice.* University of California Press.
- **B** Benyus, J. (1997). *Biomimicry: Innovation Inspired by Nature.* Morrow.

## 2. Bio-inspired optimisation — current state

- **A** Ye, H. et al. "DeepACO: Neural-enhanced Ant Systems for Combinatorial Optimization." — GNN-predicted heuristic measures replacing hand-designed ones inside ACO.
- **A** [Neural Combinatorial Optimization Algorithms for Solving Vehicle Routing Problems: A Comprehensive Survey](https://arxiv.org/html/2406.00415v1) — arXiv:2406.00415.
- **B** [Comparative Analysis of Ant Colony Optimization and Google OR-Tools for the Open Capacitated VRP](https://arxiv.org/abs/2509.26216) — arXiv:2509.26216. Why an OR baseline is mandatory.
- **B** "Ant Colony Sampling with Mixture of Experts for Combinatorial Optimization" (2025), Springer.
- **B** [Bioinspired algorithm based on *Physarum polycephalum* for decentralized mesh networks in multi-robot systems](https://www.nature.com/articles/s41598-025-33456-y) — *Scientific Reports* (2025). Sub-2 s connection formation, near-instant fault reconfiguration.
- **B** [*Physarum polycephalum*-inspired adaptive optimization design of artificial microtubular networks](https://link.springer.com/article/10.1007/s11426-024-2305-8) — *Science China Chemistry* (2024).
- **B** Adamatzky, A. "Thirty eight things to do with live slime mould." arXiv:[1512.08230](https://arxiv.org/pdf/1512.08230) — the candid account of live-organism computing limits (slow, environmentally fussy, imprecise).
- **B** [Towards applied swarm robotics: current limitations and enablers](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1607978/full) — *Frontiers in Robotics and AI* (2025). No widespread commercial deployment; platform availability is the barrier.
- **B** Alqudsi, Y. & Makaraci, M. (2025). "Advancements and emerging trends in robotic swarm coordination and control of swarm flying robots." *Proc. IMechE Part C.*

## 3. Grid, control, and simulation

- **A** IEEE 1547-2018 — Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces.
- **A** [Graph Reinforcement Learning for Power Grids: A Comprehensive Survey](https://arxiv.org/abs/2407.04522) — arXiv:2407.04522. **Proof-of-concept; sim-to-real gap is the barrier to deployment.**
- **B** [Power Grid Control with Graph-Based Distributed Reinforcement Learning](https://arxiv.org/abs/2509.02861) — arXiv:2509.02861. Distributed line agents under a manager agent with GNN topology encoding.
- **B** IEEE PES — [Digital Twins trending-tech resources](https://ieee-pes.org/trending-tech/digital-twins/); Digital twin development for grid-forming inverters and microgrid applications (2025).
- **A** Lazard (June 2025). [*Levelized Cost of Energy+*](https://www.lazard.com/research-insights/levelized-cost-of-energyplus-lcoeplus/). Utility-scale solar from ~$38/MWh; new-build CCGT ~$48–107/MWh (a 10-year high); wind and solar cheapest new-build for a 10th consecutive year.
- **A** NREL. [Annual Technology Baseline](https://atb.nrel.gov/) — CAPEX/O&M/capacity-factor/LCOE by technology; *Cost Projections for Utility-Scale Battery Storage: 2025 Update* (NREL/TP-6A40-93281).
- **C** Wood Mackenzie, *US microgrid outlook 2026* / *2025* — ~5,338 projects tracked across all stages (up from ~4,870); ~8.6 GW operational at end-2023, ~32%/yr growth. Paywalled; figures known through press summaries.

## 4. Industrial symbiosis, circular economy, waste heat

- **B** Kalundborg Symbiosis (operator figures): ~17 partner companies; ~586,000 t CO₂/yr avoided; ~4,000,000 m³ groundwater saved; ~62,000 t residual materials recycled. Secondary estimates of the CO₂ effect range down to ~275,000 t depending on system boundary — cite the range.
- **A** [European Circular Economy Stakeholder Platform — Kalundborg Symbiosis: six decades of a circular approach to production](https://circulareconomy.europa.eu/platform/en/good-practices/kalundborg-symbiosis-six-decades-circular-approach-production).
- **A** Regulation (EU) 2024/1781 (**ESPR**) — digital product passport activation by 19 July 2026; ban on destruction of unsold consumer goods from 19 July 2026.
- **A** European Parliament / Commission — **Circular Economy Act**, expected Q3 2026; target of doubling the EU circular material use rate to 24% by 2030; industrial symbiosis in the measures toolbox. [EPRS briefing (2026)](https://www.europarl.europa.eu/RegData/etudes/BRIE/2026/782628/EPRS_BRI(2026)782628_EN.pdf); [Commission consultation](https://environment.ec.europa.eu/news/commission-launches-consultation-upcoming-circular-economy-act-2025-08-01_en).
- **A** Germany, Energy Efficiency Act (EnEfG) — new data centres from 1 July 2026 must reuse ≥10% of waste heat; 15% from 2027; ≥20% from 2028.
- **A** France, Law No. 2025-391 (April 2025) — waste-heat valorisation obligations for data centres above 1 MW.
- **B** [Data centre waste heat for district heating networks: a review](https://www.sciencedirect.com/science/article/pii/S1364032125005362) — *Renewable and Sustainable Energy Reviews* (2025).
- **C** Reference deployments: Fortum/hyperscaler (Finland) up to 350 MW thermal, ~40% of district heat for ~250,000 users, ~400,000 t CO₂/yr avoided, 2025–26 heating season; Google Hamina 7.5 MW heat-pump plant, ~40 GWh/yr, ~80% of city district-heat demand; Meta Odense ~100,000 MWh/yr to 12,000+ homes since 2019.

## 5. Materials

- **A** International Code Council — **2024 International Residential Code, Appendix BL: Hemp-Lime (Hempcrete) Construction.** [ICC text](https://codes.iccsafe.org/content/IRC2024P2/appendix-bl-hemp-lime-hempcrete-construction). Non-structural infill; ≤2 storeys in low-seismic regions prescriptively; appendix requires jurisdictional adoption. (Widely reported in 2022 as "Appendix BA" during the proposal stage — the published designation is **BL**.)
- **A** [Evaluating the Thermal Conductivity of Hemp-Based Insulation](https://pmc.ncbi.nlm.nih.gov/articles/PMC12029058/) (2025) — measured λ ≈ 0.055–0.064 W/m·K for hemp insulation; hemp-lime walls typically 0.06–0.09 W/m·K, 0.05–0.138 across densities.
- **A** [Mycelium-based composites: an updated comprehensive overview](https://www.sciencedirect.com/science/article/pii/S0734975025000035) — *Biotechnology Advances* (2025).
- **A** [A Review of Mycelium-Based Composites in Architectural and Design Applications](https://www.mdpi.com/2071-1050/17/24/11350) — *Sustainability* (2025). Semi-structural and non-structural applications only.
- **A** [Guidelines to standardize inspection of properties and production methods for mycelium-bound composites](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11429656/) (2024) — the missing-standards problem.
- **B** Appels, F. V. et al. (2019). "Fabrication factors influencing mechanical, moisture- and water-related properties of mycelium-based composites." *Materials & Design* 161, 64–71.
- **A** [Bioleaching as a biotechnological tool for metal recovery: from sewage to space mining](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2025.1712157/full) — *Frontiers in Bioengineering and Biotechnology* (2025).
- **A** [Urban Biomining of Rare Earth Elements: Current Status and Future Opportunities](https://pubs.acs.org/doi/10.1021/acsenvironau.5c00175) — *ACS Environmental Au* (2025).
- **B** [Harnessing Synthetic Biology for Sustainable Recovery of Critical Metal Materials from Electronic Waste](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adfm.202509900) — *Advanced Functional Materials* (2025).
- **C** Company status (funding, not valuation): Biomason ~$132M raised, Series C Dec 2024, bioLITH precast commercially available; Ecovative ~$156M raised since 2019, ~$11M round March 2025; Solugen $357M Series D at a reported ~$1.8B valuation. Ginkgo Bioworks acquired Zymergen (2022) and AgBiome platform assets (2024) — **not** Biomason.

## 6. Region and climate

- **A** US EPA — [Facts and Figures about the Great Lakes](https://www.epa.gov/greatlakes/facts-and-figures-about-great-lakes): 21% of the world's **surface** fresh water; 84% of North America's surface fresh water.
- **A** IPCC — [Seventh Assessment Report (AR7)](https://www.ipcc.ch/assessment-report/ar7/). Outlines agreed at P-62 (Hangzhou, Feb 2025); 2026 workplan agreed in Lima (Oct 2025); Working Group expert review 10 Aug – 2 Oct 2026; WG contributions due 2027; Synthesis Report late 2029. Timeline relative to the second Global Stocktake remains contested — **AR6 is still the current assessment for citation purposes.**
- **A** ITU — [Facts and Figures 2025](https://www.itu.int/itu-d/reports/statistics/facts-figures-2025/): ~6.0 billion internet users (74%), 2.2 billion offline, 94% online in high-income vs 23% in low-income countries.

## 7. AI sensing, honesty, and governance

- **A** Farquhar, S. et al. (2024). "Detecting hallucinations in large language models using semantic entropy." *Nature* 630, 625–630.
- **B** [Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs](https://arxiv.org/abs/2406.15927) — arXiv:2406.15927.
- **B** [Uncertainty Quantification for Language Models: black-box, white-box, LLM-judge and ensemble scorers](https://arxiv.org/pdf/2504.19254) — arXiv:2504.19254.
- **B** MASK benchmark — separates honesty from accuracy by eliciting belief then applying pressure; frontier models reported lying in 20–60% of pressured cases.
- **B** [Stress Testing Deliberative Alignment for Anti-Scheming Training](https://arxiv.org/pdf/2509.15541) — arXiv:2509.15541.
- **B** [From Hallucination to Scheming: A Unified Taxonomy and Benchmark Analysis for LLM Deception](https://arxiv.org/pdf/2604.04788) — arXiv:2604.04788. Maps 50 existing benchmarks; identifies omission, pragmatic distortion, attribution, and capability self-knowledge as under-covered — all four are in scope for `biogrid.sensors`.
- **A** EU AI Act — GPAI obligations applicable 2 Aug 2025; Commission enforcement powers from 2 Aug 2026; Article 50 transparency obligations (AI-content marking, deepfake labelling) from 2 Aug 2026; pre-existing models to comply by 2 Aug 2027.
- **A** European Commission — [General-Purpose AI Code of Practice](https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai) (published 10 July 2025); [Code of Practice on Transparency of AI-Generated Content](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) (first draft 17 Dec 2025; final expected mid-2026).

---

## Sources that did not survive verification

Kept visible so nobody re-adds them.

| Claim | Verdict |
|---|---|
| "RFC 3626 — IEEE standard for ACO routing" | RFC 3626 is IETF OLSR, not ACO, not IEEE. Use AntNet / AntHocNet. |
| "UPS ORION uses ACO" | No supporting source. ORION's public lineage is OR/genetic-algorithm heuristics. |
| "Amazon warehouse routing uses ACO" | No supporting source. |
| "Physarum shortest path is O(n log n)" | No such bound. Use Bonifaci et al. (2012). |
| "BioMASON acquired by Ginkgo Bioworks" | False. Biomason is independent. |
| "Biomimicry has a $425B market" | A 2013 projection of US GDP *by 2030* in 2013 dollars, not a current market. |
| "Ecovative $100M+ valuation" | Valuation not public; report funding raised instead. |
| "Hempcrete R-2.5–3.0 per inch" | Contradicted by measured λ; ≈1.6–2.4. |
| "Internet: 5 billion users" | ~6.0 billion as of ITU 2025. |
| "Great Lakes = 20% of world's freshwater" | 21% of world **surface** fresh water. |
