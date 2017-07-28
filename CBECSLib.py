import numpy as np
import pandas as pd

from collections import defaultdict, Counter

pbaLabels = {
    1 : 'Vacant',
    2 : 'Office',
    4 : 'Laboratory',
    5 : 'Nonrefrigerated warehouse',
    6 : 'Food sales',
    7 : 'Public order and safety',
    8 : 'Outpatient health care',
    11 : 'Refrigerated warehouse',
    12 : 'Religious worship',
    13 : 'Public assembly',
    14 : 'Education',
    15 : 'Food service',
    16 : 'Inpatient health care',
    17 : 'Nursing',
    18 : 'Lodging',
    23 : 'Strip shopping mall',
    24 : 'Enclosed mall',
    25 : 'Retail other than mall',
    26 : 'Service',
    91 : 'Other'
}

pbaPlusLabels = {
    1  : 'Vacant',
    2  : 'Administrative/professional office',
    3  : 'Bank/other financial',
    4  : 'Government office',
    5  : 'Medical office (non-diagnostic)',
    6  : 'Mixed-use office',
    7  : 'Other office',
    8  : 'Laboratory',
    9  : 'Distribution/shipping center',
    10 : 'Non-refrigerated warehouse',
    11 : 'Self-storage',
    12 : 'Convenience store',
    13 : 'Convenience store with gas station',
    14 : 'Grocery store/food market',
    15 : 'Other food sales',
    16 : 'Fire station/police station',
    17 : 'Other public order and safety',
    18 : 'Medical office (diagnostic)',
    19 : 'Clinic/other outpatient health',
    20 : 'Refrigerated warehouse',
    21 : 'Religious worship',
    22 : 'Entertainment/culture',
    23 : 'Library',
    24 : 'Recreation',
    25 : 'Social/meeting',
    26 : 'Other public assembly',
    27 : 'College/university',
    28 : 'Elementary/middle school',
    29 : 'High school',
    30 : 'Preschool/daycare',
    31 : 'Other classroom education',
    32 : 'Fast food',
    33 : 'Restaurant/cafeteria',
    34 : 'Other food service',
    35 : 'Hospital/inpatient health',
    36 : 'Nursing home/assisted living',
    37 : 'Dormitory/fraternity/sorority',
    38 : 'Hotel',
    39 : 'Motel or inn',
    40 : 'Other lodging',
    41 : 'Vehicle dealership/showroom',
    42 : 'Retail store',
    43 : 'Other retail',
    44 : 'Post office/postal center',
    45 : 'Repair shop',
    46 : 'Vehicle service/repair shop',
    47 : 'Vehicle storage/maintenance',
    48 : 'Other service',
    49 : 'Other',
    50 : 'Strip shopping mall',
    51 : 'Enclosed mall',
    52 : 'Courthouse/probation office',
    53 : 'Bar/pub/lounge'
}

def to_categorical(y, nb_classes=None):
    '''Convert class vector (integers from 0 to nb_classes) to binary class matrix, for use with categorical_crossentropy.

    # Arguments
        y: class vector to be converted into a matrix
        nb_classes: total number of classes

    # Returns
        A binary matrix representation of the input.
    '''
    y = np.array(y, dtype='int')
    if not nb_classes:
        nb_classes = np.max(y)+1
    Y = np.zeros((len(y), nb_classes))
    for i in range(len(y)):
        Y[i, y[i]] = 1.
    return Y

