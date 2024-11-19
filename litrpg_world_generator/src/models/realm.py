"""
Model for realms and planes of existence in the LITRPG world.
Defines the structure and properties of different reality layers.
"""
from datetime import datetime
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

from ..constants import RealmTier, WORLD_LAWS

class NaturalLaws(BaseModel):
    """Defines the fundamental rules governing a realm."""
    qi_density: float = Field(ge=0.0)
    space_stability: float = Field(ge=0.0, le=1.0)
    time_flow_rate: float = Field(ge=0.1)  # 1.0 is baseline
    gravity_factor: float = Field(ge=0.0)
    elemental_balance: Dict[str, float]  # element: concentration
    law_strength: Dict[str, float]  # law_type: power
    reality_compression: float = Field(ge=1.0)  # space compression ratio

class SpatialAttributes(BaseModel):
    """Describes the spatial characteristics of the realm."""
    dimensions: int = Field(ge=1, le=11)  # Number of spatial dimensions
    size: float  # in cubic kilometers
    boundary_stability: float = Field(ge=0.0, le=1.0)
    connection_points: Dict[str, float]  # location: stability
    spatial_anchors: List[Dict[str, any]]
    fold_density: float = Field(ge=0.0)  # pocket space density
    distortion_zones: List[Dict[str, any]]

class EnergyGrid(BaseModel):
    """Represents the energy distribution and flow in the realm."""
    base_energy_level: float = Field(ge=0.0)
    energy_types: Dict[str, float]  # type: concentration
    ley_lines: List[Dict[str, any]]
    nodes: List[Dict[str, any]]
    flow_patterns: Dict[str, List[float]]
    regeneration_rate: float = Field(ge=0.0)
    stability_index: float = Field(ge=0.0, le=1.0)

class PopulationMetrics(BaseModel):
    """Tracks population and resource distribution."""
    total_population: int = Field(ge=0)
    species_distribution: Dict[str, int]
    cultivation_levels: Dict[str, int]
    resource_density: Dict[str, float]
    civilization_centers: List[Dict[str, any]]
    power_distribution: Dict[str, float]
    karmic_density: float = Field(ge=0.0)

class FormationDetails(BaseModel):
    """Details about the realm's formation and maintenance."""
    age: int = Field(ge=0)  # in years
    stability_cycle: int  # in years
    maintenance_cost: float = Field(ge=0.0)
    core_elements: List[str]
    supporting_formations: List[Dict[str, any]]
    weakness_points: List[Dict[str, any]]
    repair_mechanisms: Dict[str, float]

class EnvironmentalEffects(BaseModel):
    """Tracks environmental conditions and effects."""
    weather_patterns: Dict[str, float]
    elemental_phenomena: List[str]
    natural_hazards: List[Dict[str, any]]
    beneficial_regions: List[Dict[str, any]]
    seasonal_effects: Dict[str, Dict[str, any]]
    background_radiation: float = Field(ge=0.0)
    magical_interference: float = Field(ge=0.0)

class Realm(BaseModel):
    """Main model representing a plane of existence."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    tier: RealmTier
    description: str
    
    # Core attributes
    natural_laws: NaturalLaws
    spatial_attributes: SpatialAttributes
    energy_grid: EnergyGrid
    population_metrics: PopulationMetrics
    formation_details: FormationDetails
    environmental_effects: EnvironmentalEffects
    
    # Tracking fields
    creation_date: datetime = Field(default_factory=datetime.now)
    last_stabilized: datetime = Field(default_factory=datetime.now)
    stability_history: List[Dict[str, any]]
    major_events: List[Dict[str, any]]
    
    # Connections and relationships
    parent_realm: Optional[UUID]
    child_realms: List[UUID] = Field(default_factory=list)
    connected_realms: Dict[UUID, float] = Field(default_factory=dict)  # realm_id: connection_strength
    
    # Access and control
    controlling_factions: Dict[str, float]  # faction_name: influence_level
    access_restrictions: List[Dict[str, any]]
    security_measures: List[str]
    
    # Data quality tracking
    measurement_accuracy: float = Field(ge=0.0, le=1.0)
    last_surveyed: datetime = Field(default_factory=datetime.now)
    data_reliability: float = Field(ge=0.0, le=1.0)
    unmapped_regions: Set[str] = Field(default_factory=set)

    class Config:
        arbitrary_types_allowed = True

    def calculate_stability(self) -> float:
        """Calculate the overall stability of the realm."""
        base_stability = self.spatial_attributes.boundary_stability
        energy_factor = self.energy_grid.stability_index
        formation_age = (datetime.now() - self.creation_date).days / 365.25
        age_factor = min(1.0, formation_age / self.formation_details.stability_cycle)
        
        return base_stability * energy_factor * (0.5 + 0.5 * age_factor)

    def needs_stabilization(self) -> bool:
        """Check if the realm needs stabilization maintenance."""
        if not self.last_stabilized:
            return True
            
        time_since_last = datetime.now() - self.last_stabilized
        current_stability = self.calculate_stability()
        energy_state = self.energy_grid.base_energy_level / self.tier.value
        
        return (time_since_last.days >= 30 or 
                current_stability < 0.7 or 
                energy_state < 0.5)

    def calculate_suppression(self, target_power: float) -> float:
        """Calculate realm suppression on a given power level."""
        base_suppression = 1.0 - (0.1 * (self.tier.value - 1))
        law_strength = sum(self.natural_laws.law_strength.values()) / len(self.natural_laws.law_strength)
        power_ratio = target_power / (self.tier.value * 1000)
        
        return max(0.1, base_suppression * (1 - power_ratio) * law_strength)

    def update_energy_grid(self, time_passed: float) -> None:
        """Update the energy grid based on time passed."""
        base_regen = self.energy_grid.regeneration_rate * time_passed
        
        for energy_type in self.energy_grid.energy_types:
            current_level = self.energy_grid.energy_types[energy_type]
            max_level = self.tier.value * 1000
            
            # Natural regeneration
            regen_amount = base_regen * (1 - current_level / max_level)
            self.energy_grid.energy_types[energy_type] = min(
                max_level,
                current_level + regen_amount
            )
        
        # Update stability based on energy levels
        total_energy = sum(self.energy_grid.energy_types.values())
        optimal_energy = self.tier.value * 1000 * len(self.energy_grid.energy_types)
        self.energy_grid.stability_index = min(1.0, total_energy / optimal_energy)