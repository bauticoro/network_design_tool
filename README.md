# Infralast | Supply Chain Network Design Tool
Welcome to **Infralast**!
This is an open-source tool designed to support you in 
adding more intelligence power to operations wherever you go.


 This tool was created by Bautista Coronado, leveraging in 
 previous programs created by Michael Watson for educational 
 purposes in the book [Supply Chain Network Design](http://networkdesignbook.com/).

Infralast, in particular, is a result of our intention to
*Empower people to make data-based decisions through 
the usage of simple tools with low entry barriers*.

In this github, you will find the script of our [network-design-tool library](https://test.pypi.org/project/network-design-tool/).
Additionally, you can interact with this library through this [Google Colab.](https://colab.research.google.com/drive/1K8Z877KGMSydmfKuKmSEgpYu93ToyB2b?usp=sharing)

Contributions and constructive feedback are very welcome. 
Please [Reach out](bauticoro@gmail.com) to us.

---
### How to setup my specific case
It is recommended to use this tool after reading [Supply Chain Network Design Book](http://networkdesignbook.com/),  which introduces many concepts useful for a successful design. 
Once you have done that, you will find the first module of the Jupyter Notebook Script where you can manage the different parameters to work with.
### How to open a Jupyter Notebook
1. Install the necessary programs by following [this steps](http://networkdesignbook.com/wp-content/uploads/2019/02/Steps-to-install-Python-Anaconda-and-PuLP-and-plotly-packages.pdf)
2. To open Jupyter on Windows, go to the search bar at the bottom left and type in "Jupyter." You should see the Jupyter notebooks.
3. Jupyter Notebooks will open in your browser.  Just navigate to the folder where you downloaded [IntegratedOptimization.ipynb](https://github.com/bauticoro/network_design_tool/blob/main/IntegratedOptimization.ipynb) and open them.


---
### Legacy code
In this github, you will find a Jupyter Notebook which is useful as the main optimization tool: [IntegratedOptimization.ipynb](https://github.com/bauticoro/network_design_tool/blob/main/legacy/IntegratedOptimization.ipynb)
And you will find [data folder](https://github.com/bauticoro/network_design_tool/tree/main/legacy/data) which establishes the input data schema to make this tool work. 
It is important not to change the first row of each file, nor the order of the columns.w

---
### This tool is being built at this moment. Only two end points are validated to be used:
- minimize_total_weighted_demand (not totally validated)
- maximize_demand_within_a_distance
- minimize_total_distance

The rest of the endpoints are not ready to be used yet and don't have their unit test developed. Therefore, it is still not ready to be used.
