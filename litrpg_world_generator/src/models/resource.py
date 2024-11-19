"""
Model for resources, treasures, and artifacts in the LITRPG world.
Handles everything from basic cultivation materials to divine artifacts.
"""
from datetime import datetime
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

from ..constants import ResourceTier, RealmTier

class EnergyProfile(BaseModel):
    """Represents the energy/qi characteristics of a resource."""
    base_power: float = Field(ge=0.0)
    energy_type: str
    purity: float = Field(ge=0.0, le=1.0)
    stability: float = Field(ge=0.0, le=1.0)
    resonance_frequencies: List[str]
    absorption_rate: float = Field(ge=0.0)
    saturation_point: float = Field(ge=0.0)

class FormationAttributes(BaseModel):
    """Tracks the formation and aging of resources."""
    formation_date: datetime
    maturity_age: int = Field(ge=0)  # in years
    current_age: int = Field(ge=0)
    environment_type: str
    natural_born: bool
    geological_pressure: float = Field(ge=0.0)
    ambient_energy: float = Field(ge=0.0)

class QualityMetrics(BaseModel):
    """Measures various aspects of resource quality."""
    base_grade: float = Field(ge=0.0, le=1.0)
    impurities: float = Field(ge=0.0, le=1.0)
    stability_rating: float = Field(ge=0.0, le=1.0)
    potency_factor: float = Field(ge=0.0)
    preservation_state: float = Field(ge=0.0, le=1.0)
    refinement_level: int = Field(ge=0)

class CraftingRequirements(BaseModel):
    """Defines requirements for using the resource in crafting."""
    minimum_realm: RealmTier
    tool_requirements: Set[str]
    skill_requirements: Dict[str, float]  # skill_name: minimum_level
    environment_requirements: Set[str]
    energy_requirements: Dict[str, float]  # energy_type: amount
    time_requirements: int  # in hours

class SpecialEffects(BaseModel):
    """Tracks special properties and effects of the resource."""
    primary_effect: str
    secondary_effects: List[str]
    side_effects: List[str]
    activation_conditions: List[str]
    duration: Optional[int]  # in seconds, None for permanent
    cooldown: Optional[int]  # in seconds, None for no cooldown
    power_scaling: Dict[str, float]  # attribute: scaling_factor

class UsageMetrics(BaseModel):
    """Tracks how the resource can be used and consumed."""
    consumption_method: str
    absorption_efficiency: float = Field(ge=0.0, le=1.0)
    usage_limit: Optional[int]
    remaining_uses: Optional[int]
    recharge_rate: Optional[float]
    degradation_rate: float = Field(ge=0.0)
    compatibility: Dict[str, float]  # cultivation_type: compatibility_rating

class Resource(BaseModel):
    """Main model representing a cultivation resource or artifact."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    tier: ResourceTier
    category: str
    subcategory: str
    
    # Core attributes
    energy_profile: EnergyProfile
    formation_attributes: FormationAttributes
    quality_metrics: QualityMetrics
    crafting_requirements: Optional[CraftingRequirements]
    special_effects: Optional[SpecialEffects]
    usage_metrics: UsageMetrics
    
    # Tracking fields
    discovery_date: datetime = Field(default_factory=datetime.now)
    last_refined: Optional[datetime]
    refinement_history: List[Dict[str, any]]
    known_locations: Set[str] = Field(default_factory=set)
    
    # Market and value information
    rarity_index: float = Field(ge=0.0)
    market_value: Dict[str, float]  # currency_type: value
    demand_rating: float = Field(ge=0.0)
    supply_count: int = Field(ge=0)
    
    # Data quality tracking
    measurement_accuracy: float = Field(ge=0.0, le=1.0)
    last_assessed: datetime = Field(default_factory=datetime.now)
    data_reliability: float = Field(ge=0.0, le=1.0)
    hidden_properties: Set[str] = Field(default_factory=set)

    class Config:
        arbitrary_types_allowed = True

    def calculate_true_value(self) -> float:
        """Calculate the true value of the resource based on all attributes."""
        base_value = self.tier.value * self.quality_metrics.base_grade
        age_factor = min(1 + (self.formation_attributes.current_age / 
                            self.formation_attributes.maturity_age), 2)
        energy_factor = self.energy_profile.base_power * self.energy_profile.purity
        
        return base_value * age_factor * energy_factor * (1 + self.rarity_index)

    def can_be_refined(self) -> bool:
        """Check if the resource can undergo further refinement."""
        if not self.last_refined:
            return True
            
        time_since_refinement = datetime.now() - self.last_refined
        stability_check = self.quality_metrics.stability_rating > 0.3
        refinement_limit = self.quality_metrics.refinement_level < 9
        
        return (time_since_refinement.days >= 7 and 
                stability_check and 
                refinement_limit)

    def calculate_absorption_efficiency(self, cultivator_realm: RealmTier) -> float:
        """Calculate how efficiently a cultivator can absorb this resource."""
        base_efficiency = self.usage_metrics.absorption_efficiency
        realm_difference = cultivator_realm.value - self.crafting_requirements.minimum_realm.value
        
        if realm_difference < 0:
            return 0.0  # Cannot use resource above their realm
        
        realm_bonus = min(0.5, realm_difference * 0.1)  # Max 50% bonus from realm
        purity_factor = self.energy_profile.purity
        
        return min(1.0, base_efficiency * (1 + realm_bonus) * purity_factor)

    def degrade(self, time_passed: int) -> None:
        """Apply natural degradation based on time passed."""
        degradation = self.usage_metrics.degradation_rate * time_passed
        
        self.quality_metrics.preservation_state *= (1 - degradation)
        self.energy_profile.stability *= (1 - degradation * 0.5)
        self.energy_profile.purity *= (1 - degradation * 0.3)
        
        if self.usage_metrics.remaining_uses:
            self.usage_metrics.remaining_uses = max(
                0, 
                self.usage_metrics.remaining_uses - int(degradation * 10)
            )