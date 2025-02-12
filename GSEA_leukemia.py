# -*- coding: utf-8 -*-
""" Paper : https://doi.org/10.1073/pnas.0506580102 <br>

---

> Installing required packages:
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# # Install python 3.8;
# %sx sudo apt-get update -y && sudo apt-get install python3.8
# 
# # Change Syslinks;
# %sx sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
# %sx sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
# 
# # Install Miniconda and friends.
# %sx wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh
# %sx chmod +x Miniconda3-py38_4.10.3-Linux-x86_64.sh
# %sx bash ./Miniconda3-py38_4.10.3-Linux-x86_64.sh -b -f -p /usr/local
# %sx rm Miniconda3-py38_4.10.3-Linux-x86_64.sh
# 
# # Friends;
# %sx conda install -c conda-forge rust -y
# %sx pip install gseapy==0.13.0
# # We do not need to specify pandas/mpl as they are within the gseapy requirements.
# 
# # Rename so the import works (preserving the original file).
# %sx cp /usr/local/lib/python3.8/site-packages/gseapy/gse.cpython-38-x86_64-linux-gnu.so \
# /usr/local/lib/python3.8/site-packages/gseapy/gse.so
# 
# # Link the packages so they are visible to the Runtime.
# from sys import path as link
# link.append('/usr/local/lib/python3.8/site-packages/')

---

# Check the amount of cores we can use
from os import cpu_count

# Packages to run the gsea functions
import pandas as pd
import gseapy as gp
import matplotlib.pyplot as plt

# Specific functions we need for plotting
try:
  from gseapy.plot import gseaplot
except ImportError:
  from gseapy.plot import gsea_plot as gseaplot

"Loading the downloaded files and performing GSEA." 
import gseapy as gp

# Run the cell below in BASH 
path_to_files = "/content/"
permutation_number = 100 # reduce number to speed up test
core_count = cpu_count() - 2
# =========== #

# Set the path to all files
dataset_cls = path_to_files + "Leukemia.cls.txt"
dataset_collapsed = path_to_files + "Leukemia_collapsed_symbols.gct.txt"
c2_symbols = path_to_files + "c2.all.v7.4.symbols.gmt"

# A function to provide some quick feedback
def finished(name):
    print(f"Finished processing {name}..")

# Open the downloaded files
phenoA, phenoB, class_vector = gp.parser.gsea_cls_parser(dataset_cls)
finished(dataset_cls)

gene_exp = pd.read_csv(dataset_collapsed, sep = "\t")
finished(dataset_collapsed)

gs_res = gp.gsea(
    data = gene_exp,
    gene_sets = c2_symbols,                # Library name
    cls = class_vector,
    min_size = 15,
    permutation_type = 'gene_set',
    permutation_num = permutation_number,
    outdir = None,                         # do not write output to disk
    no_plot = True,                        # Skip plotting
    method = 'signal_to_noise',
    threads = core_count,
    seed = 7,
    format = 'png'
)

finished(c2_symbols)

from google.colab import drive
drive.mount('/content/drive')

"""
---

*Print statement showing Leukemia phenotybe labels in the Leukemia.cls.txt file. <br>
"""

labelsFile = pd.read_csv("Leukemia.cls.txt", sep="\t")
print(labelsFile)

"""
---

GSEA results: store Gene Names inside of `terms` and index the items: <br>
* `terms[0]` gives us the first (highest ranked) gene set <br>
* `terms[-1]` is the lowest ranked gene set <br>
"""

terms = gs_res.res2d.Term.values

first_plot = terms[0]
second_plot = terms[-1]
# =========== #

# Plot for the first number
gseaplot(gs_res.ranking, term = first_plot, **gs_res.results[first_plot])
# Plot for the second number
gseaplot(gs_res.ranking, term = second_plot, **gs_res.results[second_plot])

"""> **Note:** Want to save the plot? Add `, ofname='your_file_name.pdf'` to the end of `gseaplot()`.

**Choosing gene set from the `terms_list` below. These names are in the [GSEA Database](https://www.gsea-msigdb.org/gsea/msigdb/genesets.jsp?collection=C2) <br>
"""

terms_list = terms.tolist()
print(terms_list)

index = terms_list.index('GOLUB_ALL_VS_AML_DN')
print(index)

"""The number you obtained after running the previous cell is the number you will have to put instead of the dots in the cell below. <br>"""

gseaplot(gs_res.ranking, term = terms[8], **gs_res.results[terms[8]])

index = terms_list.index('HADDAD_B_LYMPHOCYTE_PROGENITOR')
print(index)

gseaplot(gs_res.ranking, term = terms[4], **gs_res.results[terms[4]])

gseaplot(gs_res.ranking, term = terms[20], **gs_res.results[terms[20]])

""" <br>
Replacing the dots with the name of the geneset you downloaded from the website, to only run GSEA with this one gene set. 
First run the code with `permutation_type= 'gene_set'`. Then change this parameter to 'phenotype'.
"""

new_gene_set = path_to_files + "... .gmt"   # Fill in the name of the downloaded file on the dots.
gs_res_new1 = gp.gsea(
    data = gene_exp,
    gene_sets = new_gene_set,
    cls = class_vector,

    min_size =15,

    permutation_type = 'phenotype',
    permutation_num = permutation_number,
    outdir = None,                          # do not write output to disk
    no_plot = True,                         # Skip plotting
    method = 'signal_to_noise',
    threads = core_count,
    seed = 7,
    format = 'png'
)

terms_new = gs_res_new1.res2d.Term.values
gseaplot(gs_res_new1.ranking, term=terms_new[0], **gs_res_new1.results[terms_new[0]])

"""
---

The code below installs nbconvert.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !git clone https://github.com/jupyter/nbconvert.git
# !cd nbconvert
# !pip install -e .
# !apt-get install pandoc
# !apt-get install texlive-xetex texlive-fonts-recommended texlive-generic-recommended
# !jupyter nbconvert --to pdf '2022ComputerPractical.ipynb'
# !cd ..
#

"""If you want to create a PDF directly in Colab, you have to mount your google drive files to Colab:

When the code above executed succesfully, you can use nbconvert to create a PDF of your notebook. If you have saved the file in a different location than your home directory in Drive, or if you have changed the name of the file, you will have to change the line below as well.
"""

!jupyter nbconvert --to pdf '/content/drive/MyDrive/ComputerPractical.ipynb'
