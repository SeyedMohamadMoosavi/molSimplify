# Written by JP Janet for HJK Group
# Dpt of Chemical Engineering, MIT

##########################################################
######## This script contains a neural network  ##########
#####  trained on octahedral metal-ligand          #######
########   bond distances and spin propensity  ###########
##########################################################


## import 
import keras
from keras import backend as K
from keras.models import model_from_json, load_model
from keras.optimizers import Adam
import numpy as np
import csv
from pkg_resources import resource_filename, Requirement
from clf_analysis_tool import array_stack, get_layer_outputs, dist_neighbor, get_entropy
from molSimplify.Classes.globalvars import *
from molSimplify.python_nn.ANN import matrix_loader
import sys, os
import json
import pandas as pd
import glob
import time


## Functions
def get_key(predictor, suffix=False):
    if suffix:
        if predictor in ['ls_ii', 'hs_ii', 'ls_iii', 'hs_iii']:
            key = 'geos/' + predictor + '_%s' % suffix
        elif predictor in ['homo', 'gap']:
            key = 'homolumo/' + predictor + '_%s' % suffix
        elif predictor in ['oxo', 'hat']:
            key = 'oxocatalysis/' + predictor + '_%s' % suffix
        elif predictor in ['geo_static_clf', 'sc_static_clf']:
            key = predictor + '/' + predictor + '_%s' % suffix
        else:
            key = predictor + '/' + predictor + '_%s' % suffix
    else:
        if predictor in ['ls_ii', 'hs_ii', 'ls_iii', 'hs_iii']:
            key = 'geos/'
        elif predictor in ['homo', 'gap']:
            key = 'homolumo/'
        elif predictor in ['oxo', 'hat']:
            key = 'oxocatalysis/'
        elif predictor in ['geo_static_clf', 'sc_static_clf']:
            key = predictor + '/' + predictor + '_%s' % suffix
        else:
            key = predictor
    return key


def data_rescale(scaled_dat, train_mean, train_var):
    d = np.shape(train_mean)[0]
    # print('unnormalizing with number of dimensions = ' +str(d))
    dat = (np.multiply(scaled_dat.T, np.sqrt(train_var), ) + train_mean).T
    return (dat)


def data_normalize(data, train_mean, train_var):
    data = data.astype(float)  # Make sure the data is always in float form
    d = np.shape(train_mean)[0]

    # print('normalizing with number of dimensions = ' +str(d))
    ### double check the variance in the training data
    delete_ind = list()
    # print(train_var)
    for idx, var in enumerate(np.squeeze(train_var)):
        if var < 1e-16:
            delete_ind.append(idx)
    if len(delete_ind) > 0:
        print('Note: There are %d features with a variance smaller than 1e-16.' % len(delete_ind))
        print('Please double check your input data if this number is not what you expect...')
        data = np.delete(data, delete_ind, axis=1)
        train_mean = np.delete(train_mean, delete_ind, axis=0)
        train_var = np.delete(train_var, delete_ind, axis=0)
    # print(data.shape, train_mean.shape, train_var.shape)
    scaled_dat = np.divide((data.T - train_mean), np.sqrt(train_var), ).T
    return (scaled_dat)


