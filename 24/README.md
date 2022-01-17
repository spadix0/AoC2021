# 2021-12-24: Arithmetic Logic Unit

The code for `MONAD` repeats the same instruction template for each digit of
the model number to accumulate a new intermediate result (call it `Zn`) from
the previous result (`Zp`) using the value of the current digit (`Xi ∈ [1,9]`).
The script for this solution just processes the template using a predetermined
analysis that applies for all the code samples I had access to.


### Calculation

The repeating digit template is parameterized and this solution is only
concerned with the variation in parameters across the digits.  Two of the
template parameters appear to be constant (although this constraint will be
relaxed later):

* `M ≡ N + 1`, complementary modulus and multiplier

and three parameters are variable, call them:

* `Di ∈ {1, M}`, divisor
* `Ai`, digit comparison value
* `Bi`, digit increment (appears always satisfy `0 ≤ Bi < M - 9`)

If we let `Ci` be the result of the comparison:

* `Ci ≡ (Xi ≠ Zp%M + Ai)`

then the calculation result for each digit can be factored as:

* `Zn ≡ Zp/Di + (Zp/Di∙N + Bi + Xi)∙Ci`


### Analysis

The two choices for divisor (`Di`) differentiate digits into distinct cases:

1. `Di = 1`, call this one "shift left" (`SHL`)
2. `Di = M`, a *conditional* "shift right" (`SHR`)

Each `SHL` is paired with a subsequent `SHR`, which pairs are possibly nested.
For `SHR`, the condition (`Ci`) determines whether the right shift is
performed.  For `SHL`, parameter `Ai` appears to be configured such that the
condition always succeeds (`Ai > 9 ⇒ Ci = 1`) and the left shift is always
performed.  This simplifies the two cases to:

1. `SHL: Zn ≡ Zp∙M + Bi + Xi`
2. `SHR: Zn ≡ Zp/M + …∙(Xi ≠ Zp%M + Ai)`

You can think of each `SHL` as building a base `M` number by appending a new
digit and `SHR` as testing and removing or replacing the least significant
digit.  In order for the final result to be 0, the condition for each `SHR`
needs to fail (`Ci = 0`) so it removes the digit added by the paired `SHL`;
otherwise they accumulate a non-0 result.  This means the paired digits
(`l`eft and `r`ight) must satisfy:

* `Xr = Xl + (Ar + Bl)`

Using those 7 constraints, the maximum (minimum) combination of digits just
selects the largest (smallest) value for each `Xl`, which then directly
determines the paired `Xr`.  Note that `M` (and the corresponding `N` and `D`)
need not be fixed throughout, so long as they are consistent for each pair of
digits.
