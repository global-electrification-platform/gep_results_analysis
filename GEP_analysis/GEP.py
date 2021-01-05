import os, sys, logging, importlib, math
import rasterio, affine

import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

from zipfile import ZipFile
from affine import Affine
from rasterio import features
from rasterio.mask import mask
from rasterio.features import rasterize


scenario_defs = {
               0:[["Medium","High"], "Population growth"],
               1:[["Top-down low","Top-down high", "bottom up"], "Electricity demand target"],
               2:[["No connections cap","Capped connections in 2025"], "Intermediate investment"],
               3:[["Estimated","High"], "Grid generation cost"],
               4:[["Estimated","High", "Low"], "PV cost"],
               5:[["Least-cost nationwide","Only grid within 1 km","Only grid within 2 km"], "Rollout"],
               }

def get_assumptions(input_scenario):
    """ Convert the six digit scenario into a list of assumptions

    input_scenario [string] - 1_0_0_1_0_0
    """
    scenario_results = []
    scenario_split = input_scenario.split("_")
    for val in range(0, len(scenario_split)):
        cur_def = scenario_defs[val]
        cur_val = cur_def[0][int(scenario_split[val])]
        scenario_results.append(f'{cur_def[1]}: {cur_val}')
    return(scenario_results)

# Functions used throughout the code to re-classify variables
def get_continent(x):
    ''' classify power pools - used in pandas apply function
    '''
    EAPP = [f'{x}-1' for x in ['bi','dj','et','ke','ly','rw','sd','ss','ug']]
    WAPP = [f'{x}-1' for x in ['bf','bj','ci','gh','gm','gn','gw','lr','ml','ng','sl','sn','tg']]
    SAPP = [f'{x}-1' for x in ['ao','bw','ls','mw','mz','na','sz','tz','za','zm','zw']]
    AFR =  [f'{x}-1' for x in ['cd','cg','cf','cm','er','ga','gq','km','mg','mr','ne','so','st','td']]
    if x in EAPP:
        return('AFR')
    if x in WAPP:
        return('AFR')
    if x in SAPP:
        return('AFR')
    if x in AFR:
        return('AFR')
    return("other")

# Functions used throughout the code to re-classify variables
def get_pp(x):
    ''' classify power pools - used in pandas apply function
    '''
    EAPP = [f'{x}-1' for x in ['bi','dj','et','ke','ly','rw','sd','ss','ug']]
    WAPP = [f'{x}-1' for x in ['bf','bj','ci','gh','gm','gn','gw','lr','ml','ng','sl','sn','tg']]
    SAPP = [f'{x}-1' for x in ['ao','bw','ls','mw','mz','na','sz','tz','za','zm','zw']]
    AFR = [f'{x}-1' for x in ['cd','cg','cf','cm','er','ga','gq','km','mg','mr','ne','so','st','td']]
    if x in EAPP:
        return('EAPP')
    if x in WAPP:
        return('WAPP')
    if x in SAPP:
        return('SAPP')
    if x in AFR:
        return('AFR')
    return("other")

def box_plot(inD, selected_attribute, out_file):
    data_bad_idx = inD['2025'] == inD['2030']
    inD = inD[~data_bad_idx]
    inD['Attribute_Num'] = inD['Attribute'].apply(lambda x: x[:1])
    inD['bad_model'] = inD['Scenario'].apply(lambda x: int(x[-1:]))
    inD = inD[inD['bad_model'] == 0]
    inD['2030_Log'] = np.log(inD['2030'])


    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    red_square = dict(markerfacecolor='gray', marker='.')
    boxprops = dict(linestyle='-', linewidth=4, color='g')
    medianprops = dict(linestyle='--', linewidth=1, color='g')

    plotArgs = {'grid':False,
                'rot':30,
                'by':'Attribute',
                #'sym':'.',
                'flierprops':red_square,
                'notch':False,
                'boxprops':boxprops,
                'medianprops':medianprops}

    regPlot = inD[inD['Attribute_Num'] == selected_attribute].boxplot('2030', ax=axes[0], **plotArgs)
    logPlot = inD[inD['Attribute_Num'] == selected_attribute].boxplot('2030_Log', ax=axes[1], **plotArgs)
    if not out_file == '':
        fig.savefig(out_file)
        def summarize_group(x):
            return(x.min(),x.mean(),x.max())

        res_grouped = inD.groupby(['Attribute'])
        xx = res_grouped[['2025','2030']].min().join(
        res_grouped[['2025','2030']].max(), rsuffix="_max").join(
        res_grouped[['2025','2030']].mean(), rsuffix="_mean")
        pd.DataFrame(xx).to_csv(out_file.replace('.png', '.csv'))
    return(inD)

