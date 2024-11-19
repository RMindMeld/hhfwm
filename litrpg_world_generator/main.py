"""
Command-line interface for the LITRPG world generator.
Provides functionality to generate and manage cultivation worlds.
"""
import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from src.generators.world_generator import WorldGenerator
from src.constants import RealmTier

def save_world_data(world: WorldGenerator, output_dir: str) -> None:
    """Save all generated world data to JSON files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = Path(output_dir) / f"world_{timestamp}"
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Save realms
    realms_data = {
        str(realm_id): {
            "name": realm.name,
            "tier": realm.tier.name,
            "description": realm.description,
            "population": len([
                b_id for b_id, r_id in world.being_locations.items()
                if r_id == realm_id
            ]),
            "resources": len([
                r_id for r_id, r_loc in world.resource_locations.items()
                if r_loc == realm_id
            ])
        }
        for realm_id, realm in world.realms.items()
    }
    
    with open(base_dir / "realms.json", "w") as f:
        json.dump(realms_data, f, indent=2)
    
    # Save beings
    beings_data = {
        str(being_id): {
            "name": being.name,
            "race": being.race,
            "age": being.age,
            "cultivation_stage": being.cultivation.stage.name,
            "realm": being.cultivation.realm.name,
            "combat_power": being.calculate_combat_power(),
            "realm_location": str(world.being_locations[being_id])
        }
        for being_id, being in world.beings.items()
    }
    
    with open(base_dir / "beings.json", "w") as f:
        json.dump(beings_data, f, indent=2)
    
    # Save resources
    resources_data = {
        str(resource_id): {
            "name": resource.name,
            "tier": resource.tier.name,
            "description": resource.description,
            "formation_age": resource.formation_attributes.current_age,
            "realm_location": str(world.resource_locations[resource_id])
        }
        for resource_id, resource in world.resources.items()
    }
    
    with open(base_dir / "resources.json", "w") as f:
        json.dump(resources_data, f, indent=2)
    
    # Save relationships
    relationships_data = {
        "realm_hierarchies": {
            str(parent): [str(child) for child in children]
            for parent, children in world.realm_hierarchies.items()
        },
        "being_relationships": {
            str(being_id): {
                "master": str(being.master_id) if being.master_id else None,
                "disciples": [str(d_id) for d_id in being.disciples],
                "allies": {str(k): v for k, v in being.allies.items()},
                "enemies": {str(k): v for k, v in being.enemies.items()}
            }
            for being_id, being in world.beings.items()
        }
    }
    
    with open(base_dir / "relationships.json", "w") as f:
        json.dump(relationships_data, f, indent=2)

def print_world_statistics(world: WorldGenerator) -> None:
    """Print basic statistics about the generated world."""
    print("\n=== World Statistics ===")
    
    print("\nRealms:")
    for tier in RealmTier:
        count = len([r for r in world.realms.values() if r.tier == tier])
        if count > 0:
            print(f"  {tier.name}: {count}")
    
    print("\nBeings:")
    total_beings = len(world.beings)
    print(f"  Total Population: {total_beings}")
    
    realm_populations = {}
    for being_id, realm_id in world.being_locations.items():
        realm_name = world.realms[realm_id].name
        realm_populations[realm_name] = realm_populations.get(realm_name, 0) + 1
    
    print("\nPopulation by Realm:")
    for realm_name, pop in realm_populations.items():
        percentage = (pop / total_beings) * 100
        print(f"  {realm_name}: {pop} ({percentage:.1f}%)")
    
    print("\nResources:")
    total_resources = len(world.resources)
    print(f"  Total Resources: {total_resources}")
    
    realm_resources = {}
    for resource_id, realm_id in world.resource_locations.items():
        realm_name = world.realms[realm_id].name
        realm_resources[realm_name] = realm_resources.get(realm_name, 0) + 1
    
    print("\nResources by Realm:")
    for realm_name, count in realm_resources.items():
        percentage = (count / total_resources) * 100
        print(f"  {realm_name}: {count} ({percentage:.1f}%)")

def main():
    """Main entry point for the LITRPG world generator."""
    parser = argparse.ArgumentParser(
        description="Generate a LITRPG cultivation world with realms, beings, and resources."
    )
    
    parser.add_argument(
        "--realms",
        type=int,
        default=6,
        help="Number of realms to generate (default: 6)"
    )
    
    parser.add_argument(
        "--beings",
        type=int,
        default=1000,
        help="Base number of beings per realm (default: 1000)"
    )
    
    parser.add_argument(
        "--resources",
        type=int,
        default=100,
        help="Base number of resources per realm (default: 100)"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible generation"
    )
    
    parser.add_argument(
        "--quality",
        type=float,
        default=1.0,
        help="Base quality level for generation (0.0-1.0, default: 1.0)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="data",
        help="Output directory for generated data (default: 'data')"
    )
    
    args = parser.parse_args()
    
    # Create world generator
    world = WorldGenerator(
        seed=args.seed,
        base_quality_level=args.quality
    )
    
    print("Generating world...")
    world.generate_world(
        num_realms=args.realms,
        beings_per_realm=args.beings,
        resources_per_realm=args.resources
    )
    
    # Print statistics
    print_world_statistics(world)
    
    # Save data
    print(f"\nSaving world data to {args.output}...")
    save_world_data(world, args.output)
    print("Done!")

if __name__ == "__main__":
    main()