def load_normalization_data(name):
    train_mean_x = list()
    path_to_file = resource_filename(Requirement.parse("molSimplify"),
                                     "molSimplify/tf_nn/" + '/rescaling_data/' + name + '_mean_x.csv')
    if os.path.isfile(path_to_file):
        with open(path_to_file, 'r') as f:
            for lines in f.readlines():
                train_mean_x.append([float(lines.strip().strip('[]'))])

        train_var_x = list()
        path_to_file = resource_filename(Requirement.parse("molSimplify"),
                                         "molSimplify/tf_nn/" + '/rescaling_data/' + name + '_var_x.csv')
        with open(path_to_file, 'r') as f:
            for lines in f.readlines():
                train_var_x.append([float(lines.strip().strip('[]'))])

        train_mean_y = list()
        path_to_file = resource_filename(Requirement.parse("molSimplify"),
                                         "molSimplify/tf_nn/" + '/rescaling_data/' + name + '_mean_y.csv')
        with open(path_to_file, 'r') as f:
            for lines in f.readlines():
                train_mean_y.append([float(lines.strip().strip('[]'))])
        train_var_y = list()
        path_to_file = resource_filename(Requirement.parse("molSimplify"),
                                         "molSimplify/tf_nn/" + '/rescaling_data/' + name + '_var_y.csv')
        with open(path_to_file, 'r') as f:
            for lines in f.readlines():
                train_var_y.append([float(lines.strip().strip('[]'))])
    else:
        print('---Mean and Variance information do not exist. Calculate from training data...---')
        train_mean_x, train_mean_y, train_var_x, train_var_y = get_data_mean_std(predictor=name)
    train_mean_x = np.array(train_mean_x)
    train_var_x = np.array(train_var_x)
    train_mean_y = np.array(train_mean_y)
    train_var_y = np.array(train_var_y)

    return train_mean_x, train_mean_y, train_var_x, train_var_y


def get_data_mean_std(predictor):
    if predictor in ['ls_ii', 'hs_ii', 'ls_iii', 'hs_iii']:
        key = 'geos/' + predictor + '_bl_x'
    elif predictor in ['homo', 'gap']:
        key = 'homolumo/' + predictor + '_train_x'
    elif predictor in ['oxo', 'hat']:
        key = 'oxocatalysis/' + predictor + '_train_x'
    elif predictor == "split":
        key = predictor + '/' + predictor + '_x_41_OHE'
    elif predictor in ['geo_static_clf', 'sc_static_clf']:
        key = 'static_clf/' + predictor + '_train_x'
    else:
        key = predictor + '/' + predictor + '_x_OHE'
    path_to_feature_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.csv')
    df_feature = pd.read_csv(path_to_feature_file)
    train_mean_x, train_var_x = list(), list()
    for col in df_feature:
        train_mean_x.append([np.mean(np.array(df_feature[col]))])
        train_var_x.append([np.var(np.array(df_feature[col]))])
    ### labels
    if predictor in ['ls_ii', 'hs_ii', 'ls_iii', 'hs_iii']:
        key = 'geos/' + predictor + '_bl_y'
    elif predictor in ['homo', 'gap']:
        key = 'homolumo/' + predictor + '_train_y'
    elif predictor in ['oxo', 'hat']:
        key = 'oxocatalysis/' + predictor + '_train_y'
    elif predictor == "split":
        key = predictor + '/' + predictor + '_y_41_OHE'
    elif predictor in ['geo_static_clf', 'sc_static_clf']:
        key = 'static_clf/' + predictor + '_train_y'
    else:
        key = predictor + '/' + predictor + '_y_OHE'
    path_to_label_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.csv')
    df_label = pd.read_csv(path_to_label_file)
    train_mean_y, train_var_y = list(), list()
    for col in df_label:
        train_mean_y.append([np.mean(np.array(df_label[col]))])
        train_var_y.append([np.var(np.array(df_label[col]))])
    return train_mean_x, train_mean_y, train_var_x, train_var_y


def load_ANN_variables(predictor, suffix='vars'):
    key = get_key(predictor, suffix)
    path_to_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.csv')
    names = []
    with open(path_to_file, 'r') as f:
        for lines in f.readlines():
            names.append(lines.strip())
    return names


def load_training_data(predictor):
    if predictor in ['ls_ii', 'hs_ii', 'ls_iii', 'hs_iii']:
        key = 'geos/' + predictor + '_bl_x'
    elif predictor in ['homo', 'gap']:
        key = 'homolumo/' + predictor + '_train_x'
    elif predictor in ['oxo', 'hat']:
        key = 'oxocatalysis/' + predictor + '_train_x'
    elif predictor == "split":
        key = predictor + '/' + predictor + '_x_41_OHE'
    elif predictor in ['geo_static_clf', 'sc_static_clf']:
        key = predictor + '/' + predictor + '_train_x'
    else:
        key = predictor + '/' + predictor + '_x_OHE'
    path_to_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.csv')
    with open(path_to_file, "r") as f:
        csv_lines = list(csv.reader(f))
        # row_names = [row[0] for row in csv_lines]
        mat = [row for row in csv_lines[1:]]
    return mat


