# MACS J1752: LoTSS catalog v1.2 cross-check

The [LoTSS DR2 release](https://lofar-surveys.org/dr2_release.html) describes a v1.2 catalog incorporating DESI DR1 redshifts. For radio source `ILTJ175159.28+443849.6`, its original v1.2 row still reports `z_best = 0.3469112`, `z_source = Phot`, and `zphot_err = 0.0308101`, matching the [v1.1 check](../macs1752-photoz-provenance/README.md). Its DESI, SDSS, and HETDEX spectroscopic redshift fields are blank. The error is the catalog's predicted 1σ photometric uncertainty, not a spectroscopic measurement.

The source lies about 5.29 arcseconds from the selected image-difference peak; the catalog's associated optical position is 9.14 arcseconds from the radio position. These positional associations and the photometric redshift do not establish that the source causes the image difference or belongs to the cluster. Blank fields do not establish that spectroscopy is unavailable in other catalogs or later releases.

## Reproduction

The official v1.2 catalog is 3,934,056,960 bytes. Two HTTP 206 range requests retrieved 131,072 header bytes and one 944-byte row; the retained header is the required first 69,120 bytes. The provisional row offset was checked against the original row's source name and coordinates, not treated as an identifier. The exact ranges, source URL and SHA-256 hashes are in `manifest.json`. A changed catalog may invalidate the offset; verify the response range, catalog version, identity and coordinates each time.

With NumPy and Astropy installed, run `python research/macs1752-photoz-v12/analyze.py /path/header.bin /path/row.bin` from the repository root. The script validates the retained bytes, reconstructs a one-row FITS table in memory and compares the result to the saved v1.1 summary. The ranges and analysis are archived privately. See also the [catalog documentation](https://www.lofar-surveys.org/public/DR2/catalogues/README-v1.1.md) and [catalog methodology](https://arxiv.org/html/2309.00102#S8.SS1).
