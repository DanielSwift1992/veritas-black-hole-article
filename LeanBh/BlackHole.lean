import Mathlib.Analysis.SpecialFunctions.Log.Basic
open Real

noncomputable section

/-- Символ золотого сечения (φ). -/
def phi : ℝ := (1 + Real.sqrt 5) / 2

/-- Аксима: рациональный бизнес + ненулевая стоимость стирания ⇒ оптимальная стратегия роста без стирания,
     соответствующая экспоненциальному коэффициенту φ (≈1.618).  -/
axiom AI_optimal (c : ℝ) (hc : 0 < c) :
  ∃ r : ℝ, r = phi

/-- Основной тезис: пусть `N0>0`, `Nmax>N0`, `r>1`. Тогда существует время `t` такое, что
    `N0 * r^t = Nmax`. (Неформально: экспоненциальный рост без стирания неизбежно достигает предела.) -/
lemma time_to_threshold {N0 Nmax r : ℝ}
    (hN0 : 0 < N0) (hNmax : N0 < Nmax) (hr : 1 < r) :
    ∃ t : ℝ, N0 * Real.exp (t * Real.log r) = Nmax := by
  -- Обозначим время явно
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
