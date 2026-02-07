# fDE_cosmo

This repository contains modified versions of **CLASS** and **MontePython** that implement a dark-energy background parametrization directly in terms of the dark-energy density evolution,

\[
f_{\rm DE}(z)\equiv \frac{\rho_{\rm DE}(z)}{\rho_{{\rm DE},0}},
\qquad\text{so that}\qquad
\rho_{\rm DE}(a)=\rho_{{\rm DE},0}\,f_{\rm DE}(a),
\]
with \(a=1/(1+z)\).

The purpose of this project is to test this parametrization against the standard CPL \(w_0\)–\(w_a\) model, using both DESI-like mock data and real DESI data.

---

## Dark-energy parametrizations implemented

All models are defined at the **background level** via \(f_{\rm DE}(a)\).

### Expansion around today (\(a=1\))

**Linear (1st order):**
\[
f_{\rm DE}(a)=1+f_a(1-a).
\]

**Quadratic (2nd order):**
\[
f_{\rm DE}(a)=1+f_a(1-a)+f_b(1-a)^2.
\]

These forms replace the usual equation-of-state parametrization \((w_0,w_a)\) and allow the background evolution to be specified directly in terms of \(\rho_{\rm DE}(a)\).

---

## Repository structure

- `class_fDE/`  
  Modified version of **CLASS** implementing the \(f_{\rm DE}(a)\) parametrization at the background level.

- `montepython_fDE/`  
  Modified version of **MontePython** that interfaces with `class_fDE` and allows sampling of the new dark-energy parameters.

- `mock_desi_data_dir/`  
  Utilities to generate DESI-like mock data vectors and covariances for validation and forecasting.

---

## Compilation and usage

### Compile CLASS
```bash
cd class_fDE
make clean
make
