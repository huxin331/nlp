1. the performace of Q5 is around 0.713(F1) and the algorithm is not good at analyzing the short sentence like fragments.
for example: Ad Notes ... . -- the algo will consider it as ["S", ["NP", ["NOUN", "Ad"], ["NOUN", "Notes"]], ["S", [".", "..."], [".", "."]]].  However it is ["NP", ["NOUN", "Ad"], ["NP", ["NOUN", "Notes"], ["NP", [".", "..."], [".", "."]]]].


2. the performance（F1 score） of Q6 is higher than that of Q5, it is 0.742. with the vertical markovization, this algo help give condition on parent non-terminal and increase the accuracy. 
for example in sentence 18. 
in Q5: it parses like that : 
["S", ["PP", ["ADP", "By"], ["NP+NOUN", "lunchtime"]], ["S", [".", ","], ["S", ["NP", ["DET", "the"], ["NOUN", "selling"]], ["S", ["VP", ["VERB", "was"], ["PP", ["ADP", "at"], ["NP", ["NOUN", "near-panic"], ["NOUN", "fever"]]]], [".", "."]]]]]

in Q6: it parses like it:
["S", ["PP^<S>", ["ADP", "By"], ["NP^<PP>+NOUN", "lunchtime"]], ["S", [".", ","], ["S", ["NP^<S>", ["DET", "the"], ["NOUN", "selling"]], ["S", ["VP^<S>", ["VERB", "was"], ["PP^<VP>", ["ADP", "at"], ["NP^<PP>", ["ADJ", "near-panic"], ["NOUN", "fever"]]]], [".", "."]]]]]

the Correct answer is:
["S", ["PP", ["ADP", "By"], ["NP+NOUN", "lunchtime"]], ["S", [".", ","], ["S", ["NP", ["DET", "the"], ["NOUN", "selling"]], ["S", ["VP", ["VERB", "was"], ["PP", ["ADP", "at"], ["NP", ["ADJ", "near-panic"], ["NOUN", "fever"]]]], [".", "."]]]]]

since with parent relationship,  probability of rule : NP^<PP>  -->ADJ , NOUN  is higher than the rule NP^<PP>  -->NOUN , NOUN. Thus, in Q6, it show correct answer in this sentence.