# numbeo-api-python

Numbeo API Example – Retrieve Cost of Living for a City

This repository contains a Python example application that demonstrates how to fetch and display cost of living data from the [Numbeo API](https://www.numbeo.com/common/api.jsp) for any city and country.

## Features

- Fetch real-time cost of living data from Numbeo API
- Display prices organized by category
- Show average, minimum, and maximum prices
- Command-line interface with flexible API key configuration
- Clean, formatted terminal output

## Installation

1. Clone this repository:
```bash
git clone https://github.com/mladenadamovic/numbeo-api-python.git
cd numbeo-api-python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python city_prices_example.py --city "San Francisco, CA" --country "United States" --api-key YOUR_API_KEY
```

### Using Environment Variable

Set your API key as an environment variable:

```bash
export NUMBEO_API_KEY=your_api_key
python city_prices_example.py --city "San Francisco, CA" --country "United States"
```

### More Examples

```bash
# London, UK
python city_prices_example.py --city "London" --country "United Kingdom" --api-key YOUR_KEY

# Tokyo, Japan
python city_prices_example.py --city "Tokyo" --country "Japan" --api-key YOUR_KEY

# Paris, France
python city_prices_example.py --city "Paris" --country "France" --api-key YOUR_KEY
```

## Sample Output

```
Fetching price data for San Francisco, CA, United States...

================================================================================
COST OF LIVING DATA: San Francisco, CA, United States
================================================================================
Currency: USD

Restaurants:
--------------------------------------------------------------------------------

  Meal, Inexpensive Restaurant
    Average: $25.00
    Range: $15.00 - $40.00
    Data points: 450

  Meal for 2 People, Mid-range Restaurant, Three-course
    Average: $100.00
    Range: $70.00 - $150.00
    Data points: 320

...
```

## API Key

You need a valid Numbeo API key to use this application. Visit [Numbeo API Documentation](https://www.numbeo.com/common/api.jsp) to obtain your API key.

## Requirements

- Python 3.7+
- requests library (see requirements.txt)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
