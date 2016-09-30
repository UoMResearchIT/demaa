#!/usr/bin/env python

'''
	Pupil dilation arousal module
	Run: python3 arousal.py ./test.csv
'''

import sys
import json
import pandas as pd
import math
import seaborn as sns
from collections import Counter
pd.options.mode.chained_assignment = None  # default='warn'

#import subprocess
def readPupilData(filename):
	pupil_data =  pd.read_csv(filename)
	pupil_data = pupil_data.drop_duplicates()
	pupil_data = pupil_data[pupil_data['DataQualityValue']=='>70%']
	pupil_data_AOI = pupil_data.filter(regex=("AOI.*"))
	pupil_data = pupil_data.loc[:,['ParticipantName','DataQualityValue','GenderValue','RecordingTimestamp','GazeEventType', 'PupilLeft', 'PupilRight','ValidityLeft','ValidityRight']]
	pupil_data = pd.concat([pupil_data, pupil_data_AOI], axis = 1)

	return pupil_data

def fill_aoi(pupil_data):
    pupil_data['AOI'] = 0
    all_aois = pupil_data.filter(regex=("AOI.*")).columns
    start = 'AOI'
    end = 'Hit'
    prev_aoi = 0
    aoi = 0
    for aoi_column in all_aois:
        aoi = aoi_column[aoi_column.find(start)+len(start):aoi_column.rfind(end)]
        if aoi == 0 and prev_aoi != 0:
            aoi = prev_aoi
        if aoi == 'A':
            aoi = 'I '
        elif aoi == 'B':
            aoi = 'II '
        elif aoi == 'C':
            aoi = 'III '
        elif aoi == 'D':
            aoi = 'aVR '
        elif aoi == 'E':
            aoi = 'aVL '
        elif aoi == 'F':
            aoi = 'aVF '
        elif aoi == 'G':
            aoi = 'V1 '
        elif aoi == 'H':
            aoi = 'V2 '
        elif aoi == 'I':
            aoi = 'V3 '
        elif aoi == 'J':
            aoi = 'V4 '
        elif aoi == 'K':
            aoi = 'V5 '
        elif aoi == 'L':
            aoi = 'V6 '
        elif aoi == 'M':
            aoi = 'RSII '
        elif aoi == 'N':
            aoi = 'RSV1 '
        elif aoi == 'O':
            aoi = 'RS V5'
        elif aoi == 'XRS':
            aoi = 'RS'

        pupil_data.loc[pupil_data[aoi_column] == 1, 'AOI'] = aoi
        if aoi != 0:
            prev_aoi = aoi
        aoi = 0
    return pupil_data

## Data Cleansing

# Interpolation - to replace missing or NaN values in left and right pupil
def interpolate(pupil_data):
    #convert to series
    sleft = pd.Series(pupil_data.PupilLeft)
    sright = pd.Series(pupil_data.PupilRight)
    #linear interpolation
    sleft = sleft.interpolate()
    sright = sright.interpolate()
    #convert back to dataframe
    dleft = pd.DataFrame(sleft)
    dright = pd.DataFrame(sright)
    #drop previous values of pupil
    pupil_data = pupil_data.drop('PupilLeft', 1)
    pupil_data = pupil_data.drop('PupilRight', 1)
    #append with new values after interpolation
    pupil_data = pd.concat([pupil_data, dleft, dright], axis = 1)
    pupil_data['PupilLeft'].fillna(pupil_data['PupilLeft'].mean(),inplace=True)
    pupil_data['PupilRight'].fillna(pupil_data['PupilRight'].mean(),inplace=True)
    return pupil_data

# Calibrate timestamp
def calibrate_timestamp(pupil_data):
	if len(pupil_data) > 0:
		start_time = min([element for element in pupil_data['RecordingTimestamp'] if element > 0])
		pupil_data['RecordingTimestamp'] = pupil_data['RecordingTimestamp'] - start_time
	return pupil_data

## Extract participant

#pupil data is a dataframe containing data
#participant is a string argument of the participant ID to be extracted.
def get_participant(pupil_data, participant):
    participant = pupil_data.loc[pupil_data.ParticipantName == participant]
    participant = participant.reset_index()
    return participant

## Moving Average OR Aggregated Average
def set_moving_average(pupil_data, window_size):
    pupil_data['left_window'] = 0
    pupil_data['right_window'] = 0
    for current_index in (pupil_data.index):
        offset = current_index+window_size
        if offset > len(pupil_data.index):
            offset = len(pupil_data.index)
    #left
        current_left_average = pupil_data['PupilLeft'].iloc[current_index : offset].mean()
        pupil_data['left_window'].iloc[current_index] = current_left_average
    #right
        current_right_average = pupil_data['PupilRight'].iloc[current_index : offset].mean()
        pupil_data['right_window'].iloc[current_index] = current_right_average
    return pupil_data

