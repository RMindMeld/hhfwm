"""
Main generator for creating and managing the entire LITRPG world.
Coordinates realm, being, and resource generation to create a coherent world.
"""
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Optional, Set, Tuple
from uuid import UUID

from .base_generator import BaseGenerator
from .being_generator import BeingGenerator
from .resource_generator import ResourceGenerator
from .realm_generator import RealmGenerator
from ..models.being import Being
from ..models.resource import Resource
from ..models.realm import Realm
from ..constants import RealmTier, ResourceTier, POPULATION_DISTRIBUTION

class WorldGenerator:
    """Main generator for creating and managing the LITRPG world."""
    
    def __init__(
        self,
        seed: Optional[int] = None,
        base_quality_level: float = 1.0
    ):
        """Initialize the world generator."""
        self.rng = np.random.default_rng(seed)
        self.base_quality_level = base_quality_level
        self.current_time = datetime.now()
        
        # Initialize sub-generators
        self.being_generator = BeingGenerator(seed)
        self.resource_generator = ResourceGenerator(seed)
        self.realm_generator = RealmGenerator(seed)
        
        # Storage for generated entities
        self.realms: Dict[UUID, Realm] = {}
        self.beings: Dict[UUID, Being] = {}
        self.resources: Dict[UUID, Resource] = {}
        
        # Tracking relationships
        self.realm_hierarchies: Dict[UUID, List[UUID]] = {}  # parent -> children
        self.being_locations: Dict[UUID, UUID] = {}  # being -> realm
        self.resource_locations: Dict[UUID, UUID] = {}  # resource -> realm
        
    def generate_world(
        self,
        num_realms: int = 6,
        beings_per_realm: int = 1000,
        resources_per_realm: int = 100
    ) -> None:
        """Generate a complete world with all realms, beings, and resources."""
        # Generate realms from lowest to highest
        for tier in RealmTier:
            if len(self.realms) >= num_realms:
                break
                
            realm = self.realm_generator.generate_realm(tier=tier)
            self.realms[realm.id] = realm
            
            # Generate beings for this realm
            self._populate_realm(realm.id, beings_per_realm)
            
            # Generate resources for this realm
            self._generate_realm_resources(realm.id, resources_per_realm)
            
        # Establish realm connections
        self._establish_realm_connections()
        
        # Create relationships between entities
        self._establish_being_relationships()
        self._distribute_resources()
        
    def _populate_realm(self, realm_id: UUID, population: int) -> None:
        """Populate a realm with beings."""
        realm = self.realms[realm_id]
        
        # Calculate population distribution based on realm tier
        tier_distribution = POPULATION_DISTRIBUTION[realm.tier]
        actual_population = int(population * tier_distribution)
        
        for _ in range(actual_population):
            being = self.being_generator.generate_being(
                initial_realm=realm.tier
            )
            self.beings[being.id] = being
            self.being_locations[being.id] = realm_id
            
    def _generate_realm_resources(
        self,
        realm_id: UUID,
        resource_count: int
    ) -> None:
        """Generate resources for a realm."""
        realm = self.realms[realm_id]
        
        # Higher realms have rarer resources
        available_tiers = list(ResourceTier)[:realm.tier.value + 2]
        
        for _ in range(resource_count):
            tier = self.rng.choice(available_tiers)
            resource = self.resource_generator.generate_resource(tier=tier)
            self.resources[resource.id] = resource
            self.resource_locations[resource.id] = realm_id
            
    def _establish_realm_connections(self) -> None:
        """Establish connections between realms."""
        realm_list = list(self.realms.values())
        realm_list.sort(key=lambda x: x.tier.value)
        
        for i, lower_realm in enumerate(realm_list[:-1]):
            higher_realm = realm_list[i + 1]
            
            # Set parent-child relationship
            lower_realm.parent_realm = higher_realm.id
            higher_realm.child_realms.append(lower_realm.id)
            
            # Track hierarchy
            if higher_realm.id not in self.realm_hierarchies:
                self.realm_hierarchies[higher_realm.id] = []
            self.realm_hierarchies[higher_realm.id].append(lower_realm.id)
            
            # Set connection strength
            connection_strength = 0.5 + (0.5 * self.rng.random())
            lower_realm.connected_realms[higher_realm.id] = connection_strength
            higher_realm.connected_realms[lower_realm.id] = connection_strength
            
    def _establish_being_relationships(self) -> None:
        """Establish relationships between beings."""
        for being_id, being in self.beings.items():
            realm_id = self.being_locations[being_id]
            realm_beings = [
                b_id for b_id, r_id in self.being_locations.items()
                if r_id == realm_id and b_id != being_id
            ]
            
            # Create master-disciple relationships
            if self.rng.random() < 0.1:  # 10% chance to have disciples
                potential_disciples = [
                    b_id for b_id in realm_beings
                    if self.beings[b_id].cultivation.stage.value <
                    being.cultivation.stage.value
                ]
                
                if potential_disciples:
                    disciple_count = self.rng.integers(1, 4)
                    disciples = self.rng.choice(
                        potential_disciples,
                        size=min(disciple_count, len(potential_disciples)),
                        replace=False
                    )
                    
                    for disciple_id in disciples:
                        self.beings[disciple_id].master_id = being_id
                        being.disciples.append(disciple_id)
                        
            # Create ally and enemy relationships
            num_relationships = self.rng.integers(1, 6)
            potential_relations = self.rng.choice(
                realm_beings,
                size=min(num_relationships, len(realm_beings)),
                replace=False
            )
            
            for other_id in potential_relations:
                if self.rng.random() < 0.7:  # 70% chance for ally
                    relationship_strength = 0.3 + (0.7 * self.rng.random())
                    being.allies[other_id] = relationship_strength
                    self.beings[other_id].allies[being_id] = relationship_strength
                else:  # 30% chance for enemy
                    enmity_level = 0.3 + (0.7 * self.rng.random())
                    being.enemies[other_id] = enmity_level
                    self.beings[other_id].enemies[being_id] = enmity_level
                    
    def _distribute_resources(self) -> None:
        """Distribute resources among beings."""
        for resource_id, resource in self.resources.items():
            realm_id = self.resource_locations[resource_id]
            realm_beings = [
                b_id for b_id, r_id in self.being_locations.items()
                if r_id == realm_id
            ]
            
            if not realm_beings:
                continue
                
            # Higher quality resources go to stronger beings
            if resource.tier.value >= ResourceTier.RARE.value:
                potential_owners = [
                    b_id for b_id in realm_beings
                    if self.beings[b_id].cultivation.stage.value >= 
                    resource.tier.value
                ]
                
                if potential_owners:
                    owner_id = self.rng.choice(potential_owners)
                    owner = self.beings[owner_id]
                    owner.inventory.artifacts[resource.name] = resource.quality_metrics.base_grade
                    
    def advance_time(self, years: float = 0.0, days: float = 0.0) -> None:
        """Advance time in the world and update all entities."""
        time_delta = timedelta(days=days + years * 365.25)
        self.current_time += time_delta
        
        # Update all entities
        self._update_realms(time_delta)
        self._update_beings(time_delta)
        self._update_resources(time_delta)
        
    def _update_realms(self, time_delta: timedelta) -> None:
        """Update all realms based on time passed."""
        for realm in self.realms.values():
            # Update energy grid
            realm.energy_grid.base_energy_level *= (
                1 + realm.energy_grid.regeneration_rate * 
                time_delta.total_seconds() / (365.25 * 24 * 3600)
            )
            
            # Degrade formation
            realm.formation_details.age += time_delta.days / 365.25
            
            # Update stability
            if realm.needs_stabilization():
                realm.last_stabilized = self.current_time
                realm.stability_history.append({
                    'timestamp': self.current_time,
                    'stability': realm.calculate_stability(),
                    'energy_state': realm.energy_grid.stability_index
                })
                
    def _update_beings(self, time_delta: timedelta) -> None:
        """Update all beings based on time passed."""
        for being in self.beings.values():
            # Age the being
            being.age += time_delta.days / 365.25
            
            # Check for breakthroughs
            if being.can_breakthrough():
                tribulation = being.generate_tribulation()
                being.tribulation_history.append(tribulation)
                being.last_breakthrough = self.current_time
                
            # Update karma
            being.update_karma('time_passage', 0.001 * time_delta.days)
            
    def _update_resources(self, time_delta: timedelta) -> None:
        """Update all resources based on time passed."""
        for resource in self.resources.values():
            # Age the resource
            resource.formation_attributes.current_age += time_delta.days / 365.25
            
            # Apply natural degradation
            resource.degrade(time_delta.days / 365.25)
            
    def get_realm_beings(self, realm_id: UUID) -> List[Being]:
        """Get all beings in a specific realm."""
        return [
            being for being_id, being in self.beings.items()
            if self.being_locations[being_id] == realm_id
        ]
        
    def get_realm_resources(self, realm_id: UUID) -> List[Resource]:
        """Get all resources in a specific realm."""
        return [
            resource for resource_id, resource in self.resources.items()
            if self.resource_locations[resource_id] == realm_id
        ]
        
    def get_being_realm(self, being_id: UUID) -> Optional[Realm]:
        """Get the realm a being is currently in."""
        realm_id = self.being_locations.get(being_id)
        return self.realms.get(realm_id) if realm_id else None
        
    def get_resource_realm(self, resource_id: UUID) -> Optional[Realm]:
        """Get the realm a resource is currently in."""
        realm_id = self.resource_locations.get(resource_id)
        return self.realms.get(realm_id) if realm_id else None