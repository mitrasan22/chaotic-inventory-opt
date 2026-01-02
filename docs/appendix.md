# Appendix: Hyperparameter Interpretation and Practical Ranges

---

## A. Summary of FCIO Hyperparameters

| Parameter | Meaning | Typical Range |
|---------|-------|---------------|
| alpha | Chaos damping gain | 0.5 – 2.0 |
| beta | Fractal amplification | 0.3 – 1.5 |
| rho | Estimator smoothing | 0.5 – 0.9 |
| scale_min | Minimum scaling | 0.5 – 0.8 |
| scale_max | Maximum scaling | 1.2 – 1.6 |
| gamma | Regime sensitivity | 1.0 – 2.0 |
| k_cap | Inventory acceleration cap | 0.3 – 1.0 |
| window | Estimation horizon | 30 – 100 |

---

## B. Why These Are Not Arbitrary

Each hyperparameter corresponds to a **control-theoretic role**:

- gains (`alpha`, `beta`) regulate feedback strength
- bounds (`scale_min`, `scale_max`, `k_cap`) ensure stability
- smoothing (`rho`, `window`) controls noise–bias tradeoff
- regime gain (`gamma`) enables nonlinear switching

Thus hyperparameter tuning is **structured optimization**, not brute force.

---

## C. Relation to Classical Control

FCIO parameters correspond to:

- proportional gain (α, β)
- low-pass filtering (ρ)
- saturation limits (scale bounds)
- rate limiters (k_cap)

This places FCIO within the framework of **robust nonlinear control**.

---