#pupil data is a dataframe containing data
#window size is a number representing the window size
def create_aggregated_average(pupil_data, window_size):
	pupil_data['left_window'] = 0
	pupil_data['right_window'] = 0
	aggregated_pupil_data = pd.DataFrame(columns=pupil_data.columns)
	temp_pupil_data = pd.DataFrame(columns=pupil_data.columns)

	for current_index in range(1, len(pupil_data)-1, window_size):
		temp_pupil_data = pupil_data.iloc[current_index:current_index+window_size-1]
		aggregated_pupil_data = aggregated_pupil_data.append(temp_pupil_data.iloc[0])
		data = Counter(temp_pupil_data['AOI'])
		aoi = data.most_common(1)
		aggregated_pupil_data['left_window'].iloc[len(aggregated_pupil_data)-1] = temp_pupil_data['PupilLeft'].mean()
		aggregated_pupil_data['right_window'].iloc[len(aggregated_pupil_data)-1] = temp_pupil_data['PupilRight'].mean()
		aggregated_pupil_data['AOI'].iloc[len(aggregated_pupil_data)-1] = aoi[0][0]
		aggregated_pupil_data = aggregated_pupil_data.reset_index(drop=True)

	return aggregated_pupil_data

## Get level of arousal
def convert_to_scale(pupil_data, levels):
    levels = levels - 1
    left_window_mean = pupil_data['left_window'].mean()
    right_window_mean = pupil_data['right_window'].mean()
    left_span = pupil_data['left_window'].max() - pupil_data['left_window'].min()
    right_span = pupil_data['right_window'].max() - pupil_data['right_window'].min()
    left_unit = left_span / levels
    right_unit = right_span / levels
    pupil_data['left_level'] = 0
    pupil_data['right_level'] = 0
    for current_index in pupil_data.index:
        pupil_data['left_level'].iloc[current_index] = ((pupil_data['left_window'].iloc[current_index] - left_window_mean) / left_unit).round()
        pupil_data['right_level'].iloc[current_index] = ((pupil_data['right_window'].iloc[current_index] - right_window_mean) / right_unit).round()
    return pupil_data

## Useful functions
def get_n_lowest_arousal(pupil_data, n, pupil):
    if pupil == 'r':
        column = 'right_level'
    else:
        column = 'left_level'
    pupil_data = pupil_data.sort_values(by=column)
    return pupil_data.head(n)

def get_n_highest_arousal(pupil_data, n, pupil):
    if pupil == 'r':
        column = 'right_level'
    else:
        column = 'left_level'
    pupil_data = pupil_data.sort_values(column)
    return pupil_data.tail(n)

def get_arousal_above_n(pupil_data, n, pupil):
    if pupil == 'r':
        column = 'right_level'
    else:
        column = 'left_level'
    pupil_data = pupil_data[pupil_data[column] > n]
    return pupil_data

def get_arousal_below_n(pupil_data, n, pupil):
    if pupil == 'r':
        column = 'right_level'
    else:
        column = 'left_level'
    pupil_data = pupil_data[pupil_data[column] < n]
    return pupil_data

def get_aoi_by_mean_arousal_level(pupil_data):
    aoi_by_mean_arousal = pd.DataFrame(columns = ('AOI', 'mean_left_level', 'mean_right_level', 'count'))
    aois = pupil_data['AOI'].unique()
    for aoi in aois:
        mean_left_level = pupil_data[pupil_data['AOI'] == aoi].left_level.mean()
        mean_right_level = pupil_data[pupil_data['AOI'] == aoi].right_level.mean()
        count = pupil_data[pupil_data['AOI'] == aoi].right_level.count()
        aoi_by_mean_arousal.loc[len(aoi_by_mean_arousal)] = [aoi, mean_left_level, mean_right_level, count]
    return aoi_by_mean_arousal

def get_last_x(pupil_data, x):
    new_pupil_data = pd.DataFrame(columns=pupil_data.columns)
    for participant in pupil_data['ParticipantName'].unique():
        new_pupil_data = new_pupil_data.append(pupil_data[pupil_data['ParticipantName']==participant].tail(x))
    return new_pupil_data

