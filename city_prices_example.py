#!/usr/bin/env python3
"""
Numbeo City Prices Example

This script fetches cost of living data from the Numbeo API for a given city and country,
and displays the prices in a formatted terminal output.

Usage:
    python city_prices_example.py --city "San Francisco, CA" --country "United States" --api-key YOUR_API_KEY

    Or set the API key as an environment variable:
    export NUMBEO_API_KEY=your_api_key
    python city_prices_example.py --city "San Francisco, CA" --country "United States"
"""

import argparse
import os
import sys
from typing import Dict, Any
import requests


class NumbeoAPIClient:
    """Client for interacting with the Numbeo API."""

    BASE_URL = "https://www.numbeo.com/api"

    def __init__(self, api_key: str):
        """
        Initialize the Numbeo API client.

        Args:
            api_key: Your Numbeo API key
        """
        self.api_key = api_key
        self.session = requests.Session()

    def get_city_prices(self, city: str, country: str) -> Dict[str, Any]:
        """
        Fetch city prices from the Numbeo API.

        Args:
            city: City name (e.g., "San Francisco, CA")
            country: Country name (e.g., "United States")

        Returns:
            Dictionary containing the API response

        Raises:
            requests.RequestException: If the API request fails
        """
        endpoint = f"{self.BASE_URL}/city_prices"
        params = {
            "city": city,
            "country": country,
            "api_key": self.api_key
        }

        try:
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response: {response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise


def format_price(price: float, currency: str = "USD") -> str:
    """Format a price value for display."""
    return f"${price:.2f}" if currency == "USD" else f"{price:.2f} {currency}"


def display_prices(data: Dict[str, Any]) -> None:
    """
    Display the city prices in a formatted terminal output.

    Args:
        data: The JSON response from the Numbeo API
    """
    if not data:
        print("No data received from the API.")
        return

    # Display city information
    city = data.get("name", "Unknown")
    country = data.get("country", "Unknown")
    currency = data.get("currency", "USD")

    print("\n" + "=" * 80)
    print(f"COST OF LIVING DATA: {city}, {country}")
    print("=" * 80)
    print(f"Currency: {currency}\n")

    # Display prices
    prices = data.get("prices", [])

    if not prices:
        print("No price data available.")
        return

    # Group prices by category if available
    categories = {}
    for item in prices:
        item_name = item.get("item_name", "Unknown Item")
        average_price = item.get("average_price")
        lowest_price = item.get("lowest_price")
        highest_price = item.get("highest_price")
        data_points = item.get("data_points", 0)
        category = item.get("category_name", "Other")

        if category not in categories:
            categories[category] = []

        categories[category].append({
            "name": item_name,
            "average": average_price,
            "lowest": lowest_price,
            "highest": highest_price,
            "data_points": data_points
        })

    # Display prices by category
    for category, items in categories.items():
        print(f"\n{category}:")
        print("-" * 80)

        for item in items:
            print(f"\n  {item['name']}")

            if item['average'] is not None:
                print(f"    Average: {format_price(item['average'], currency)}")

            if item['lowest'] is not None and item['highest'] is not None:
                print(f"    Range: {format_price(item['lowest'], currency)} - {format_price(item['highest'], currency)}")

            if item['data_points']:
                print(f"    Data points: {item['data_points']}")

    print("\n" + "=" * 80 + "\n")


def main():
    """Main function to run the example."""
    parser = argparse.ArgumentParser(
        description="Fetch and display Numbeo city prices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --city "San Francisco, CA" --country "United States" --api-key YOUR_KEY
  %(prog)s --city "London" --country "United Kingdom" --api-key YOUR_KEY

Environment Variables:
  NUMBEO_API_KEY    Your Numbeo API key (alternative to --api-key)
        """
    )

    parser.add_argument(
        "--city",
        required=True,
        help="City name (e.g., 'San Francisco, CA')"
    )

    parser.add_argument(
        "--country",
        required=True,
        help="Country name (e.g., 'United States')"
    )

    parser.add_argument(
        "--api-key",
        help="Numbeo API key (or set NUMBEO_API_KEY environment variable)"
    )

    args = parser.parse_args()

    # Get API key from arguments or environment
    api_key = args.api_key or os.environ.get("NUMBEO_API_KEY")

    if not api_key:
        print("Error: API key is required.", file=sys.stderr)
        print("Provide it via --api-key argument or NUMBEO_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    # Create client and fetch data
    try:
        print(f"Fetching price data for {args.city}, {args.country}...")
        client = NumbeoAPIClient(api_key)
        data = client.get_city_prices(args.city, args.country)
        display_prices(data)
    except requests.exceptions.RequestException as e:
        print(f"\nError fetching data: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
