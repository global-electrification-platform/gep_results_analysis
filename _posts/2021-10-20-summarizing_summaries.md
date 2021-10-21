---
title: "Understanding the range of scenarios"
date: 2021-10-20
---
## Introduction
The Global Electrification Platform (GEP) explores solutions for achieving universal electrification across 58 countries, covering 90% of the world’s electrification deficit. The GEP is an interactive, online platform that allows users to explore ~100 scenarios per country, each scenario combines important model considerations, such as estimates of demand, grid and PV costs, and specific planning solutions. The model used to generate these scenarios has been fully open-sourced (see here), allowing users to generate their own scenarios, adjusting any of the over 250 parameters that go into the full model runs.
Considering the complicated nature of the electrification model, the size and complexity of the underlying datasets, and the difficulty of generating consistent, justifiable assumptions about the nature of current, and future electricity access, there is huge variation in the scenarios generated for each country. Herein, I will explore the range of results, discuss some of the more interesting observations, and propose potential next steps.
## Data
The unit of analysis for the GEP is the settlement – each settlement is analyzed to assess the electrification status, the nature of the residential and commercial demand, and the status of infrastructure. Based on these variables, we calculate a pathway to universal electrification by 2030, and determine the least-cost solution for each of the ~100 scenarios for each country. This blog will focus on the summary files for each scenario, in each country; these summarize the population connected, grid capacity added, and total investment required. All the scenario files are available on energydata.info, and an example of a specific scenario file can be found here (Link TBD).
## Results
Based on the analysis of the summary scenario files, the total cost to reach universal electrification in sub-Saharan Africa ranges from 68 billion USD to 420 billion USD; the expectation is 191 billion USD. This is a huge range in investment cost, driven primarily by expectations of consumer demand, and variations in the quality and availability of data describing electrification and infrastructure.  

| Tech           | Attr                | Global default   | Global minimum  | Global maximum   | Africa default   | Africa minimum  | Africa maximum   |
| -------------- | ------------------- | ---------------- | --------------- | ---------------- | ---------------- | --------------- | ---------------- |
| GRID           | New population      | 2,562,930,216    | 2,302,368,852   | 2,833,417,914    | 1,646,059,345    | 1,472,478,680   | 1,893,234,413    |
| GRID           | New connections     | 581,440,504      | 373,554,637     | 646,951,394      | 457,999,143      | 309,573,879     | 516,116,461      |
| GRID           | Capacity added      | 57,244,639       | 17,482,209      | 109,812,310      | 46,623,654       | 15,460,311      | 98,155,576       |
| GRID           | Investment required | $170,177,852,595 | $57,947,066,792 | $339,042,843,022 | $136,427,016,442 | $50,411,463,892 | $294,971,404,507 |
| Mini-grid      | New population      | 153,006,448      | 20,032,246      | 432,677,920      | 114,623,047      | 19,521,441      | 377,374,833      |
| Mini-grid      | New connections     | 119,503,684      | 17,262,807      | 350,524,856      | 90,909,005       | 16,752,002      | 306,126,278      |
| Mini-grid      | Capacity added      | 16,209,773       | 3,127,278       | 64,069,051       | 11,014,143       | 3,033,988       | 56,089,735       |
| Mini-grid      | Investment required | $24,357,878,760  | $2,513,485,238  | $95,449,693,792  | $16,248,570,907  | $2,421,939,324  | $83,678,398,290  |
| Stand-alone PV | New population      | 674,756,302      | 1,068,533,910   | 124,836,548      | 620,588,060      | 889,511,865     | 110,907,782      |
| Stand-alone PV | New connections     | 410,848,210      | 720,975,034     | 114,317,319      | 376,138,577      | 598,720,924     | 102,805,157      |
| Stand-alone PV | Capacity added      | 8,308,179        | 4,892,276       | 10,360,728       | 6,859,632        | 4,347,625       | 9,256,529        |
| Stand-alone PV | Investment required | $45,557,651,821  | $17,743,673,732 | $46,500,203,084  | $38,709,714,112  | $15,571,331,603 | $41,515,795,702  |
| TOTAL          | New population      | 3,390,692,966    | 3,390,935,008   | 3,390,932,382    | 2,381,270,453    | 2,381,511,986   | 2,381,517,028    |
| TOTAL          | New connections     | 1,111,792,397    | 1,111,792,478   | 1,111,793,568    | 925,046,725      | 925,046,806     | 925,047,896      |
| TOTAL          | Capacity added      | 81,762,591       | 25,501,763      | 184,242,089      | 64,497,428       | 22,841,925      | 163,501,839      |
| TOTAL          | Investment required | $240,093,383,176 | $78,204,225,762 | $480,992,739,898 | $191,385,301,460 | $68,404,734,820 | $420,165,598,499 |


## Discussion
There is a $350 billion gap in our estimates to achieve universal electrification, driven by our confidence in the data surrounding our estimates. Data on expectations of consumer demand, current electrification status, and national grid infrastructure. 
## Important Links
[Global Electrification Platform](https://electrifynow.energydata.info/)  
[Energydata.info](https://energydata.info/dataset?q=Global+Electrification+Platform)  
[Open University Training](https://www.open.edu/openlearncreate/course/view.php?id=6816)
