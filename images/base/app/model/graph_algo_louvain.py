#!/usr/bin/env python
# coding: utf-8


    
# In[1]:


# this definition exposes all python module imports that should be available in all subsequent commands
import json
import numpy as np
import pandas as pd
import cugraph
import cudf
# ...
# global constants
MODEL_DIRECTORY = "/srv/app/model/data/"







    
# In[3]:


# this cell is not executed from MLTK and should only be used for staging data into the notebook environment
def stage(name):
    with open("data/"+name+".csv", 'r') as f:
        df = pd.read_csv(f)
    with open("data/"+name+".json", 'r') as f:
        param = json.load(f)
    return df, param







    
# In[5]:


# initialize your model
# available inputs: data and parameters
# returns the model object which will be used as a reference to call fit, apply and summary subsequently
def init(df,param):
    model = {}
    return model







    
# In[7]:


# train your model
# returns a fit info json object and may modify the model object
def fit(model,df,param):
    model = {}
    return model









    
# In[12]:


# apply your model
# returns the calculated results
def apply(model,df,param):

    src_dest_name = param['feature_variables']
    dfg = df[src_dest_name]
    gdf = cudf.DataFrame(dfg)

    # create graph 
    G = cugraph.Graph()
    G.from_cudf_edgelist(gdf, source='src', destination='dest', renumber=True)
    max_iter = 100
    if 'max_iter' in param['options']['params']:
        max_iter = int(param['options']['params']['max_iter'])

    # cugraph Louvain Call
    dfr, mod = cugraph.louvain(G)
    dfr = dfr.to_pandas().rename(columns={"vertex": src_dest_name[0]})                   
    df = df.join(dfr.set_index(src_dest_name[0]), on=src_dest_name[0])
    df = df.rename(columns={"partition": src_dest_name[0]+"_partition"})   
    dfr = dfr.rename(columns={src_dest_name[0]: src_dest_name[1]})
    df = df.join(dfr.set_index(src_dest_name[1]), on=src_dest_name[1])
    df = df.rename(columns={"partition": src_dest_name[1]+"_partition"})   
    model['louvain_modularity'] = mod
    return df







    
# In[ ]:


# save model to name in expected convention "<algo_name>_<model_name>"
def save(model,name):
    # with open(MODEL_DIRECTORY + name + ".json", 'w') as file:
    #    json.dump(model, file)
    return model





    
# In[ ]:


# load model from name in expected convention "<algo_name>_<model_name>"
def load(name):
    model = init(None,None)
    # with open(MODEL_DIRECTORY + name + ".json", 'r') as file:
    #    model = json.load(file)
    return model





    
# In[ ]:


# return a model summary
def summary(model=None):
    returns = {"version": {"pandas": pd.__version__, "cudf": cudf.__version__, "cugraph": cugraph.__version__} }
    return returns





