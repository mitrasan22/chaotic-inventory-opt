# Fractal–Chaotic Inventory Optimization (FCIO)
## Theoretical Foundations

---

## 1. Problem Formulation

We consider a discrete-time inventory system governed by:

$$
I_{t+1} = I_t + Q_t - D_t
$$

where $I_t$ is inventory, $Q_t$ is order quantity, and $D_t$ is realized demand.

The control objective is to minimize expected cumulative cost under non-stationary demand.

---

## 2. Cost Structure

Per-period cost:

$$
C_t = h \max(I_t, 0) + p \max(-I_t, 0) + k \mathbb{1}[Q_t > 0]
$$

where $h$ is holding cost, $p$ stockout penalty, and $k$ fixed ordering cost.

---

## 3. Classical Inventory Policies

Classical policies such as (s, S) and Base-Stock assume demand stationarity and linear response. These assumptions fail under persistent, bursty, or chaotic demand.

---

## 4. Fractal Demand Structure

### 4.1 Hurst Exponent

Demand exhibits long-range dependence when:

$$
\text{Cov}(D_t, D_{t+k}) \sim k^{2H-2}
$$

The **Hurst exponent** $H$ controls memory depth.

- $H > 0.5$: persistence  
- $H < 0.5$: anti-persistence  

---

## 5. Chaotic Sensitivity in Inventory Dynamics

Inventory recursion defines a nonlinear dynamical system.

The largest Lyapunov exponent:

$$
\lambda = \lim_{n \to \infty} \frac{1}{n} \sum_{t=1}^{n} \log \left| \frac{\partial I_{t+1}}{\partial I_t} \right|
$$

measures sensitivity to perturbations.

---

## 6. FCIO Control Law

### 6.1 Core Equation

FCIO defines a **dynamic order-up-to level**:

$$
S_t = S_0 \cdot \exp \left( -\alpha \lambda_t + \beta (H_t - 0.5) \right)
$$

This equation introduces two primary hyperparameters:

- **$\alpha$** — chaos damping gain  
- **$\beta$** — fractal memory amplification gain  

---

## 7. Extended FCIO Hyperparameters

To ensure stability, robustness, and generalization, FCIO introduces additional structural parameters.

---

### 7.1 Scale Bounds: `scale_min`, `scale_max`

The exponential response is bounded:

$$
S_t \leftarrow S_0 \cdot \min(\max(\exp(\cdot), s_{\min}), s_{\max})
$$

where:

- `scale_min = s_{\min}` prevents under-ordering collapse  
- `scale_max = s_{\max}` prevents explosive inventory growth  

These bounds enforce **input-to-state stability**.

---

### 7.2 Temporal Smoothing Parameter: `rho`

Fractal and chaos estimators are noisy. FCIO applies exponential smoothing:

$$
\tilde{H}_t = \rho \tilde{H}_{t-1} + (1 - \rho) H_t
$$

$$
\tilde{\lambda}_t = \rho \tilde{\lambda}_{t-1} + (1 - \rho) \lambda_t
$$

where:

- $\rho \in (0,1)$ controls estimator inertia  
- higher $\rho$ → slower adaptation, higher robustness  
- lower $\rho$ → faster reaction, higher variance  

---

### 7.3 Regime Sensitivity Gain: `gamma`

Regime-aware scaling modifies the control signal:

$$
S_t^{(\text{regime})} = S_t \cdot g(\text{regime}; \gamma)
$$

where $\gamma$ controls **how aggressively FCIO responds to detected instability**.

Higher $\gamma$:
- stronger suppression in chaotic regimes  
- stronger amplification in persistent regimes  

---

### 7.4 Inventory Growth Cap: `k_cap`

To prevent multi-period accumulation, FCIO enforces:

$$
S_t \le S_{t-1} (1 + k_{\text{cap}})
$$

This limits **inter-temporal inventory acceleration**, ensuring bounded second-order dynamics.

---

### 7.5 Estimation Window: `window`

All estimators operate on a rolling window of size $W$:

$$
\{D_{t-W+1}, \dots, D_t\}
$$

Tradeoff:
- small $W$: responsive but noisy  
- large $W$: stable but slow  

---

## 8. Hyperparameter Optimization Objective

Hyperparameters $\theta$ are optimized by minimizing:

$$
J(\theta)
=
\mathbb{E}
\left[
\text{Cost}
+ \eta_1 \cdot \text{Stockouts}
+ \eta_2 \cdot \max(0, \text{ServiceLevel}^* - \text{ServiceLevel})
\right]
$$

This objective balances:
- efficiency
- service quality
- stability

---

## 9. Cross-SKU Generalization

Since hyperparameters regulate **structural response**, not SKU identity:

$$
\theta^* = \arg\min_\theta \mathbb{E}_{\text{SKU}} [ J(\theta) ]
$$

They generalize across SKUs drawn from the same demand class.

---
