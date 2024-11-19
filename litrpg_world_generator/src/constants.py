"""
Constants and configuration for the LITRPG world data generator.
Defines core aspects of the world's mechanics and natural laws.
"""
from enum import Enum, auto
from typing import Dict, List, Tuple

# Realm Definitions
class RealmTier(Enum):
    MORTAL = auto()
    SPIRIT = auto()
    MYSTIC = auto()
    CELESTIAL = auto()
    DIVINE = auto()
    PRIMORDIAL = auto()

# Cultivation Stages
class CultivationStage(Enum):
    # Mortal Realm Stages
    BODY_REFINEMENT = auto()
    QI_CONDENSATION = auto()
    FOUNDATION_ESTABLISHMENT = auto()
    CORE_FORMATION = auto()
    
    # Spirit Realm Stages
    NASCENT_SOUL = auto()
    SPIRIT_SEVERING = auto()
    VOID_FORMATION = auto()
    
    # Mystic Realm Stages
    DAO_SEEKING = auto()
    DAO_MANIFESTATION = auto()
    DAO_MASTERY = auto()
    
    # Higher Realm Stages
    CELESTIAL_ASCENSION = auto()
    DIVINE_TRANSFORMATION = auto()
    PRIMORDIAL_UNITY = auto()

# Resource Rarity
class ResourceTier(Enum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    EPIC = auto()
    LEGENDARY = auto()
    MYTHICAL = auto()
    DIVINE = auto()
    PRIMORDIAL = auto()

# Statistical Distribution Parameters
DISTRIBUTION_PARAMS = {
    'cultivation_speed': {
        'shape': 2.5,  # Extremely right-skewed
        'scale': 1.0,
        'location': 0.0
    },
    'talent_rating': {
        'shape': 3.0,  # Natural bottlenecks
        'scale': 1.0,
        'location': 0.0
    },
    'breakthrough_chance': {
        'base_rate': 0.1,  # Base 10% success rate
        'talent_multiplier': 0.05,  # Each talent point adds 5%
        'resource_multiplier': 0.1  # Each resource quality level adds 10%
    }
}

# World Law Constants
WORLD_LAWS = {
    'qi_density': {
        'base_value': 1.0,
        'realm_multiplier': 2.0,  # Doubles each realm
        'fluctuation_range': 0.2  # ±20% random fluctuation
    },
    'space_stability': {
        'base_value': 1.0,
        'realm_decay': 0.1,  # Decreases by 10% each higher realm
        'minimum': 0.1
    },
    'time_dilation': {
        'base_rate': 1.0,
        'realm_multiplier': 1.5  # 50% faster each realm
    }
}

# Data Quality Configuration
DATA_QUALITY = {
    'measurement_error': {
        'base_error': 0.05,  # Base 5% error
        'realm_increase': 0.02  # Additional 2% per realm
    },
    'missing_data': {
        'base_rate': 0.01,  # 1% base rate
        'age_factor': 0.001  # Additional 0.1% per 1000 years
    },
    'information_decay': {
        'half_life': 1000,  # Years until 50% data degradation
        'realm_modifier': 1.5  # Higher realms preserve better
    }
}

# Population Distribution
POPULATION_DISTRIBUTION = {
    RealmTier.MORTAL: 0.9,      # 90% of total population
    RealmTier.SPIRIT: 0.08,     # 8%
    RealmTier.MYSTIC: 0.015,    # 1.5%
    RealmTier.CELESTIAL: 0.004, # 0.4%
    RealmTier.DIVINE: 0.0009,   # 0.09%
    RealmTier.PRIMORDIAL: 0.0001 # 0.01%
}

# Resource Generation
RESOURCE_GENERATION = {
    'formation_time': {
        ResourceTier.COMMON: 1,        # 1 year
        ResourceTier.UNCOMMON: 10,     # 10 years
        ResourceTier.RARE: 100,        # 100 years
        ResourceTier.EPIC: 1000,       # 1,000 years
        ResourceTier.LEGENDARY: 10000,  # 10,000 years
        ResourceTier.MYTHICAL: 100000,  # 100,000 years
        ResourceTier.DIVINE: 1000000,   # 1,000,000 years
        ResourceTier.PRIMORDIAL: 10000000 # 10,000,000 years
    },
    'quantity_multiplier': {
        ResourceTier.COMMON: 1000000,
        ResourceTier.UNCOMMON: 100000,
        ResourceTier.RARE: 10000,
        ResourceTier.EPIC: 1000,
        ResourceTier.LEGENDARY: 100,
        ResourceTier.MYTHICAL: 10,
        ResourceTier.DIVINE: 1,
        ResourceTier.PRIMORDIAL: 0.1
    }
}

# Bloodline Inheritance
BLOODLINE_INHERITANCE = {
    'mutation_chance': 0.001,  # 0.1% chance per generation
    'power_inheritance': 0.5,  # Children inherit 50% of parent's power
    'talent_inheritance': 0.7  # 70% of parent's talent is inherited
}

# Combat Power Scaling
COMBAT_POWER = {
    'base_power': 1.0,
    'realm_multiplier': 10.0,  # 10x power per realm
    'stage_multiplier': 2.0,   # 2x power per stage
    'talent_factor': 0.1       # Each talent point adds 10% power
}

# Sect Development
SECT_PARAMETERS = {
    'min_members': 10,
    'max_members': 10000,
    'resource_consumption': {
        'per_member': 1.0,
        'cultivation_multiplier': 2.0
    },
    'knowledge_accumulation': {
        'base_rate': 0.1,
        'member_contribution': 0.01
    }
}

# Artifact Creation
ARTIFACT_CRAFTING = {
    'base_success_rate': 0.3,
    'mastery_multiplier': 0.05,  # Each mastery level adds 5%
    'resource_quality_factor': 0.1,  # Each resource tier adds 10%
    'failure_salvage_rate': 0.5  # 50% of resources can be salvaged on failure
}

# Spatial Formation Parameters
SPATIAL_PARAMETERS = {
    'stability_threshold': 0.8,
    'energy_density_requirement': {
        'base': 1.0,
        'tier_multiplier': 2.0
    },
    'maintenance_cost': {
        'base': 1.0,
        'size_multiplier': 1.5,
        'complexity_multiplier': 2.0
    }
}