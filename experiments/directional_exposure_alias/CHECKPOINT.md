# D-07 checkpoint, 2026-10-23

Status: D07-C1 DERIVED/KNOWN; D07-C2 SIMULATION_RESULT; D07-C3 DATA_INSUFFICIENT.

One executed deterministic Python/NumPy process on a Linux container, seed null, 7 checks plus JSON readback passed, exit 0, 0.0321 s numerical core. Python 3.13.5, NumPy 2.3.5. Executed code SHA256 e8ea5eefa8e10394ecdfef9a14fbf7fa7d637a044ab56792a4d86decc15dc8c9.

SIMULATED 14-day masked 108 live hour bins: worst retained sidereal information 0.00487978; solar-only Asimov expectation, wrongly fit without solar nuisance, yields 1.76690 counts/live-hour fake sidereal coefficient amplitude; profiled Fisher worst-phase coefficient uncertainty 6.19755 counts/live-hour. 365-day masked 2784 live hours: retained 0.99992595, sigma 0.0804148. The correctly specified nuisance model yields zero sidereal coefficient to round-off. These are model calculations, not experimental bounds.

Source checks: arXiv:2602.15947v1 methods (17 Feb 2026), DAMIC-M PRD 114 032010 (19 Aug 2026), and arXiv:2608.06452v1 (6 Aug 2026). No primary event files, detector uptime masks or anisotropic material-response tensors were recovered.

Prior failed hypotheses retained: C-03 globally unscreened R+R² gravity fails Cassini; N-06 corrected dark-charge asymmetry norm sign on 21 Oct. The new D-07 script does not revisit them. GitHub main was b6b85682f0843ae0d097b5f192d90b51b130788d when this branch was prepared; PRs #4–8 remained open.

Learning: introduced template design matrices, solar/sidereal beat phase, projection and information loss. User understanding NOT_ASSESSED.

Next: a real live-time mask + physical material response + held-out calibrated background for a single baseline likelihood. No discovery or material sensitivity claim.