def load_test_data(predictor):
    if predictor in ['ls_ii', 'hs_ii', 'ls_iii', 'hs_iii']:
        key = 'geos/' + predictor + '_bl_x'  # Note, this test data is not available, will return train.
    elif predictor in ['homo', 'gap']:
        key = 'homolumo/' + predictor + '_test_x'
    elif predictor in ['oxo', 'hat']:
        key = 'oxocatalysis/' + predictor + '_test_x'
    elif predictor == "split":
        key = predictor + '/' + predictor + '_x_41_OHE'  # Note, this test data is not available, will return train
    elif predictor in ['geo_static_clf', 'sc_static_clf']:
        key = predictor + '/' + predictor + '_test_x'
    else:
        key = predictor + '/' + predictor + '_x_OHE'
    path_to_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.csv')
    with open(path_to_file, "r") as f:
        csv_lines = list(csv.reader(f))
        # row_names = [row[0] for row in csv_lines]
        mat = [row for row in csv_lines[1:]]
    return mat


def load_training_labels(predictor):
    if predictor in ['ls_ii', 'hs_ii', 'ls_iii', 'hs_iii']:
        key = 'geos/' + predictor + '_bl_y'
    elif predictor in ['homo', 'gap']:
        key = 'homolumo/' + predictor + '_train_y'
    elif predictor in ['oxo', 'hat']:
        key = 'oxocatalysis/' + predictor + '_train_y'
    elif predictor == "split":
        key = predictor + '/' + predictor + '_y_41_OHE'
    elif predictor in ['geo_static_clf', 'sc_static_clf']:
        key = predictor + '/' + predictor + '_train_y'
    else:
        key = predictor + '/' + predictor + '_y_OHE'
    path_to_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.csv')
    with open(path_to_file, "r") as f:
        csv_lines = list(csv.reader(f))
        # row_names = [row[0] for row in csv_lines]
        mat = [row for row in csv_lines[1:]]
    return mat


def load_test_labels(predictor):
    if predictor in ['ls_ii', 'hs_ii', 'ls_iii', 'hs_iii']:
        key = 'geos/' + predictor + '_bl_y'
    elif predictor in ['homo', 'gap']:
        key = 'homolumo/' + predictor + '_test_y'
    elif predictor in ['oxo', 'hat']:
        key = 'oxocatalysis/' + predictor + '_test_y'
    elif predictor == "split":
        key = predictor + '/' + predictor + '_y_41_OHE'
    elif predictor in ['geo_static_clf', 'sc_static_clf']:
        key = predictor + '/' + predictor + '_test_y'
    else:
        key = predictor + '/' + predictor + '_y_OHE'
    path_to_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.csv')
    with open(path_to_file, "rU") as f:
        csv_lines = list(csv.reader(f))
        # row_names = [row[0] for row in csv_lines]
        mat = [row for row in csv_lines[1:]]
    return mat


def load_train_info(predictor, suffix='info'):
    key = get_key(predictor, suffix)
    path_to_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.json')
    json_file = open(path_to_file, 'r')
    loaded_info_dict = json.loads(json_file.read())
    json_file.close()
    return loaded_info_dict


