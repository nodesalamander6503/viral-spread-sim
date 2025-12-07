# Viral Spread & Profitability Simulator

This tool simulates the spread of a meme, product, or idea through a population and estimates profitability under different marketing and advertising conditions. It extends a basic compartmental model (Unreached -> Converts / Deniers) with optional economic shocks and paid-advertising dynamics.

## Features

### Initial Conditions
Specify:
	- Starting fraction of Converts
	- Starting fraction of Deniers
	- The rest of the population is treated as Unreached

### Basic Parameters
Control the behavior of the population via:
	- Convert exposure coefficient
	- Denier exposure coefficient
	- Fondness rate (likelihood that someone who ceases to be an Unreached will become a Convert and not a Denier)
	- Advertisement reach rate
	- Simulation duration (in time steps)

### Economic Shock
Optionally introduce a one-time structural change to the system:
	- Enable/disable shock
	- Choose shock time
	- Override starting parameters

### Profitability Modeling
The simulator provides economic outputs using your configured advertising and funnel assumptions:
	- Spending per time step
	- Earnings per time step
	- Net profit per time step
It depends on parameters:
	- Cost of advertising to the entire population
	- Population reach boundary (maximum proportion of populace to advertise to)

### Time-Series Plots
Generate dynamic graphs showing:
	- Proportion of population in each bucket (Unreached, Converts, Deniers) over time
	- Spending, earnings, and net profit over time

### Box Plot via Monte Carlo simulations
Run multiple simulations with randomized parameters (or noise) to obtain:
	- Distribution of final adoption levels
	- Spread of outcomes for Converts, Deniers, and Unreached
	- Visualization of uncertainty in long-run adoption

## Usage Overview

1. Enter initial conditions in the **Basic Controls** tab.
2. Adjust exposure, fondness, and advertisement parameters as needed.
3. (Optional) Configure a shock event in **Advanced Controls**.
4. Press **Plot** to:
   - Run the simulation
   - Generate population time plot
   - Generate profitability time plot
5. Use the **Box plot** tab to evaluate outcome variability across many runs, each with very small variations in parameters.
6. Review the **Summary** tab for aggregated metrics.

## Interpretation

	- **Converts**: Individuals who adopt and may promote the meme/product.
	- **Deniers**: Individuals who actively reject the meme/product but still influence others.
	- **Unreached**: Individuals with no exposure so far.
	- **Economic plots** show whether the campaign becomes profitable given the parameters.
	- **Shock system** helps model major publicity events, algorithm changes, scandals, or policy shifts.

## See Also

This README is intentionally minimal.
I am missing data about:
	- Parameter meanings
	- Mathematical model (ODEs or update rules)
	- Economic formulas
	- Installation / dependencies
	- Example runs and screenshots
The core codebase is primarily dependent on the Euclidean approximation and Reimann sum algorithm.
These are used to facilitate advanced time-series simulation without needing to first calculate integrals or derivatives or solve a system of differential equations.
All the other parts were made by following the documentation.

