### Hansard Analysis

#### What's this?

This repo contains code to analyse the Hansard archives, which are an official record of every debate, question, or other spoken contribution made in the Houses of Parliament from 1803 to the present day.

#### Why bother?

Looking at changes in political discourse over time is fascinating. We can infer a lot about which issues were prioritised by different governments, how Members of Parliament responded to global events, when emerging technologies were first mentioned in Parliament, how the tone surrounding different issues has changed, and which MPs are the most talkative.

##### hansard.py

Contains functions to track usage of key words in the House of Commons from 1803 to the present day. Because the online archives (http://www.hansard-archive.parliament.uk/) are a bit of a mess, this code relies on having copies of Hansard for every day (!) saved locally on your system, with each HTML file following the naming convention 'yyyy mm dd'.

Instances of user-specific keywords or phrases (e.g. "internet", "European Union") are counted and plotted over time.

Future iterations will show breakdowns by party (e.g. do the Conservatives use the word "stable" more than Labour?) and by member (e.g. which MP uses the word "technology" most frequently?).

#### What's next?

Comparing the 'airtime' given to male vs female backbenchers and figuring out whether this is in proportion to their numbers.

Assessing which backbenchers are disproportionately talkative/the worst filibusterers.

Using sentiment analysis to assess how the tone of Parliamentary discourse has changed over time.

Some spicy stuff analysing the register of members' interests. 
