#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 23:03:37 2018

@author: maximoskaliakatsos-papakostas
"""

# import numpy as np
import music21 as m21
import os
import MBL_music_processing_functions as mpf
import MBL_melody_features_functions as mff
import MBL_evolution as evo
import MP_file_export_functions as fef
import MBL_feature_blending_functions as fbl

# use examples of altdeut1 and han melodies
deut_file = 'melodies/deut3961.krn';
han_file = 'melodies/han0987.krn';
session_folder = 'deut3961_han0987/'
# evo constants
nGens = 100
nPop = 50

# vvvvv WE ACTUALLY NEED ALL THESE FOR EXTRACTING INTITIAL FEATURES vvvvv
# vvvvv TO FORM THE FINAL "BLENDED" TARGET FEATURES vvvvv
# parse pieces
ds = m21.converter.parse(deut_file)
hs = m21.converter.parse(han_file)

# put a piano instrument to both parents - this also needs to happen in evolution
for i in hs.recurse():
    if 'Instrument' in i.classes:
        i.activeSite.replace(i, m21.instrument.Piano())
for i in ds.recurse():
    if 'Instrument' in i.classes:
        i.activeSite.replace(i, m21.instrument.Piano())

# transpose
d_trans = mpf.neutral_transposition(ds)
h_trans = mpf.neutral_transposition(hs)

# fix lowest octave
d_fix = mpf.fix_lowest_octave(d_trans)
h_fix = mpf.fix_lowest_octave(h_trans)

# compute features
df = mff.get_features_of_stream(d_fix)
hf = mff.get_features_of_stream(h_fix)

# compute markov transitions
dm = mff.compute_melody_markov_transitions(d_fix)
hm = mff.compute_melody_markov_transitions(h_fix)

# make base folder based on names
base_name = 'results/'+session_folder

# first write inputs to midi
fef.write_stream_to_midi(ds, appendToPath=base_name, fileName='input1.mid')
fef.write_stream_to_midi(hs, appendToPath=base_name, fileName='input2.mid')

# open the log file
log_file = open(base_name + "Output.txt", "w")
# write the  feature titles
log_file.write('Feature names:' + str(mff.get_accepted_feature_labels()) + '\n')
# and features of each input melody
log_file.write('d features:' + str(df) + '\n')
log_file.write('h features:' + str(hf) + '\n')

# make markov target - which remains the same during all simulations
target_markov = ( dm + hm )/2.0
# all scenarios for deut into han
for i in range(4):
    print('deut into han: ', i)
    folder_name = base_name+'blends/'
    # check if folder exists, else make it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # make target features
    target_features = fbl.blend_single_feature(df, hf, i)
    evoSession = evo.EvoSession( deut_file, han_file, target_features, target_markov, nPop=nPop, nGen=nGens, print_gens=True )
    # write to midi files
    fef.write_stream_to_midi(evoSession.best_individual.stream, appendToPath=folder_name, fileName='one_d_into_h_'+str(i)+'.mid')
    # write to log file
    log_file.write('one_d_into_h_'+str(i)+' ================== \n')
    log_file.write('target features: ' + str(evoSession.target_features) + '\n')
    log_file.write('best features: ' + str(evoSession.best_individual.features) + '\n')
# all scenarios for han into deut
for i in range(4):
    print('han into deut: ', i)
    folder_name = base_name+'blends/'
    # check if folder exists, else make it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # make target features
    target_features = fbl.blend_single_feature(hf, df, i)
    evoSession = evo.EvoSession( deut_file, han_file, target_features, target_markov, nPop=nPop, nGen=nGens, print_gens=True )
    # write to midi files
    fef.write_stream_to_midi(evoSession.best_individual.stream, appendToPath=folder_name, fileName='one_h_into_d_'+str(i)+'.mid')
    # write to log file
    log_file.write('one_h_into_d_'+str(i)+' ================== \n')
    log_file.write('target features: ' + str(evoSession.target_features) + '\n')
    log_file.write('best features: ' + str(evoSession.best_individual.features) + '\n')
# close log file
log_file.close()