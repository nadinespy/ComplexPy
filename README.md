## complexpy

# ComplexPy - a Library for Measures of Emergence & Complexity
This is the repository for a Python library whose aim is to apply several measures of emergence & complexity to either empirical or simulated time-series data, and provide guidance for comparisons among and conclusions about different measures. It thereby aims to enhance reproducibility, accessibility, systematicity, inclusivity, as well as drive the iterative cycle of theory and application in relevant fields of research.

# Emergence & Complexity - an Introduction
Multi-scale relationships in emergent phenomena and complex systems are studied across various disciplines. They explore the unresolved subject of how macro- and micro-scales relate to each other – are they independent, reducible, or is their relationship more complex? Examples of the phenomena in question would be, for instance, the way galaxies are formed, how crowds and herds behave, or how conscious human experience arises from the collective activity of neurons. An emergence poster child is given by a moving flock of starlings, the aesthetics of which is appealing to many.

[FLOCK_VIDEO](https://github.com/nadinespy/ComplexPy/assets/46372572/f487455d-a412-4fe9-b69b-f52866715ee3)

Historically, the lack of formalism hindered empirical investigation, but recent research introduced quantitative measures based on information theory to quantify emergence in systems whose components evolve over *time*. Measuring emergence is new terrain, therefore requiring extensive testing and cumulative evidence. A Python library with all measures at one place will facilitate this endeavour, and help drive the iterative cycle of theory-building and empirical testing. 

# Measures of Complexity & Emergence
Measures of complexity operationalize the idea that a system of interconnected parts is both segregated (i.e., parts act "independently"), and integrated (i.e., parts show "unified" behaviour, they form a "coherent whole"), the coexistence of which makes a system "complex". Take as an example the brain: all neurons eventually work together to guide behaviour and ultimately ensure survival, but parts thereof may "do their own thing" quite in separation from the rest of the system (e. g., there are language- and motor-focused parts of the brain), or they may be redundant (if some part of the brain ceases to function, conscious experience may continue to unfold, as it doesn't "sit" in any particular area). Emergence, on the other hand, is a phenomenon in which a property occurs only in a collection of elements (e. g., the moving shape in a flock of starlings, or consciousness in a sufficient set of neurons), but not in the individual elements themselves (e. g., the single birds, or the single neurons). Both emergence and complexity are studied in the context of the brain.

Quantifications of emergence can take on very different flavours - depending how emergence is defined - and there is no one-size-fits-all way to do it. Most of them operationalize multi-scale measures using information-theoretic language and are applicable to time-series data. While a plethora of complexity measures have been investigated quite substantially in the last couple of decades (see, e. g., [Wiesner, 2020](https://arxiv.org/pdf/1909.13243.pdf) for an overview), quantifying emergence is completely new territory (see, e. g., [Dynamical Independence](https://arxiv.org/pdf/2106.06511.pdf), or [Whole-Parts Emergence](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008289))

# Goals for this Library
Measures are not readily implementable - they are scattered over different GitHub repositories and programming languages (including MATLAB which is not open source). They are not made for use in different environments, and (academic) resources about them are not well accessible. Hence, reproducibility of applications is overall hampered. 

A way to easily and reproducibly use & compare a set of state of the art emergence and complexity measures - in an educated way, using only a few lines of code, and across environments - is thus missing. This is the gap this library is supposed to fill. 

This library will be useful for anyone interested in micro/macro relationships using time-series data (simulated or empirical), and for anyone aiming to make research on emergence & complexity more *open*, *reproducible*, *systematic*, *inclusive*, and thus *better*.

# A Minimally Viable Model - What This Library Can Already Do For You
Imagine you want to generate time-series data according to some time-series model, the function of which is stored in ```model_functions``` while the model-specific parameters are in ```model_variables```, and intend to compute several measures of emergence, as defined in ```emergence_functions``` with correspdonding measure-specific parameters in ```measure_variables```. You can then use the following line of code to do a sweep over all models and measures, including all involved parameters. (```parameters``` stores all parameters from both ```model_variables``` and ```measure_variables```.)
 
```r
import complex_py as cp

emergence_df = cp.compute_emergence(model_functions, model_variables, emergence_functions, measure_variables, parameters)
```

Calling single emergence functions is possible, too:
```r
cp.phiid_wpe()
cp.shannon_wpe()
```

(```cp.phiid_wpe()``` calculates Whole-Parts-Emergence based on Partial Information Decomposition, whereas ```cp.shannon_wpe()``` computes the same measure based on standard Shannon information.)

# The Big Picture - Future Plans

# Documentation

*Installation

# Citing

# Contribute

Once I have succeeded in releasing a mini-version of the library, I welcome contributions especially from people with software engineering/coding skills, and/or knowledge in information theory & complex systems, and/or a general interest in mathematical/formal micro-macro relationships, and/or a combination of the things just mentioned. Generally, contributions from anyone at any career stage and with any amount of coding experience will be welcome. Both contribution guidelines and Contributor Code of Conduct will be provided once a first release is achieved. 

### Licensing

This code uses the MIT license. More info can be found in the `LICENSE` file. 

### Getting cited

It has long been private due to unsettled publications statuses of software used, and has been made public only very recently. For that reason, preparations to make it ready for contributions from others lay dormant. I aim to change this soon, and all necessary info (e. g., contributor's guide) will be included, and further work on the code base that is necessary to have a minimally working library will follow.