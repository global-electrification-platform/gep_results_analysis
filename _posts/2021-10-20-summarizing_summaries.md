---
title: "Understanding the range of scenarios"
date: 2021-10-20
---
# Important Links
Global Electrification Platform – https://electrifynow.energydata.info/  
Energydata.info - https://energydata.info/dataset?q=Global+Electrification+Platform  
Example scenario table – TBD, add to github  
Open University Training - https://www.open.edu/openlearncreate/course/view.php?id=6816  

# Introduction
The Global Electrification Platform (GEP) explores solutions for achieving universal electrification across 58 countries, covering 90% of the world’s electrification deficit. The GEP is an interactive, online platform that allows users to explore ~100 scenarios per country, each scenario combines important model considerations, such as estimates of demand, grid and PV costs, and specific planning solutions. The model used to generate these scenarios has been fully open-sourced (see here), allowing users to generate their own scenarios, adjusting any of the over 250 parameters that go into the full model runs.
Considering the complicated nature of the electrification model, the size and complexity of the underlying datasets, and the difficulty of generating consistent, justifiable assumptions about the nature of current, and future electricity access, there is huge variation in the scenarios generated for each country. Herein, I will explore the range of results, discuss some of the more interesting observations, and propose potential next steps.
# Data
The unit of analysis for the GEP is the settlement – each settlement is analyzed to assess the electrification status, the nature of the residential and commercial demand, and the status of infrastructure. Based on these variables, we calculate a pathway to universal electrification by 2030, and determine the least-cost solution for each of the ~100 scenarios for each country. This blog will focus on the summary files for each scenario, in each country; these summarize the population connected, grid capacity added, and total investment required. All the scenario files are available on energydata.info, and an example of a specific scenario file can be found here (Link TBD).
# Results
Based on the analysis of the summary scenario files, the total cost to reach universal electrification in sub-Saharan Africa ranges from 68 billion USD to 420 billion USD; the expectation is 191 billion USD. This is a huge range in investment cost, driven primarily by expectations of consumer demand, and variations in the quality and availability of data describing electrification and infrastructure
Discussion
There is a $350 billion gap in our estimates to achieve universal electrification, driven by our confidence in the data surrounding our estimates. Data on expectations of consumer demand, current electrification status, and national grid infrastructure. 
