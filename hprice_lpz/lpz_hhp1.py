import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple

class HousingDataSimulator:
    def __init__(self, n_samples: int = 1000, random_state: int = 42):
        """
        Initialize the housing data simulator.
        
        Args:
            n_samples: Number of housing records to generate
            random_state: Random seed for reproducibility
        """
        self.n_samples = n_samples
        np.random.seed(random_state)
        
        # Define location-based parameters
        self.locations = {
            'Zona Sur': {'weight': 0.2, 'altitude_range': (3200, 3400)},
            'Miraflores': {'weight': 0.15, 'altitude_range': (3500, 3600)},
            'Centro': {'weight': 0.2, 'altitude_range': (3600, 3700)},
            'El Alto': {'weight': 0.25, 'altitude_range': (3800, 4100)},
            'Achumani': {'weight': 0.1, 'altitude_range': (3300, 3500)},
            'Obrajes': {'weight': 0.1, 'altitude_range': (3400, 3600)}
        }
        
        # Define income quartile probabilities for each location
        self.income_quartiles = {
            'Zona Sur': [0.05, 0.1, 0.25, 0.6],
            'Miraflores': [0.1, 0.3, 0.4, 0.2],
            'Centro': [0.2, 0.3, 0.3, 0.2],
            'El Alto': [0.5, 0.3, 0.15, 0.05],
            'Achumani': [0.1, 0.2, 0.4, 0.3],
            'Obrajes': [0.1, 0.2, 0.4, 0.3]
        }

    def generate_structural_variables(self) -> pd.DataFrame:
        """Generate structural variables for the houses."""
        df = pd.DataFrame()
        
        # Number of rooms (Shifted Poisson)
        df['num_rooms'] = np.random.poisson(lam=3, size=self.n_samples) + 1
        df.loc[df['num_rooms'] > 10, 'num_rooms'] = 10  # Cap at reasonable maximum
        
        # Number of bathrooms (Shifted Poisson)
        df['num_bathrooms'] = np.random.poisson(lam=1, size=self.n_samples) + 1
        df.loc[df['num_bathrooms'] > 6, 'num_bathrooms'] = 6
        
        # Size in square meters (Lognormal)
        df['size_m2'] = np.random.lognormal(mean=np.log(180), sigma=0.3, size=self.n_samples)
        
        # Lot size (mixture of discrete and continuous)
        urban_mask = np.random.random(self.n_samples) < 0.7
        df['lot_size_m2'] = np.where(
            urban_mask,
            np.random.choice([200, 300, 400], size=self.n_samples),
            np.random.lognormal(mean=np.log(500), sigma=0.5, size=self.n_samples)
        )
        
        # House age (bimodal distribution)
        age_distribution = np.concatenate([
            np.random.normal(20, 5, self.n_samples // 2),
            np.random.normal(50, 5, self.n_samples // 2)
        ])
        df['house_age'] = np.abs(age_distribution).astype(int)
        
        # Heating system
        df['heating_system'] = np.random.choice(['Yes', 'No'], size=self.n_samples, p=[0.6, 0.4])
        
        return df

    def generate_location_variables(self) -> pd.DataFrame:
        """Generate location-based variables."""
        df = pd.DataFrame()
        
        # Generate locations based on weights
        location_probs = [loc['weight'] for loc in self.locations.values()]
        df['location'] = np.random.choice(
            list(self.locations.keys()),
            size=self.n_samples,
            p=location_probs
        )
        
        # Generate altitude based on location
        df['altitude'] = df['location'].apply(
            lambda x: np.random.uniform(
                *self.locations[x]['altitude_range']
            )
        )
        
        # Generate income quartiles based on location
        df['income_quartile'] = df['location'].apply(
            lambda x: np.random.choice(
                ['Q1', 'Q2', 'Q3', 'Q4'],
                p=self.income_quartiles[x]
            )
        )
        
        return df

    def generate_neighborhood_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate neighborhood-related variables."""
        # Crime rate (exponential, influenced by income quartile)
        base_crime_rate = np.random.exponential(0.2, self.n_samples)
        quartile_multiplier = {
            'Q1': 1.5, 'Q2': 1.2, 'Q3': 0.8, 'Q4': 0.5
        }
        df['crime_rate'] = base_crime_rate * df['income_quartile'].map(quartile_multiplier)
        
        # School quality index (uniform, influenced by income quartile)
        base_quality = np.random.uniform(3, 10, self.n_samples)
        quality_multiplier = {
            'Q1': 0.7, 'Q2': 0.9, 'Q3': 1.1, 'Q4': 1.3
        }
        df['school_quality_index'] = base_quality * df['income_quartile'].map(quality_multiplier)
        df['school_quality_index'] = df['school_quality_index'].clip(0, 10)
        
        # Green space proportion (beta distribution)
        df['green_space_proportion'] = np.random.beta(2, 5, self.n_samples)
        
        # Noise pollution (normal distribution)
        df['noise_pollution'] = np.random.normal(60, 10, self.n_samples)
        
        return df

    def generate_environmental_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate environmental variables."""
        # Sunlight hours (normal distribution)
        df['sunlight_hours'] = np.random.normal(6, 1, self.n_samples)
        df['sunlight_hours'] = df['sunlight_hours'].clip(3, 9)
        
        return df

    def generate_market_variables(self) -> pd.DataFrame:
        """Generate market-related variables."""
        df = pd.DataFrame()
        
        # Market condition
        df['market_condition'] = np.random.choice(
            ["Buyer's", 'Balanced', "Seller's"],
            size=self.n_samples,
            p=[0.3, 0.4, 0.3]
        )
        
        # Season
        df['season'] = np.random.choice(
            ['Spring', 'Summer', 'Autumn', 'Winter'],
            size=self.n_samples,
            p=[0.3, 0.3, 0.2, 0.2]
        )
        
        return df

    def calculate_price(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate house prices based on all variables and their interactions.
        Returns prices in Bolivianos.
        """
        # Base price (lognormal distribution)
        base_price = np.random.lognormal(mean=np.log(750000), sigma=0.4, size=self.n_samples)
        
        # Location multiplier
        location_multiplier = {
            'Zona Sur': 1.5,
            'Miraflores': 1.2,
            'Centro': 1.0,
            'El Alto': 0.7,
            'Achumani': 1.3,
            'Obrajes': 1.2
        }
        
        # Calculate multipliers for various factors
        location_effect = df['location'].map(location_multiplier)
        size_effect = np.log1p(df['size_m2']) / np.log1p(180)
        rooms_effect = 1 + (df['num_rooms'] / 10)
        age_effect = 1 - (df['house_age'] / 100) + (df['house_age'] / 100) ** 2
        crime_effect = 1 - (df['crime_rate'] / df['crime_rate'].max())
        school_effect = 1 + (df['school_quality_index'] / 10) * 0.5
        green_space_effect = 1 + df['green_space_proportion'] * 0.3
        noise_effect = 1 - (df['noise_pollution'] > 70) * 0.2
        
        # Market condition effect
        market_multiplier = {
            "Buyer's": 0.9,
            'Balanced': 1.0,
            "Seller's": 1.1
        }
        market_effect = df['market_condition'].map(market_multiplier)
        
        # Season effect
        season_multiplier = {
            'Spring': 1.05,
            'Summer': 1.05,
            'Autumn': 0.95,
            'Winter': 0.95
        }
        season_effect = df['season'].map(season_multiplier)
        
        # Combine all effects
        final_price = (base_price * 
                      location_effect * 
                      size_effect * 
                      rooms_effect * 
                      age_effect * 
                      crime_effect * 
                      school_effect * 
                      green_space_effect * 
                      noise_effect * 
                      market_effect * 
                      season_effect)
        
        return final_price.round(2)

    def generate_dataset(self) -> pd.DataFrame:
        """Generate complete housing dataset."""
        # Generate all variable groups
        structural_df = self.generate_structural_variables()
        location_df = self.generate_location_variables()
        
        # Combine dataframes
        df = pd.concat([structural_df, location_df], axis=1)
        
        # Generate dependent variables
        df = self.generate_neighborhood_variables(df)
        df = self.generate_environmental_variables(df)
        
        # Add market variables
        market_df = self.generate_market_variables()
        df = pd.concat([df, market_df], axis=1)
        
        # Calculate price
        df['price'] = self.calculate_price(df)
        
        return df

# Usage example
def generate_housing_data(n_samples: int = 1000, random_state: int = 42) -> pd.DataFrame:
    """
    Generate a simulated housing dataset.
    
    Args:
        n_samples: Number of samples to generate
        random_state: Random seed for reproducibility
    
    Returns:
        pd.DataFrame: Simulated housing dataset
    """
    simulator = HousingDataSimulator(n_samples=n_samples, random_state=random_state)
    return simulator.generate_dataset()

# Generate example dataset
if __name__ == "__main__":
    housing_data = generate_housing_data(n_samples=1000)
    print(f"Generated {len(housing_data)} housing records")
    print("\nSample of the data:")
    print(housing_data.head())
    print("\nSummary statistics:")
    print(housing_data.describe())
    
    # Save to CSV
    housing_data.to_csv("simulated_housing_data.csv", index=False)
    print("\nData saved to 'simulated_housing_data.csv'")