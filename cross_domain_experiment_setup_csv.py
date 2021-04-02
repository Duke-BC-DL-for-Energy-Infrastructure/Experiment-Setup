import random
import glob
import os

'''
This file creates .txt files, .data files, .names files and directories for a cross domain experiment
Inputs:
    The inputs are labeled with 'INPUT:', which include the paths for the real and synthetic images in each region as well
    as the names, training and validation real images, ratios/counts of real to synthetic images, and synthetic data used 
    for each experiment.

Outputs:
    Creates directories and files inside the OUTPUT_DIR. Inside OUTPUT_DIR, it creates a folder for each experiment,
    and within each experiment, there is a folder for the baseline, and then the adding synthetic folder. In the baseline
    and adding synthetic folder, it creates a .txt for the training image paths, training label paths, validation image paths,
    validation label paths, names file, and .data file which is used as the actual input to the YOLOv3 train.py script.

'''

separator = '\\' # The type of character used on your system to separate directories in paths

# INPUT:
# Directory where the program will output all of the files
OUTPUT_DIR = r'C:\Users\sarah\Documents\TYLER\Bass\Experiment Setup'

# INPUT:
# Collect paths for the real images of each region

with open('Train-and-Test-Splits' + separator + 'EM_cluster_train.csv', 'r') as f:
    EM_train = [line.split(',')[1] for line in f.readlines()][1:]

with open('Train-and-Test-Splits' + separator + 'EM_cluster_test.csv', 'r') as f:
    EM_val = [line.split(',')[1] for line in f.readlines()][1:]

# Special treatment for NE, since some of the image names have commas in them, and we need to ignore those
NE_train = []
with open('Train-and-Test-Splits' + separator + 'NE_cluster_train.csv', 'r') as f:
    for line in f:
        if 'name' in line:
            continue
        if '"' in line:
            NE_train.append(line.split('"')[1])
        else:
            NE_train.append(line.split(',')[1])

with open('Train-and-Test-Splits' + separator + 'NE_cluster_test.csv', 'r') as f:
    NE_val = [line.split(',')[1] for line in f.readlines()][1:]

with open('Train-and-Test-Splits' + separator + 'NW_cluster_train.csv', 'r') as f:
    NW_train = [line.split(',')[1] for line in f.readlines()][1:]

with open('Train-and-Test-Splits' + separator + 'NW_cluster_test.csv', 'r') as f:
    NW_val = [line.split(',')[1] for line in f.readlines()][1:]


# INPUT:
# Collect paths for the synthetic images of each region
EM_syn = [path.replace('.txt', '.png') for path in glob.glob(r'C:\Users\sarah\Documents\TYLER\Bass\synthetic_labels\EM*.txt')]
NE_syn = [path.replace('.txt', '.png') for path in glob.glob(r'C:\Users\sarah\Documents\TYLER\Bass\synthetic_labels\NE*.txt')]
NW_syn = [path.replace('.txt', '.png') for path in glob.glob(r'C:\Users\sarah\Documents\TYLER\Bass\synthetic_labels\NW*.txt')]

# Shuffle paths
random.shuffle(EM_train)
random.shuffle(NE_train)
random.shuffle(NW_train)
random.shuffle(EM_val)
random.shuffle(NE_val)
random.shuffle(NW_val)
random.shuffle(EM_syn)
random.shuffle(NE_syn)
random.shuffle(NW_syn)

# INPUT:
# Provide pairs of regions, synthetic data used for each experiment, and ratios of real and synthetic images
ratios = [[100, 50]] # In format [[# real, # syn], ...]
pairs = [[EM_train, EM_val], [EM_train, NW_val]] # Pairs of regions for each experiment. In format [[training_paths, validation_paths], ...]
pairs_names = [['EM', 'EM'], ['EM', 'NW']] # Pairs of regions for each experiment, but in string format
syn_data = [EM_syn, NW_syn] # Synthetic images for each experiment. As we are doing it now, this should match up with the validation region

# NAMING CONFIGURATIONS:
# Names of the .txt files
training_img_txt_filename = 'training_img_paths.txt'
training_lbl_txt_filename = 'training_lbl_paths.txt'
validation_img_txt_filename = 'val_img_paths.txt'
validation_lbl_txt_filename = 'val_lbl_paths.txt'

# Names of the .data files
baseline_data_filename = 'baseline.data'
adding_synthetic_data_filename = 'adding_synthetic.data'

# Names of the folders for the baseline and adding synthetic
baseline_folder_name = 'baseline'
adding_synthetic_folder_name = 'adding_synthetic'


