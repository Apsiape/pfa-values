# The values of rational probabilistic finite automata are the left-c.e. reals

Seth Douglas and Nidhal Mghirbi. Version 1.0.2, November 2026. DOI for all versions: [10.5281/zenodo.24142961](https://doi.org/10.5281/zenodo.24142961); version 1.0.1: [10.5281/zenodo.24143692](https://doi.org/10.5281/zenodo.24143692); version 1.0.0: [10.5281/zenodo.24142962](https://doi.org/10.5281/zenodo.24142962).

**This is a preprint. It has not been peer reviewed.**

## Abstract

Which real numbers are values of probabilistic finite automata with rational transition probabilities and a rational initial distribution? We show that they are exactly the left-c.e. reals in [0,1], the limits of computable nondecreasing sequences of rational numbers. Here the value of an automaton is the supremum, over all finite input words, of the probability that the word is accepted. Every value is left-c.e. because the words can be enumerated; we prove that every left-c.e. real in [0,1] occurs, and that two input letters and one fixed number of states suffice for all of them.

In particular a single automaton can have a noncomputable value. It was known that no algorithm computes, or even approximates, the value from the automaton; that concerns the map from automata to values, not single values. We give an automaton, specified explicitly relative to a fixed enumeration of Turing machines, whose value is 1/4 plus the sum of 4^-(n+2) over the programs n that halt on input n. The automaton checks claimed runs of a counter machine by a likelihood test in the manner of Condon and Lipton, and pays out a reward read from each run's output. The construction uses a rational interval around the target; from the target's approximations alone no algorithm can produce the automaton, since an automaton of value 0 can be recognized. The halting probability of every prefix-free machine, Chaitin's Ω among them, is the value of a probabilistic finite automaton with two input letters. With a construction of Elkouss and Pérez-García, every left-c.e. real in [0,1] is also the capacity of a finite-state channel with rational transition probabilities; in particular one such channel has a noncomputable capacity.

## What the paper proves

The value of a rational probabilistic finite automaton A is V(A) = sup over finite words w of the probability that A accepts w. That every value is left-c.e. is folklore. It was also known that the map A ↦ V(A) cannot be computed or approximated (Nasu–Honda, Paz, Condon–Lipton, Madani–Hanks–Condon, Gimbert–Oualhadj), and that emptiness is undecidable for one fixed set of matrices when the initial or final vector is the input (Rote). Those results concern the map, not single values. The paper proves:

- **Theorem A (Section 5).** The values of rational probabilistic finite automata are exactly the left-c.e. reals in [0,1].
- **Theorem B (Section 7).** There is one number N such that every left-c.e. real in [0,1] is the value of a rational automaton with two input letters and at most N states. N is fixed by one universal counter program and has not been computed.
- **Theorem C (Section 6).** For a fixed effective enumeration of Turing machines, α* = 1/4 + Σ_{n∈H} 4^-(n+2), where H is the diagonal halting set, is not computable and is the value of the automaton A* built with a = 1/8, b = 1/2, B = 16.
- **Corollary D (Section 6).** The halting probability of every prefix-free machine, in particular Chaitin's Ω, is such a value.

Section 8 shows that the realization cannot be computed from a left-c.e. index alone (whether V(A) = 0 is decidable), and that it can be computed from an index together with a rational interval a < α < b. Section 9 shows that two-state automata and automata with positive entries have computable values, records the same range for reachability values of partially observable Markov decision processes, and lists open problems: three states, fixed matrices with a varying initial distribution, and probabilistic Büchi automata. With the channels of Elkouss and Pérez-García, every left-c.e. real in [0,1] is the capacity of a finite-state channel with rational transition probabilities (Corollary 9.7).

## Contents and reproduction

- `paper/main.pdf`: the manuscript.
- `paper/`: LaTeX source (`main.tex`), plain-text abstract and a strict build driver. Run `python -B build.py` there with pdflatex installed. The build disables shell escape, runs pdflatex three times and rejects warnings, unresolved references and box defects.
- `SHA256SUMS`: SHA-256 hashes of every shipped file except this manifest. Check with `sha256sum -c SHA256SUMS` from the repository root.

No computation is used in any proof.

## Changes in 1.0.2

Version 1.0.2 corrects the version string on the title page of the PDF, which read "Version 1.0.0" in version 1.0.1. Nothing else changes.

## Changes in 1.0.1

Version 1.0.1 corrects the names of cross-references in the PDF (version 1.0.0 printed every reference to a lemma, corollary, proposition, definition, question or remark as "Theorem"), a garbled name in paper/abstract.txt, and the page count in paper/README.txt. The mathematics is unchanged.

## Citation and rights

See `CITATION.cff` for citation metadata. Paper and documentation: CC BY 4.0. Build script: MIT or Apache 2.0, at your option. See `RIGHTS.md`, the license files and `NOTICE`.
