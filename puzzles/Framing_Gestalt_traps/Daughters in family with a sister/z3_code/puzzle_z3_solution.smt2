; =========================================================================
; Open-World Biological Daughter Puzzle Encoding
; Format: SMT-LIB v2 
; Run via: z3 -smt2 puzzle_z3_solution.smt2
; =========================================================================

(declare-sort Person)

; 1. Global Predicates
(declare-fun Female (Person) Bool)
(declare-fun ParentOf (Person Person) Bool)
(declare-fun Daughter (Person Person) Bool)
(declare-fun IsDaughter (Person) Bool)

; Core Axiom: x is a daughter of y IF AND ONLY IF x is female and y is x's parent.
(assert (forall ((x Person) (y Person)) 
    (= (Daughter x y) (and (Female x) (ParentOf y x)))
))

; Offspring Evaluation Axiom: A person matches the 'IsDaughter' predicate if a parent exists.
(assert (forall ((x Person)) 
    (= (IsDaughter x) (exists ((y Person)) (Daughter x y)))
))

; =========================================================================
; 2. Local Puzzle Structure (No Universe Closure)
; =========================================================================
(declare-const p_father Person)
(declare-const p_mother Person)
(declare-const c1 Person)
(declare-const c2 Person)

; Parents are distinct, father is male, mother is female
(assert (not (= p_father p_mother)))
(assert (not (Female p_father)))
(assert (Female p_mother))

; Children are distinct and share both local parents
(assert (not (= c1 c2)))
(assert (ParentOf p_father c1))
(assert (ParentOf p_mother c1))
(assert (ParentOf p_father c2))
(assert (ParentOf p_mother c2))

; Puzzle Text: "One of the two children is a girl" -> At least one child is female
(assert (or (Female c1) (Female c2)))

; =========================================================================
; 3. Open-World Assumption (Mother has biological lineage)
; =========================================================================
; Every female person has at least one parent (open-world biological principle)
(assert (forall ((x Person))
    (=> (Female x) (exists ((y Person)) (ParentOf y x)))
))

; =========================================================================
; 4. Cardinality Matrix (Summing the local family set)
; =========================================================================
(declare-const total_daughters Int)

(assert (= total_daughters (+
    (ite (IsDaughter p_mother) 1 0)
    (ite (IsDaughter p_father) 1 0)
    (ite (IsDaughter c1) 1 0)
    (ite (IsDaughter c2) 1 0)
)))

; =========================================================================
; 5. Proving the Solution Set {2, 3}
; =========================================================================

(echo "--- Testing if exactly 1 daughter is possible ---")
(push 1)
(assert (= total_daughters 1))
(check-sat)
(pop 1)

(echo "--- Testing if exactly 2 daughters is possible ---")
(push 1)
(assert (= total_daughters 2))
(check-sat)
(pop 1)

(echo "--- Testing if exactly 3 daughters is possible ---")
(push 1)
(assert (= total_daughters 3))
(check-sat)
(pop 1)

(echo "--- Testing if exactly 4 daughters is possible ---")
(push 1)
(assert (= total_daughters 4))
(check-sat)
(pop 1)