if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# CREATE OUTPUTS:
for ratio in ratios:
    for i in range(len(pairs)):
        pair_names = pairs_names[i] # format: ['EM', 'NW']
        pair = pairs[i] # format: [EM, NW]

        # Create the folder for the current pair of regions
        output_folder = os.path.join(OUTPUT_DIR, f'Train {pair_names[0]} Val {pair_names[1]} {str(ratio[0])} real {str(ratio[1])} syn')
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        # Create folders for the baseline and adding_synthetic data for the current pair of regions
        baseline_folder = os.path.join(output_folder, baseline_folder_name)
        if not os.path.exists(baseline_folder):
            os.mkdir(baseline_folder)

        adding_synthetic_folder = os.path.join(output_folder, adding_synthetic_folder_name)
        if not os.path.exists(adding_synthetic_folder):
            os.mkdir(adding_synthetic_folder)

        # Create .data file for baseline folder
        with open(os.path.join(baseline_folder, baseline_data_filename), 'w') as baseline_data:
            baseline_data.write(f'train={baseline_folder_name}/{training_img_txt_filename}\n')
            baseline_data.write(f'train_label={baseline_folder_name}/{training_lbl_txt_filename}\n')
            baseline_data.write('classes=1\n')
            baseline_data.write(f'valid={baseline_folder_name}/{validation_img_txt_filename}\n')
            baseline_data.write(f'valid_label={baseline_folder_name}/{validation_lbl_txt_filename}\n')
            baseline_data.write(f'names={baseline_folder_name}/wnd.names\n')
            baseline_data.write('backup=backup/\n')
            baseline_data.write('eval=wnd')

        # Create .data file for adding synthetic folder
        with open(os.path.join(adding_synthetic_folder, adding_synthetic_data_filename), 'w') as adding_synthetic_data:
            adding_synthetic_data.write(f'train={adding_synthetic_folder_name}/{training_img_txt_filename}\n')
            adding_synthetic_data.write(f'train_label={adding_synthetic_folder_name}/{training_lbl_txt_filename}\n')
            adding_synthetic_data.write('classes=1\n')
            adding_synthetic_data.write(f'valid={adding_synthetic_folder_name}/{validation_img_txt_filename}\n')
            adding_synthetic_data.write(f'valid_label={adding_synthetic_folder_name}/{validation_lbl_txt_filename}\n')
            adding_synthetic_data.write(f'names={adding_synthetic_folder_name}/wnd.names\n')
            adding_synthetic_data.write('backup=backup/\n')
            adding_synthetic_data.write('eval=wnd')

        # Create .names file for baseline folder
        with open(os.path.join(baseline_folder, 'wnd.names'), 'w') as baseline_names:
            baseline_names.write('Wind-Turbine')

        # Create .names file for adding synthetic folder
        with open(os.path.join(adding_synthetic_folder, 'wnd.names'), 'w') as adding_synthetic_names:
            adding_synthetic_names.write('Wind-Turbine')

        # Create paths for baseline training set
        baseline_training_imgs = open(os.path.join(baseline_folder, training_img_txt_filename), 'w')
        baseline_training_lbls = open(os.path.join(baseline_folder, training_lbl_txt_filename), 'w')
        for img in pair[0][:ratio[0]]:
            baseline_training_imgs.write('../data/images/' + img + '.jpg' + '\n')
            baseline_training_lbls.write('../data/labels/' + img + '.txt' + '\n')
        baseline_training_imgs.close()
        baseline_training_lbls.close()

        # Create paths for baseline validation set
        baseline_validation_imgs = open(os.path.join(baseline_folder, validation_img_txt_filename), 'w')
        baseline_validation_lbls = open(os.path.join(baseline_folder, validation_lbl_txt_filename), 'w')
        for img in pair[1][:ratio[0]]:
            baseline_validation_imgs.write('../data/images/' + img + '.jpg' + '\n')
            baseline_validation_lbls.write('../data/labels/' + img + '.txt' + '\n')
        baseline_validation_imgs.close()
        baseline_validation_lbls.close()

        # Create paths for adding synthetic training set
        adding_synthetic_training_imgs = open(os.path.join(adding_synthetic_folder, training_img_txt_filename), 'w')
        adding_synthetic_training_lbls = open(os.path.join(adding_synthetic_folder, training_lbl_txt_filename), 'w')
        for img in syn_data[i][:ratio[1]]:
            adding_synthetic_training_imgs.write('../data/synthetic_images/' + img.split(separator)[-1] + '\n')
            adding_synthetic_training_lbls.write('../data/synthetic_labels/' + img.split(separator)[-1].replace('.png', '.txt') + '\n')
        for img in pair[0][:ratio[0]]:
            adding_synthetic_training_imgs.write('../data/images/' + img + '.jpg' + '\n')
            adding_synthetic_training_lbls.write('../data/labels/' + img + '.txt' + '\n')
        adding_synthetic_training_imgs.close()
        adding_synthetic_training_lbls.close()

        # Create paths for adding synthetic validation set
        adding_synthetic_validation_imgs = open(os.path.join(adding_synthetic_folder, validation_img_txt_filename), 'w')
        adding_synthetic_validation_lbls = open(os.path.join(adding_synthetic_folder, validation_lbl_txt_filename), 'w')
        for img in pair[1][:ratio[0]]:
            adding_synthetic_validation_imgs.write('../data/images/' + img + '.jpg' + '\n')
            adding_synthetic_validation_lbls.write('../data/labels/' + img + '.txt' + '\n')
        adding_synthetic_validation_imgs.close()
        adding_synthetic_validation_lbls.close()