def load_keras_ann(predictor, suffix='model'):
    ## this function loads the ANN for property
    ## "predcitor" 
    # disable TF output text to reduce console spam
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    key = get_key(predictor, suffix)
    # print('THIS IS THE KEY',key)
    if not "clf" in predictor:
        path_to_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.json')
        json_file = open(path_to_file, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into  model
        path_to_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.h5')
        loaded_model.load_weights(path_to_file)
    if "clf" in predictor:
        path_to_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.h5')
        loaded_model = load_model(path_to_file)
    # complile model
    if predictor == 'homo':
        loaded_model.compile(loss="mse", optimizer=Adam(beta_2=1 - 0.0016204733101599046, beta_1=0.8718839135783554,
                                                        decay=7.770243145972892e-05, lr=0.0004961686075897741),
                             metrics=['mse', 'mae', 'mape'])
    elif predictor == 'gap':
        loaded_model.compile(loss="mse", optimizer=Adam(beta_2=1 - 0.00010929248596488832, beta_1=0.8406735969305784,
                                                        decay=0.00011224350434148253, lr=0.0006759924688701965),
                             metrics=['mse', 'mae', 'mape'])
    elif predictor in ['oxo', 'hat']:
        loaded_model.compile(loss="mse", optimizer=Adam(beta_2=0.9637165412871632, beta_1=0.7560951483268549,
                                                        decay=0.0006651401379502965, lr=0.0007727366541920176),
                             metrics=['mse', 'mae', 'mape'])
    elif predictor in ['geo_static_clf', 'sc_static_clf']:
        loaded_model.compile(loss='binary_crossentropy',
                             optimizer=Adam(lr=0.00005,
                                            beta_1=0.95,
                                            decay=0.0001,
                                            amsgrad=True),
                             metrics=['accuracy'])
    else:
        loaded_model.compile(loss="mse", optimizer='adam',
                             metrics=['mse', 'mae', 'mape'])
    # print("Keras/tf model loaded for " + str(predictor) + " from disk")
    return (loaded_model)


def tf_ANN_excitation_prepare(predictor, descriptors, descriptor_names):
    ## this function reforms the provided list of descriptors and their
    ## names to match the expectations of the target ANN model.
    ## it does NOT perfrom standardization

    ## get variable names
    target_names = load_ANN_variables(predictor)
    if len(target_names) > str(len(descriptors)):
        print(
                'Error: preparing features for ' + str(predictor) + ', recieved ' + str(
            len(descriptors)) + ' descriptors')
        print('model requires ' + str(len(target_names)) + ' descriptors, attempting match')
    excitation = []
    valid = True
    for var_name in target_names:

        try:
            excitation.append(descriptors[descriptor_names.index(var_name)])
        except:
            print('looking for  ' + str(var_name))
            print('Error! variable  ' + str(var_name) + ' not found!')
            valid = False
            break
    excitation = np.array(excitation)
    # print('SHAPE IN EXCITATION PREPARE', excitation.shape)
    excitation = np.reshape(excitation, (1, len(target_names)))
    return excitation


def ANN_supervisor(predictor, descriptors, descriptor_names, debug=False):
    print('ANN activated for ' + str(predictor))
    # _start = time.time()

    ## form the excitation in the corrrect order/variables
    excitation = tf_ANN_excitation_prepare(predictor, descriptors, descriptor_names)
    if debug:
        print('excitation is ' + str(excitation.shape))
        print('fetching non-dimensionalization data... ')
    train_mean_x, train_mean_y, train_var_x, train_var_y = load_normalization_data(predictor)
    if debug:
        print('rescaling input excitation...')

    excitation = data_normalize(excitation, train_mean_x, train_var_x)

    ## fetch ANN
    # print('This is the predictor......',predictor)
    loaded_model = load_keras_ann(predictor)
    result = data_rescale(loaded_model.predict(excitation), train_mean_y, train_var_y)
    if not "clf" in predictor:
        if debug:
            print('LOADED MODEL HAS ' + str(
                len(loaded_model.layers)) + ' layers, so latent space measure will be from first ' + str(
                len(loaded_model.layers) - 1) + ' layers')
        get_outputs = K.function([loaded_model.layers[0].input, K.learning_phase()],
                                 [loaded_model.layers[len(loaded_model.layers) - 2].output])
        latent_space_vector = get_outputs([excitation, 0])  # Using test phase.
        if debug:
            print('calling ANN model...')
    else:
        latent_space_vector = find_clf_lse(predictor, excitation, loaded_model=loaded_model, ensemble=False,
                                           modelname=False)
    # print("Finished in %f s" % (time.time() - _start))
    return result, latent_space_vector


def find_true_min_eu_dist(predictor, descriptors, descriptor_names):
    # returns scaled euclidean distance to nearest trainning 
    # vector in desciptor space
    train_mean_x, train_mean_y, train_var_x, train_var_y = load_normalization_data(predictor)

    ## form the excitation in the corrrect order/variables
    excitation = tf_ANN_excitation_prepare(predictor, descriptors, descriptor_names)
    excitation = excitation.astype(float)  # ensure that the excitation is a float, and not strings
    scaled_excitation = data_normalize(excitation, train_mean_x, train_var_x)  # normalize the excitation
    ## getting train matrix info
    mat = load_training_data(predictor)
    train_mat = np.array(mat, dtype='float64')
    ## loop over rows
    min_dist = 100000000
    min_ind = 0
    for i, rows in enumerate(train_mat):
        scaled_row = np.squeeze(
            data_normalize(rows, train_mean_x.T, train_var_x.T))  # Normalizing the row before finding the distance
        this_dist = np.linalg.norm(np.subtract(scaled_row, np.array(scaled_excitation)))
        if this_dist < min_dist:
            min_dist = this_dist
            min_ind = i
            # best_row = rownames[i]
            min_row = rows

    # flatten min row
    min_row = np.reshape(min_row, excitation.shape)
    print('min dist EU is ' + str(min_dist))
    if predictor in ['oxo', 'hat', 'homo', 'gap']:
        if predictor in ['homo', 'gap']:
            key = 'homolumo/' + predictor + '_train_names'
        elif predictor in ['oxo', 'hat']:
            key = 'oxocatalysis/' + predictor + '_train_names'
        path_to_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.csv')
        with open(path_to_file, "r") as f:
            csv_lines = list(csv.reader(f))
            print('Closest Euc Dist Structure:  ' + str(csv_lines[min_ind]).strip('[]') + ' for predictor ' + str(
                predictor))
    # need to get normalized distances 

    ########################################################################################
    # Changed by Aditya on 08/13/2018. Previously, nearest neighbor was being found in the #
    # unnormalized space, and then that was normalized. This was resulting in bad nearest  #
    # neighbor candidate structures. Now routine normalizes before finding the distance.   #
    ########################################################################################

    # train_mean_x,train_mean_y,train_var_x,train_var_y = load_normalization_data(predictor)

    # scaled_excitation = data_normalize(excitation,train_mean_x,train_var_x)
    # scaled_row = data_normalize(min_row,train_mean_x,train_var_x)
    # min_dist = np.linalg.norm(np.subtract(scaled_row,(scaled_excitation)))
    return (min_dist)


def find_ANN_latent_dist(predictor, latent_space_vector, debug=False):
    # returns scaled euclidean distance to nearest trainning 
    # vector in desciptor space
    train_mean_x, train_mean_y, train_var_x, train_var_y = load_normalization_data(predictor)

    ## getting train matrix info
    mat = load_training_data(predictor)
    train_mat = np.array(mat, dtype='float64')
    ## loop over rows
    min_dist = 100000000
    min_ind = 0

    loaded_model = load_keras_ann(predictor)
    if debug:
        print('measuring latent distances:')
        print('loaded model has  ' + str(
            len(loaded_model.layers)) + ' layers, so latent space measure will be from first ' + str(
            len(loaded_model.layers) - 1) + ' layers')
    get_outputs = K.function([loaded_model.layers[0].input, K.learning_phase()],
                             [loaded_model.layers[len(loaded_model.layers) - 2].output])
    for i, rows in enumerate(train_mat):
        # print('row',rows)
        scaled_row = np.squeeze(
            data_normalize(rows, train_mean_x.T, train_var_x.T))  # Normalizing the row before finding the distance
        # print('scaled_row',scaled_row)
        latent_train_row = get_outputs([np.array([scaled_row]), 0])
        # print('LATENT TRAIN ROW', latent_train_row)
        this_dist = np.linalg.norm(np.subtract(np.squeeze(latent_train_row), np.squeeze(latent_space_vector)))
        # print(this_dist)
        if this_dist < min_dist:
            min_dist = this_dist
            min_ind = i
            # best_row = rownames[i]
            min_row = rows

    # flatten min row
    if debug:
        print('min dist is ' + str(min_dist) + ' at  ' + str(min_ind))
    if predictor in ['oxo', 'hat', 'homo', 'gap']:
        if predictor in ['homo', 'gap']:
            key = 'homolumo/' + predictor + '_train_names'
        elif predictor in ['oxo', 'hat']:
            key = 'oxocatalysis/' + predictor + '_train_names'
        path_to_file = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key + '.csv')
        with open(path_to_file, "r") as f:
            csv_lines = list(csv.reader(f))
            print('Closest Latent Dist Structure: ' + str(csv_lines[min_ind]) + ' for predictor ' + str(predictor))
    return (min_dist)


