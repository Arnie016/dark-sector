# N-06 | When dark-neutrino refraction is unidentifiable

**20 October 2026 | N-06-C1: DERIVED + SIMULATION_RESULT + UNIDENTIFIABLE for matched profiles; observations DATA_INSUFFICIENT.**

## Physical question

Can a measured astrophysical neutrino-flavor difference distinguish new dark-matter refraction from ordinary electron-matter refraction? Not when they produce the same *flavor-potential differences* along the path. That is an exact observation-level degeneracy. Independently calibrated source environments can make the two restricted models predict different probabilities.

**Primary prior art:** Dev, Gaido, Ibarra, Porto, [Resonant neutrino flavor conversion within dark matter spikes](https://arxiv.org/abs/2609.26773), preprint 22 September 2026, sections II–VI and Appendix A. It solves the *three-flavor, radially evolving AGN spike* model; the bounded study below is a two-state constant-slab teaching/identifiability model, not their reproduction. The [IceCube three-flavor analysis](https://arxiv.org/abs/2510.24957), first submitted 28 October 2025 and published August 2026 in PRL, used 11.4 years of earlier exposure. It measures diffuse 5 TeV–10 PeV neutrino flavor, not individual-AGN flavor or new 2026 exposure. No released IceCube event/likelihood or detector response was fitted here.

## Explicit physical Hamiltonian

For effective vector coupling to Dirac dark matter, the source-background **net** density is Delta n = n_chi - n_antichi. With A_chi = Delta n/(n_chi+n_antichi), rho_chi = mchi(n_chi+n_antichi), the coherent matter potential in natural units is

$$V_{\chi,\alpha}=2\sqrt2 G_F\epsilon_\alpha A_\chi\frac{\rho_\chi}{m_\chi},\qquad H(E,r)=\frac{UM^2U^\dagger}{2E}+V_{\rm SM}(r)+\mathrm{diag}(V_{\chi,\alpha}(r)).$$

Hamiltonian rows/columns label **flavors**; entries have dimensions of energy. Symmetric particle-antiparticle dark matter has A_chi=0 and therefore no *vector forward-scattering* potential even if its mass density is large. This does not rule out hard scattering, scalar interactions or other dark sectors.

Adding a common v(r)I changes only a shared phase and no flavor probabilities. At fixed source profile, oscillations constrain products epsilon_alpha*A_chi*rho_chi/mchi and flavor differences, not the separate dark mass, coupling, asymmetry or universal component.

**AHA, explanatory rather than a new discovery:** an interaction's name is not measured. A dark muon potential diag(0,-V) and ordinary electron potential diag(V,0) differ only by -V times the identity matrix. If their spatial profiles match, *all* neutrino-flavor probabilities agree for every energy. No amount of extra data from the same measurement can distinguish them without new information about their physical environments.

## SIMULATED single-source degeneracy and a second-source control

The exact two-state constant-H solver propagates an initially mu-flavor state across a 1e-4 pc uniform layer, then averages vacuum mass phases before detection. It uses an illustrative angle 33.4 degrees, mass-squared splitting 7.42e-5 eV² and source energies 30–300 TeV. The synthetic dark benchmark: rho_chi=4e18 GeV/cm³, mchi=1 GeV, A_chi=1 and epsilon_mu=-1, yielding V_mu=-1.0139206666924082e-18 eV. Source A has synthetic electron density ne=8e18 cm^-3, yielding Ve=+V. **Neither density is a measurement or a validated AGN environment.** Source B stipulates 5% of A's electron density but 60% of A's dark net density, assumed independently known solely for a proof-of-principle control.

| SIMULATED source and energy | Ordinary Earth electron fraction | Dark Earth electron fraction |
| --- | ---: | ---: |
| A, 100 TeV | 0.52525 | 0.52525 |
| B, 50 TeV | 0.43062 | 0.46390 |
| B, 100 TeV | 0.42903 | 0.63910 |
| B, 200 TeV | 0.52292 | 0.52963 |

**Results:** maximum A difference across seven energies = 3.33e-16, as predicted by a common-phase equivalence. Maximum B difference = 0.25162 in probability *under the stipulated known-density profiles*. At B, 100 TeV the ordinary model with an arbitrary initial e/mu source fraction gives Earth electron fraction between 0.42903 and 0.57097, while the chosen dark pure-mu prediction is 0.63910. This does **not** survive arbitrary density, source-spectrum or detector freedom by assumption.

One bounded standard-library CPU process, one worker, seed=null/no randomness. **86 finite implementation and limiting checks passed, not 86 independent physical validations.** [Executed code](run.py) regenerates full JSON and CSV; archived source SHA-256 cfb8ec6fbb3da5c222e5416e901e9647abb5c1909eb6a04246453bc7c22f4205. See [frozen output summary](RESULTS_SUMMARY.md). No telescope data, three-flavor AGN evolution, sensitivity forecast, paid resource, researcher contact or manuscript submission.

## Research and learning checkpoint

**N-06-C1, DERIVED:** the Hamiltonian's identity-null and product-scaling degeneracies. **N-06-H1, CONJECTURE:** independently constrained electron and dark columns across multiple AGNs might resolve a specific interaction when three-flavor propagation, source mixture and detector response are modeled. **Strongest null:** flexible source emission or density profiles absorb the difference. **Stop** if no physically calibrated independent density constraint or if held-out energy/source prediction collapses after nuisance freedom.

N-04 assumed an abstract mixing gate; N-06 supplies an explicit motivated forward-scattering Hamiltonian but is not a three-flavor reproduction. C-03's globally unscreened long-range gravity benchmark remains FAILED. **Learning:** introduced net-current asymmetry, forward-scattering potential, common-phase invariance and two-source controls. Understanding remains NOT_ASSESSED.

**Recommended next bounded gate:** retrieve the source-population, IceCube flavor likelihood and detector/production nuisance model; compare with standard matter in a three-flavor forward calculation. No observational likelihood is yet supported.
