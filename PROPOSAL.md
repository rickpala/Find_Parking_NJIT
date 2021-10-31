Proposal goals:
- What is the problem? Why is it interesting?
NJIT's parking decks sometimes reach capacity leaving commuters unable
to find a parking spot in time for their classes. This can be frustrating,
and NJIT has implemented measures to see the parking levels in each 
deck at http://mobile.njit.edu/parking. However, these stats are
only available in real-time. What if you want to know what the parking level
will be in 30 minutes or an hour? We seek to collect parking data over the
course of several days to be able to determine, before your commute,
whether or not you will find a parking spot at NJIT.

- Reading?
This sort of project will require some studying
regarding time series predictions.

- Data collection?
Data is publicly available at http://mobile.njit.edu/parking. We
will automate collection using a 24-hour Python script
running on a Raspberry Pi that stores the data to
Google Sheets.

- Algorithm or model? Improvements upon existing ones?
The simplest model we can use will be Linear Regression, so we''ll begin
there. We can make further improvements specifically along what data
we decide to feed into the prediction algorithm (e.g., Mondays only).

- How will we interpret results? Qualitative vs Quantitative
Luckily, a ground truth is always available. We can
compare our hypotheses against observations to determine our error.