def extract_plot(joined_data, selected_attribute, selected_scenario, title, chart_folder, plot=True):
    selected_index = [x for x in joined_data.index if (x[0][:1] == selected_attribute and x[1] == selected_scenario)]
    selected_data = joined_data.loc[selected_index]
    data_bad_idx = selected_data['2025'] == selected_data['2030']
    selected_data = selected_data[~data_bad_idx]
    if plot:
        xLabels = [x[0][2:] for x in selected_index]
        figure_title = xLabels[0].split("_")[0]

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
        selected_plot = selected_data.plot.bar(rot=30, ax=axes[0], title=f"{title} - Normal")
        selected_plot.set_xticklabels(xLabels)
        selected_plot.set_xlabel(f'Scenario - {selected_scenario}')

        logged_plot = selected_data.plot.bar(rot=30, ax=axes[1], logy=True, title=f"{title} - Logged")
        logged_plot.set_xticklabels(xLabels)
        logged_plot.set_xlabel(f'Scenario - {selected_scenario}')
        fig.savefig(f"{chart_folder}_{selected_scenario}_{title}_{figure_title}.png")
    return(selected_data)

class gep_summary(object):
    def __init__(self, file):
        self.file = file
        self.file_name = os.path.basename(file)
        self.country = self.file_name[:4]
        self.scenario = self.file_name[5:16]

    def get_data(self):
        self.summary_data = pd.read_csv(self.file)
        self.summary_data['Country'] = self.country
        self.summary_data['Scenario'] = self.scenario
        return(self.summary_data)

    def __str__(self):
        return(f'{self.country} : {self.scenario}')

class gep_results(object):
    def __init__(self, country,
                clustersFolder = '/media/gost/DATA/GEP/Clusters',
                scenariosFolder = '/media/gost/DATA/GEP/Scenarios',
                scenario = '0_0_0_0_0_0'):
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
            extractedFile = self.extract_sample_scenario(f'{country}-{scenario}.csv', self.sampleScenarioFolder)
            self.sampleScenarioFile = os.path.join(self.sampleScenarioFolder, extractedFile)
        else:
            for root, folders, files in os.walk(self.sampleScenarioFolder):
                for f in files:
                    if f == f'{country}-{scenario}.csv':
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
        for x_col in inD.columns:
            if x_col in inRes.columns and x_col != "id":
                inD = inD.drop([x_col],axis=1)
        inCombined = pd.merge(inD, inRes, on='id')

        #generate additional columns
        # Set 2025 population to 0 where 2030 elec style is different than 2025
        inCombined.loc[inCombined.FinalElecCode2025 != inCombined.FinalElecCode2030, 'NewConnections2025'] = 0
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
                 'width':width,
                 'nodata': 0}
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

class gepResults():
    def __init__(self, s3Folder, localFolder, code):
        self.s3Folder = s3Folder
        self.localFolder = localFolder
        self.countryCode = code
        self.summaryResultsFolder = os.path.join(localFolder, code, "outputs", "%s-scenarios-summaries" % code)

    def extractSummaries(self):
        outputFolder = os.path.join(self.localFolder, self.countryCode)
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)
        s3ZipFolder = os.path.join(self.s3Folder, self.countryCode, 'outputs')
        summaryResultsZip = os.path.join(s3ZipFolder, "%s-scenarios-summaries.zip" % self.countryCode)
        localResultsZip = os.path.join(outputFolder, "%s-scenarios-summaries.zip" % self.countryCode)
        if not os.path.exists(localResultsZip):
            shutil.copy(summaryResultsZip, localResultsZip)
        with zipfile.ZipFile(localResultsZip, 'r') as inZip:
            inZip.extractall(outputFolder)

    def processSummaryResults(self):
        # Summarize the scenario files
        scenarioFiles = os.listdir(self.summaryResultsFolder)
        for f in scenarioFiles:
            scenarioName = f[5:16]
            if int(scenarioName[-1]) == 0:
                inD = pd.read_csv(os.path.join(self.summaryResultsFolder, f))
                scenarioName = scenarioName.replace("_","")
                inD.columns = ["%s_%s" % (x, scenarioName) for x in inD.columns]
                try:
                    final = final.join(inD.iloc[:,1:3])
                except:
                    final = inD
        final2025 = final.loc[:,[x for x in final.columns if '2025' in x]]
        final2030 = final.loc[:,[x for x in final.columns if '2030' in x]]
        #Calculate summary columns for specific data
        final2030.loc['4.SA_total'] = final2030.iloc[[25, 26]].apply(lambda x: x.sum())
        final2030.loc['4.MG_total'] = final2030.iloc[[27, 28, 29, 30, 31]].apply(lambda x: x.sum())
        ### Running for 2030
        # Identify the scenario with the minimum and maximum value for each row in the table
        idxMax = final2030.apply(lambda x: x.idxmax(), axis=1)
        valMax = final2030.apply(lambda x: x.max(), axis=1)
        idxMin = final2030.apply(lambda x: x.idxmin(), axis=1)
        valMin = final2030.apply(lambda x: x.min(), axis=1)
        curRange = final2030.apply(lambda x: x.max() - x.min(), axis=1)
        xx = pd.DataFrame([idxMax, valMax, idxMin, valMin, curRange]).transpose()
        xx_index = list(inD.iloc[:,0])
        xx_index.append('4.SA_total')
        xx_index.append('4.MG_total')
        xx.index = xx_index
        xx.columns = ["MaxScenario","MaxVal","MinScenario","MinVal","Range"]
        return(xx)
