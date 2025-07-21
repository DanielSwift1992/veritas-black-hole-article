import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

open Real

noncomputable section

/-- Golden ratio φ -/ 
def phi : ℝ := (1 + Real.sqrt 5) / 2

/-- Helper: monotonicity argument shows characteristic root is ≥ φ for any a,b ≥ 1. -/
lemma phi_le_charRoot (a b : ℕ) (ha : 1 ≤ a) (hb : 1 ≤ b) :
    phi ≤ (a + Real.sqrt (a^2 + 4*b)) / 2 := by
  -- Cast naturals to reals
  have haR : (1 : ℝ) ≤ a := by exact_mod_cast ha
  have hbR : (1 : ℝ) ≤ b := by exact_mod_cast hb
  -- Lower bound on the square-root term
  have h_sqrt : (Real.sqrt ((a:ℝ)^2 + 4*(b:ℝ))) ≥ Real.sqrt 5 := by
    apply Real.sqrt_le_sqrt;
    have : (a:ℝ)^2 + 4*(b:ℝ) ≥ (1:ℝ)^2 + 4*1 := by
      have h1 : (a:ℝ)^2 ≥ (1:ℝ)^2 := by
        have : (1:ℝ) ≤ a := haR
        have hsq := pow_le_pow_of_le_left (by linarith) this (2:ℕ)
        simpa using hsq
      have h2 : (b:ℝ) ≥ 1 := hbR
      linarith
    simpa using this
  -- Now compare full expression
  have h_num : (a:ℝ) + Real.sqrt ((a:ℝ)^2 + 4*(b:ℝ)) ≥ 1 + Real.sqrt 5 := by
    have : (a:ℝ) ≥ 1 := haR
    linarith [this, h_sqrt]
  -- Divide by positive 2 preserves inequality
  have h_div : ((a:ℝ) + Real.sqrt ((a:ℝ)^2 + 4*(b:ℝ))) / 2 ≥ (1 + Real.sqrt 5) / 2 :=
    (div_le_div_of_le (by norm_num) h_num)
  simpa [phi] using h_div

/-- Minimality statement: equality iff a = b = 1. -/
lemma phi_eq_iff (a b : ℕ) (ha : 1 ≤ a) (hb : 1 ≤ b) :
    (a + Real.sqrt (a^2 + 4*b)) / 2 = phi ↔ (a = 1 ∧ b = 1) := by
  -- → direction: if equal, must have a=1 and b=1.
  constructor
  · intro h
    have h1 : (a:ℝ) = 1 := by
      -- from equality, derive bounds
      have H := congrArg (fun x : ℝ => 2*x) h
      have : (a:ℝ) + Real.sqrt ((a:ℝ)^2 + 4*(b:ℝ)) = 1 + Real.sqrt 5 := by
        simpa [phi] using H
      -- Compare sides: both components must match minimal values.
      have : (a:ℝ) ≤ 1 := by
        have phi_le := phi_le_charRoot a b ha hb
        have := congrArg (fun x:ℝ => 2*x) phi_le
        linarith [phi, h, haR]
      have : (a:ℝ) = 1 :=
        le_antisymm this haR
      exact (by exact_mod_cast this)
    have h2 : (b = 1) := by
      -- Using a=1, equality forces sqrt term equal
      have a1 : a = 1 := h1
      have : ((1:ℝ) + Real.sqrt ((1:ℝ)^2 + 4*(b:ℝ))) / 2 = phi := by simpa [a1] using h
      have : Real.sqrt (1 + 4*(b:ℝ)) = Real.sqrt 5 := by
        have := congrArg (fun x : ℝ => 2*x -1) this
        simpa [phi] using this
      have : 1 + 4*(b:ℝ) = 5 := by
        apply (Real.sqrt_eq_iff (by linarith)).1
        · linarith
        · linarith
        · simpa using this
      have : (b:ℝ) = 1 := by linarith
      exact (by exact_mod_cast this)
    exact ⟨h1, h2⟩
  · rintro ⟨rfl, rfl⟩
    simp [phi]

end 