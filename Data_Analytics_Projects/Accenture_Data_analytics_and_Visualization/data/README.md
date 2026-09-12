# Data

`cleaned_reactions.csv` is the joined analysis table from the Accenture
Forage Social Buzz dataset (Content + Reactions + Reaction types).

| Column | Meaning |
| --- | --- |
| Content_ID | post |
| User_ID | person who reacted |
| Type | reaction (heart, peeking, …) |
| Datetime | when they reacted (day-first) |
| Content_Type | photo / video / GIF / audio |
| Content_Category | topic label (some rows had extra quotes) |
| Sentiment | positive / negative / neutral |
| Reaction_Score | 0–75 points for that reaction type |

962 posts, 500 users, 22,534 reactions, 18 Jun 2020 – 18 Jun 2021.

Source tables are described in [`docs/data_model.pdf`](../docs/data_model.pdf).
The original Forage files are Content, Reactions, and ReactionTypes;
this CSV is the inner-joined result used for scoring.
