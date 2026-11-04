# GWTC-5.0 metadata completeness checkpoint

**Question:** Does filtering the public GWTC-5.0 event-API metadata to rows with a reported primary source mass leave a representative set of all entries? The catalog snapshot shows a strong missingness pattern. This is a descriptive data-quality check, not a new astronomical discovery, selection-corrected population estimate, gravitational-wave detection, or independent replication of a collaboration result.

## Source and reproduction

- Source: [GWOSC GWTC-5.0 JSON API](https://gwosc.org/eventapi/jsonfull/GWTC-5.0/), retrieved 4 November 2026; 830,836 bytes, SHA-256 `5a15bccb5e1764e67feece022711f740a7e616b8c6b866c08b114741c846fb70`. This endpoint describes the GWTC-5.0 release's O4b event metadata; it is not the complete cumulative GWTC event catalog.
- The authoritative [release documentation](https://gwosc.org/GWTC-5.0/) describes the criteria and states that displayed false-alarm rate is the lowest across pipelines; SNR uses the default parameter-estimation result when available and otherwise the highest search SNR. These SNR values are therefore not necessarily identical estimators between groups.
- Run `python3 fetch.py` to fetch the exact pinned snapshot, followed by `python3 analyze.py` with the dependencies in `requirements.txt` installed (validated with NumPy 2.4.3 and Matplotlib 3.10.8). If the upstream API changes, the fetcher stops rather than silently analyzing a different release; the originally verified snapshot is held in the private Azure archive. The script verifies the input hash, reports unique event-version counts, calculates missingness, writes `summary.json` and `snr-availability.png`. Graph bins cover 7–24 only and explicitly omit larger SNRs.
- GWOSC states public data are [CC BY 4.0 with acknowledgement](https://gwosc.org/acknowledgement/). Cite the GWOSC service, LIGO Scientific Collaboration, Virgo Collaboration, KAGRA and GWTC-5.0 release documentation. This snapshot is a mirror of the provider's API, not a new data release.

## Result and limitations

The saved API response contains 161 event-version entries, with 161 distinct base event names. Primary source mass is populated for 104 and absent for 57. Of 105 entries with displayed FAR < 1 per year, 104 have a mass value; of 56 with FAR >= 1 per year, none do. One entry with displayed FAR < 1 has no primary source-mass value in this API snapshot. The release describes FAR-related triggering for parameter estimation but that alone does not explain every row's processing state. Do not call the exception an error without checking the collaboration's event-specific release.

Median displayed SNR is 11.3 for rows with mass and 8.6 for rows without; these are descriptive summaries of potentially differently constructed SNR values. Missing values are not zero. Comparing mass distributions after dropping missing rows changes the selected sample, and the release-specific metadata do not themselves supply the full detection efficiency, injection selection function, posterior samples, waveform/systematics, or population likelihood. A causal explanation and independent astrophysical inference remain untested.

## Next step

Before a population study, use the versioned posterior samples and relevant sensitive-volume/injection selection product, model uncertainties and detection thresholds, reproduce one collaboration baseline, then pre-register a held-out test. For a modified-gravity question, use a defined propagation model and its appropriate observations/likelihood; the event list alone cannot establish antigravity.
