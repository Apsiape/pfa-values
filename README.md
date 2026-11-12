# The values of rational probabilistic finite automata are the left-c.e. reals

Seth Douglas and Nidhal Mghirbi. Version 1.1.0, November 2026. DOI for all versions: [10.5281/zenodo.24142961](https://doi.org/10.5281/zenodo.24142961); version 1.1.0: [10.5281/zenodo.24151741](https://doi.org/10.5281/zenodo.24151741); version 1.0.2: [10.5281/zenodo.24147354](https://doi.org/10.5281/zenodo.24147354); version 1.0.1: [10.5281/zenodo.24143692](https://doi.org/10.5281/zenodo.24143692); version 1.0.0: [10.5281/zenodo.24142962](https://doi.org/10.5281/zenodo.24142962).

**This is a preprint. It has not been peer reviewed.**

## Abstract

Which real numbers are values of probabilistic finite automata with rational transition probabilities and rational initial distributions? We prove that they are exactly the left-c.e. reals in [0,1], the limits of computable nondecreasing rational sequences, and that two input letters and one fixed number of states suffice. The value is the supremum of acceptance probabilities over finite words. It was known that the value cannot be computed or approximated from the automaton; here a single automaton has a noncomputable value, given explicitly relative to a fixed enumeration of Turing machines. The construction checks counter-machine histories by a likelihood test in the manner of Condon and Lipton and pays a reward read from the output. It is effective given a rational interval around the target, but cannot be made effective from its approximations alone. Every prefix-free halting probability, including Chaitin's Ω, is a value. A construction of Elkouss and Pérez-García also realizes every left-c.e. real in [0,1] as a rational finite-state channel capacity. For quantum automata with algebraic data, measure-once values are algebraic, while rational quantum channels and QFAs with control language realize all left-c.e. reals in [0,1]; computability for one-way Kondacs–Watrous measure-many automata remains open.

## What the paper proves

The value of a rational probabilistic finite automaton A is V(A) = sup over finite words w of the probability that A accepts w. That every value is left-c.e. is folklore. It was also known that the map A ↦ V(A) cannot be computed or approximated (Nasu–Honda, Paz, Condon–Lipton, Madani–Hanks–Condon, Gimbert–Oualhadj), and that emptiness is undecidable for one fixed set of matrices when the initial or final vector is the input (Rote). Those results concern the map, not single values. The paper proves:

- **Theorem A (Section 5).** The values of rational probabilistic finite automata are exactly the left-c.e. reals in [0,1].
- **Theorem B (Section 7).** There is one number N such that every left-c.e. real in [0,1] is the value of a rational automaton with two input letters and at most N states. N is fixed by one universal counter program and has not been computed.
- **Theorem C (Section 6).** For a fixed effective enumeration of Turing machines, α* = 1/4 + Σ_{n∈H} 4^-(n+2), where H is the diagonal halting set, is not computable and is the value of the automaton A* built with a = 1/8, b = 1/2, B = 16.
- **Corollary D (Section 6).** The halting probability of every prefix-free machine, in particular Chaitin's Ω, is such a value.

Section 8 shows that the realization cannot be computed from a left-c.e. index alone (whether V(A) = 0 is decidable), and that it can be computed from an index together with a rational interval a < α < b.

Section 9, "Quantum automata: where the ladder breaks", places quantum finite automata on a ladder. Measure-once quantum automata with algebraic data have algebraic values, computable from the automaton (Proposition 9.1, implicit in Derksen, Jeandel and Koiran). Automata whose letters act by rational quantum channels (Proposition 9.2), and quantum automata with control language in the sense of Bertoni, Mereghetti and Palano (Corollary 9.3), have exactly the left-c.e. reals in [0,1] as values; for the latter, rational real unitaries, a basis initial state and complete basis measurements suffice. Propositions 9.1 and 9.2 are immediate from known results (Derksen–Jeandel–Koiran; the folklore simulation of probabilistic by quantum automata together with Theorem A), and no priority is claimed for them. Whether the values of one-way Kondacs–Watrous measure-many automata are computable is left open (Question 9.4). Two subclasses have computable values: automata whose continuing operators are each unitary or of rank at most one, whose values are algebraic (Proposition 9.5), and automata whose continuing operators are upper block triangular in a common decomposition with unitary or strictly contracting diagonal blocks (Proposition 9.7, using Lemma 9.6). A two-way extension is deferred to version 1.2 (proof in preparation); no two-way result is claimed in this version.

Section 10 shows that two-state automata and automata with positive entries have computable values, records the same range for reachability values of partially observable Markov decision processes, and lists open problems: three states, fixed matrices with a varying initial distribution, and probabilistic Büchi automata. With the channels of Elkouss and Pérez-García, every left-c.e. real in [0,1] is the capacity of a finite-state channel with rational transition probabilities (Corollary 10.7).

## Contents and reproduction

- `paper/main.pdf`: the manuscript.
- `paper/`: LaTeX source (`main.tex`), plain-text abstract and a strict build driver. Run `python -B build.py` there with pdflatex installed. The build disables shell escape, runs pdflatex three times and rejects warnings, unresolved references and box defects.
- `paper/quantum_checks.py`: an exact checker, in rational arithmetic, for finite instances of the control-language construction of Corollary 9.3 and the channel embedding of Proposition 9.2. Run `python quantum_checks.py` in `paper/` (Python 3.10 or later, standard library only). Its recorded output is `paper/quantum_checks.txt`: 4,812 orthonormal-column checks and 1,929 acceptance comparisons, with no failures, and two planted faults detected.
- `SHA256SUMS`: SHA-256 hashes of every shipped file except this manifest. Check with `sha256sum -c SHA256SUMS` from the repository root.

No computation is used in any proof.

## Changes in 1.1.0

Version 1.1.0 adds Section 9, "Quantum automata: where the ladder breaks", with Propositions 9.1, 9.2, 9.5 and 9.7, Corollary 9.3, Question 9.4 and Lemma 9.6, described above. The short remark on quantum automata in the former open-problems section is replaced by a pointer to it. The former Section 9, "Open problems", is now Section 10, and its statements are renumbered accordingly (Corollary 9.7 is now Corollary 10.7). The abstract is shortened and gains a sentence on quantum automata, and the introduction gains one. Five references are added (Ambainis–Yakaryılmaz, Bertoni–Mereghetti–Palano, Derksen–Jeandel–Koiran, Kondacs–Watrous, Mereghetti–Palano), and the AI note, the verification status and the credits describe the new section. The exact checker `paper/quantum_checks.py` and its output are new. Sections 2 to 8, including Theorems A–D and their proofs, are unchanged.

## Changes in 1.0.2

Version 1.0.2 corrects the version string on the title page of the PDF, which read "Version 1.0.0" in version 1.0.1. Nothing else changes.

## Changes in 1.0.1

Version 1.0.1 corrects the names of cross-references in the PDF (version 1.0.0 printed every reference to a lemma, corollary, proposition, definition, question or remark as "Theorem"), a garbled name in paper/abstract.txt, and the page count in paper/README.txt. The mathematics is unchanged.

## Citation and rights

See `CITATION.cff` for citation metadata. Paper and documentation: CC BY 4.0. Build script and checker: MIT or Apache 2.0, at your option. See `RIGHTS.md`, the license files and `NOTICE`.
