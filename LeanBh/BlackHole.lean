/-!
  # Context & Disclaimer
  The following proof formalizes purely mathematical consequences of three explicit
  modelling assumptions (A1–A3) described in the accompanying article
  `article_blackhole_inevitable_en.md`. In particular, the axiom

    `AI_optimal`

  postulates that a positive erase cost `c > 0` implies an optimal growth rate
  `r = φ` for information accumulation.  This is **not** asserted as a theorem of
  physics; it is an economic modelling assumption awaiting a more rigorous
  derivation (e.g.
  from utility maximisation under Landauer constraints).  Future work will seek
  to replace `AI_optimal` with a theorem derived from micro-economic or
  game-theoretic principles.

  All results below therefore hold conditionally on these assumptions and carry
  no claim about the physical inevitability of such behaviour.  The purpose is
  to make the logical dependency chain explicit and machine-verifiable.
-/

import Mathlib.Analysis.SpecialFunctions.Log.Basic
open Real

noncomputable section

-- Golden ratio φ
def phi : ℝ := (1 + Real.sqrt 5) / 2

-- Modelling axiom: positive erase cost implies existence of growth rate r = φ
axiom AI_optimal (c : ℝ) (hc : 0 < c) : ∃ r : ℝ, r = phi

-- For N0 > 0, Nmax > N0, and r > 1, there exists t with N0 * r^t = Nmax
lemma time_to_threshold {N0 Nmax r : ℝ}
    (hN0 : 0 < N0) (hNmax : N0 < Nmax) (hr : 1 < r) :
    ∃ t : ℝ, N0 * Real.exp (t * Real.log r) = Nmax := by
  -- Define `t` explicitly
  set t : ℝ := Real.log (Nmax / N0) / Real.log r
  have r_pos : 0 < r := lt_trans zero_lt_one hr
  have npos : 0 < Nmax / N0 :=
    div_pos (lt_trans hN0 hNmax) hN0
  have hlogr : Real.log r ≠ 0 := by
    have : 0 < Real.log r := Real.log_pos hr
    exact (ne_of_gt this)
  have h_mul : t * Real.log r = Real.log (Nmax / N0) := by
    have : t = Real.log (Nmax / N0) / Real.log r := rfl
    simpa [this, mul_comm, mul_left_comm, mul_assoc, hlogr] using
      by
        field_simp [this, hlogr]
  have h_exp : Real.exp (t * Real.log r) = Nmax / N0 := by
    simpa [h_mul, Real.exp_log npos]
  have h_eq : N0 * Real.exp (t * Real.log r) = Nmax := by
    have : N0 * Real.exp (t * Real.log r) = N0 * (Nmax / N0) := by
      simpa [h_exp]
    have hN0ne : N0 ≠ 0 := (ne_of_gt hN0)
    field_simp [hN0ne] at this
    simpa using this
  exact ⟨t, h_eq⟩
