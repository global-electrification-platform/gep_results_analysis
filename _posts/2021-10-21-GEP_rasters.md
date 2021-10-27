---
title: "Rasterizing GEP results"
date: 2021-10-21
--- 
## Generating large-scale rasters
The results from the GEP models are scenarios as csv files describing the particular least-cost solution; these csv files join to the vector settlement data, which are then uploaded to a central database for serving to [electrifynow.energydata.info](https://electrifynow.energydata.info). While this works well for our individual country vie online, it is difficult to consume these data in desktop GIS, and very heavy to look at more than one country at once. Therefore, we have designed a process to convert multiple countries at once through a rasterization process.

The detailed jupyter notebook [can be found here](https://github.com/global-electrification-platform/gep_results_analysis/blob/master/GEP_analysis/GEP_rasterize_results.ipynb), and the results of rasterizing the default scenario is below.
  
### Dynamic map #1  

<iframe src="https://geowb.maps.arcgis.com/apps/instant/basic/index.html?appid=5e3762690ae44cfe8eb57f79d867ef7e" width="600" height="450" frameborder="0" style="border:0" allowfullscreen>iFrames are not supported on this page.</iframe>

### Dynamic map #2  
  
<style>.embed-container {position: relative; padding-bottom: 80%; height: 0; max-width: 100%;} .embed-container iframe, .embed-container object, .embed-container iframe{position: absolute; top: 0; left: 0; width: 100%; height: 100%;} small{position: absolute; z-index: 40; bottom: 0; margin-bottom: -15px;}</style><div class="embed-container"><iframe width="500" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="GEP default map" src="//www.arcgis.com/apps/Embed/index.html?webmap=b2fdb4d597a049b9b6d498eedd3f4d5f&extent=-27.9107,-48.8213,58.0464,42.6664&zoom=true&previewImage=false&scale=true&legend=true&disable_scroll=true&theme=light"></iframe></div>
  
### Static image  
  
![GEP default Scenario](https://raw.githubusercontent.com/global-electrification-platform/gep_results_analysis/gh-pages/_posts/media/GEP_v2_0_0_0_1_0_0.png)
