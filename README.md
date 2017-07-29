# SEI-ENERGY - Commercial-Energy

In this repository we provide all the code used to reproduce the results from the paper "Machine Learning Approaches for Estimating Commercial Building Energy Consumption" (in submission at Applied Energy), and to apply the trained models to new locations. We also provide instructions for downloading and organizing the free data sources included in our study.

In the four sections below we describe how our project is organized, how to obtain the data used for the experiments we run, how to reproduce the results shown in our paper, and how to apply our trained models in external situations.



## Code descriptions

The code for this project is in Python using Jupter notebooks (see [Jupyter webpage](http://jupyter.org/)). The code is organized as follows:

`CBECSLib.py` - Contains several methods and definitions that are used by other files.

Jupyter notebooks (each notebook starts with description of what it does):
- `Create CBECS datasets.ipynb`
- `Feature importances.ipynb` 
- `Generate MFBTU distributions per PBA.ipynb`
- `Run experiments.ipynb`
- `Train models on CBECS.ipynb`
- `Variable tables.ipynb`
- `Generate dummy data.ipynb`
- `Apply model.ipynb`
- `NYC - Data centroids.ipynb`
- `NYC - Run experiments.ipynb`
- `NYC - Validation.ipynb`
- `NYC - Write joined PLUTO-LL84 dataset.ipynb`



## Organizing external data

We use the 2012 CBECS microdata, downloadable from [here](https://www.eia.gov/consumption/commercial/data/2012/index.php?view=microdata). We have included the `2012_public_use_data_aug2016.csv` file in `data/cbecs/`. If there is a more recent version of the data released, then our file should be replaced with it, and the appropriate filename references in `Create CBECS datasets.ipynb` should be updated.

Because of the large sizes of the PLUTO and LL84 datasets we do not include them in this repository. You must download and add them to the `data/nyc/` directory as follows:


### Option 1 (Dropbox copy)
- Download a prepared zip file of the PLUTO and LL84 data from [here](https://www.dropbox.com/s/uefktqmsj63z387/nyc.zip?dl=0).
- Unzip this file to `data/nyc/`. There should now be two subdirectores in `data/nyc/`: "BORO_zip_files_csv" and "shapefiles".


### Option 2 (External copy)
- Goto [here](http://www.nyc.gov/html/gbee/html/plan/ll84_scores.shtml) and download the "2016 Energy and Water Data Disclosure (Data for Calendar Year 2015)" spreadsheet. Export the downloaded file, "nyc_benchmarking_disclosure_data_reported_in_2016.xlsx", as a csv file with "|" delimiters to `data/nyc/nyc_benchmarking_disclosure_data_reported_in_2016.csv`.
- Goto [here](https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page)
    - Download "nyc_pluto_16v2.zip" (this is the PLUTO (.csv format) download) and unzip to `data/nyc/BORO_zip_files_csv/`. This directory should contain: "BK.csv", "BX.csv", "MN.csv", "QN.csv", and "SI.csv"
    - Download all of the individual borough shapefiles to `data/nyc/shapefiles/`. There should be 5 subdirectories in `data/nyc/shapefiles`: "bk_mappluto_16v2", "bx_mappluto_16v2", "mn_mappluto_16v2", "qn_mappluto_16v2", and "si_mappluto_16v2".



## Reproducing paper results

Use these steps to reproduce the results shown in Tables 2 through 7:


### For the CBECS experiments

1. Run `Create CBECS datasets.ipynb`
2. Run `Run experiments.ipynb`
3. Run `Feature importances.ipynb`


### For the LL84 validation experiments

1. Run `Train models on CBECS.ipynb`
2. Run `NYC - Data centroids.ipynb`
3. Run `NYC - Write joined PLUTO-LL84 dataset.ipynb`
4. Run `NYC - Run experiments.ipynb`
5. Run `NYC - Validation.ipynb`



## Applying trained models to estimate energy consumption of commercial buildings in US cities

One of the main purposes of this project is to create a method for estimating commercial building energy consumption across a diverse range of metropolitan areas with limited access to building data. To help facilitate this goal we have created scripts for applying our trained models in external settings. The file `Train models on CBECS.ipynb` will train all of the models described in the paper on the full CBECS dataset, then save the trained models to disk to be applied on different datasets. In the paper we show results from applying our models to the Atlanta metropolitan area using commercial data from [CoStar](http://www.costar.com/). As this data is not free, we cannot distribute it, however we have included a way to generate "dummy" data to run our models in an external setting. The following steps demonstrate the pipeline we use to run our models on external data.

1. First, run `Generate dummy data.ipynb`. This will create two ".npy" files that represent "external" commercial building data. This dummy data is simply data from CBECS where each "row" in CBECS is assigned to a random (lat, lon) location within the downtown Atlanta area.
2. Second, run `Apply model.ipynb`. This script requires two input tables: a table of building features (like CBECS), and a table of building locations. The building features table should be of size $n \times 24$, where $n$ is the number of buildings. Each row in this table should represent the data for a specific building with the first four columns as the building's: square footage, coolding degree days, heating degree days, and number of floors and the last 20 columns as a one-hot encoding of the building's principal building activity. The building locations table should be of size $n \times 2$, where each row represents a building, and the rows match to the rows from the building features table (e.g. row 1 in both tables should have data about the same table). The first column should contain the latitude of the building and the second column should contain the longitude of the building. `Apply model.ipynb` also requires a shapefile to aggregate the energy consumption estimates by. In `data/shapefiles/` we provide a Traffic Analysis Zone shapefile for Atlanta, and a shapefile of US counties. The script will make an energy consumption estimate for each building in the input, then use the point locations and shapefile input to aggregate the energy consumption values to the zone level. The script outputs a shapefile named `output/ModelOutput.shp` that is a copy of the input shapefile, where each shape has a new field named "sumEnergy" which contains the aggregate modeled energy consumption value.