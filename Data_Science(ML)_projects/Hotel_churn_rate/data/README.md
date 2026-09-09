# Data

`hotel_bookings.csv` is the public Hotel Booking Demand dataset:

Antonio, Nuno, Ana de Almeida, and Luis Nunes. “Hotel booking demand
datasets.” *Scientific Data* 6, 22 (2019).
https://doi.org/10.1038/s41597-019-0075-9

Two hotels in Portugal, arrivals July 2015 – August 2017. 119,390 rows,
32 columns.

I kept the original column names. The CSV uses the string `NULL` for
missing agent / company / country values. The notebook reads it with
`na_values=["NULL", "NA", ""]`.

The label is `is_canceled`. `reservation_status` is the same information
written as text (`Check-Out` / `Canceled` / `No-Show`) and should not be
used as a feature.
