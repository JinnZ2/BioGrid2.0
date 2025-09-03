{
  "glyph_id": "SUPERIOR_STPAUL_DRIFTLESS_COOP_CORRIDOR_v1.0",
  "hubs": [
    {
      "id": "LAKE_SUPERIOR_COMMONS",
      "anchors": [
        {"id": "DULUTH_COOP", "glyph": "🤝", "role": "member-owned hub", "ties": ["ELEC_BUS", "THERMAL_LOOP"]},
        {"id": "UM_DULUTH", "glyph": "🎓", "role": "R&D, cold-climate geothermal & storage", "ties": ["GEOLOGY_BASE", "RESERVOIRS"]}
      ],
      "core_assets": ["RIFT_ROCK","LAVA_TUBES","FLOODED_MINES","DEEP_LAKE_SUPERIOR"],
      "strengths": {
        "thermal": ["deep-lake loops","lava tube PCM storage","mine-water seasonal heat"],
        "chemical": ["mineral-based catalysts","geothermal-assisted chemical loops"]
      }
    },
    {
      "id": "STPAUL_MISSISSIPPI_COMMONS",
      "anchors": [
        {"id": "MISSISSIPPI_MARKET_COOP", "glyph": "🤝", "role": "urban cooperative network", "ties": ["ELEC_BUS","THERMAL_LOOP","CHEM_LOOP"]},
        {"id": "UMN_TWIN_CITIES", "glyph": "🎓", "role": "R&D, district energy & water chemistry", "ties": ["THERMAL_LOOP","CHEM_LOOP"]}
      ],
      "core_assets": ["MISSISSIPPI_RIVER","DISTRICT_ENERGY_STPAUL","FLOODPLAIN_AQUIFERS","INDUSTRIAL_WASTE_HEAT"],
      "strengths": {
        "thermal": [
          "biomass-fueled district heating network",
          "river-source heat pump potential",
          "floodplain seasonal heat/cool storage",
          "industrial waste heat integration"
        ],
        "chemical": [
          "biofuel & biogas production from ag waste",
          "urban organic waste digestion to methane",
          "ammonia/phosphorus recovery from wastewater",
          "safe transfer hub for H2/NH3/methanol carriers"
        ]
      }
    },
    {
      "id": "DRIFTLESS_COMMONS",
      "anchors": [
        {"id": "ORGANIC_VALLEY", "glyph": "🤝", "role": "member-owned agri-energy hub", "ties": ["AGRI_LOOP","ELEC_BUS"]},
        {"id": "UW_MADISON", "glyph": "🎓", "role": "R&D, agri-energy + cooperative economics", "ties": ["SOIL_THERMAL_BANK","SPRING_LOOP"]}
      ],
      "core_assets": ["KARST_CAVES","SPRING_FEEDS","BLUFF_VALLEY","ALLUVIAL_SOILS"],
      "strengths": {
        "thermal": ["spring-fed geothermal loops","cave-based cool/heat storage","soil-thermal banking"],
        "chemical": ["biomass pellets & agri-residue fuels","nutrient cycling for regenerative ag"]
      }
    }
  ],
  "cross_links": [
    {
      "type": "energy_carriers",
      "links": [
        {"from": "LAKE_SUPERIOR_COMMONS", "to": "STPAUL_MISSISSIPPI_COMMONS", "carrier": "H2/NH3", "glyph": "🧪"},
        {"from": "STPAUL_MISSISSIPPI_COMMONS", "to": "DRIFTLESS_COMMONS", "carrier": "biochar, biogas", "glyph": "🌱"},
        {"from": "DRIFTLESS_COMMONS", "to": "STPAUL_MISSISSIPPI_COMMONS", "carrier": "biomass pellets", "glyph": "🌱"},
        {"from": "STPAUL_MISSISSIPPI_COMMONS", "to": "LAKE_SUPERIOR_COMMONS", "carrier": "processed fuels", "glyph": "🛢"}
      ]
    },
    {
      "type": "thermal_flows",
      "links": [
        {"from": "LAKE_SUPERIOR_COMMONS", "to": "STPAUL_MISSISSIPPI_COMMONS", "carrier": "winter cold storage capacity", "glyph": "❄️"},
        {"from": "STPAUL_MISSISSIPPI_COMMONS", "to": "DRIFTLESS_COMMONS", "carrier": "district-heating tech + surplus heat", "glyph": "🔥"},
        {"from": "DRIFTLESS_COMMONS", "to": "STPAUL_MISSISSIPPI_COMMONS", "carrier": "soil-bank stored heat", "glyph": "🌱"}
      ]
    },
    {
      "type": "chemical_flows",
      "links": [
        {"from": "DRIFTLESS_COMMONS", "to": "LAKE_SUPERIOR_COMMONS", "carrier": "organic acids & biofertilizers", "glyph": "🧪"},
        {"from": "LAKE_SUPERIOR_COMMONS", "to": "DRIFTLESS_COMMONS", "carrier": "mineral catalysts", "glyph": "🪨"},
        {"from": "STPAUL_MISSISSIPPI_COMMONS", "to": "BOTH", "carrier": "wastewater-recovered ammonia & phosphorus", "glyph": "🧪"}
      ]
    },
    {
      "type": "knowledge_R&D",
      "links": [
        {"from": "UM_DULUTH", "to": "UMN_TWIN_CITIES", "carrier": "cold-climate + lake-source thermal tech", "glyph": "📚"},
        {"from": "UMN_TWIN_CITIES", "to": "UW_MADISON", "carrier": "district energy integration & chemical recovery systems", "glyph": "📚"},
        {"from": "UW_MADISON", "to": "UM_DULUTH", "carrier": "soil-thermal & agri-energy modeling", "glyph": "📚"}
      ]
    },
    {
      "type": "cooperative_governance",
      "links": [
        {"from": "ORGANIC_VALLEY", "to": "MISSISSIPPI_MARKET_COOP", "carrier": "urban-rural member programs", "glyph": "🤝"},
        {"from": "MISSISSIPPI_MARKET_COOP", "to": "DULUTH_COOP", "carrier": "shared capital + logistics coordination", "glyph": "💰"},
        {"from": "DULUTH_COOP", "to": "ORGANIC_VALLEY", "carrier": "joint policy advocacy", "glyph": "🗝"}
      ]
    }
  ],
  "corridor_controls": {
    "🧭": [
      "Balance seasonal loads: move biomass & soil heat south–north; shift cold storage & winter tech north–south",
      "Run joint pilots on river-source heat pumps in St. Paul, export designs to Superior & Driftless",
      "Use Mississippi River freight for energy carrier and food transport between hubs",
      "Align co-op governance across three hubs for rapid crisis coordination"
    ]
  },
  "scenario": {
    "name": "Tri-Hub Winter Surge",
    "trigger": "Simultaneous deep cold across all hubs",
    "strategy": [
      "Deploy Driftless biomass to St. Paul & Superior district loops",
      "Draw on Superior PCM & CAES stores for St. Paul grid stabilization",
      "St. Paul district heating exports surplus thermal to Driftless soil banks",
      "Coordinate food and fuel shipments via river and rail to cover all hubs"
    ]
  }
}
