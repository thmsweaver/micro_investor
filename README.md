# micro_investor
Script to ensure personal IRA contributions follow dollar-cost averaging (DCA).

DCA is an investment technique of buying a fixed dollar amount of a particular investment on a regular schedule. The intent is to track the market as closely as possible with one's constributions rather than attempt to capitalize on perceived trends.

While the initial goal of this project was to automate the contribution process entirely, despite my online trading brokerage not offering an API, relying on a static DOM to develop against is a fool's hope. In addition, having written Javascript applications in a former life, I know firsthand how browser events can be intercepted and manipulated on the fly - I eventually hit a wall in development as programmatic clicks on modal controls (trigger by Python or JS) simply weren't working.

### Prerequisites
 * Chrome internet browser
 * Fidelity Online Brokergage account with personal Roth IRA investment account
 * wget (brew install wget)
 
### Installing and Running
 1. Fork this repository to your own GitHub account and then clone it to your local device
 2. open a shell session and enter `make prereqs`
 3. ensure appropriate values for `FIDELITY_PASSWORD`, `FIDELITY_USERNAME`, `FIDELITY_ROTH_IRA_ACCOUNT_NUMBER` are `export`ed
 4. `python micro_investor.py`
 
