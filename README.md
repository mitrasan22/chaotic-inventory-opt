# 🌀 Chaotic Inventory Optimization (FCIO)

**Fractal–Chaotic Inventory Optimization (FCIO)** is a research-grade Python library for **non-stationary inventory control**, designed to operate under **persistent, bursty, and chaotic demand** where classical inventory policies fail.

FCIO is **not a forecasting model**.  
It is a **nonlinear control algorithm** that stabilizes inventory dynamics using **fractal memory** and **chaos suppression**.

---

## 🔍 Why This Library Exists

Classical inventory policies such as:

- (s, S)
- Base-Stock

implicitly assume:
- stationary demand
- finite memory
- linear response

However, real demand (retail, pharma, FMCG, supply chains) exhibits:

- long-range dependence
- regime shifts
- clustered volatility
- chaotic sensitivity

**FCIO addresses this gap** by embedding tools from:

- fractal theory
- nonlinear dynamics
- chaos control
- robust feedback control

into inventory decision-making.

---

## 🧠 Core Idea (In One Line)

> FCIO dynamically adjusts order-up-to levels by damping chaos and amplifying demand memory, ensuring bounded, stable, and low-cost inventory trajectories under non-stationary demand.

---

## 📐 Mathematical Overview

### Inventory Dynamics

Inventory evolves as:

$$
I_{t+1} = I_t + Q_t - D_t
$$

Where:
- $I_t$ = inventory
- $Q_t$ = order quantity
- $D_t$ = realized demand

---

### Fractal Demand Memory (Hurst Exponent)

Demand often exhibits **long-range dependence**:

$$
\text{Cov}(D_t, D_{t+k}) \sim k^{2H-2}
$$

- $H > 0.5$: persistent demand (bursts cluster)
- $H < 0.5$: mean-reverting demand

FCIO **measures** this using rolling Hurst estimation.

---

### Chaos in Inventory Systems (Lyapunov Exponent)

Inventory control is a nonlinear dynamical system.

The **largest Lyapunov exponent**:

$$
\lambda =
\lim_{n \to \infty}
\frac{1}{n}
\sum_{t=1}^{n}
\log \left| \frac{\partial I_{t+1}}{\partial I_t} \right|
$$

- $\lambda < 0$: stable  
- $\lambda > 0$: chaotic (errors explode)

Classical policies **do not control** $\lambda$.  
FCIO does.

---

## 🌀 FCIO Control Law

The **dynamic order-up-to level is:

$$
S_t = S_0 \cdot \exp\!\left(-\alpha \lambda_t + \beta (H_t - 0.5)\right)
$$

Where:

- $S_0$ = baseline stock  
- $H_t$ = Hurst exponent  
- $\lambda_t$ = Lyapunov exponent  
- $\alpha$ = chaos damping gain  
- $\beta$ = fractal amplification gain  

Orders are placed using a stabilized $(s_t, S_t)$ rule.


---

## ⚙️ Hyperparameters (What They Mean)

FCIO hyperparameters are **not arbitrary** — each has a control-theoretic role.

| Parameter | Meaning | Role |
|---------|--------|-----|
| `alpha` | Chaos damping gain | Suppresses instability |
| `beta` | Fractal amplification | Responds to persistence |
| `rho` | Estimator smoothing | Noise vs responsiveness |
| `scale_min` | Min scaling | Prevents under-ordering |
| `scale_max` | Max scaling | Prevents explosion |
| `gamma` | Regime sensitivity | Nonlinear regime response |
| `k_cap` | Growth cap | Limits acceleration |
| `window` | Estimation window | Bias–variance tradeoff |

These parameters are tuned using **structured hyperparameter optimization**.

---

## 🔧 Hyperparameter Optimization

FCIO uses **Optuna-based optimization** with:

- SKU subsampling
- temporal truncation
- early pruning
- multi-objective cost functions

### Optimization Objective

$$
J(\theta)
=
\text{Total Cost}
+ \eta_1 \cdot \text{Stockouts}
+ \eta_2 \cdot \max(0, SL^* - SL)
$$

Where:

- $SL$ = service level  
- $SL^*$ = target service level
 
This ensures:

- low cost  
- high service  
- stable dynamics


---

## 🏗️ Library Architecture

```
chaotic_inventory_opt/
│
├── core/              # Inventory system dynamics and cost models
│   ├── inventory_system.py
│   └── cost.py
│
├── control/           # Inventory control policies
│   ├── classical.py   # (s,S), Base-Stock policies
│   ├── fcio.py        # Fractal–Chaotic Inventory Optimization (FCIO)
│   └── network.py     # Multi-SKU orchestration
│
├── fractal/           # Fractal demand analysis
│   ├── hurst.py       # Hurst exponent estimation
│   ├── rs_analysis.py # Rescaled range statistics
│   └── wavelets.py    # Multi-scale energy analysis
│
├── chaos/             # Chaos theory diagnostics
│   ├── lyapunov.py    # Largest Lyapunov exponent
│   ├── entropy.py     # Entropy-based complexity measures
│   └── recurrence.py # Recurrence plots and RQA metrics
│
├── regimes/           # Demand and stability regime classification
│   └── classifier.py
│
├── evaluation/        # Metrics and validation
│   ├── performance.py # Cost, service level, stockouts
│   ├── stability.py   # Variance and Lyapunov stability
│   └── robustness.py # Stress and sensitivity analysis
│
├── rl/                # (Optional) Reinforcement learning extensions
│   ├── env.py         # Gym-compatible environment
│   ├── reward.py      # Cost + stability-aware rewards
│   └── agent.py       # PPO / DQN wrappers
│
├── utils/             # Utilities and helpers
│   ├── rolling.py     # Rolling window operations
│   └── validation.py  # Input and parameter validation
```
---

## 📓 Notebooks (Reproducible Experiments)

All notebooks are **disposable**, dataset-specific, and reproducible.

### `notebooks/m5/`

| Notebook | Purpose |
|-------|--------|
| `01_load_m5.ipynb` | Load and inspect M5 demand dataset(Example dataset used)|
| `02_single_sku_analysis.ipynb` | Fractal & chaos diagnostics |
| `03_classical_vs_fcio.ipynb` | FCIO vs (s,S), Base-Stock |
| `04_multi_sku_network.ipynb` | Multi-SKU inventory control |
| `05_cross_sku_generalization.ipynb` | Test for all SKUs|

---

## 📄 Documentation

All theory and proofs live in `docs/`:

| File | Contents |
|----|---------|
| `theory.md` | Mathematical foundations |
| `proofs.md` | Stability & boundedness proofs |
| `appendix.md` | Hyperparameters |

## 📌 Key Takeaway

> FCIO treats inventory as a **dynamical system**, not a static optimization problem.

This shift enables:
- stability
- robustness
- lower long-run cost
- higher service levels

under real-world demand.

---

## 📜 License

This project is licensed under the MIT License.

---

## 🤝 Contributions

Contributions are welcome in:
- theory extensions
- coupled multi-SKU control
- faster simulators
- real-world case studies
- reinforcement learning extensions

---
## Author

Santanu Mitra

