"""
Generator for creating cultivation resources in the LITRPG world.
Handles creation of resources, treasures, and artifacts with realistic properties.
"""
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Optional, Set, Tuple
from uuid import UUID

from .base_generator import BaseGenerator
from ..models.resource import (
    Resource, EnergyProfile, FormationAttributes,
    QualityMetrics, CraftingRequirements, SpecialEffects,
    UsageMetrics
)
from ..constants import ResourceTier, RealmTier

class ResourceGenerator(BaseGenerator):
    """Generator for creating cultivation resources."""
    
    def __init__(
        self,
        seed: Optional[int] = None,
        quality_level: float = 1.0,
        realm_tier: RealmTier = RealmTier.MORTAL
    ):
        """Initialize the resource generator."""
        super().__init__(seed, quality_level, realm_tier)
        self.element_types = ['Fire', 'Water', 'Earth', 'Wind', 'Lightning', 'Dark', 'Light']
        self.environment_types = ['Mountain', 'Ocean', 'Desert', 'Forest', 'Volcano', 'Arctic']
        
    def generate_resource(
        self,
        tier: Optional[ResourceTier] = None,
        age: Optional[int] = None,
        environment_type: Optional[str] = None
    ) -> Resource:
        """Generate a complete resource with all attributes."""
        if tier is None:
            tier = self._determine_resource_tier()
        if age is None:
            age = self.generate_resource_formation_time(tier)
        if environment_type is None:
            environment_type = self.rng.choice(self.environment_types)
            
        name = self._generate_name(tier)
        description = self._generate_description(tier, environment_type)
        
        # Generate core attributes
        energy_profile = self._generate_energy_profile(tier)
        formation_attributes = self._generate_formation_attributes(age, environment_type)
        quality_metrics = self._generate_quality_metrics(tier)
        crafting_requirements = self._generate_crafting_requirements(tier)
        special_effects = self._generate_special_effects(tier)
        usage_metrics = self._generate_usage_metrics(tier)
        
        # Calculate market and rarity information
        rarity_index = self._calculate_rarity_index(tier, quality_metrics)
        market_value = self._calculate_market_value(tier, quality_metrics, age)
        
        # Calculate data quality metrics
        measurement_accuracy = self._calculate_measurement_accuracy(tier)
        data_reliability = self._calculate_data_reliability(age)
        
        return Resource(
            name=name,
            description=description,
            tier=tier,
            category=self._determine_category(tier),
            subcategory=self._determine_subcategory(tier),
            energy_profile=energy_profile,
            formation_attributes=formation_attributes,
            quality_metrics=quality_metrics,
            crafting_requirements=crafting_requirements,
            special_effects=special_effects,
            usage_metrics=usage_metrics,
            rarity_index=rarity_index,
            market_value=market_value,
            demand_rating=self._calculate_demand_rating(tier, special_effects),
            supply_count=self._calculate_supply_count(tier),
            measurement_accuracy=measurement_accuracy,
            data_reliability=data_reliability,
            hidden_properties=self._generate_hidden_properties(tier)
        )
        
    def _generate_name(self, tier: ResourceTier) -> str:
        """Generate a resource name based on its tier."""
        prefixes = {
            ResourceTier.COMMON: ['Basic', 'Simple', 'Crude'],
            ResourceTier.UNCOMMON: ['Refined', 'Quality', 'Enhanced'],
            ResourceTier.RARE: ['Superior', 'Excellent', 'Premium'],
            ResourceTier.EPIC: ['Magnificent', 'Extraordinary', 'Supreme'],
            ResourceTier.LEGENDARY: ['Mythical', 'Legendary', 'Ancient'],
            ResourceTier.DIVINE: ['Divine', 'Heavenly', 'Celestial'],
            ResourceTier.PRIMORDIAL: ['Primordial', 'Eternal', 'Ultimate']
        }
        
        types = ['Pill', 'Elixir', 'Stone', 'Ore', 'Crystal', 'Essence']
        elements = ['Fire', 'Water', 'Earth', 'Wind', 'Lightning']
        
        prefix = self.rng.choice(prefixes[tier])
        type_ = self.rng.choice(types)
        element = self.rng.choice(elements)
        
        return f"{prefix} {element} {type_}"
        
    def _generate_description(self, tier: ResourceTier, environment: str) -> str:
        """Generate a description for the resource."""
        age_desc = "ancient" if tier.value >= ResourceTier.LEGENDARY.value else "old"
        power_desc = "overwhelming" if tier.value >= ResourceTier.DIVINE.value else "strong"
        
        return f"A {age_desc} treasure formed in the {environment} regions, containing {power_desc} energy."
        
    def _generate_energy_profile(self, tier: ResourceTier) -> EnergyProfile:
        """Generate energy characteristics for the resource."""
        base_power = 100 * (tier.value ** 2)
        energy_type = self.rng.choice(self.element_types)
        
        return EnergyProfile(
            base_power=base_power,
            energy_type=energy_type,
            purity=0.3 + (0.7 * self.rng.random()),
            stability=0.4 + (0.6 * self.rng.random()),
            resonance_frequencies=[
                self.rng.choice(self.element_types)
                for _ in range(self.rng.integers(1, 4))
            ],
            absorption_rate=0.1 + (0.9 * self.rng.random()),
            saturation_point=base_power * 10
        )
        
    def _generate_formation_attributes(
        self,
        age: int,
        environment_type: str
    ) -> FormationAttributes:
        """Generate formation characteristics for the resource."""
        return FormationAttributes(
            formation_date=self.current_time - timedelta(days=age*365),
            maturity_age=age * 2,
            current_age=age,
            environment_type=environment_type,
            natural_born=self.rng.random() > 0.3,
            geological_pressure=self.rng.random() * 1000,
            ambient_energy=self.rng.random() * 100
        )
        
    def _generate_quality_metrics(self, tier: ResourceTier) -> QualityMetrics:
        """Generate quality metrics for the resource."""
        base_grade = 0.3 + (0.7 * (tier.value / ResourceTier.PRIMORDIAL.value))
        
        return QualityMetrics(
            base_grade=base_grade,
            impurities=max(0, 1 - base_grade),
            stability_rating=0.4 + (0.6 * self.rng.random()),
            potency_factor=10 * (tier.value ** 1.5),
            preservation_state=0.5 + (0.5 * self.rng.random()),
            refinement_level=self.rng.integers(0, tier.value + 1)
        )
        
    def _generate_crafting_requirements(
        self,
        tier: ResourceTier
    ) -> Optional[CraftingRequirements]:
        """Generate crafting requirements if applicable."""
        if tier.value <= ResourceTier.UNCOMMON.value:
            return None
            
        min_realm = RealmTier(max(1, tier.value - 2))
        
        return CraftingRequirements(
            minimum_realm=min_realm,
            tool_requirements={'Cauldron', 'Formation Array'},
            skill_requirements={
                'Alchemy': 0.3 * tier.value,
                'Formation': 0.2 * tier.value,
                'Energy Control': 0.4 * tier.value
            },
            environment_requirements={'Clean', 'Stable'},
            energy_requirements={
                'Pure Qi': 100 * tier.value,
                'Spirit Energy': 50 * tier.value
            },
            time_requirements=24 * tier.value
        )
        
    def _generate_special_effects(
        self,
        tier: ResourceTier
    ) -> Optional[SpecialEffects]:
        """Generate special effects if applicable."""
        if tier.value <= ResourceTier.COMMON.value:
            return None
            
        effects = [
            'Strength Enhancement',
            'Spirit Refinement',
            'Soul Tempering',
            'Body Fortification'
        ]
        
        return SpecialEffects(
            primary_effect=self.rng.choice(effects),
            secondary_effects=self.rng.choice(effects, size=2).tolist(),
            side_effects=['Minor Fatigue'] if self.rng.random() > 0.7 else [],
            activation_conditions=['Qi Circulation', 'Mental Focus'],
            duration=int(3600 * (1 + self.rng.random() * tier.value)),
            cooldown=int(7200 * (1 + self.rng.random())),
            power_scaling={
                'cultivation_base': 0.5,
                'talent': 0.3,
                'comprehension': 0.2
            }
        )
        
    def _generate_usage_metrics(self, tier: ResourceTier) -> UsageMetrics:
        """Generate usage metrics for the resource."""
        return UsageMetrics(
            consumption_method='Absorption' if tier.value <= 3 else 'Refinement',
            absorption_efficiency=0.3 + (0.7 * self.rng.random()),
            usage_limit=10 * tier.value if tier.value <= 4 else None,
            remaining_uses=10 * tier.value if tier.value <= 4 else None,
            recharge_rate=0.1 if tier.value >= 5 else None,
            degradation_rate=0.01 * (1 / tier.value),
            compatibility={
                'Fire Path': self.rng.random(),
                'Water Path': self.rng.random(),
                'Earth Path': self.rng.random()
            }
        )
        
    def _determine_resource_tier(self) -> ResourceTier:
        """Determine appropriate resource tier for the realm."""
        available_tiers = list(ResourceTier)[:self.realm_tier.value + 2]
        weights = np.array([10, 5, 3, 2, 1, 0.5, 0.1])[:len(available_tiers)]
        weights = weights / weights.sum()
        
        return self.rng.choice(available_tiers, p=weights)
        
    def _determine_category(self, tier: ResourceTier) -> str:
        """Determine the resource category."""
        categories = ['Pill', 'Elixir', 'Ore', 'Spirit Plant', 'Beast Core']
        weights = [0.4, 0.3, 0.15, 0.1, 0.05]
        return self.rng.choice(categories, p=weights)
        
    def _determine_subcategory(self, tier: ResourceTier) -> str:
        """Determine the resource subcategory."""
        subcategories = {
            'Pill': ['Cultivation', 'Healing', 'Enhancement'],
            'Elixir': ['Spirit', 'Body', 'Soul'],
            'Ore': ['Pure', 'Mixed', 'Legendary'],
            'Spirit Plant': ['Herb', 'Flower', 'Root'],
            'Beast Core': ['Low Grade', 'Mid Grade', 'High Grade']
        }
        
        category = self._determine_category(tier)
        return self.rng.choice(subcategories[category])
        
    def _calculate_rarity_index(
        self,
        tier: ResourceTier,
        quality: QualityMetrics
    ) -> float:
        """Calculate the resource's rarity index."""
        base_rarity = tier.value / len(ResourceTier)
        quality_factor = quality.base_grade
        
        return base_rarity * (1 + quality_factor)
        
    def _calculate_market_value(
        self,
        tier: ResourceTier,
        quality: QualityMetrics,
        age: int
    ) -> Dict[str, float]:
        """Calculate market value in different currencies."""
        base_value = 100 * (tier.value ** 3)
        quality_multiplier = 1 + quality.base_grade
        age_multiplier = 1 + (age / 1000)
        
        spirit_stone_value = base_value * quality_multiplier * age_multiplier
        
        return {
            'spirit_stones': spirit_stone_value,
            'contribution_points': spirit_stone_value * 0.1,
            'merit_points': spirit_stone_value * 0.01
        }
        
    def _calculate_demand_rating(
        self,
        tier: ResourceTier,
        effects: Optional[SpecialEffects]
    ) -> float:
        """Calculate the resource's demand rating."""
        base_demand = 1.0 - (0.1 * tier.value)  # Lower tiers have higher demand
        
        if effects:
            effect_bonus = len(effects.secondary_effects) * 0.1
            base_demand += effect_bonus
            
        return min(1.0, max(0.1, base_demand))
        
    def _calculate_supply_count(self, tier: ResourceTier) -> int:
        """Calculate the resource's supply count."""
        base_count = 1000 // (tier.value ** 2)
        variation = self.rng.integers(-base_count//10, base_count//10)
        return max(1, base_count + variation)
        
    def _calculate_measurement_accuracy(self, tier: ResourceTier) -> float:
        """Calculate how accurately the resource can be measured."""
        base_accuracy = 0.9
        tier_penalty = 0.1 * tier.value
        
        return max(0.1, min(1.0, base_accuracy - tier_penalty))
        
    def _calculate_data_reliability(self, age: int) -> float:
        """Calculate how reliable the resource's data is based on age."""
        base_reliability = 0.95
        age_penalty = 0.001 * (age / 100)
        
        return max(0.1, min(1.0, base_reliability - age_penalty))
        
    def _generate_hidden_properties(self, tier: ResourceTier) -> Set[str]:
        """Determine which properties are hidden from measurement."""
        possible_hidden = {
            'true_energy_content',
            'formation_secrets',
            'special_resonance',
            'compatibility_matrix',
            'evolution_potential'
        }
        
        hide_probability = 0.1 * tier.value
        return {prop for prop in possible_hidden if self.rng.random() < hide_probability}