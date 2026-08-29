# The Capital Census — Global Market Portfolio Weight History, 1976–2026

Fifty years of asset-class weights for the investable Global Market Portfolio (GMP),
estimated from public data under a frozen, fully disclosed methodology.

## What this is

**Annual** asset-class weights of the Capital Census Global Market Portfolio Index
(CC-GMP Index), reconstructed back to 1975. Each row is the observable composition at that
year-end; it is the reconstruction target for January of the following year, which is why a
1975–2025 measurement series produces a 1976–2026 portfolio history.

Two independent estimation paths were compared at the 2025 reconstruction: this series
(rebuilt from BIS, World Bank and WGC primary data) and the frozen v3 engine used for
monthly publication. They agree to within **1.71 percentage points in total absolute
difference across all sleeves**, the largest single-sleeve gap being 0.67pt.

## Columns

`weight_history_1976_2026.csv` — **official publication, 7 sleeves**

| Column | Description |
|---|---|
| `asof` | Year-end measurement date (YYYY-12-31), 1975–2025 |
| `Global Equity` | World equity market capitalisation × investability scalar |
| `DM Govt Bond` | Developed-market government debt, net of central-bank holdings |
| `Inflation Linked` | Inflation-linked share of the government block |
| `Credit` | IG credit + high yield, **combined** (see below) |
| `Securitised` | Securitised share of the credit block |
| `EM Debt` | Emerging-market debt |
| `Gold` | Above-ground stock × investable share × LBMA price |

Weights are percentages (0–100), rounded to 4 decimal places (basis-point precision).
Each row sums to exactly 100.0000; the rounding residual is absorbed by the largest sleeve.

`weight_history_1976_2026_auxiliary_8sleeve.csv` — **auxiliary, 8 sleeves.** Identical except
that `Credit` is split into `IG Credit` and `High Yield`. Under the index rulebook
(amendment_03) this split is an **uncalibrated auxiliary estimate**: the IG:HY ratio is a
fixed constant (15.1 : 1.7) applied to every year from 1984 onward, not a year-by-year
observation. No rating-level breakdown of outstanding balances exists in free primary data.
The split carries no time-series information and must not be read as one. The same caution
applies to `Inflation Linked`, whose share of the government block is fixed from 1997.

## Disclosure conditions (read before use)

This historical reconstruction is subject to three structural assumptions, disclosed in full:

1. Securitized-debt sleeve is anchored to the frozen v3 calibration values rather than
   re-estimated per period.
2. High-yield and inflation-linked shares within bond sleeves are held at their fixed
   calibrated structure across the full history.
3. Central-bank holdings are deducted for three institutions only (Federal Reserve, ECB,
   Bank of Japan); other official-sector holdings are not netted out.

Users who require different treatments should re-derive weights from the disclosed
methodology rather than adjust these figures ad hoc.

## What this is NOT

- Not investment advice, not a product, not a solicitation.
- Not a claim of performance superiority over any benchmark. Over our 50-year verification
  (1976–2026), the annualized return difference versus a 60/40 portfolio was within ±0.80
  percentage points at equal risk (90% confidence interval; equivalence not superiority —
  TOST p = 0.0177 at ±1.0pt bounds).
- All results are USD-denominated. No claims are made for other numeraires.

## Source and method

All figures are the author's own calculations from publicly available data. No third-party
proprietary data is redistributed. Methodology:
https://thecapitalcensus.github.io/methodology.html
Errors are corrected with a visible revision history, never silently.

## Use of AI tools

AI tools are used throughout this project — in literature search, in specifying and
implementing the estimation engine, in running the calculations, and in drafting the English
text. The author defines the protocol, checks every output against it, and is solely
responsible for what is published. What guards against error is not the absence of AI but
reproducibility: the inputs are public, the method is documented in full, and every
correction stays visible in the revision history.

## Author

Keisuke Nakanishi, Independent Researcher — ORCID [0009-0000-3780-9450](https://orcid.org/0009-0000-3780-9450)

## License and citation

The dataset (`*.csv`) is released under **CC BY 4.0** — see `LICENSE-DATA.txt`.
The build and verification scripts (`*.py`) are released under the **MIT License** —
see `LICENSE-CODE.txt`. Attribution is the only condition for the data.

Cite as:

> Nakanishi, K. (2026). *Global Market Portfolio Weight History, 1976–2026
> (The Capital Census)* (Version 1.0.0) [Dataset]. Zenodo.
> https://doi.org/10.5281/zenodo.22151403
>
> To cite **all versions**, use the concept DOI, which always resolves to the most
> recent release: https://doi.org/10.5281/zenodo.22151402

## Affiliation

The Capital Census is an independent, non-commercial research project. It is not affiliated
with State Street, MSCI, or any index provider, nor with any government statistical agency.
"Global Market Portfolio" is used as a generic academic term.

## Attribution notice

When reusing this dataset, please retain the following:

> Nakanishi, K. (2026). *Global Market Portfolio Weight History, 1976–2026* (v1.0.0)
> [Data set]. Zenodo. https://doi.org/10.5281/zenodo.22151403
>
> This is the DOI for version 1.0.0. A concept DOI resolving to the most recent
> version will be added here once the record is published.
> Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/).

Indicate if you modified the data. No additional restrictions may be imposed on
downstream recipients.
