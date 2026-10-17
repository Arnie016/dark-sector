## D-02 | Methods, status and stopping rule

17 October 2026. **DERIVED**: independent Poisson channel probabilities with means mu_i factor into Poisson(total count, sum mu_i) times multinomial(category allocation, probabilities mu_i/sum mu_i). **DATA_INSUFFICIENT**: no full dark-matter signal likelihood reproduced.

Published DAMIC-M solar-reflection arXiv:2607.09352v1, Sec II Eqs 2, 5, 7: channels 11,21,111,31,22,211; counts 144,0,0,1,0,0. Nominal coincidence means 141.4,.111,.042,.019,.000025,.000058. Nominal radiogenic means .039,.039,.016,.052,.011,.035. Background scale fixed at one; control-region 98 events not fitted.

Rare five-channel total: N=1, B=.325083 events. At least one: 1-exp(-B)=.2775326. At least one in category 31: 1-exp(-.071)=.0685381. Conditional assignment to 31 given exactly one rare event: .071/.325083=.2184058. These are elementary fixed-background probabilities, not detector significance tests. One-sided count-only bound on extra expected rare events 3.564637 assumes perfectly known background and cannot be converted to a physical scattering bound.

Actual deterministic standard-library source: run.py SHA-256 7de9752611bb186c87f9fb9ba80b41823643f360f36e7f3aa560487024b3f867; six finite checks, JSON readback. No simulations, raw events, fitted response or independent validation. Strongest null: random-coincidence and radiogenic backgrounds. Stop at no particle detection claim. Next: retrieve one authentic six-channel signal benchmark and control nuisance model.
