"""
Generator for creating realms and planes of existence in the LITRPG world.
Handles creation of different reality layers with their natural laws and characteristics.
"""
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Optional, Set, Tuple
from uuid import UUID

from .base_generator import BaseGenerator
from ..models.realm import (
    Realm, NaturalLaws, SpatialAttributes, EnergyGrid,
    PopulationMetrics, FormationDetails, EnvironmentalEffects
)
from ..constants import RealmTier, WORLD_LAWS

class RealmGenerator(BaseGenerator):
    """Generator for creating cultivation realms."""
    
    def __init__(
        self,
        seed: Optional[int] = None,
        quality_level: float = 1.0,
        realm_tier: RealmTier = RealmTier.MORTAL
    ):
        """Initialize the realm generator."""
        super().__init__(seed, quality_level, realm_tier)
        self.element_types = ['Fire', 'Water', 'Earth', 'Wind', 'Lightning', 'Dark', 'Light']
        self.law_types = ['Space', 'Time', 'Fate', 'Creation', 'Destruction']
        
    def generate_realm(
        self,
        tier: Optional[RealmTier] = None,
        age: Optional[int] = None,
        parent_realm: Optional[UUID] = None
    ) -> Realm:
        """Generate a complete realm with all attributes."""
        if tier is None:
            tier = self.realm_tier
        if age is None:
            age = self._generate_age(tier)
            
        name = self._generate_name(tier)
        description = self._generate_description(tier)
        
        # Generate core attributes
        natural_laws = self._generate_natural_laws(tier)
        spatial_attributes = self._generate_spatial_attributes(tier)
        energy_grid = self._generate_energy_grid(tier)
        population_metrics = self._generate_population_metrics(tier)
        formation_details = self._generate_formation_details(age, tier)
        environmental_effects = self._generate_environmental_effects(tier)
        
        # Calculate data quality metrics
        measurement_accuracy = self._calculate_measurement_accuracy(tier)
        data_reliability = self._calculate_data_reliability(age)
        
        return Realm(
            name=name,
            tier=tier,
            description=description,
            natural_laws=natural_laws,
            spatial_attributes=spatial_attributes,
            energy_grid=energy_grid,
            population_metrics=population_metrics,
            formation_details=formation_details,
            environmental_effects=environmental_effects,
            parent_realm=parent_realm,
            child_realms=[],
            connected_realms={},
            controlling_factions=self._generate_controlling_factions(tier),
            access_restrictions=self._generate_access_restrictions(tier),
            security_measures=self._generate_security_measures(tier),
            measurement_accuracy=measurement_accuracy,
            data_reliability=data_reliability,
            unmapped_regions=self._generate_unmapped_regions(tier)
        )
        
    def _generate_name(self, tier: RealmTier) -> str:
        """Generate a realm name."""
        prefixes = {
            RealmTier.MORTAL: ['Mortal', 'Human', 'Physical'],
            RealmTier.SPIRIT: ['Spirit', 'Soul', 'Ethereal'],
            RealmTier.MYSTIC: ['Mystic', 'Dao', 'Profound'],
            RealmTier.CELESTIAL: ['Celestial', 'Heavenly', 'Astral'],
            RealmTier.DIVINE: ['Divine', 'Godly', 'Supreme'],
            RealmTier.PRIMORDIAL: ['Primordial', 'Origin', 'Eternal']
        }
        
        suffixes = ['Realm', 'Domain', 'World', 'Plane', 'Dimension']
        prefix = self.rng.choice(prefixes[tier])
        suffix = self.rng.choice(suffixes)
        
        return f"{prefix} {suffix}"
        
    def _generate_description(self, tier: RealmTier) -> str:
        """Generate a realm description."""
        power_levels = {
            RealmTier.MORTAL: "mundane",
            RealmTier.SPIRIT: "spiritual",
            RealmTier.MYSTIC: "mystical",
            RealmTier.CELESTIAL: "celestial",
            RealmTier.DIVINE: "divine",
            RealmTier.PRIMORDIAL: "primordial"
        }
        
        return f"A {power_levels[tier]} plane of existence where the laws of reality operate at a {tier.name.lower()} level."
        
    def _generate_natural_laws(self, tier: RealmTier) -> NaturalLaws:
        """Generate natural laws for the realm."""
        base_qi = self.generate_qi_density(100.0)
        
        return NaturalLaws(
            qi_density=base_qi,
            space_stability=self.generate_space_stability(1000, 0.8),
            time_flow_rate=self.generate_time_flow(tier.value - 1),
            gravity_factor=1.0 + (0.5 * tier.value),
            elemental_balance={
                element: self.rng.random()
                for element in self.element_types
            },
            law_strength={
                law: 0.2 + (0.8 * self.rng.random())
                for law in self.law_types
            },
            reality_compression=1.0 + (tier.value * self.rng.random())
        )
        
    def _generate_spatial_attributes(self, tier: RealmTier) -> SpatialAttributes:
        """Generate spatial characteristics for the realm."""
        base_size = 1000000 * (10 ** tier.value)  # in cubic kilometers
        
        return SpatialAttributes(
            dimensions=3 + (tier.value // 2),  # Higher realms have more dimensions
            size=base_size,
            boundary_stability=0.5 + (0.5 * self.rng.random()),
            connection_points={
                f"Portal {i}": 0.3 + (0.7 * self.rng.random())
                for i in range(1, tier.value + 2)
            },
            spatial_anchors=[
                {
                    "location": f"Anchor {i}",
                    "strength": 0.5 + (0.5 * self.rng.random()),
                    "type": self.rng.choice(self.law_types)
                }
                for i in range(tier.value + 1)
            ],
            fold_density=0.1 * tier.value * self.rng.random(),
            distortion_zones=[
                {
                    "location": f"Zone {i}",
                    "intensity": self.rng.random(),
                    "effect": self.rng.choice(self.law_types)
                }
                for i in range(tier.value)
            ]
        )
        
    def _generate_energy_grid(self, tier: RealmTier) -> EnergyGrid:
        """Generate energy distribution for the realm."""
        base_energy = 1000 * (10 ** tier.value)
        
        return EnergyGrid(
            base_energy_level=base_energy,
            energy_types={
                element: base_energy * self.rng.random()
                for element in self.element_types
            },
            ley_lines=[
                {
                    "path": f"Line {i}",
                    "power": base_energy * self.rng.random(),
                    "stability": 0.5 + (0.5 * self.rng.random())
                }
                for i in range(tier.value + 3)
            ],
            nodes=[
                {
                    "location": f"Node {i}",
                    "capacity": base_energy * self.rng.random(),
                    "type": self.rng.choice(self.element_types)
                }
                for i in range(tier.value + 2)
            ],
            flow_patterns={
                direction: [self.rng.random() for _ in range(3)]
                for direction in ['North', 'South', 'East', 'West']
            },
            regeneration_rate=0.1 + (0.1 * tier.value),
            stability_index=0.6 + (0.4 * self.rng.random())
        )
        
    def _generate_population_metrics(self, tier: RealmTier) -> PopulationMetrics:
        """Generate population distribution for the realm."""
        base_population = 1000000 * (10 ** (6 - tier.value))  # Higher realms have fewer beings
        
        return PopulationMetrics(
            total_population=base_population,
            species_distribution={
                'Human': 0.6,
                'Spirit': 0.2,
                'Beast': 0.15,
                'Ancient': 0.05
            },
            cultivation_levels={
                f"Level {i}": int(base_population * (0.1 ** i))
                for i in range(1, tier.value + 4)
            },
            resource_density={
                'Spirit Stones': 1000 * tier.value,
                'Medicinal Herbs': 500 * tier.value,
                'Treasures': 100 * tier.value
            },
            civilization_centers=[
                {
                    "name": f"City {i}",
                    "population": int(base_population * self.rng.random() * 0.1),
                    "development": 0.5 + (0.5 * self.rng.random())
                }
                for i in range(tier.value + 2)
            ],
            power_distribution={
                'Mortal': 0.7,
                'Spirit': 0.2,
                'Mystic': 0.08,
                'Beyond': 0.02
            },
            karmic_density=0.1 * tier.value * self.rng.random()
        )
        
    def _generate_formation_details(
        self,
        age: int,
        tier: RealmTier
    ) -> FormationDetails:
        """Generate formation characteristics for the realm."""
        return FormationDetails(
            age=age,
            stability_cycle=1000 * tier.value,
            maintenance_cost=1000000 * (10 ** tier.value),
            core_elements=self.rng.choice(
                self.element_types,
                size=tier.value + 1,
                replace=False
            ).tolist(),
            supporting_formations=[
                {
                    "type": f"Formation {i}",
                    "power": 1000 * self.rng.random(),
                    "purpose": self.rng.choice(self.law_types)
                }
                for i in range(tier.value + 2)
            ],
            weakness_points=[
                {
                    "location": f"Point {i}",
                    "severity": self.rng.random(),
                    "type": self.rng.choice(self.law_types)
                }
                for i in range(max(1, tier.value - 1))
            ],
            repair_mechanisms={
                'Self-Healing': 0.5 + (0.5 * self.rng.random()),
                'Energy Absorption': 0.3 + (0.7 * self.rng.random()),
                'Law Reinforcement': 0.2 + (0.8 * self.rng.random())
            }
        )
        
    def _generate_environmental_effects(self, tier: RealmTier) -> EnvironmentalEffects:
        """Generate environmental conditions for the realm."""
        return EnvironmentalEffects(
            weather_patterns={
                'Energy Storms': 0.3 * tier.value,
                'Law Fluctuations': 0.2 * tier.value,
                'Reality Distortions': 0.1 * tier.value
            },
            elemental_phenomena=self.rng.choice(
                self.element_types,
                size=tier.value + 1,
                replace=False
            ).tolist(),
            natural_hazards=[
                {
                    "type": f"Hazard {i}",
                    "danger_level": self.rng.random(),
                    "frequency": 0.1 + (0.9 * self.rng.random())
                }
                for i in range(tier.value + 1)
            ],
            beneficial_regions=[
                {
                    "location": f"Region {i}",
                    "benefit_type": self.rng.choice(self.element_types),
                    "power_level": 0.5 + (0.5 * self.rng.random())
                }
                for i in range(tier.value)
            ],
            seasonal_effects={
                'Spring': {'growth_rate': 1.2, 'energy_density': 1.1},
                'Summer': {'power_boost': 1.3, 'stability': 0.9},
                'Autumn': {'comprehension': 1.2, 'consolidation': 1.1},
                'Winter': {'preservation': 1.3, 'purification': 1.2}
            },
            background_radiation=0.1 * tier.value * self.rng.random(),
            magical_interference=0.2 * tier.value * self.rng.random()
        )
        
    def _generate_age(self, tier: RealmTier) -> int:
        """Generate appropriate age for the realm."""
        base_age = 1000 * (10 ** tier.value)
        variation = self.rng.integers(-base_age//10, base_age//10)
        return max(1000, base_age + variation)
        
    def _generate_controlling_factions(self, tier: RealmTier) -> Dict[str, float]:
        """Generate controlling factions and their influence."""
        return {
            'Cultivator Sects': 0.4,
            'Ancient Clans': 0.3,
            'Beast Tribes': 0.2,
            'Hidden Forces': 0.1
        }
        
    def _generate_access_restrictions(self, tier: RealmTier) -> List[Dict[str, any]]:
        """Generate access restrictions for the realm."""
        return [
            {
                "type": "Cultivation Level",
                "minimum": tier.value * 1000,
                "bypass_method": "Special Token"
            },
            {
                "type": "Bloodline Strength",
                "minimum": 0.5 * tier.value,
                "bypass_method": "Ancient Artifact"
            }
        ]
        
    def _generate_security_measures(self, tier: RealmTier) -> List[str]:
        """Generate security measures for the realm."""
        measures = [
            "Boundary Array",
            "Energy Shield",
            "Law Enforcement",
            "Space Lock",
            "Time Barrier"
        ]
        return measures[:tier.value + 1]
        
    def _generate_unmapped_regions(self, tier: RealmTier) -> Set[str]:
        """Generate unmapped regions in the realm."""
        possible_regions = {
            'Deep Wilderness',
            'Void Zones',
            'Ancient Ruins',
            'Forbidden Areas',
            'Chaotic Regions'
        }
        
        unmapped_count = self.rng.integers(1, tier.value + 2)
        return set(self.rng.choice(list(possible_regions), size=unmapped_count, replace=False))