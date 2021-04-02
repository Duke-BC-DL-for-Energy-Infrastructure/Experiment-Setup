# Experiment-Setup
## Purpose of the repo
This repo is meant to automatically setup experiments and generate necessary files for our experiments with synthetic imagery. 

## Using the repo
To use the repo, you can first clone it onto your computer. Then you can pick a script depending on which type of experiment you want to set up. For example, if we want to set up an experiment using the clustered real wind turbine data, you would use cross_domain_experiment_setup_csv.py, which uses the training and testing csv files that are already uploaded. Then, edit the code as necessary, particularly the portions of the code that are labeled with "INPUT:", which mostly just have to do with the paths on your local computer. 

If using the script that uses the csv files, then that should be simple, but otherwise, you need to use glob to collect the paths for the real imagery. For the synthetic imagery, you can also use glob to collect the paths for those images for each region. If the images aren't readily available on your local computer, you could download/use the generated labels from the Synthetic-Label-Generation process and use glob to collect the paths, and then use list comprehension to replace each of the paths with the particular image extension. 

Once the paths are correct, you can edit the setup, including the ratios to use, the pairs of regions, the name of the pairs, and the synthetic data being used for each pair of regions. After that, it should work as intended, but you can also change the naming configurations of the files being generated.