"""
def print_summary_per_participant(pupil_data, n, pupil):
    print (n, "lowest arousal datapoints on", pupil, "eye")
    print (get_n_lowest_arousal(pupil_data, n, pupil))
    print ("All datapoints below", n)
    print (get_arousal_above_n(pupil_data, n, pupil))
    print ("All datapoints above", n)
    print (get_arousal_below_n(pupil_data, n, pupil))
    print ("Mean arousal level, by aoi")
    print (get_aoi_by_mean_arousal_level(pupil_data))
    return

def evaluate_participant(pupil_data, n, pupil):
    print ('Evaluating participant ', pupil_data['ParticipantName'].iloc[0], pupil, 'eye')
    print (n, " lowest arousal datapoints")
    print (get_n_lowest_arousal(pupil_data, n, pupil))
    print ("All datapoints above level", n)
    print (get_arousal_above_n(pupil_data, n, pupil))
    print ("All datapoints below level", -n)
    print (get_arousal_below_n(pupil_data, -n, pupil))
    print ("Mean arousal level, by aoi")
    print (get_aoi_by_mean_arousal_level(pupil_data))
    pupil_data.plot(x='RecordingTimestamp',y='left_level')
    return
"""

## Probablistic algorithms
def get_Transition_Matrix(states_vector):
    minimum = (states_vector.min()* -1 ) + 1
    a = states_vector
    a += minimum
    array_size=len(a.unique())
    Tm = np.zeros((array_size,array_size))
    for (x,y), c in Counter(zip(a, a[1:])).iteritems():
        #print x, y
        Tm[x-1,y-1] = c
    return Tm

def convert_Transition_To_Probability_Matrix(Tm):
    Pr = Tm.copy()
    array_size= len(Pr)
    for x in range(0, (array_size)):
        row_sum = 0
        for y in range(0, (array_size)):
            row_sum = row_sum + Pr[x][y]
        Pr[x] = Pr[x] / row_sum
    return Pr

def evaluate_participant(participant_data, aggregate_size, levels, pupil, analysis_type, pupil_data):
	participants = participant_data
	single_participant = False

	if len(participants) == 1:
		single_participant = True

	n = levels

	if pupil == 'r':
		pupil_side = 'right_level'
	else:
		pupil_side = 'left_level'

	pupils = pd.DataFrame(columns=pupil_data.columns)

	for participant in participants:
		participant_data = get_participant(pupil_data, participant)

		if(analysis_type=='Aggregate'):
			participant_data = create_aggregated_average(participant_data, aggregate_size)
		elif(analysis_type=='Moving_average'):
			participant_data = set_moving_average(participant_data, aggregate_size)

		participant_data = convert_to_scale(participant_data, n)
		participant_data = calibrate_timestamp(participant_data)
		participant_data = participant_data.sort_values(by='RecordingTimestamp')
		participant_data = participant_data.reset_index()
		pupils = pupils.append(participant_data)

	for participant in participants:
		current_participant = pupils[pupils['ParticipantName']==participant]
		if single_participant:
			current_participant['index1'] = current_participant.index.tolist()
			current_participant['x_label'] = current_participant['AOI'].map(str) + current_participant['index1'].map(str)

	return {'participants':participants,
		'aggregate_size':aggregate_size,
		'levels':n,
		'pupil':pupil,
		'pupil_data':participant_data,
		'analysis_type':analysis_type}

"""

REQUIRED:
The process function passes the input file,
and it must return data as JSON.

"""

def process(input):
	all_participants = ['P2F','P10F','P13M','P18F','P19F','P20F','P21M','P23F','P24M','P26F','P32M',
	                'P37F','P38F','P40F','P41F','P5M','P6F','P9M','P11F','P16F','P25F','P27F','P28F',
	                'P29F','P30M','P31F','P33F','P34M','P36F','P39F','P42F']
	correct_participants = ['P5M','P6F','P9M','P11F','P16F','P25F','P27F','P28F','P29F',
	                        'P30M','P31F','P33F','P34M','P36F','P39F','P42F']
	incorrect_participants = ['P2F','P10F','P13M','P18F','P19F','P20F','P21M','P23F','P24M',
	                          'P26F','P32M','P37F','P38F','P40F','P41F']

	## Main
	pupil_data = readPupilData(input)
	pupil_data = fill_aoi(pupil_data)
	pupil_data = interpolate(pupil_data)

	## Evaluate participant
	participant = 'P2F'
	aggregate_size = 50
	levels = 15
	pupil = 'r'
	analysis_type = 'Aggregate'

	participant_data = get_participant(pupil_data, participant)
	participant_data = create_aggregated_average(participant_data, aggregate_size)
	participant_data = convert_to_scale(participant_data,levels)
	participant_data = calibrate_timestamp(participant_data)
	participant_data = participant_data.sort_values(by='RecordingTimestamp')
	participant_data = participant_data.reset_index()

	evalData = evaluate_participant(participant_data, aggregate_size, levels, pupil, analysis_type, pupil_data)
	print(evalData)

process(sys.argv[1])
