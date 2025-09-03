{
  "module": "CRITICAL_RESOURCES_LAYER",
  "purpose": "Map the production and exchange of essential resources across the three-hub corridor for resilience",
  "categories": [
    {
      "category": "Water & Sanitation",
      "resources": [
        {
          "item": "Clean Drinking Water",
          "primary_hub": ["LAKE_SUPERIOR_COMMONS","STPAUL_MISSISSIPPI_COMMONS","DRIFTLESS_COMMONS"],
          "method": "Surface/groundwater intake + filtration (sand, ceramic, membrane) + disinfection (bleach, UV, boiling)",
          "distribution": "Inter-hub tanker/barge in emergencies"
        },
        {
          "item": "Wastewater Treatment & Nutrient Recovery",
          "primary_hub": ["STPAUL_MISSISSIPPI_COMMONS","LAKE_SUPERIOR_COMMONS"],
          "method": "Existing municipal plants with ammonia/phosphorus capture; portable biofilters for Driftless",
          "distribution": "Nutrients to Driftless agri-loops"
        }
      ]
    },
    {
      "category": "Food Security & Preservation",
      "resources": [
        {
          "item": "Cold Storage",
          "primary_hub": ["DRIFTLESS_COMMONS","LAKE_SUPERIOR_COMMONS","STPAUL_MISSISSIPPI_COMMONS"],
          "method": "Cave PCM cold vaults, lava-tube PCM, aquifer cooling",
          "distribution": "Shared surplus storage for all hubs"
        },
        {
          "item": "Staple Crop Processing",
          "primary_hub": ["DRIFTLESS_COMMONS"],
          "method": "Grain milling, oil pressing, dairy processing at co-op facilities",
          "distribution": "Processed staples shipped to other hubs"
        }
      ]
    },
    {
      "category": "Fuel & Energy Storage",
      "resources": [
        {
          "item": "Biomass Pellets",
          "primary_hub": ["DRIFTLESS_COMMONS"],
          "method": "Pelletizing agricultural residues and wood waste",
          "distribution": "Winter heating support for Superior & St. Paul"
        },
        {
          "item": "Biogas",
          "primary_hub": ["STPAUL_MISSISSIPPI_COMMONS"],
          "method": "Anaerobic digestion of urban organic waste",
          "distribution": "Heat/electricity generation at all hubs"
        },
        {
          "item": "Ammonia (NH3)",
          "primary_hub": ["LAKE_SUPERIOR_COMMONS"],
          "method": "Renewable H2 + N2 catalytic synthesis",
          "distribution": "Fertilizer and energy carrier across corridor"
        }
      ]
    },
    {
      "category": "Medical & Hygiene",
      "resources": [
        {
          "item": "Bleach (NaOCl)",
          "primary_hub": ["STPAUL_MISSISSIPPI_COMMONS"],
          "method": "Electrolysis of brine",
          "distribution": "Cleaning and disinfection supplies to all hubs"
        },
        {
          "item": "Vinegar (Acetic Acid)",
          "primary_hub": ["DRIFTLESS_COMMONS"],
          "method": "Fermentation of ethanol to acetic acid",
          "distribution": "Food preservation and cleaning agent to all hubs"
        },
        {
          "item": "Ethanol/Isopropanol",
          "primary_hub": ["DRIFTLESS_COMMONS"],
          "method": "Fermentation/distillation and chemical synthesis",
          "distribution": "Hand sanitizer and disinfectant for all hubs"
        },
        {
          "item": "Soap",
          "primary_hub": ["STPAUL_MISSISSIPPI_COMMONS","DRIFTLESS_COMMONS"],
          "method": "Saponification using lye and oils/fats",
          "distribution": "Hygiene supplies for all hubs"
        }
      ]
    },
    {
      "category": "Minerals & Industrial Inputs",
      "resources": [
        {
          "item": "Salt (NaCl)",
          "primary_hub": ["LAKE_SUPERIOR_COMMONS"],
          "method": "Great Lakes salt shipping + evaporation",
          "distribution": "Feedstock for bleach, lye, baking soda production"
        },
        {
          "item": "Lye (NaOH)",
          "primary_hub": ["STPAUL_MISSISSIPPI_COMMONS"],
          "method": "Chlor-alkali process from NaCl",
          "distribution": "Soap making, pH control, chemical synthesis"
        },
        {
          "item": "Baking Soda (NaHCO3)",
          "primary_hub": ["STPAUL_MISSISSIPPI_COMMONS"],
          "method": "React CO2 with NaOH from chlor-alkali to form NaHCO3",
          "distribution": "Baking, cleaning, medical antacid uses"
        },
        {
          "item": "Lime (CaO/Ca(OH)2)",
          "primary_hub": ["DRIFTLESS_COMMONS"],
          "method": "Calcining limestone, hydrating to Ca(OH)2",
          "distribution": "Construction, water treatment, soil amendment"
        },
        {
          "item": "Iron & Mineral Catalysts",
          "primary_hub": ["LAKE_SUPERIOR_COMMONS"],
          "method": "Mining/refining iron ores and catalytic minerals",
          "distribution": "Energy carrier synthesis and industrial processes"
        }
      ]
    }
  ],
  "controls": {
    "🧭": [
      "Maintain modular production capacity for all listed items at designated hubs",
      "Run quarterly drills to verify production, QA, and distribution readiness",
      "Integrate these flows into the main corridor freight and governance plan",
      "Educate co-op members on uses and storage of each resource"
    ]
  }
}