def find_clf_lse(predictor, excitation, loaded_model, ensemble=False, modelname=False):
    if modelname == False:
        modelname = "spectro"
        if predictor == "geo_static_clf":
            avrg_latent_dist = 33.21736244173539
        elif predictor == "sc_static_clf":
            avrg_latent_dist = 38.276809428032685
        else:
            print("Unknown model type")
            return -1
    key = get_key(predictor, suffix='')
    base_path = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key)
    train_mean_x, train_mean_y, train_var_x, train_var_y = load_normalization_data(predictor)
    fmat_train = load_training_data(predictor)
    labels_train = np.array(load_training_labels(predictor), dtype='int')
    fmat_train = np.array(fmat_train, dtype='float64')
    fmat_train = data_normalize(fmat_train, train_mean_x, train_var_x)
    fmat_train = np.array(fmat_train)
    if not ensemble:
        # model = base_path + 'model.h5'
        # loaded_model = load_model(model)
        train_latent = get_layer_outputs(loaded_model, -4, fmat_train, training_flag=False)
        test_latent = get_layer_outputs(loaded_model, -4, excitation, training_flag=False)
        nn_latent_dist_test, nn_dists, nn_labels = dist_neighbor(test_latent, train_latent, labels_train,
                                                                 l=5, dist_ref=avrg_latent_dist)
        lse = get_entropy(nn_dists, nn_labels)
    else:
        print("Using ensemble averaged LSE.")
        base_path = base_path + 'ensemble_%s/' % modelname
        model_list = sorted(glob.glob(base_path + '/*.h5'))
        if len(model_list) != 10:
            print(key)
            print(base_path)
            print(model_list)
            print("Error: LSE cannot be calculated with modelname %s--The number of models is wrong." % modelname)
            return -1
        fmat_train = np.array_split(fmat_train, 10, axis=0)
        labels_train = np.array_split(labels_train, 10, axis=0)
        entropies_list = []
        for model in model_list:
            print(model)
            loaded_model = load_model(model)
            model_idx = int(model.split("/")[-1].split(".")[0].split("_")[-1])
            _fmat_train = array_stack(fmat_train, model_idx)
            _labels_train = array_stack(labels_train, model_idx)
            train_latent = get_layer_outputs(loaded_model, -4, _fmat_train, training_flag=False)
            test_latent = get_layer_outputs(loaded_model, -4, excitation, training_flag=False)
            nn_latent_dist_train, _, __ = dist_neighbor(train_latent, train_latent, _labels_train,
                                                        l=5, dist_ref=1)
            avrg_latent_dist = np.mean(nn_latent_dist_train)
            nn_latent_dist_test, nn_dists, nn_labels = dist_neighbor(test_latent, train_latent, _labels_train,
                                                                     l=5, dist_ref=avrg_latent_dist)
            entropies = get_entropy(nn_dists, nn_labels)
            entropies_list.append(entropies)
        lse = np.mean(np.array(entropies_list), axis=0)
    return lse


def save_model(model, predictor, num=None, suffix=False):
    key = get_key(predictor, suffix)
    base_path = resource_filename(Requirement.parse("molSimplify"), "molSimplify/tf_nn/" + key)
    base_path = base_path + 'ensemble_models'
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    if not num == None:
        name = '%s/%s_%d' % (base_path, predictor, num)
    else:
        name = '%s/%s' % (base_path, predictor)
    # serialize model to JSON
    model_json = model.to_json()
    with open("%s.json" % name, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("%s.h5" % name)
    print("Saved model !%s! to disk" % name.split('/')[-1])
