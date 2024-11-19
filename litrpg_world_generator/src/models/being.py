"""
Core model for beings in the LITRPG world.
Represents individual entities with their cultivation paths and attributes.
"""
from datetime import datetime
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

from ..constants import CultivationStage, RealmTier

class Bloodline(BaseModel):
    """Represents a being's bloodline inheritance and traits."""
    name: str
    purity: float = Field(ge=0.0, le=1.0)
    traits: Set[str]
    mutation_factor: float = Field(ge=0.0, le=1.0)
    inherited_power: float = Field(ge=0.0)
    special_abilities: List[str]

class CultivationBase(BaseModel):
    """Represents a being's cultivation foundation and progress."""
    stage: CultivationStage
    realm: RealmTier
    foundation_quality: float = Field(ge=0.0, le=1.0)
    cultivation_speed: float = Field(ge=0.0)
    bottleneck_threshold: float = Field(ge=0.0, le=1.0)
    comprehension_rate: float = Field(ge=0.0, le=1.0)
    dao_insights: Dict[str, float] = Field(default_factory=dict)

class Soul(BaseModel):
    """Represents a being's soul attributes and cultivation."""
    strength: float = Field(ge=0.0)
    purity: float = Field(ge=0.0, le=1.0)
    stability: float = Field(ge=0.0, le=1.0)
    resonance: Dict[str, float] = Field(default_factory=dict)
    cultivation_affinity: List[str]
    dao_marks: Set[str] = Field(default_factory=set)

class Combat(BaseModel):
    """Represents a being's combat capabilities."""
    base_power: float = Field(ge=0.0)
    technique_mastery: Dict[str, float] = Field(default_factory=dict)
    battle_experience: float = Field(ge=0.0)
    weapon_proficiency: Dict[str, float] = Field(default_factory=dict)
    special_moves: Set[str] = Field(default_factory=set)

class Inventory(BaseModel):
    """Represents a being's possessions and equipment."""
    storage_rings: int = Field(ge=0)
    artifacts: Dict[str, float]  # name: quality
    resources: Dict[str, int]    # name: quantity
    currency: Dict[str, int]     # type: amount
    equipment_slots: Dict[str, Optional[str]]  # slot: item_name

class Karma(BaseModel):
    """Represents a being's karmic relationships and destiny."""
    fate_value: float
    connections: Dict[UUID, float]  # being_id: connection_strength
    destiny_threads: List[str]
    karmic_debt: float = Field(ge=0.0)
    fortune: float
    tribulation_counter: int = Field(ge=0)

class Achievement(BaseModel):
    """Represents a being's accomplishments and titles."""
    titles: Set[str] = Field(default_factory=set)
    reputation: Dict[str, float] = Field(default_factory=dict)
    accomplishments: List[str] = Field(default_factory=list)
    hidden_achievements: Set[str] = Field(default_factory=set)

class Being(BaseModel):
    """Main model representing a cultivator or any sentient being."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    race: str
    age: int = Field(ge=0)
    creation_date: datetime = Field(default_factory=datetime.now)
    
    # Core attributes
    bloodline: Bloodline
    cultivation: CultivationBase
    soul: Soul
    combat: Combat
    inventory: Inventory
    karma: Karma
    achievements: Achievement
    
    # Tracking fields
    last_breakthrough: Optional[datetime]
    tribulation_history: List[Dict[str, any]]
    cultivation_insights: List[str]
    battle_records: List[Dict[str, any]]
    
    # Social connections
    sect_id: Optional[UUID]
    master_id: Optional[UUID]
    disciples: List[UUID] = Field(default_factory=list)
    allies: Dict[UUID, float] = Field(default_factory=dict)  # being_id: relationship_strength
    enemies: Dict[UUID, float] = Field(default_factory=dict)  # being_id: enmity_level
    
    # Data quality tracking
    measurement_accuracy: float = Field(ge=0.0, le=1.0)
    last_updated: datetime = Field(default_factory=datetime.now)
    data_reliability: float = Field(ge=0.0, le=1.0)
    hidden_attributes: Set[str] = Field(default_factory=set)

    class Config:
        arbitrary_types_allowed = True

    def calculate_combat_power(self) -> float:
        """Calculate the being's total combat power."""
        base = self.combat.base_power
        realm_mult = self.cultivation.realm.value
        technique_bonus = sum(self.combat.technique_mastery.values())
        soul_factor = self.soul.strength
        
        return base * realm_mult * (1 + technique_bonus) * soul_factor

    def can_breakthrough(self) -> bool:
        """Check if the being can attempt breakthrough to next stage."""
        if not self.last_breakthrough:
            return True
            
        time_since_last = datetime.now() - self.last_breakthrough
        required_insights = len(self.cultivation_insights)
        foundation_check = self.cultivation.foundation_quality > self.cultivation.bottleneck_threshold
        
        return (time_since_last.days >= 30 and 
                required_insights >= 3 and 
                foundation_check)

    def generate_tribulation(self) -> Dict[str, any]:
        """Generate a tribulation event based on cultivation stage."""
        power_level = self.calculate_combat_power()
        stage_factor = self.cultivation.stage.value
        karma_influence = self.karma.fate_value
        
        return {
            'power_level': power_level,
            'difficulty': stage_factor * (1 + abs(karma_influence)),
            'type': f"{self.cultivation.stage.name}_TRIBULATION",
            'timestamp': datetime.now()
        }

    def update_karma(self, event: str, magnitude: float) -> None:
        """Update karmic values based on actions and events."""
        self.karma.fate_value += magnitude
        self.karma.fortune = max(-1, min(1, self.karma.fortune + magnitude * 0.1))
        
        if abs(self.karma.fate_value) > 10:
            self.karma.tribulation_counter += 1