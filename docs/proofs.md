# Mathematical Proofs and Stability Guarantees

---

## Theorem 1 — Boundedness Under Scale Constraints

Assume bounded demand and bounded scaling:

$$
s_{\min} \le \frac{S_t}{S_0} \le s_{\max}
$$

Then the FCIO inventory process is mean-square bounded.

---

### Proof Sketch

Using Lyapunov candidate $V(I_t) = I_t^2$:

$$
\mathbb{E}[V(I_{t+1}) - V(I_t)]
=
\mathbb{E}[(Q_t - D_t)^2 + 2I_t(Q_t - D_t)]
$$

Since $Q_t \le S_t - I_t \le S_0 s_{\max}$, all higher-order terms are bounded.

Thus:

$$
\mathbb{E}[V(I_{t+1}) - V(I_t)] \le -c I_t^2 + K
$$

for constants $c, K > 0$.

∎

---

## Theorem 2 — Chaos Suppression via $\alpha$

Let $\lambda_t$ be the uncontrolled Lyapunov exponent.

Then FCIO induces an effective exponent:

$$
\lambda_{\text{eff}} = (1 - \alpha)\lambda_t + \epsilon
$$

where $\epsilon$ is bounded estimator error.

For $\alpha > 1$, $\lambda_{\text{eff}} < 0$, ensuring exponential stability.

∎

---

## Proposition — Effect of $\rho$ on Stability

Smoothing parameter $\rho$ reduces estimator variance:

$$
\text{Var}(\tilde{\lambda}_t)
=
(1 - \rho)^2
\sum_{k=0}^{\infty}
\rho^{2k}
\text{Var}(\lambda_{t-k})
$$

Higher $\rho$ implies lower variance but slower adaptation.

∎

---

## Proposition — Bounded Acceleration via `k_cap`

Limiting inter-temporal growth ensures:

$$
|S_t - S_{t-1}| \le k_{\text{cap}} S_{t-1}
$$

This prevents second-order divergence even under persistent demand.

∎

---
