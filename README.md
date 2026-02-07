# fDE_cosmo

This repository contains modified versions of **CLASS** and **MontePython** that implement a dark-energy background parametrization directly in terms of the dark-energy density evolution

    f_DE(z) = rho_DE(z) / rho_DE,0

equivalently

    rho_DE(a) = rho_DE,0 * f_DE(a)    with    a = 1/(1+z).

The goal is to test this parametrization against the standard CPL w0–wa model, using both DESI-like mock data and real DESI data.

---

## Dark-energy parametrizations implemented (background level)

Expansion around today (a = 1):

- Linear (1st order):
  
      f_DE(a) = 1 + f_a (1 - a)

- Quadratic (2nd order):
  
      f_DE(a) = 1 + f_a (1 - a) + f_b (1 - a)^2

These forms replace specifying (w0, wa) and instead directly parameterize rho_DE(a).

---

## Repository structure

- `class_fDE/`  
  Modified **CLASS** implementing the f_DE(a) parametrization at the background level.

- `montepython_fDE/`  
  Modified **MontePython** that interfaces with `class_fDE` and allows sampling of the new DE parameters.

- `mock_desi_data_dir/`  
  Utilities to generate DESI-like mock data vectors and covariances for validation/forecasting.

---

## Compilation and usage

### Compile CLASS
```bash
cd class_fDE
make clean
make
