import os, sys, logging, importlib, math
import rasterio, affine

import geopandas as gpd
import pandas as pd

from zipfile import ZipFile
from affine import Affine
from rasterio import features
from rasterio.mask import mask
from rasterio.features import rasterize

from gep_results import gep_results

class gep_results(object):
    def __init__(self, country,
                clustersFolder = '/media/gost/DATA/GEP/Clusters',
                scenariosFolder = '/media/gost/DATA/GEP/Scenarios'):
        ''' Object for extracting and processing GEP results files

        INPUT
        country [ string ] - name of country, stored as ISO2-1 eg - et-1
        '''
        self.country = country
        self.clustersFolder = clustersFolder
        self.clustersZipFile = os.path.join(clustersFolder, f'{country}.zip')
        self.scenariosZipFile = os.path.join(scenariosFolder, f'{country}-scenarios-results.zip')

        #Extract the scenario sample
        self.sampleScenarioFolder = os.path.join(scenariosFolder, "%s-scenarios-results" % country)
        if not os.path.exists(self.sampleScenarioFolder):
            if not os.path.exists(self.scenariosZipFile):
                raise(ValueError(f"The scenario results for {country} have not been downloaded: {self.sampleScenarioFolder}"))
            os.makedirs(self.sampleScenarioFolder)
            extractedFile = self.extract_sample_scenario(f'{country}-0_0_0_0_0_0.csv', self.sampleScenarioFolder)
            self.sampleScenarioFile = os.path.join(self.sampleScenarioFolder, extractedFile)
        else:
            for root, folders, files in os.walk(self.sampleScenarioFolder):
                for f in files:
                    if f == f'{country}-0_0_0_0_0_0.csv':
                        self.sampleScenarioFile = os.path.join(root, f)

        #Extract the clusters
        self.countryClustersFolder = os.path.join(clustersFolder, country)
        try:
            os.makedirs(self.countryClustersFolder)
        except:
            pass
        extract = True

        for root, folders, files in os.walk(self.countryClustersFolder):
            for f in files:
                if f[-4:] == ".shp":
                    self.clustersFile = os.path.join(root, f)
                    extract = False

        if extract:
            with ZipFile(self.clustersZipFile, 'r') as zipObj:
                zipObj.extractall(self.countryClustersFolder)
                allNames = zipObj.namelist()
                for f in allNames:
                    if f[-4:] == ".shp":
                        self.clustersFile = os.path.join(self.countryClustersFolder, f)

    def extract_sample_scenario(self, scenario, outFolder):
        ''' Extract a single scenario file from the scenario zipfile

        INPUT
        scenario [ string ] - et-1-0_0_0_0_0_0.csv
        outFiole [ string ] - full path to the file to create
        '''
        with ZipFile(self.scenariosZipFile, 'r') as zipObj:
            allFiles = zipObj.namelist()
            for f in allFiles:
                if scenario in f:
                    zipObj.extract(f, outFolder)
                    return(f)


    def join_results(self):
        ''' read in the scenario results and the clusters and join them
        '''
        inD = gpd.read_file(self.clustersFile)
        inRes = pd.read_csv(self.sampleScenarioFile)
        inCombined = pd.merge(inD, inRes, on='id')

        #generate additional columns
        # Set 2025 population to 0 where 2030 elec style is different than 2025
        inCombined['NewConnections2025'][inCombined['FinalElecCode2025'] != inCombined['FinalElecCode2030']] = 0
        gridIdx = inCombined['FinalElecCode2030'] == 1.0
        offGridIdx = inCombined['FinalElecCode2030'] != 1.0
        inCombined['GridPop2030'] = (inCombined['NewConnections2030'] + inCombined['NewConnections2025']) * gridIdx
        inCombined['OffGridPop2030'] = (inCombined['NewConnections2030'] + inCombined['NewConnections2025']) * offGridIdx
        return(inCombined)

    def create_subset_data(self, inD, outFile_name = "clusters_subset.shp", minPop=100, execute=True,
                          selFields = ['geometry','ElecPop','Pop','Pop2030','GridPop2030','OffGridPop2030','FinalElecCode2030']):
        ''' Create a subset clusters dataset with a series of input datasets
        '''
        selFields = ['geometry','ElecPop','Pop','Pop2030','GridPop2030','OffGridPop2030','FinalElecCode2030']
        inD = inD[inD['Pop2030'] > minPop]
        inD = inD[selFields]
        if execute:
            inD.to_file(os.path.join(self.clustersFolder, outFile_name))
        else:
            pass
        return(inD)


    def rasterize_results(self, inD, outFile,
                          field='FinalElecCode2030', res=0.1, dtype='uint8'):
        ''' Create raster describing a field in the shapefile

        INPUT
        inD [ geopandas dataframe created from join_results ]
        outFile [ string ] - path to output raster file
        [ optional ] field [ string ] - column to rasterize from inD
        [ optional ] res [ number ] - resolution of output raster in units of inD crs
        '''

        # create metadata
        bounds = inD.total_bounds
        # calculate height and width from resolution
        width = math.ceil((bounds[2] - bounds[0]) / res)
        height = math.ceil((bounds[3] - bounds[1]) / res)

        cAffine = affine.Affine(res, 0, bounds[0], 0, res * -1, bounds[3])
        nTransform = cAffine #(res, 0, bounds[2], 0, res * -1, bounds[1])
        cMeta = {'count':1,
                 'crs': inD.crs,
                 'dtype':dtype,
                 'affine':cAffine,
                 'driver':'GTiff',
                 'transform':nTransform,
                 'height':height,
                 'width':width}
        inD = inD.sort_values(by=[field], ascending=False)
        shapes = ((row.geometry, row[field]) for idx, row in inD.iterrows())
        with rasterio.open(outFile, 'w', **cMeta) as out:
            burned = features.rasterize(shapes=shapes,
                                        fill=0,
                                        all_touched=True,
                                        out_shape=(cMeta['height'], cMeta['width']),
                                        transform=out.transform,
                                        merge_alg=rasterio.enums.MergeAlg.replace)
            burned = burned.astype(cMeta['dtype'])
            out.write_band(1, burned)
