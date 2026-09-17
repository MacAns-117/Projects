# CSV Insights — eval

Default table: hotel bookings after clean (arrivals July 2015 – August 2017).

## Pandas facts (no LLM)

- Checks passed: **19/19**
- Clean rows: **87,230**
- Cancellation rate: **27.52%**
- Lead time canceled vs stayed: **105.7 vs 70.2 days**
- Busiest arrival month: **August**

| id | pandas |
|---|---|
| q01_row_count | pass |
| q02_cancel_rate | pass |
| q03_hotel_cancel | pass |
| q04_lead_time | pass |
| q05_bookings_by_month | pass |
| q06_adr_by_hotel | pass |
| q07_market_segments | pass |
| q08_lead_corr | pass |
| q09_countries | pass |
| q10_special_requests | pass |
| q11_repeated | pass |
| q12_years | pass |
| q13_booking_changes | pass |
| q14_deposit | pass |
| q15_nights | pass |
| q16_families | pass |
| q17_wait | pass |
| q18_customer_adr | pass |
| q19_busiest_month | pass |
| q20_capabilities | — |

## LLM run

Skipped. `python -m eval.run_eval --llm` needs GROQ_API_KEY.
Phrase matching is not a faithfulness score.
