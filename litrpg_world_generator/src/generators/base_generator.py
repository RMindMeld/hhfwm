"""
Base generator utility for creating LITRPG world data.
Provides common functionality for all specific generators.
"""
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from uuid import UUID

from ..constants import (
    DISTRIBUTION_PARAMS,
    DATA_QUALITY,
    WORLD_LAWS,
    RealmTier,
    ResourceTier
)

class BaseGenerator:
    """Base class for all data generators."""
    
    def __init__(
        self,
        seed: Optional[int] = None,
        quality_level: float = 1.0,
        realm_tier: RealmTier = RealmTier.MORTAL
    ):
        """Initialize the generator with given parameters."""
        self.rng = np.random.default_rng(seed)
        self.quality_level = min(1.0, max(0.0, quality_level))
        self.realm_tier = realm_tier
        self.current_time = datetime.now()
        
    def generate_cultivation_speed(self) -> float:
        """Generate a realistic cultivation speed value."""
        params = DISTRIBUTION_PARAMS['cultivation_speed']
        base = self.rng.gamma(
            shape=params['shape'],
            scale=params['scale']
        )
        noise = self._apply_measurement_noise(base)
        return max(0.0, noise)
    
    def generate_talent_rating(self) -> float:
        """Generate a talent rating following natural bottlenecks."""
        params = DISTRIBUTION_PARAMS['talent_rating']
        base = self.rng.gamma(
            shape=params['shape'],
            scale=params['scale']
        )
        # Apply bottleneck effects
        bottleneck = 1.0 / (1.0 + np.exp(-2 * (base - 2)))
        return self._apply_measurement_noise(bottleneck)
    
    def calculate_breakthrough_chance(
        self,
        talent: float,
        resources: List[Tuple[ResourceTier, float]]
    ) -> float:
        """Calculate breakthrough success chance based on talent and resources."""
        params = DISTRIBUTION_PARAMS['breakthrough_chance']
        base_rate = params['base_rate']
        talent_bonus = talent * params['talent_multiplier']
        
        resource_bonus = 0.0
        for tier, quality in resources:
            resource_bonus += tier.value * quality * params['resource_multiplier']
        
        total_chance = min(0.95, base_rate + talent_bonus + resource_bonus)
        return self._apply_measurement_noise(total_chance)
    
    def generate_resource_formation_time(
        self,
        tier: ResourceTier,
        environment_factor: float = 1.0
    ) -> int:
        """Generate time required for resource formation."""
        base_time = tier.value * 100  # Base years
        environment_modifier = max(0.1, min(2.0, environment_factor))
        actual_time = int(base_time * environment_modifier)
        
        # Add some natural variation
        variation = self.rng.normal(loc=1.0, scale=0.1)
        return max(1, int(actual_time * variation))
    
    def generate_qi_density(
        self,
        base_level: float,
        location_factor: float = 1.0
    ) -> float:
        """Generate qi density for a location."""
        params = WORLD_LAWS['qi_density']
        base = base_level * params['base_value']
        realm_boost = params['realm_multiplier'] ** (self.realm_tier.value - 1)
        location_modifier = max(0.1, min(2.0, location_factor))
        
        # Add natural fluctuations
        fluctuation = 1.0 + self.rng.uniform(
            -params['fluctuation_range'],
            params['fluctuation_range']
        )
        
        raw_density = base * realm_boost * location_modifier * fluctuation
        return self._apply_measurement_noise(raw_density)
    
    def generate_space_stability(
        self,
        age_years: int,
        formation_quality: float
    ) -> float:
        """Generate space stability value for a region."""
        params = WORLD_LAWS['space_stability']
        base = params['base_value']
        realm_decay = 1.0 - (params['realm_decay'] * (self.realm_tier.value - 1))
        
        # Age effects
        age_factor = 1.0 - (0.1 * np.log1p(age_years / 1000))
        
        # Quality effects
        quality_bonus = formation_quality * 0.5
        
        raw_stability = max(
            params['minimum'],
            base * realm_decay * age_factor * (1.0 + quality_bonus)
        )
        return self._apply_measurement_noise(raw_stability)
    
    def generate_time_flow(self, realm_difference: int) -> float:
        """Generate time flow rate between realms."""
        params = WORLD_LAWS['time_dilation']
        if realm_difference <= 0:
            return 1.0
            
        base_dilation = params['realm_multiplier'] ** realm_difference
        variation = self.rng.normal(loc=1.0, scale=0.05)
        
        return base_dilation * variation
    
    def _apply_measurement_noise(self, value: float) -> float:
        """Apply realistic measurement noise to a value."""
        if self.quality_level >= 1.0:
            return value
            
        params = DATA_QUALITY['measurement_error']
        base_error = params['base_error']
        realm_error = params['realm_increase'] * (self.realm_tier.value - 1)
        total_error = (base_error + realm_error) * (1.0 - self.quality_level)
        
        noise = self.rng.normal(loc=1.0, scale=total_error)
        return max(0.0, value * noise)
    
    def _apply_information_decay(
        self,
        value: float,
        age_years: int
    ) -> Tuple[float, bool]:
        """Apply information decay based on age."""
        params = DATA_QUALITY['information_decay']
        decay_rate = np.log(2) / (params['half_life'] * 
                                 params['realm_modifier'] ** (self.realm_tier.value - 1))
        
        decay_factor = np.exp(-decay_rate * age_years)
        decayed_value = value * decay_factor
        
        # Determine if information is lost
        loss_threshold = 0.1 * (1.0 - self.quality_level)
        is_lost = decay_factor < loss_threshold
        
        return decayed_value, is_lost
    
    def generate_missing_data_mask(
        self,
        size: int,
        age_years: int
    ) -> np.ndarray:
        """Generate a mask for missing data points."""
        params = DATA_QUALITY['missing_data']
        base_rate = params['base_rate']
        age_effect = params['age_factor'] * age_years
        
        total_rate = min(0.9, base_rate + age_effect) * (1.0 - self.quality_level)
        return self.rng.random(size) < total_rate
    
    def generate_karmic_value(
        self,
        base_destiny: float,
        actions: List[Tuple[str, float]]
    ) -> float:
        """Generate a karmic value based on destiny and actions."""
        karmic_sum = base_destiny
        
        for _, magnitude in actions:
            karmic_sum += magnitude * self.rng.normal(loc=1.0, scale=0.1)
        
        # Add realm influence
        realm_factor = 0.1 * (self.realm_tier.value - 1)
        karmic_sum *= (1.0 + realm_factor)
        
        return self._apply_measurement_noise(karmic_sum)
    
    def generate_relationship_strength(
        self,
        base_affinity: float,
        interaction_count: int,
        time_known_years: float
    ) -> float:
        """Generate relationship strength between entities."""
        # Base relationship strength
        strength = base_affinity
        
        # Interaction effects
        interaction_factor = np.log1p(interaction_count) * 0.1
        strength += interaction_factor
        
        # Time effects
        time_factor = np.log1p(time_known_years) * 0.05
        strength += time_factor
        
        # Normalize to [0, 1] range
        normalized = 1.0 / (1.0 + np.exp(-strength))
        return self._apply_measurement_noise(normalized)
    
    def advance_time(self, years: float = 0.0, days: float = 0.0) -> None:
        """Advance the generator's internal time."""
        delta = timedelta(days=days + years * 365.25)
        self.current_time += delta