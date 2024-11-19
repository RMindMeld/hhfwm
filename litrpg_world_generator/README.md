# LITRPG World Generator

A Python-based generator for creating detailed LITRPG/cultivation worlds with realistic mechanics, relationships, and progression systems.

## Features

- **Multi-Realm Generation**: Create hierarchical realms from mortal to divine planes
- **Complex Being Generation**: Generate cultivators with realistic attributes, relationships, and progression paths
- **Resource System**: Create cultivation resources with formation mechanics and quality variations
- **Realistic Mechanics**: Implements natural laws, breakthrough mechanics, and realm suppression
- **Data Quality Simulation**: Models realistic information gathering challenges and measurement errors
- **Relationship Systems**: Generates master-disciple relationships, alliances, and enmities
- **Time Progression**: Supports time advancement with appropriate world updates

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/litrpg-world-generator.git
cd litrpg-world-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Generate a world using the command-line interface:

```bash
python main.py --realms 6 --beings 1000 --resources 100
```

### Command Line Options

- `--realms`: Number of realms to generate (default: 6)
- `--beings`: Base number of beings per realm (default: 1000)
- `--resources`: Base number of resources per realm (default: 100)
- `--seed`: Random seed for reproducible generation
- `--quality`: Base quality level for generation (0.0-1.0, default: 1.0)
- `--output`: Output directory for generated data (default: 'data')

## Generated Data

The generator creates several JSON files containing the world data:

### realms.json
Contains information about each realm:
```json
{
    "realm_id": {
        "name": "Mortal Realm",
        "tier": "MORTAL",
        "description": "A mortal plane of existence...",
        "population": 1000,
        "resources": 100
    }
}
```

### beings.json
Contains information about all beings:
```json
{
    "being_id": {
        "name": "Azure Dragon 1234",
        "race": "Human",
        "age": 100,
        "cultivation_stage": "FOUNDATION_ESTABLISHMENT",
        "realm": "MORTAL",
        "combat_power": 1000,
        "realm_location": "realm_id"
    }
}
```

### resources.json
Contains information about all resources:
```json
{
    "resource_id": {
        "name": "Divine Fire Crystal",
        "tier": "RARE",
        "description": "A rare crystal formed in...",
        "formation_age": 1000,
        "realm_location": "realm_id"
    }
}
```

### relationships.json
Contains relationship data between entities:
```json
{
    "realm_hierarchies": {
        "parent_realm_id": ["child_realm_id1", "child_realm_id2"]
    },
    "being_relationships": {
        "being_id": {
            "master": "master_id",
            "disciples": ["disciple_id1", "disciple_id2"],
            "allies": {"ally_id": 0.8},
            "enemies": {"enemy_id": 0.6}
        }
    }
}
```

## Project Structure

```
litrpg_world_generator/
├── src/
│   ├── models/
│   │   ├── being.py         # Being/cultivator model
│   │   ├── resource.py      # Resource/treasure model
│   │   └── realm.py         # Realm/plane model
│   ├── generators/
│   │   ├── base_generator.py     # Base generation utilities
│   │   ├── being_generator.py    # Being generation
│   │   ├── resource_generator.py # Resource generation
│   │   ├── realm_generator.py    # Realm generation
│   │   └── world_generator.py    # Main world generation
│   └── constants.py         # Configuration and constants
├── data/                    # Generated data output
├── main.py                 # CLI interface
└── requirements.txt        # Project dependencies
```

## Example Usage

Generate a small world for testing:
```bash
python main.py --realms 3 --beings 100 --resources 20
```

Generate a large world with high quality:
```bash
python main.py --realms 9 --beings 5000 --resources 500 --quality 1.0
```

Generate a reproducible world:
```bash
python main.py --seed 12345
```

## Data Model Features

### Beings
- Cultivation paths and stages
- Bloodline inheritance
- Soul attributes
- Combat capabilities
- Inventory system
- Karma and destiny
- Relationships and connections

### Resources
- Formation mechanics
- Energy characteristics
- Quality metrics
- Usage requirements
- Special effects
- Natural aging

### Realms
- Natural laws
- Space-time characteristics
- Energy distribution
- Population metrics
- Formation stability
- Environmental effects

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.