# Theoretical Foundation

This document explains the theoretical concepts underlying ComplexPy's emergence and complexity measures. For implementation details, see [architecture.md](architecture.md). For practical usage, see [getting-started.md](getting-started.md).

## Table of Contents
- [What is Emergence?](#what-is-emergence)
- [What is Complexity?](#what-is-complexity)
- [Information Theory Primer](#information-theory-primer)
- [Integrated Information Decomposition (PhiID)](#integrated-information-decomposition-phiid)
- [Whole-Parts Emergence](#whole-parts-emergence)
- [Shannon-Based Measures](#shannon-based-measures)
- [Multivariate Autoregressive Models](#multivariate-autoregressive-models)
- [When to Use Which Measure](#when-to-use-which-measure)
- [References](#references)

---

## What is Emergence?

**Emergence** refers to properties that appear in a collection of elements but not in the individual elements themselves.

### Examples from Nature

**Flocking behavior** (starlings):
- Individual birds follow simple rules (alignment, cohesion, separation)
- The collective creates complex, beautiful patterns
- The moving "shape" of the flock is emergent - no single bird contains or controls it

**Consciousness** (neurons):
- Individual neurons fire according to biochemical rules
- Subjective experience emerges from billions of neurons acting together
- No single neuron is "conscious" - consciousness is emergent

**Other examples**:
- Waves in crowds (the "Mexican wave" at stadiums)
- Traffic jams (emerging from individual driving behaviors)
- Ant colonies (collective intelligence from simple individual rules)
- Markets (prices emerging from individual trades)

### Defining Characteristics

Emergence involves:
1. **Parts**: Individual elements or components (birds, neurons, etc.)
2. **Whole**: The collective system (flock, brain, etc.)
3. **Emergent property**: Something at the whole level not present at parts level
4. **Non-reducibility**: The whole's behavior can't be fully explained by parts in isolation

### The Challenge

How do we **measure** emergence? How much emergence is present? When is emergence "strong" vs "weak"?

This is what ComplexPy addresses using information theory.

---

## What is Complexity?

**Complexity** captures the coexistence of two seemingly contradictory properties:

1. **Segregation**: Parts act independently, have specialized functions
2. **Integration**: Parts form a coherent whole, work together

### The Brain as a Complex System

**Segregation**:
- Visual cortex processes vision
- Motor cortex controls movement
- Language areas handle speech
- These regions have specialized functions (differentiation)

**Integration**:
- All regions communicate and coordinate
- Vision guides movement
- Language describes what we see
- Unified conscious experience

**Complexity**: The brain balances specialization with coordination.

### Complexity vs Simplicity vs Disorder

```
Low Complexity          High Complexity         Low Complexity
(too ordered)           (balanced)              (too disordered)
     ↓                       ↓                        ↓
All parts identical ← Parts specialized  → All parts random
No integration       but integrated        No coordination
```

**Examples**:
- **Simple**: A crystal (all atoms in regular pattern, no functional differentiation)
- **Complex**: An organism (specialized organs that work together)
- **Disordered**: A gas (random motion, no coordination)

### Measuring Complexity

Complexity measures quantify the balance between segregation and integration:
- Too much integration → no specialization → low complexity
- Too much segregation → no coordination → low complexity
- Optimal balance → high complexity

---

## Information Theory Primer

ComplexPy uses **information theory** to quantify emergence and complexity. Key concepts:

### Entropy

**Shannon Entropy** H(X) measures uncertainty or "surprise":

```
H(X) = -Σ p(x) log₂ p(x)
```

- High entropy: Variable is unpredictable (coin flip: H = 1 bit)
- Low entropy: Variable is predictable (loaded coin: H < 1 bit)
- Units: **bits** (binary digits of information)

**Intuition**: How many yes/no questions to determine the value?

### Mutual Information

**Mutual Information** I(X;Y) measures shared information between variables:

```
I(X;Y) = H(X) + H(Y) - H(X,Y)
       = H(X) - H(X|Y)
```

- I(X;Y) = 0: X and Y are independent (knowing Y tells nothing about X)
- I(X;Y) = H(X): X and Y are perfectly correlated (knowing Y fully determines X)
- Units: **bits**

**Intuition**: How much does knowing Y reduce uncertainty about X?

### Time-Delayed Mutual Information

For time-series, we often use **time-delayed MI**:

```
I(X_t; Y_{t+τ})
```

Measures how much information X at time t provides about Y at time t+τ.

**Interpretation**:
- **Prediction**: How well does past X predict future Y?
- **Causation**: Does X have causal influence on Y? (with caveats)

### Joint Mutual Information

For multiple sources and targets:

```
I(X₁,X₂; Y₁,Y₂)
```

Measures information that sources (X₁,X₂) jointly provide about targets (Y₁,Y₂).

**Key question**: How is this information decomposed?
- How much is unique to X₁?
- How much is unique to X₂?
- How much is redundant (both X₁ and X₂ provide it)?
- How much is synergistic (requires both X₁ and X₂ together)?

This is what **Integrated Information Decomposition** answers.

---

## Integrated Information Decomposition (PhiID)

**PhiID** decomposes mutual information into **16 atoms** representing different types of information.

### The Setup

Consider:
- **Two sources**: X₁ₜ, X₂ₜ (e.g., two neurons at time t)
- **Two targets**: Y₁ₜ₊τ, Y₂ₜ₊τ (e.g., same neurons at time t+τ)

We want to decompose: I(X₁,X₂; Y₁,Y₂)

### Four Types of Source Information

1. **Redundant (r)**: Both X₁ and X₂ provide the same information
   - Example: Both neurons firing together always predict target

2. **Unique to X₁ (x)**: Only X₁ provides this information
   - Example: X₁'s pattern predicts target, X₂'s pattern doesn't

3. **Unique to X₂ (y)**: Only X₂ provides this information
   - Example: X₂'s pattern predicts target, X₁'s pattern doesn't

4. **Synergistic (s)**: X₁ and X₂ together provide information neither has alone
   - Example: XOR pattern - need both to predict target

### Four Types of Target Information

1. **Redundant (r)**: Both Y₁ and Y₂ receive the same information
   - Example: Both targets respond identically

2. **Unique to Y₁ (x)**: Information goes only to Y₁
   - Example: Source influences Y₁ but not Y₂

3. **Unique to Y₂ (y)**: Information goes only to Y₂
   - Example: Source influences Y₂ but not Y₁

4. **Synergistic (s)**: Information goes to Y₁ and Y₂ jointly
   - Example: Source influences their relationship, not individually

### The 16 PhiID Atoms

Combining source types (4) × target types (4) = **16 atoms**:

| Atom | Source Information | Target Information | Interpretation |
|------|-------------------|-------------------|----------------|
| **rtr** | Redundant | Redundant | Both sources → both targets (shared info) |
| **rtx** | Redundant | Unique to Y₁ | Both sources → only Y₁ |
| **rty** | Redundant | Unique to Y₂ | Both sources → only Y₂ |
| **rts** | Redundant | Synergistic | Both sources → Y₁+Y₂ relationship |
| **xtr** | Unique to X₁ | Redundant | Only X₁ → both targets |
| **xtx** | Unique to X₁ | Unique to Y₁ | Only X₁ → only Y₁ |
| **xty** | Unique to X₁ | Unique to Y₂ | Only X₁ → only Y₂ |
| **xts** | Unique to X₁ | Synergistic | Only X₁ → Y₁+Y₂ relationship |
| **ytr** | Unique to X₂ | Redundant | Only X₂ → both targets |
| **ytx** | Unique to X₂ | Unique to Y₁ | Only X₂ → only Y₁ |
| **yty** | Unique to X₂ | Unique to Y₂ | Only X₂ → only Y₂ |
| **yts** | Unique to X₂ | Synergistic | Only X₂ → Y₁+Y₂ relationship |
| **str** | Synergistic | Redundant | X₁+X₂ together → both targets |
| **stx** | Synergistic | Unique to Y₁ | X₁+X₂ together → only Y₁ |
| **sty** | Synergistic | Unique to Y₂ | X₁+X₂ together → only Y₂ |
| **sts** | Synergistic | Synergistic | X₁+X₂ together → Y₁+Y₂ relationship |

### Redundancy Functions

Computing PhiID requires defining **redundancy**: red(X₁,X₂;Y).

Two options in ComplexPy:

**1. Minimum Mutual Information (MMI)**:
```
red(X₁,X₂;Y) = min{I(X₁;Y), I(X₂;Y)}
```
- Conservative (lower bound on redundancy)
- Always non-negative
- Interpretation: Redundant info can't exceed what either source alone provides

**2. Common Change in Surprisal (CCS)**:
```
red(X₁,X₂;Y) = I(X₁;Y) + I(X₂;Y) - I(X₁,X₂;Y)
```
- Based on co-information
- Can be negative
- Interpretation: Redundancy is what's "double-counted" if we sum individual contributions

**Which to use?**
- MMI is more conservative and standard
- CCS can reveal negative redundancy (unique info creating apparent redundancy)
- Try both and compare!

---

## Whole-Parts Emergence

**Whole-Parts Emergence (WPE)** applies PhiID to measure emergence between micro and macro scales.

### Setup

- **Micro level**: Individual components X₁, X₂, ..., Xₙ (e.g., neurons)
- **Macro level**: Aggregate variable V = f(X₁, X₂, ..., Xₙ) (e.g., population activity)
- **Time evolution**: How do micro/macro at time t relate to macro at time t+τ?

### Three Emergence Measures

**1. Whole-Parts Emergence (WPE / Ψ)**

**Question**: How much information does the macro level have about its own future that the micro parts individually lack?

**PhiID-based**:
```
WPE = synergistic source information about macro targets
```
Sum of relevant PhiID atoms representing joint micro information about macro.

**Interpretation**:
- WPE > 0: Macro has emergent predictive capacity
- The whole has information about its future not present in sum of parts
- Example: Flock's shape predicts its future better than individual bird trajectories

**2. Downward Causation (DC / Δ)**

**Question**: How much does the macro level causally influence the micro parts beyond micro self-prediction?

**PhiID-based**:
```
DC = macro information about micro futures - micro self-information
```

**Interpretation**:
- DC > 0: Macro constrains or influences micro dynamics
- "Top-down" causation from whole to parts
- Example: Flock shape constrains individual bird movements

**3. Causal Decoupling (CD / Γ)**

**Question**: How much are macro dynamics independent of micro details?

**PhiID-based**:
```
CD = macro self-information - macro dependence on micro
```

**Interpretation**:
- CD > 0: Macro has autonomous dynamics
- Macro evolves partly independently of micro details
- Example: Flock moves coherently regardless of which specific birds are in it

### Relationship Between Measures

```
         WPE
          ↓
    (emergent capacity)
          ↓
    ┌─────┴─────┐
    ↓           ↓
   DC          CD
(downward    (macro
causation)   autonomy)
```

- High WPE suggests emergence is present
- DC and CD reveal different aspects of how emergence manifests
- All three can be computed from PhiID decomposition

---

## Shannon-Based Measures

**Shannon WPE** provides practical approximations without full PhiID decomposition.

These use standard mutual information (no decomposition into atoms).

### 1. Shannon Ψ (Psi) - Whole-Parts Emergence

**Formula**:
```
Ψ = MI(Vₜ, Vₜ₊τ) - Σᵢ MI(Xᵢₜ, Vₜ₊τ)
```

Where:
- Vₜ = macro at time t
- Vₜ₊τ = macro at time t+τ
- Xᵢₜ = micro component i at time t

**Interpretation**:
- First term: How much does past macro predict future macro?
- Second term: How much do past micros (individually) predict future macro?
- Ψ > 0: Macro self-prediction exceeds sum of micro-to-macro predictions
- **Emergence**: Macro has predictive info not in individual micro parts

**Example**:
- Flock position at t predicts flock position at t+τ
- Individual bird positions at t each predict flock position less well
- Difference = emergent predictive capacity

### 2. Shannon Δ (Delta) - Downward Causation

**Formula**:
```
Δ = Σᵢ MI(Vₜ, Xᵢₜ₊τ) - MI(Vₜ, Xₜ₊τ)
```

Where:
- Xₜ₊τ = all micro components at time t+τ

**Interpretation**:
- First term: How much does past macro predict each future micro (summed)?
- Second term: How much does past macro predict future micros jointly?
- Δ > 0: Macro explains micro futures better individually than jointly
- **Downward causation**: Macro constrains parts beyond parts' self-dynamics

### 3. Shannon Γ (Gamma) - Causal Decoupling

**Formula**:
```
Γ = MI(Vₜ, Vₜ₊τ) - MI(Vₜ, Xₜ₊τ)
```

**Interpretation**:
- First term: Macro self-prediction
- Second term: How much past macro determines future micros
- Γ > 0: Macro dynamics contain info beyond what determines micros
- **Causal decoupling**: Macro has autonomous dynamics

### Shannon vs PhiID Measures

| Aspect | Shannon WPE | PhiID WPE |
|--------|-------------|-----------|
| **Computation** | Fast, simple MI calculations | Slower, full decomposition |
| **Information** | Approximation | Complete decomposition |
| **Interpretation** | Practical, intuitive | Detailed, precise |
| **Use case** | Exploratory analysis, large datasets | Detailed analysis, theory testing |

**Recommendation**:
- Start with Shannon for quick insights
- Use PhiID for detailed understanding
- Compare both to validate findings

---

## Multivariate Autoregressive Models

**MVAR models** are used in ComplexPy to generate synthetic time-series data.

### The MVAR(1) Model

**Equation**:
```
Xₜ = A × Xₜ₋τ + Eₜ
```

Where:
- Xₜ = state vector at time t (e.g., [X₁ₜ, X₂ₜ]ᵀ)
- A = coupling matrix (determines interactions)
- τ = time lag
- Eₜ = noise vector (Gaussian)

### 2-Node Example

```
X₁ₜ = a₁₁·X₁ₜ₋₁ + a₁₂·X₂ₜ₋₁ + ε₁ₜ
X₂ₜ = a₂₁·X₁ₜ₋₁ + a₂₂·X₂ₜ₋₁ + ε₂ₜ
```

**Coupling matrix**:
```
A = [a₁₁  a₁₂]
    [a₂₁  a₂₂]
```

**Parameters**:
- **Diagonal elements** (a₁₁, a₂₂): Self-coupling (autoregressive terms)
- **Off-diagonal elements** (a₁₂, a₂₁): Cross-coupling (interactions between nodes)
- **coupling parameter**: Controls strength of a₁₂ and a₂₁
- **noise_corr parameter**: Correlation between ε₁ and ε₂

### Macro Variable

**Aggregation**:
```
Vₜ = X₁ₜ + X₂ₜ
```

Simple summation creates the macro-level variable.

**Why this matters**:
- Emergence measures compare micro (X₁, X₂) to macro (V)
- Different coupling and noise create different emergence profiles
- Parameter sweeps explore emergence across different network configurations

### Interpreting Parameters

**Coupling strength** (0 to 1):
- 0: Independent nodes (no interaction)
- 0.5: Moderate coupling
- 1: Strong coupling (near synchronization)

**Noise correlation** (0 to 1):
- 0: Independent noise (nodes have separate noise sources)
- 0.5: Partially correlated noise
- 1: Fully correlated noise (common noise source)

**Effect on emergence**:
- Higher coupling → more integration → potentially more emergence
- Noise correlation → common cause (vs true interaction)
- Exploring parameter space reveals where emergence is strongest

---

## When to Use Which Measure

### Decision Tree

```
Do you need detailed decomposition?
├─ YES → Use PhiID measures
│         ├─ Full decomposition? → phiid_2sources_2targets()
│         └─ Just WPE/DC/CD? → phiid_wpe()
│
└─ NO  → Use Shannon measures
          └─ shannon_wpe()

Which redundancy function? (for PhiID)
├─ Standard/conservative → red_func='mmi'
└─ Explore negative redundancy → red_func='ccs'

What time lag?
├─ Natural system timescale → use domain knowledge
├─ Exploratory → sweep multiple lags
└─ No idea → start with τ=1
```

### Use Cases

**Exploratory Analysis**:
- Use `shannon_wpe()` for speed
- Sweep parameters broadly
- Identify interesting regimes

**Detailed Investigation**:
- Use `phiid_wpe()` for precision
- Focus on specific parameter regimes
- Understand information structure

**Theory Testing**:
- Use `phiid_2sources_2targets()` for full decomposition
- Examine all 16 atoms
- Test hypotheses about information flow

**Large Datasets**:
- Shannon measures scale better
- Consider downsampling for PhiID
- Parallelize parameter sweeps

### Interpreting Results

**WPE values**:
- WPE ≈ 0: Little to no emergence
- WPE > 0: Emergence present, magnitude matters
- WPE < 0: (Shannon) Micro parts predict macro better than macro predicts itself (unusual)

**DC values**:
- DC > 0: Downward causation present (macro → micro)
- DC ≈ 0: No downward causation
- Magnitude indicates strength

**CD values**:
- CD > 0: Macro has autonomous dynamics
- CD ≈ 0: Macro fully determined by micro
- High CD: Macro "decouples" from micro details

**Comparing measures**:
- Shannon and PhiID should agree qualitatively
- Quantitative differences are normal
- Large discrepancies → investigate further

---

## References

### Foundational Papers

**Integrated Information Decomposition**:
- Rosas, F. E., et al. (2020). [Reconciling Emergences: An information-theoretic approach to identify causal emergence in multivariate data](https://arxiv.org/abs/2004.08220). *arXiv preprint*.

**Whole-Parts Emergence**:
- Mediano, P. A. M., et al. (2021). [Towards an extended taxonomy of information dynamics via Integrated Information Decomposition](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008289). *PLOS Computational Biology*.

**Redundancy Measures**:
- Finn, C., & Lizier, J. T. (2017). [Measuring multivariate redundant information with pointwise common change in surprisal](https://www.mdpi.com/1099-4300/19/7/318). *Entropy, 19*(7), 318.

**Dynamical Independence** (related measure):
- Rosas, F. E., et al. (2020). [Dynamical independence: discovering emergent macroscopic processes in complex dynamical systems](https://arxiv.org/pdf/2106.06511.pdf). *arXiv preprint*.

### Information Theory Background

**General Introduction**:
- Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.

**Partial Information Decomposition**:
- Williams, P. L., & Beer, R. D. (2010). [Nonnegative decomposition of multivariate information](https://arxiv.org/abs/1004.2515). *arXiv preprint*.

**Transfer Entropy and Time-Series**:
- Lizier, J. T. (2014). [JIDT: An information-theoretic toolkit for studying the dynamics of complex systems](https://www.frontiersin.org/articles/10.3389/frai.2021.689301/full). *Frontiers in Robotics and AI*.

### Complexity and Emergence

**Emergence Overview**:
- Bedau, M. A. (1997). Weak emergence. *Philosophical Perspectives, 11*, 375-399.

**Complexity Measures**:
- Wiesner, K. (2020). [What is complexity?](https://arxiv.org/pdf/1909.13243.pdf). *arXiv preprint*.

**Applications to Neuroscience**:
- Tononi, G., et al. (2016). Integrated information theory: from consciousness to its physical substrate. *Nature Reviews Neuroscience, 17*(7), 450-461.

---

For implementation details, see [architecture.md](architecture.md). For hands-on usage, see [getting-started.md](getting-started.md). To contribute to the theory, see [CONTRIBUTING.md](../CONTRIBUTING.md).
