---
title: "Ratserizing GEP results"
date: 2021-10-20
--- 
## Generating large-scale rasters
The results from the GEP models are scenarios as csv files describing the particular least-cost solution; these csv files join to the vector settlement data, which are then uploaded to a central database for serving to [electrifynow.energydata.info](https://electrifynow.energydata.info). While this works well for our individual country vie online, it is difficult to consume these data in desktop GIS, and very heavy to look at more than one country at once. Therefore, we have designed a process to convert multiple countries at once through a rasterization process.

The detailed jupyter notebook [can be found here](), and the results of rasterizing the default scenario is below.

![GEP default Scenario](https://github.com/global-electrification-platform/gep_results_analysis/blob/gh-pages/_posts/media/GEP_v2_0_0_0_1_0_0.png)
