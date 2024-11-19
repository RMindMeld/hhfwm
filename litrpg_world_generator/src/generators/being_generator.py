"""
Generator for creating cultivator beings in the LITRPG world.
Handles creation of individuals with realistic attributes and relationships.
"""
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Optional, Set, Tuple
from uuid import UUID

from .base_generator import BaseGenerator
from ..models.being import (
    Being, Bloodline, CultivationBase, Soul,
    Combat, Inventory, Karma, Achievement
)
from ..constants import CultivationStage, RealmTier

class BeingGenerator(BaseGenerator):
    """Generator for creating cultivator beings."""
    
    def __init__(
        self,
        seed: Optional[int] = None,
        quality_level: float = 1.0,
        realm_tier: RealmTier = RealmTier.MORTAL
    ):
        """Initialize the being generator."""
        super().__init__(seed, quality_level, realm_tier)
        self.name_prefixes = ['Azure', 'Jade', 'Golden', 'Sacred', 'Divine', 'Ancient']
        self.name_suffixes = ['Dragon', 'Phoenix', 'Tiger', 'Turtle', 'Serpent', 'Lion']
        
    def generate_being(
        self,
        age: Optional[int] = None,
        bloodline_strength: Optional[float] = None,
        initial_realm: Optional[RealmTier] = None
    ) -> Being:
        """Generate a complete being with all attributes."""
        if age is None:
            age = self._generate_age()
        if bloodline_strength is None:
            bloodline_strength = self.rng.random()
        if initial_realm is None:
            initial_realm = self.realm_tier
            
        name = self._generate_name()
        race = self._generate_race()
        
        # Generate core attributes
        bloodline = self._generate_bloodline(bloodline_strength)
        cultivation = self._generate_cultivation_base(initial_realm)
        soul = self._generate_soul(bloodline_strength)
        combat = self._generate_combat(cultivation.stage)
        inventory = self._generate_inventory(cultivation.stage)
        karma = self._generate_karma()
        achievements = self._generate_achievements()
        
        # Calculate data quality metrics
        measurement_accuracy = self._calculate_measurement_accuracy(cultivation.stage)
        data_reliability = self._calculate_data_reliability(age)
        
        return Being(
            name=name,
            race=race,
            age=age,
            bloodline=bloodline,
            cultivation=cultivation,
            soul=soul,
            combat=combat,
            inventory=inventory,
            karma=karma,
            achievements=achievements,
            measurement_accuracy=measurement_accuracy,
            data_reliability=data_reliability,
            hidden_attributes=self._generate_hidden_attributes(cultivation.stage)
        )
        
    def _generate_name(self) -> str:
        """Generate a cultivator name."""
        prefix = self.rng.choice(self.name_prefixes)
        suffix = self.rng.choice(self.name_suffixes)
        number = self.rng.integers(1, 9999)
        return f"{prefix} {suffix} {number}"
        
    def _generate_race(self) -> str:
        """Generate a being's race."""
        races = ['Human', 'Dragon', 'Phoenix', 'Demon', 'Spirit', 'Ancient']
        weights = [0.7, 0.1, 0.05, 0.1, 0.03, 0.02]
        return self.rng.choice(races, p=weights)
        
    def _generate_age(self) -> int:
        """Generate an appropriate age based on realm."""
        base_age = self.rng.integers(16, 100)
        realm_bonus = self.realm_tier.value * 100
        return base_age + realm_bonus
        
    def _generate_bloodline(self, strength: float) -> Bloodline:
        """Generate bloodline attributes."""
        purity = strength * self.rng.random()
        mutation_factor = self.rng.random() * 0.1
        
        traits = set()
        num_traits = self.rng.integers(1, 4)
        possible_traits = [
            'Fire Affinity', 'Water Mastery', 'Lightning Soul',
            'Earth Heart', 'Wind Spirit', 'Time Perception',
            'Space Comprehension', 'Fate Sensitivity'
        ]
        traits.update(self.rng.choice(possible_traits, size=num_traits, replace=False))
        
        return Bloodline(
            name=f"{self.rng.choice(self.name_prefixes)} Bloodline",
            purity=purity,
            traits=traits,
            mutation_factor=mutation_factor,
            inherited_power=strength * 100,
            special_abilities=[f"{trait} Mastery" for trait in traits]
        )
        
    def _generate_cultivation_base(self, realm: RealmTier) -> CultivationBase:
        """Generate cultivation attributes."""
        stage = self._determine_cultivation_stage(realm)
        foundation_quality = self.generate_talent_rating()
        cultivation_speed = self.generate_cultivation_speed()
        
        return CultivationBase(
            stage=stage,
            realm=realm,
            foundation_quality=foundation_quality,
            cultivation_speed=cultivation_speed,
            bottleneck_threshold=0.7 + (0.1 * self.rng.random()),
            comprehension_rate=0.1 + (0.4 * self.rng.random()),
            dao_insights={
                'Heaven': self.rng.random(),
                'Earth': self.rng.random(),
                'Humanity': self.rng.random(),
                'Fate': self.rng.random(),
                'Time': self.rng.random(),
                'Space': self.rng.random()
            }
        )
        
    def _generate_soul(self, bloodline_strength: float) -> Soul:
        """Generate soul attributes."""
        base_strength = bloodline_strength * 100
        realm_multiplier = self.realm_tier.value
        
        return Soul(
            strength=base_strength * realm_multiplier,
            purity=0.3 + (0.7 * self.rng.random()),
            stability=0.4 + (0.6 * self.rng.random()),
            resonance={
                'Natural': self.rng.random(),
                'Artificial': self.rng.random(),
                'Divine': self.rng.random(),
                'Demonic': self.rng.random()
            },
            cultivation_affinity=['Fire', 'Water', 'Earth', 'Wind', 'Lightning'],
            dao_marks={'Heaven', 'Earth'} if self.rng.random() > 0.8 else set()
        )
        
    def _generate_combat(self, stage: CultivationStage) -> Combat:
        """Generate combat capabilities."""
        base_power = 10 * (stage.value + 1)
        
        techniques = {
            'Sword': self.rng.random(),
            'Palm': self.rng.random(),
            'Movement': self.rng.random(),
            'Formation': self.rng.random(),
            'Body': self.rng.random()
        }
        
        weapons = {
            'Sword': self.rng.random(),
            'Spear': self.rng.random(),
            'Bow': self.rng.random(),
            'Staff': self.rng.random()
        }
        
        return Combat(
            base_power=base_power,
            technique_mastery=techniques,
            battle_experience=self.rng.random() * 1000,
            weapon_proficiency=weapons,
            special_moves={
                'Dragon Strike',
                'Phoenix Flame',
                'Tiger Roar'
            } if self.rng.random() > 0.7 else set()
        )
        
    def _generate_inventory(self, stage: CultivationStage) -> Inventory:
        """Generate inventory contents."""
        storage_rings = max(1, stage.value // 3)
        
        return Inventory(
            storage_rings=storage_rings,
            artifacts={
                'Basic Sword': 0.5,
                'Protection Talisman': 0.3,
                'Flying Sword': 0.8
            },
            resources={
                'Spirit Stone': 1000,
                'Qi Condensing Pill': 50,
                'Foundation Pill': 10
            },
            currency={
                'Spirit Stones': 10000,
                'Contribution Points': 1000
            },
            equipment_slots={
                'weapon': 'Basic Sword',
                'armor': 'Cotton Robe',
                'accessory': 'Jade Pendant'
            }
        )
        
    def _generate_karma(self) -> Karma:
        """Generate karmic attributes."""
        return Karma(
            fate_value=self.rng.normal(0, 1),
            connections={},  # Empty initially
            destiny_threads=[
                'Great Fortune',
                'Minor Calamity',
                'Hidden Opportunity'
            ],
            karmic_debt=max(0, self.rng.normal(0, 10)),
            fortune=self.rng.random() * 2 - 1,  # -1 to 1
            tribulation_counter=0
        )
        
    def _generate_achievements(self) -> Achievement:
        """Generate achievements and titles."""
        return Achievement(
            titles={'Cultivator'},
            reputation={
                'Mortal World': self.rng.random(),
                'Spirit World': self.rng.random(),
                'Demon World': self.rng.random()
            },
            accomplishments=[
                'Began Cultivation',
                'Formed Core',
                'Survived Tribulation'
            ],
            hidden_achievements=set()
        )
        
    def _determine_cultivation_stage(self, realm: RealmTier) -> CultivationStage:
        """Determine appropriate cultivation stage for realm."""
        if realm == RealmTier.MORTAL:
            stages = [
                CultivationStage.BODY_REFINEMENT,
                CultivationStage.QI_CONDENSATION,
                CultivationStage.FOUNDATION_ESTABLISHMENT,
                CultivationStage.CORE_FORMATION
            ]
        elif realm == RealmTier.SPIRIT:
            stages = [
                CultivationStage.NASCENT_SOUL,
                CultivationStage.SPIRIT_SEVERING,
                CultivationStage.VOID_FORMATION
            ]
        else:
            stages = [
                CultivationStage.DAO_SEEKING,
                CultivationStage.DAO_MANIFESTATION,
                CultivationStage.DAO_MASTERY
            ]
            
        weights = np.array([4, 2, 1])  # Higher weights for lower stages
        weights = weights[:len(stages)]
        weights = weights / weights.sum()
        
        return self.rng.choice(stages, p=weights)
        
    def _calculate_measurement_accuracy(self, stage: CultivationStage) -> float:
        """Calculate how accurately the being's attributes can be measured."""
        base_accuracy = 0.7
        stage_penalty = 0.05 * stage.value
        realm_penalty = 0.1 * self.realm_tier.value
        
        return max(0.1, min(1.0, base_accuracy - stage_penalty - realm_penalty))
        
    def _calculate_data_reliability(self, age: int) -> float:
        """Calculate how reliable the being's data is based on age."""
        base_reliability = 0.9
        age_penalty = 0.001 * (age / 100)
        realm_penalty = 0.05 * self.realm_tier.value
        
        return max(0.1, min(1.0, base_reliability - age_penalty - realm_penalty))
        
    def _generate_hidden_attributes(self, stage: CultivationStage) -> Set[str]:
        """Determine which attributes are hidden from measurement."""
        possible_hidden = {
            'true_power_level',
            'dao_comprehension',
            'fate_connection',
            'soul_structure',
            'bloodline_secrets'
        }
        
        hide_probability = 0.1 * stage.value
        return {attr for attr in possible_hidden if self.rng.random() < hide_probability}