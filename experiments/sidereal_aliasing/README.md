# D-04 | Solar and sidereal aliasing

**21 October 2026.** This work establishes a conditional mathematical non-identifiability result. A model with annual changes in the amplitude and phase of an ordinary 24-hour background can reproduce a pure sidereal cosine exactly:

$$\cos[(\omega_{\rm sol}+\Omega_{\rm year})t]=\cos(\omega_{\rm sol}t)\cos(\Omega_{\rm year}t)-\sin(\omega_{\rm sol}t)\sin(\Omega_{\rm year}t).$$

This is established trigonometry, not a dark-matter detection or a new theorem. An independent SIMULATED exposure audit compared three 720-hour observing schedules spread over 30, 120 and 360 days. With a stationary solar-day background, the retained Fisher information fraction is respectively 0.021878, 0.677875, 0.999998. Allow both annual nuisance components, and the signal is mathematically **UNIDENTIFIABLE** from timestamps in all schedules.

**Explanatory AHA:** spreading observing time over a year helps distinguish two clocks only if the allowed background cannot already reproduce the proposed sidereal waveform. More detector-hours cannot identify distinct causes sharing the exact same time series.

**Status:** D-04-C1 DERIVED; D-04-C2 SIMULATION_RESULT; D-04-C3 UNIDENTIFIABLE. Data used: **none**, all masks/rates invented. One bounded CPU run, 23 software/mathematical checks, no external likelihood reproduced. Published prior art: [Blanco et al. 2602.15947v1](https://arxiv.org/html/2602.15947v1) already derives nuisance Fisher projection and sidereal stacking. [SENSEI 2510.20889v1](https://arxiv.org/html/2510.20889v1) supplies real data acquisition methods, not inputs used here.

This note is separate from the [C-03 gravitational model](../field_closure/README.md) and older N-03 neutrino work. The next gate is the acquisition of actual exposure/efficiency tables and microscopic detector-response models. A hypothetical two-channel differential response only helps if its nuisance covariance is independently constrained. Researcher understanding NOT_ASSESSED.