def getDataset(datasetType=0,pbaOneHot=True):
    X,Y,columnNames = None,None,None

    if datasetType == 0: #All features
        X = np.load("output/cbecs_X_MFBTU.npy")
        Y = np.load("output/cbecs_Y_MFBTU.npy")
        columnNames = np.load("output/cbecs_headers_MFBTU.npy")
    elif datasetType == 1:
        X = np.load("output/cbecs_reduced_X_MFBTU.npy")
        Y = np.load("output/cbecs_reduced_Y_MFBTU.npy")
        columnNames = np.load("output/cbecs_reduced_headers_MFBTU.npy")
    else:
        raise ValueError("Invalid datasetType")

    classVals = X[:,columnNames=="PBA"].copy().flatten()

    excludedColumnNames = ["PUBID","PBA","PBAPLUS","REGION","CENDIV"]
    excludedMask = (columnNames!=excludedColumnNames[0])
    for i in range(1,len(excludedColumnNames)):
        excludedMask = excludedMask & (columnNames!=excludedColumnNames[i])

    X = X[:,excludedMask]
    columnNames = columnNames[excludedMask]

    # Do a 1-hot encoding of the PBA column and add the features to X
    if pbaOneHot:
        oneHotClasses,uniqueVals = doOneHot(classVals.copy(),returnNames=True)
        X = np.hstack([X,oneHotClasses])

        oneHotNames = []
        for val in uniqueVals:
            oneHotNames.append("PBA %d" % (val))
        columnNames = np.hstack([columnNames,oneHotNames])

    return X,Y,columnNames,classVals

def doOneHot(classVals,uniqueVals=None,returnNames=False):

    oneHotClasses = classVals.copy()

    if uniqueVals is None:
        uniqueVals = sorted(list(set(classVals)))

    print "%d classes" % (len(uniqueVals))
    uniqueValsMap = {val:i for i,val in enumerate(uniqueVals)}
    for i in range(oneHotClasses.shape[0]):
        oneHotClasses[i] = uniqueValsMap[oneHotClasses[i]]
    oneHotClasses = to_categorical(oneHotClasses)
    
    if returnNames:
        return oneHotClasses, uniqueVals
    else:
        return oneHotClasses

def filterDataset(X,Y,columnNames,classVals,columnsToRemove):

    mask = columnNames != columnsToRemove[0]
    for i in range(1,len(columnsToRemove)):
        mask = mask & (columnNames != columnsToRemove[i])
    return X[:,mask].copy(),Y.copy(),columnNames[mask].copy(),classVals.copy()

def getClassFrequencies(classVals):
    '''
    Input: 
        classVals - a vector of class labels.
    Output:
        classOrdering - a list where the first element is the most common class label, second element is second most common, etc.
        classFrequencies - a dictionary where keys are class labels and values are frequencies
    '''
    classVals = map(int, classVals)
    classFrequencies = Counter(classVals)
    classOrdering = sorted(classFrequencies, key=classFrequencies.get, reverse=True)
    return classOrdering,classFrequencies

def getDataSubset(X,Y,classVals,label):
    mask = classVals == label
    return X[mask,:].copy(), Y[mask].copy()

def getDataSubsetWithClassvals(X,Y,classVals,label):
    mask = classVals == label
    return X[mask,:].copy(), Y[mask].copy(), classVals[mask].copy()


regressors = [
    LinearRegression(n_jobs=-1),
    Ridge(),
    SVR(),
    Lasso(),
    ElasticNet(),
    LinearSVR(verbose=0),
    AdaBoostRegressor(),
    BaggingRegressor(n_jobs=-1),
    GradientBoostingRegressor(verbose=0),
    RandomForestRegressor(n_jobs=-1, verbose=0),
    ExtraTreesRegressor(n_jobs=-1, verbose=0),
    MLPRegressor(),
    KNeighborsRegressor()    
]
regressorNames = [
    "Linear Regression",
    "Ridge Regressor",
    "SVR",
    "Lasso",
    "ElasticNet",
    "Linear SVR",
    "AdaBoost",
    "Bagging",
    "XGBoost",
    "Random Forest Regressor",
    "Extra Trees Regressor",
    "MLP Regressor",
    "KNN Regressor"
]
assert len(regressors) == len(regressorNames)
numRegressors = len(regressors)

metrics = [
    mean_absolute_error,
    lambda y_true, y_pred: 10.0 ** mean_absolute_error(y_true, y_pred),
    median_absolute_error,
    lambda y_true, y_pred: 10.0 ** median_absolute_error(y_true, y_pred),
    r2_score
]
metricNames = [
    "Mean Absolute Error",
    "10^Mean AE",
    "Median Absolute Error",
    "10^Median AE",
    "$r^2$"
]
assert len(metrics) == len(metricNames)
numMetrics = len(metrics)