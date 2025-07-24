# Profit Optimizer




## Requirements

- Python 3.13 or higher
- uv

## Installation

###  Using uv 

**Install uv** (if not already installed):
   ```bash
   pip install uv
   ```

**Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ocpy07
   ```

**Install dependencies**:
   ```bash
   # Install production dependencies only
   uv sync
   
   # Install with development dependencies (for development/testing)
   uv sync --group dev
   ```

## Running the Application

   ```bash
  uv run profit
   ```
### CLI Arguments
   ```bash
   
# Run greedy algorithm with default parameters on dataset_1
uv run profit --file dataset_1 --greedy
# Run greedy algorithm with default parameters
uv run profit --greedy

# Run greedy algorithm with custom budget
uv run profit --greedy --budget 1000

# Run greedy algorithm with purchase limit
uv run profit --greedy --limit 5

# Run greedy algorithm with all parameters
uv run profit --file dataset_1 --greedy --budget 1000 --limit 3
   ```
**Others values for args are:**
- **data files**: dataset_test | dataset_1 | dataset_2
- **algorithm**: greedy | knapsack | brute | pruning
- **budget**: at your convenience
- **limit**: at your convenience
  

⚠️⚠️⚠️**Warning**⚠️⚠️⚠️:
  
Brute force algorithm has exponential time complexity: O(2^n).
  
It may take several **years** to run on dataset_1 and dataset_2 (files with 1000 rows each) but 0.5 sec to run on 
dataset_test (20 rows)


## Development

### Code Quality Tools

This project uses several code quality tools:
- **flake8**: Code linting and style checking
- **black**: Code formatting
- **flake8-pyproject**: Integration between flake8 and pyproject.toml
