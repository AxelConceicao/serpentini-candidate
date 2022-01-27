# Level 3

## Data
Each user has a name, an objective and an id (which will be used to reference the user in a deal).
Each deal has an amount, a user who closed the deal and two dates (when the contract was signed and when it was paid).

## Goal
You are trying to calculate the total of commissions an employer has to pay its two salesmen, for each month. 

/!\ This implies the output format changes, now commissions are stored in an object, the key being the year and month of payment (format YYYY-MM) and the value the total of commission paid in the month.

/!\ You also have to store the commission of each deal (just check the expected_output.json file to make sure you have the right format)

## Commissioning
Now, each deal has a commission associated, which is calculated when the deal is closed, but only paid when the deal is paid.
For instance, a deal closed on May but paid in June implies the user will get its commission on June.

Commissioning works as on level 2, the only difference being that you have to calculate a compensation for each deal.
- 5% of what they sell between 0% and 50% of their objective
- 10% of what they sell between 50% and 100% of their objective
- 15% of what they sell above their objective

/!\ Deals should be commissioned on the chronological order (from close_date), but they are already sorted this way in the input data !

## Example
You have 4 deals (in the chronological order), worth respectively 500, 300, 700 and 200
The objective of your salesman is 1000

### 1st deal
The first deal is commissioned to 5% because it matches perfectly the [0% - 50%] interval.

Commission: 5% * 500 = 25

### 2nd deal
The second deal is commissioned to 10% because it is contained in the [50% - 100%] interval.

Commission: 10% * 300 = 30

### 3rd deal
The third deal is split between two intervals. One part of the deal is commissioned at 10% and the rest at 15%. 

Commission: 10% * 200 + 15% * 500 = 95

### 4th deal
The last deal is in the 15% interval, as all following deals. 

Commission: 15% * 200 = 30

500 800 700 1000 600
5% * 500 = 25 // NOT PAID BEFORE THE NEXT DEAL
5% * 500 + 10% * 300 = 25 + 30 = 95 / 55
15% * 700 = 105
15% * 1000 = 150
15% * 600 = 90
25 + 95 + 105 + 150 + 90 = 465
425 OK

1000 700 550
5% * 250 + 10% * 250 + 15% * 500 = 12.5 + 25 + 75 = 112.5
15% * 700 = 105
15% * 550 = 82.5
300 OK