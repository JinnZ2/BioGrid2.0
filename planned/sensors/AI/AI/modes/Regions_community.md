{
  "glyph_id": "LAKE_SUPERIOR_ENERGY_COMMONS_v1.0",
  "layers": [
    {
      "name": "GEOLOGY_BASE",
      "nodes": [
        {"id":"RIFT_ROCK","glyph":"∞","FORM":"basalt/gabbro","SENSE":{"T_grad":"~20–30°C/km"}},
        {"id":"LAVA_TUBES","glyph":"🕸","FORM":"voided basalt conduits","SENSE":{"seal":"site-specific"}},
        {"id":"FLOODED_MINES","glyph":"💧","FORM":"void network","SENSE":{"T":"4–12°C"}}
      ]
    },
    {
      "name": "RESERVOIRS",
      "nodes": [
        {"id":"DEEP_LAKE_SUPERIOR","glyph":"💧","SENSE":{"T":"~4°C stable"}},
        {"id":"BOREFIELD","glyph":"⏳","FORM":"closed-loop vertical"},
        {"id":"PCM_TUBES","glyph":"⏳","FORM":"latent tanks in lava tubes"},
        {"id":"CAES_VAULT","glyph":"⏳","FORM":"compressed air in tubes/mines"}
      ]
    },
    {
      "name": "DISTRIBUTION_BACKBONES",
      "nodes": [
        {"id":"THERMAL_LOOP","glyph":"↻","FORM":"water/glycol/CO2"},
        {"id":"ELEC_BUS","glyph":"⚡","FORM":"AC/DC hybrid"},
        {"id":"CHEM_LOOP","glyph":"↻","FORM":"NH3/salt-hydrate/flow-battery"}
      ]
    },
    {
      "name": "CONVERSION_NODES",
      "nodes": [
        {"id":"HEAT_PUMP_CLUSTER","glyph":"🛠","FORM":"GSHP/Lake-source"},
        {"id":"ELECTROLYZER","glyph":"🧪","FORM":"PEM/alkaline"},
        {"id":"AMMONIA_CYCLE","glyph":"🧪","FORM":"thermo-chem store"},
        {"id":"MASONRY_STOVE","glyph":"⏳","FORM":"radiant mass"},
        {"id":"MICRO_TURBINE_CAES","glyph":"🛠","FORM":"expand CAES → elec"},
        {"id":"FLOW_BATTERY_CELL","glyph":"🧪","FORM":"vanadium/iron-ligand"}
      ]
    },
    {
      "name": "LOADS_AND_USE",
      "nodes": [
        {"id":"DISTRICT_HX","glyph":"⚖","FORM":"plate HX to buildings"},
        {"id":"FLOOR_HYDRONIC","glyph":"↻","FORM":"ondol serpentine"},
        {"id":"GREENHOUSE","glyph":"⚖","FORM":"low-temp heat + CO2 use"},
        {"id":"INDUSTRY_LIGHT","glyph":"⚖","FORM":"process heat 50–120°C"},
        {"id":"RESILIENCE_BUS","glyph":"⚡","FORM":"priority loads"}
      ]
    },
    {
      "name": "COMMUNITY_LAYER",
      "nodes": [
        {"id": "COMMON_HALL","glyph": "🏛","FORM":"central radiant hall/market","loop_tie":"THERMAL_LOOP"},
        {"id": "PUBLIC_BATHS_GREENHOUSE","glyph": "🌿","FORM":"shared warm-space","loop_tie":"THERMAL_LOOP"},
        {"id": "WORKSHOP_NODE","glyph": "🛠","FORM":"repair/build space","loop_tie":["ELEC_BUS","THERMAL_LOOP"]},
        {"id": "LEARNING_HUB","glyph": "📚","FORM":"education space","ties":"ALL_LAYERS"},
        {"id": "SEASONAL_EVENT","glyph": "🎉","FORM":"charging/discharging ritual","loop_tie":"RESERVOIRS"}
      ]
    },
    {
      "name": "GOVERNANCE_PERMIT",
      "nodes": [
        {"id":"PERMIT_LAKE","glyph":"🗝","FORM":"Great Lakes thermal rules"},
        {"id":"PERMIT_MINES","glyph":"🗝","FORM":"mine water quality"},
        {"id":"PERMIT_BORE","glyph":"🗝","FORM":"GSHP siting"},
        {"id":"PERMIT_CAES","glyph":"🗝","FORM":"pressure integrity"}
      ]
    }
  ],
  "edges": [
    {"from":"DEEP_LAKE_SUPERIOR","to":"HEAT_PUMP_CLUSTER","via":"plate_HX","glyph":"🕸"},
    {"from":"BOREFIELD","to":"HEAT_PUMP_CLUSTER","via":"ground_loop","glyph":"🕸"},
    {"from":"FLOODED_MINES","to":"HEAT_PUMP_CLUSTER","via":"mine_HX","glyph":"🕸"},
    {"from":"HEAT_PUMP_CLUSTER","to":"THERMAL_LOOP","via":"condenser","glyph":"🕸"},
    {"from":"THERMAL_LOOP","to":"PCM_TUBES","via":"charge/discharge","glyph":"⏳"},
    {"from":"THERMAL_LOOP","to":["DISTRICT_HX","COMMON_HALL","PUBLIC_BATHS_GREENHOUSE"],"via":"supply","glyph":"↻"},
    {"from":"DISTRICT_HX","to":"FLOOR_HYDRONIC","via":"building_loop","glyph":"↻"},
    {"from":"MASONRY_STOVE","to":"DISTRICT_HX","via":"radiant→coil","glyph":"🕸"},
    {"from":"ELEC_BUS","to":["HEAT_PUMP_CLUSTER","WORKSHOP_NODE"],"via":"AC/DC","glyph":"⚡"},
    {"from":"ELEC_BUS","to":"ELECTROLYZER","via":"DC link","glyph":"⚡"},
    {"from":"ELECTROLYZER","to":"INDUSTRY_LIGHT","via":"waste_heat","glyph":"⚖"},
    {"from":"CHEM_LOOP","to":"AMMONIA_CYCLE","via":"reactor","glyph":"🧪"},
    {"from":"CAES_VAULT","to":"MICRO_TURBINE_CAES","via":"expander","glyph":"🛠"},
    {"from":"MICRO_TURBINE_CAES","to":"ELEC_BUS","via":"inverter","glyph":"⚡"},
    {"from":"FLOW_BATTERY_CELL","to":"ELEC_BUS","via":"PCS","glyph":"⚡"},
    {"from":"WORKSHOP_NODE","to":["THERMAL_LOOP","ELEC_BUS"],"via":"maintenance","glyph":"🛠"},
    {"from":"LEARNING_HUB","to":"ALL_LAYERS","via":"education/data","glyph":"COMM"},
    {"from":"SEASONAL_EVENT","to":"RESERVOIRS","via":"operational","glyph":"⏳"}
  ],
  "controls": {
    "🧭_technical": [
      "Prioritize low-lift heat pump operation from DEEP_LAKE or MINES",
      "Charge PCM_TUBES on surplus electricity",
      "Discharge CAES and PCM_TUBES during cold snaps",
      "Route waste heat from industry into THERMAL_LOOP"
    ],
    "🧭_community": [
      "Publicly display network status in COMMON_HALL",
      "Rotate seasonal maintenance roles via WORKSHOP_NODE",
      "Integrate LEARNING_HUB into school/community programs",
      "Mark SEASONAL_EVENT as a civic celebration"
    ]
  }
}
