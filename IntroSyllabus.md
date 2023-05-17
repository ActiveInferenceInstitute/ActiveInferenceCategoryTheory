# Introduction to Category Theory applied to Active Inference, Adventure Mode

*May 2023*

# Course Information

## For Whom

Any curious, thrill-seeking Active Inference Institute participant who wishes to study and conduct further research on active inference-related papers that involve category theoretical tools.

> We have a finite time on this earth, right and a finite time to dedicate to learning things --Christopher Whyte on [Modelstream #001.1](https://www.youtube.com/watch?v=H5AolqFl2Nw&t=1096s)

## Objective

To enable learners to read and study Active Inference papers that involve category theoretical tools, hence forming a pathway to bring researchers closer to the frontier in these areas relatively more quickly (or less completely bewilderingly) than without this syllabus. This syllabus can not be expected to result in full understanding, but can reduce uncertainty.

The syllabus traces somewhat of a parallel path, or extension, to the main threads of Active Inference as it has been studied from circa 2003-2023. Most Active Inference papers approach these topics from a quantitative or empirical angle (e.g. discussion of data-fitting applied to given statistical distributions and particular partitions).

Recently, as the field of Applied Category Theory has grown in momentum and relevance, people have begun applying it to areas of organizational studies, data science, cybernetic systems, and Active Inference (e.g. [MathStream #004.1](https://www.youtube.com/watch?v=aN1GXOZp6xY) with David Spivak). 

A course based on this syllabus can be seen as a supplement, appetizer, dessert, adventure companion, or accounting system that provides a different way to organize thinking about earlier and non-Category Theoretic Active Inference works.

**Notes**

1. This is an “adventure mode” course that may seem bewildering at times. However, it is possible for the reward to be great given such an approach. If you are interested in alternative adventures, links to university taught and YouTube courses are included towards the end of the document.
2. This is a prototype syllabus and has not yet been taught or studied explicitly as such — yet! Try it out and provide feedback or by sharing your end-of-course reflection on [Twitter](http://twitter.com/InferenceActive) or [Discord](https://discord.gg/BEpgX3z7) (on Discord, join the Category Theory channel). Please feel free to make suggestions and improvements directly here on the Github repository — this is a collaborative curriculum that is always in progress!

## Structure and Estimated Workload

This self-paced course is structured as a basic core with go-deeper resources for those with more time.

It sometimes takes an approach that involves multiple readings of the same chapters, where you start with a high-level skim, then go deeper as you update your generative model of mathematical knowledge. Because of this, there will be no one-size-fits-all estimate of student workloads. Instead, there is a suggested percentage time/effort estimate as follows:

1. Introduction (10%)
2. Foundations (10%)
3. Basic Category Theory (25%)
4. Higher Category Theory (25%)
5. Connections (20%)
6. Pathways Forward (10%)
7. Applying in the variability-retained world (?%)

There are various levels of understanding that may form student expectations. If a student is content with a first pass and exposure to the topics, the syllabus may be completed in ten months. If the student wishes to go deeper, one to two years of more weekly hours may be a more accurate estimate.

## Pre- or Co-Requisites

It is not compulsory to do the following before this syllabus, but it would help a lot. Otherwise, these can be done at the same time. Note that the Textbook Group runs in cycles and has set start dates.

* Participate in Active Inference Textbook Group cohort, at least Chapters 1-5 and 6 ([sign-up link](https://www.activeinference.org/education/textbook-group))
* Work through Smith, Friston, and Whyte (2022) “A step-by-step tutorial on active inference and its application to empirical data.” Journal of Mathematical Psychology ([link to paper](https://linkinghub.elsevier.com/retrieve/pii/S0022249621000973)), to read in conjunction with Chapter 4 of the Active Inference Textbook.

Knowledge of higher level mathematics or category theory is not expected. However, reading the following before or during the course may be helpful:

* Cheng, E. (2015, 2016) How to Bake Pi 

## Readings and Videos

Main resources we will follow in this syllabus

* Cheng, E. [*The Joy of Abstraction*](https://www.cambridge.org/core/books/joy-of-abstraction/00D9AFD3046A406CB85D1AFF5450E657) (2023)
  * Associated [The Joy of Abstraction book club videos](https://topos.site/joa-bookclub/), organized by The Topos Institute (2023) (Links below)
* St Clere Smithe, T. [*Mathematical Foundations for a Compositional Account of the Bayesian Brain*](https://arxiv.org/abs/2212.12538) (2023)
  * Associated livestreams [#054.0](https://www.youtube.com/watch?v=HK9ZkbxieLY), [#054.1](https://www.youtube.com/watch?v=fzFDvJhrn0U), and [#054.2](https://www.youtube.com/watch?v=GfImcptiLsY)

One additional suggested resource for the syllabus

* Riehl, E. [*Category Theory in Context*](https://math.jhu.edu/~eriehl/context/) (2016) as a reference reading

Other resources are in the eponymous section below.

# Topics and Sections

## Introduction

Introductions to category theory, how it is used in Active Inference, and first exposure to category theory applied to neuroscience

**Readings and Videos:**
1. Cheng: Prologue, Chapter 1 ([Chapter 1](https://youtu.be/zW-RGn1hrk4) of the book club on YouTube)
2. St. Clere Smithe: Abstract, Chapter 1
    
**Activities:**
1. *Getting to know terms.* Play with the terms in the Abstract and Chapter 1 of St. Clere Smithe however your brain works best. The goal is to become familiar with the words, not to know what them mean yet. List them on various different pieces of paper and color them in, make a spreadsheet or table. Form hypotheses of how they connect with what you already know.

## Foundations

Building intuition for basic category theory, reconnaissance of application to active inference

**Topics:** To be discovered in Story Map Light Sketch Activity

**Readings and Videos:**
1. Cheng: Chapters 2-8, watch corresponding book club videos ([Chapter 2](https://youtu.be/C6A8tqGsQWM) and onwards on YouTube), Appendices A, B, and C whenever referenced in text
2. St. Clere Smithe: Chapters 2-6, first pass: ***only the informal discussions***. This means: skip the formulas, definitions, propositions, proofs, and diagrams.
3. Livestream #054.0 ([on YouTube](https://www.youtube.com/watch?v=HK9ZkbxieLY)) (5/31/2023)
4. OPTIONAL: Cheng, E. (2015, 2016) How to Bake Pi, for background on mathematics (Chapters 1-8) and category theory intution presented less formally (Chapters 9-15)

**Activities:**
1. *Beginning to think categorically.* Attempt the Things to Think About in Cheng
2. *Story map, light sketch.* Follow the story that St. Clere Smithe is trying to tell by skteching a map. What looks familiar from your previous/concurrent study of Active Inference? What are the main mathematical constructions he uses and how do they fit together? That is, what notions lead to what other notions? This is a sketch. (Hint: Draw in pencil a directed graph connecting notions that stand out for you. Use different colors, shapes, and images if so moved. If it helps, set a time limit and stick to it - there wil be more time to expand and fill in details later.)

## Basic Category Theory

Basic category theory and introduction to 2-categories

**Topics:** category, functor, natural transformation, diagram, enriched category, functor, bicategory, 2-category, adjunction, universal constructions, dependent product, Yoneda Lemma

**Readings and Videos**

1. Cheng: Chapters 14 - Epilogue, corresponding book club videos (search Chapter 14 and onwards on YouTube)
2. Riehl: Preface, Chapter 1 - 2, Section 4.1 (exercises are optional)
3. St. Clere Smithe: Chapter 2, second pass. Read and try to follow the definitions, propositions, and proofs if you didn’t the first time around.
4. Livestream #054.1 ([on YouTube](https://www.youtube.com/watch?v=fzFDvJhrn0U)) (6/7/2023)

**Activities**

1. *Thinking categorically.* Attempt the Things to Think About in Cheng (but feel free to move along if you get stuck)
2. *Story map, darker sketch.* Refine the story map with formalism on basic category theory in St. Clere Smithe Chapter 2. Feel free to add sections or re-draw your map. Why were the definitions stated that way? What notions support other notions?

## Higher category theory and application

Higher category theoretical concepts and ramp-up into Bayesian inference. 

*(Note: I don't know whether a "strict" delineation between basic and higher category theory is, the header distinction is to help keep the syllabus organized)*

**Topics:**

1. String diagrams, monoidal category, bicategory, parametrized system, multicategory, monad, T-algebras, polynomial functors
2. Compositional probability, Kleisi category, compositional Bayes’ theorem, Grothendieck constructions, Bayesian lenses, Bayesian inversion, pseudofunctor
3. Open dynamical system, cilia (monoidal bicategories of cybernetic systems), differential systems
4. Statistical game, fitness function, profunctors, complex contexts, approximate inference doctrines, Bayesian inference, KL divergence, generative model, D-free energy, evidence upper bound,variational free energy, autoencoder games,  externally parametrized statistical games, Laplacian statistical game, Laplacian free energy, Hebbian-Laplacian statistical game

**Readings and Videos**

1. St. Clere Smithe: Chapters 3-6, second pass. Read and try to follow the definitions, propositions, and proofs if you haven’t yet. If you don’t fully understand, don’t worry too much.
2. Consult other resources, focusing on **looking up** concepts that remain hazy. This is a research and referencing exercise, rather than a reading to work through the book (Riehl’s book is a one-semester introduction to category theory!). Helpful resources, other than Wikipedia, are:
  * Riehl: Chapters 1-6, E2, E4
  * Math Stack Exchange and other similar platforms, exchanges with mathematicians in person or on socials
  * See **Other Resources - Books and Papers** below

**Activities**

1. *Story map, ink.* Refine the story map with formalism with notions that jump out at you from St. Clere Smithe Chapters 3-6. Why were the definitions stated that way? What leads to familiar Active Inference notions? What are the main mathematical constructions to focus on? How do they or could they fit together?
2. *Bayes’ rule compositionally.* Turn your regime of attention to Equation 4.2. What notions support other notions? What notions, in turn, does Equation 4.2 support?

## Connections

Tying together Active Inference and category theory

**Topics:** Synthesis of understanding

**Readings and videos:**

1. St. Clere Smithe: Chapter 6 deeper read if necessary. Revisit key storylines and concepts from previous chapters as needed.
2. Livestream #054.2 ([on YouTube](https://www.youtube.com/watch?v=GfImcptiLsY)) (6/15/2023)

**Activities**

*Map the model.* What kind of Active Inference model has St. Clere Smithe gotten to? Have a hand at mapping, drawing, or representing that categorically. Formalism is not expected - this is a representation of your understanding of what Active Inference and category theory notions correspond - an update of your generative model. Helpful resources to focus on Active Inference are:
  1. Parr, T., Markovic, D., Kiebel, S., and Friston, K. (2019) “Neuronal message passing using mean-field, Bethe, and Marginal approximations” ([link to paper](https://pubmed.ncbi.nlm.nih.gov/30760782/))
  2. Smékal, J. and Friedman, D.A. (2023) “Generalized Notation Notation for Active Inference Models.” ([link to paper](https://zenodo.org/record/7803328#.ZFo4js5Bzb00)
  3. Smith, R., Friston, R., and Whyte, C. (2022) “A step-by-step tutorial on active inference and its application to empirical data.” *Journal of Mathematical Psychology* ([link to paper](https://linkinghub.elsevier.com/retrieve/pii/S0022249621000973)) and associated [ModelStream #001.1](https://www.youtube.com/watch?v=H5AolqFl2Nw&t=1096s): "A Step-by-Step Tutorial on Active Inference"

## Pathways forward

Further areas to explore

**Topics:** dealing with correlated fitness functions/resolving potential problem of double-counting, making generative model dynamic, mapping Bayesian brain to biology, incorporating action into compositional framework, dealing with interrelated bidirectional processes, Bayesian mechanics, biosemiotics, better definition of “random dynamical system on a polynomial interface”, computation

**Readings and videos**

1. St. Clere Smithe: Chapter 7

**Activities**

*Reflection.* This course has been an experience in active inference. Using Active Inference terms, reflect on what and how you learned since first undertaking this journey. There is no strict format, but here are some ideas to get you started: 2-3 page document, 20-minute video, tapestry-like poster, a screenplay, blog post series. Here are some guiding questions:

1. What were your priors?
2. What were your observations?
3. Were there any parts of your generative model that resisted updating?
4. What was easy to update?
5. What pathways forward, if any, are you curious about?

*Further exploration.* Consider exploring Active Inference and related work that use category theory, such as:

1. Fields, C. and Glazebrook, J. (2020) “Information flow in context-dependent hierarchical Bayesian inference” ([link to paper](https://www.tandfonline.com/doi/abs/10.1080/0952813X.2020.1836034?journalCode=teta20)) and accompanying Livestream #017 ([#017.0](https://www.youtube.com/live/o7sJ-5vFJGk?feature=share), [#017.1](https://www.youtube.com/live/ldg2An-tEIE?feature=share), [#017.2](https://www.youtube.com/live/zF-EUnA-di4?feature=share))
2. Fields, C. and Glazebrook, J. (2020) “Do Process-1 simulations generate the epistemic feelings that drive Process-2 decision making?” (cones and cocones, [link to paper](https://link.springer.com/article/10.1007/s10339-020-00981-9))
3. Safron, A. (2022) “Integrated world modeling theory expanded: Implications for the future of consciousness” ([link to paper](https://www.frontiersin.org/articles/10.3389/fncom.2022.642397/full))
4. Sennesh, E., Xu, T., and Maruyama, Y. (2023) “Computing with Categories in Machine Learning” ([link to paper](https://arxiv.org/abs/2303.04156v1))
5. Get in touch with the [Active Inference Institute](https://www.activeinference.org/) to suggest a project or learning group, possibly to be done as a collaboration with the [Topos Institute](https://topos.site/)


# Other Resources

## Books and Websites

* Fong, B. and Spivak, D. (2019) *An Invitation to Applied Category Theory: Seven Sketches in Compositionality*
* Lawvere, W. and Schanuel, S. (2009) *Conceptual Mathematics*
* Mac Lane, S. (1998) *Categories for the working mathematician*
* Milewski, B. (2016) *Category Theory for Programmers*
* Spivak, D. (2013) *Category Theory for Scientists*
* [nLab](https://ncatlab.org/nlab/show/HomePage), higher catgory theory among others

More resources are listed in Cheng p. 416-416, “Further Reading”

## University Taught Courses

* MIT, Department of Mathematics, [Applied Category Theory](https://ocw.mit.edu/courses/18-s097-applied-category-theory-january-iap-2019/). As taught in January 2019 (videos included; Brendan and David co-founded the Topos Institute since)
* University of Cambridge, Department of Computer Science and Technology, [Category Theory](https://www.cl.cam.ac.uk/teaching/2122/L108/). 2021-22 (syllabus only)
* University of Edinburgh, School of Mathematics, [Category Theory](http://www.drps.ed.ac.uk/22-23/dpt/cxmath11237.htm). 2022-23 (syllabus only)

## YouTube Online Courses

* Borcherds, R. [Categories for the Idle Mathematician](https://youtu.be/JOp7mH72Jlg). 2021
* Milewski, B. [Category Theory for Programmers](https://youtu.be/I8LbkfSSR58). 2016
* Roman, S. [Course: Category Theory](https://youtu.be/If6VUXZIB-4)). 2015, and related book [*An Introduction to the Language of Category Theory*](https://link.springer.com/book/10.1007/978-3-319-41917-6) (2017)

# Encouragement

If you ever feel completely bewildered, you can get encouragement from elven paladin JR Learnstomath, who has a chronicle of their adventure exploring category theory and Active Inference [on this blog](https://jrlearnstomath.wordpress.com/).

# Thanks

Gratitude to Daniel F. of the Active Inference Institute for the support and scaffolding, the AII Category Theory learning group, especially Ali Rahmjoo, all of the authors cited above, and The Topos Institute with Brendan Fong and David Spivak. Thanks especially to Eugenia Cheng and Toby St. Clere Smithe, and, of course, Samuel Eilenberg and Saunders MacLane, and Karl Friston, and the other pioneers of these wonderful fields of exploration.

## Enjoy the adventure!





I Heart Little λ
