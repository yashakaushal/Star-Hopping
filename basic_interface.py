import numpy as np
import matplotlib
import matplotlib.pyplot as plt,mpld3
import pandas as pd
from IPython.core.display import HTML # To include images as HTML
import requests
import ast
import json 
from mpld3 import plugins,utils


#reading catalog and dropping nan values
star_cat = pd.read_csv("basic_interface_files/data_webscraping.csv")  #required database path 
star_cat = star_cat.dropna(subset=["spect","mag"])

#reading columns
ra = star_cat["rarad"]
dec = star_cat["decrad"]
spect = star_cat["spect"]
mag = star_cat["mag"]
flux = 10**(-mag/2.5)

#defining spectral cuts
omask = spect.str.startswith('O')
bmask = spect.str.startswith('B')
fmask = spect.str.startswith('F')
mmask = spect.str.startswith('M')

#variable star cat
var_star = star_cat[["rarad","decrad","var_min","var_max",]]
var_star = var_star.dropna()



class ClickInfo(plugins.PluginBase):
    """Plugin for getting info on click"""
    
    JAVASCRIPT = """
    mpld3.register_plugin("clickinfo", ClickInfo);
    ClickInfo.prototype = Object.create(mpld3.Plugin.prototype);
    ClickInfo.prototype.constructor = ClickInfo;
    ClickInfo.prototype.requiredProps = ["id"];
    function ClickInfo(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };
    
    ClickInfo.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);
        obj.elements().on("mousedown",
                          function(d, i){alert("clicked on RA DEC [" + d + "]");});
                         
    }
    """
    def __init__(self, points):
        self.dict_ = {"type": "clickinfo",
                      "id": utils.get_id(points)}

        
plt.rcParams["figure.figsize"]=(15,8)
fig, ax = plt.subplots()
points = ax.scatter(ra[omask],dec[omask],s=1e4*flux[omask],color="skyblue")

d = ax.collections[0]
#d.set_offset_position('data')
#print (d.get_offsets())      

labels = ["[RA {0:.5f} \n  Dec {1:.5f}]".format(i,j,'.2f','.2f') for i,j in zip(ra[omask],dec[omask])]
tooltip = plugins.PointLabelTooltip(points, labels)
plugins.connect(fig, tooltip)
plugins.connect(fig, ClickInfo(points))

ax.set_facecolor('black')
ax.grid(alpha=0.3)
ax.set_xlabel("RA", size =20)
ax.set_ylabel("DEC", size =20)
plt.savefig("basic_interface_files/test1.png")   #output stored in this folder

mpld3.show()













