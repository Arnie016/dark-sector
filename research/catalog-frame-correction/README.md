# Frame-aware peak-to-catalog offsets

The [computational replay](../psz2-independent-reproduction/README.md) established that the two image WCS grids return FK5 J2000 coordinates. Some earlier comparisons treated those numeric peak coordinates as ICRS without a transformation. This check transforms each stored peak to ICRS before comparing it with the catalog coordinates, **assuming the catalog numbers are ICRS as in the earlier analysis**. The public VizieR tables label the coordinates J2000; sub-arcsecond absolute frame and astrometric accuracy still require source-level verification. No catalog uncertainty or likelihood is inferred from these values.

| Position relative to selected difference peak | Earlier numeric comparison | With FK5-to-ICRS transformation |
| --- | ---: | ---: |
| MACS LoTSS radio position | 5.277 arcsec | 5.264 arcsec |
| MACS LoTSS-associated optical position | 3.869 arcsec | 3.884 arcsec |
| MACS Keck optical object | 3.919 arcsec | 3.934 arcsec |
| PSZ2 LoTSS radio position | 20.542 arcsec | 20.537 arcsec |

The largest change is about 0.015 arcseconds, well below the map beams. These are comparisons with selected pixels, not fitted centroids; association, membership and physical interpretation remain unresolved. The [catalog-to-catalog MACS optical match](../macs1752-keck-crossmatch/README.md) does not use the image peak and is not altered here. The map-derived pair separations use a common WCS, so this cross-catalog coordinate correction does not change them.

## Reproduce

Run `python research/catalog-frame-correction/analyze.py /path/macs-T50kpcSUB.fits /path/psz2-T50kpcSUB.fits /path/v12-header.bin /path/v12-row.bin /path/psz2-radio-cone.tsv` from the repository root with Astropy. The code checks SHA-256 of both maps, the two original LoTSS FITS byte ranges, the PSZ2 catalog response and the stored Keck response; verifies the image WCS frames and object identifiers; transforms the saved peaks; and writes `summary.json`. All inputs are already archived privately in Azure or versioned in the repository. Cite the [LoTSS value-added catalog documentation](https://lofar-surveys.org/public/DR2/catalogues/README-v1.1.md), [LoTSS raw catalog](https://cdsarc.cds.unistra.fr/viz-bin/cat/J/A+A/659/A1) and [Keck survey catalog](https://cdsarc.cds.unistra.fr/viz-bin/cat/J/ApJS/240/39). Further work must verify coordinate conventions and astrometric errors against primary survey documentation before assigning association probabilities.
