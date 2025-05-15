Working LLM Text Correction Prompt Below:

Blacklist: {yellow}

Instructions:
1. Replace each word in the blacklist with asterisks — one asterisk per letter. For example, "yellow" becomes "******".
2. Do not censor any words that are not in the blacklist.
3. Fix all grammar, punctuation, and clarity issues in the text.
4. Output only the corrected and censored paragraph — no extra explanation.

Example:
Input: I seen the yellow sky and it dont look normal.
Output: I saw the ****** sky, and it didn't look normal.

Input:
yesterday i seen a yellow bird outside it was flying real fast and then it land on the tree but it dont make no sound or nothing i was like wow thats crazy maybe yellow looking for food but i aint sure
