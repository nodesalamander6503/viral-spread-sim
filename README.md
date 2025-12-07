# Viral Spread & Profitability Simulator

This tool simulates the spread of a meme, product, or idea through a population and estimates profitability under different marketing and advertising conditions. It extends a basic compartmental model (Unreached -> Converts / Deniers) with optional economic shocks and paid-advertising dynamics.

The current version of the tool is in `4para-sim.py`.
It is based on the code in `basic-sim.py`, which is far less powerful, but served as an initial proof-of-concept.
I created `basic-sim.py` in about 2 hours, then upgraded it to `4para-sim.py` after finals.

# Systems

## Initial Conditions

Since this is based on a system of differential equations, it requires some starting parameters.

First, we must know the starting population proportions.
The user specifies the proportion of population that are converts, and the proportion that are deniers.
The proportion that are unreached is assumed to be the remainder.

## Basic Parameters

The simulation is dependent on several parameters.

The exposure coefficients are the rate at which converts and deniers are able to autonomously reach the unreached, respectively.
This is included because it is assumed that people talk naturally, and that this is one possible method for spreading a meme.
We treat these as non-uniform to account for differences in opinion.
However, you can disable communication for a population by setting their coefficient to zero.
You can also treat the exposure coefficients as uniform by setting them to the same value.

## Economic Shock

You can introduce a one-time economic shock (that is, a change to the system's parameters) in order to model the effects of some decision.
This model assumes that these decisions are instantaneous, as though modeled by Heaviside step function.

Shocks are optional and are toggled in their menu.

You can modify any parameter in a shock.
However, you can not modify a starting condition in a shock.

## Profitability Modeling

The simulator provides economic outputs using your configured advertising and funnel assumptions:

- Spending per time step
- Earnings per time step
- Net profit per time step
It depends on parameters:

- Cost of advertising to the entire population
- Population reach boundary (maximum proportion of populace to advertise to)

## Plots

The simulation generates three plots.

The population time-series plot gives you an idea of the state of the population at various points in time throughout the simulation.
It contains one line for each stratum of society.

The financial time-series plot indicates quantity spent, quantity earned, and net.
Note that this plot shows the actual value and not the rates of change.
At points where net is negative, the advertising campaign has lost money.

Every time-series plot has a vertical dotted line at the point of a shock.
This allows you to discern the effect that a shock has.

The simulation automatically repeats all simulations with minor variations in parameters.
It then uses these Monte Carlo simulations to discern a predicted range of results.
This range is visualized in the box-and-whisker plot.
The numerical results can also be accessed in the summary.

# Usage Overview

1. Enter initial conditions in the **Basic Controls** tab.
2. Adjust exposure, fondness, and advertisement parameters as needed.
3. (Optional) Configure a shock event in **Advanced Controls**.
4. Press **Plot** to:
   - Run the simulation
   - Generate population time plot
   - Generate profitability time plot
5. Use the **Box plot** tab to evaluate outcome variability across many runs, each with very small variations in parameters.
6. Review the **Summary** tab for aggregated metrics.

# Interpretation

- **Converts**: Individuals who adopt and may promote the meme/product.
- **Deniers**: Individuals who actively reject the meme/product but still influence others.
- **Unreached**: Individuals with no exposure so far.
- **Economic plots** show whether the campaign becomes profitable given the parameters.
- **Shock system** helps model major publicity events, algorithm changes, scandals, or policy shifts.

# See Also

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

