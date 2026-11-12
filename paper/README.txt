The values of rational probabilistic finite automata are the left-c.e. reals
Seth Douglas and Nidhal Mghirbi
Version 1.1.0, November 2026

Build: python -B build.py [--build-dir NEW_OR_EMPTY_DIRECTORY]
Requires Python 3 and pdflatex. The bibliography is inline. The build runs pdflatex three times without shell escape and rejects
warnings, unresolved references and overfull or underfull boxes. main.pdf is the compiled preprint (28 pages). abstract.txt is the
abstract as plain text, after a version header.

This version adds Section 9, "Quantum automata: where the ladder breaks": measure-once algebraicity, the rational CPTP range,
rational-unitary quantum automata with control language, the open one-way Kondacs-Watrous measure-many question, and proofs for
two computable subclasses of that model. A proposed two-way range statement is deferred to v1.2 (proof in preparation); no
two-way result is claimed here. Section 9 of v1.0.x ("Open problems") is Section 10 here.

Exact checker: python quantum_checks.py (standard library only; Python 3.10 or later)
quantum_checks.txt is its recorded output: 4,812 orthonormal-column inner products; 126 direct dyadic simulations; 376 padded
sampling codes; 1,364 exhaustive short syntax/partial-trial cases (1,320 malformed); and 63 CPTP/PFA comparisons. All 1,929
acceptance comparisons passed. Both a planted nonunitary coin and a planted incorrect sampler were detected. The checker uses
exact rational arithmetic and checks finite instances of the control-language and channel constructions, not a two-way counter
compiler.

No computation is used in any proof. No publication or submission is performed by the build or the checker.
