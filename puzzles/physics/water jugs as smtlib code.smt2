(set-option :produce-models true)

; Constants
(declare-const capacity12 Int)
(declare-const capacity6 Int)
(assert (= capacity12 12))
(assert (= capacity6 6))

; Number of steps
(define-const N Int 5) ; arbitrary max steps

; For each step i = 0..N, jug volumes
(declare-fun jug12 (Int) Int)
(declare-fun jug6 (Int) Int)

; Actions: fill12_i, fill6_i, empty12_i, empty6_i, pour12to6_i, pour6to12_i
(declare-fun fill12 (Int) Bool)
(declare-fun fill6 (Int) Bool)
(declare-fun empty12 (Int) Bool)
(declare-fun empty6 (Int) Bool)
(declare-fun pour12to6 (Int) Bool)
(declare-fun pour6to12 (Int) Bool)

; Initial state constraints
(assert (= (jug12 0) 0))
(assert (= (jug6 0) 0))

; For each step, define transition constraints (simplified for clarity)
; ... (you would loop or unroll these constraints for i=0..N-1)

; Goal at step N: one jug has exactly 6 liters
(assert (or (= (jug6 N) 6) (= (jug12 N) 6)))

(check-sat)
(get-model)
