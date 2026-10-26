# Data audit

All five source files were checked during preprocessing.

| Check | Result |
| --- | --- |
| Sales series per file | 30,490 |
| Validation/evaluation history | 1,913 / 1,941 days |
| Overlapping sales values | Exact match after aligning series IDs |
| Missing, negative, fractional sales | 0 |
| Duplicate series or price keys | 0 |
| Price records | 6,841,121; positive, no missing cells |
| Calendar | 1,969 consecutive dates |
| Submission | 60,980 unique IDs, 28 forecast columns |

Blank event fields represent no recorded event. Missing product/week price
combinations remain missing; zero sales are retained and do not prove stockouts.
The two sales files overlap and are not concatenated. The final local holdout is
`d_1914`–`d_1941`; final `d_1942`–`d_1969` target sales are unavailable.

Full audit counts and raw-file fingerprints are in `data/processed/audit.json`.
