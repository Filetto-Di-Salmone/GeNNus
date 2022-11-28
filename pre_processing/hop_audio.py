import torch
from torch.utils.data import Dataset

import torchaudio
import torchaudio.transforms

import sys, os

from pprint import pprint

from tqdm import tqdm

import json

import numpy as np

import matplotlib.pylab as plt
import seaborn as sns

import librosa
import librosa.display

import pandas as pd

from pathlib import Path

import argparse

# "audio_hop" --> take one sample ever hop_length elements
def resample_audio(og_audio_list, hop_length: int):
  
  resampled_audio_tensor_list = []
  
  for audio in tqdm(og_audio_list, colour="green"):
    
    resampled_waveform = torchaudio.functional.resample(
        audio["waveform"], 
        # as per Torch Audio docs, this is the way of performing "hopping" in a 
        # similar way as the Mel Spectrogram transform does
        orig_freq=hop_length, new_freq=1
      )
    
    resampled_audio_tensor_list.append(
      {
        "waveform": resampled_waveform.numpy(), 
        "og_sample_rate": audio["og_sample_rate"],
        "hop_length": hop_length,
        "label_one_hot": audio["label_one_hot"].numpy(),
        "label": audio["label"]
      }
    )
    
  return resampled_audio_tensor_list


# code taken from: https://stackoverflow.com/a/47626762

class NumpyEncoder(json.JSONEncoder):
  
  def default(self, obj):
    
    if isinstance(obj, np.ndarray):
      return obj.tolist()
    
    return json.JSONEncoder.default(self, obj)

def export_pre_processed_data(
  pre_processed_data, export_path: str, export_name: str
):
  
  with open(f"{export_path}/{export_name}", "w") as final:
    json.dump(pre_processed_data, final, cls=NumpyEncoder)
    
    
def load_dataset_from_disk(dataset_path: str, data_type: str):
  f = open(dataset_path)

  pre_processed_data_from_disk = json.load(f)
  
  for i in tqdm(range(len(pre_processed_data_from_disk)), colour="blue"):
    
    pre_processed_data_from_disk[i][data_type] = torch.tensor(
      pre_processed_data_from_disk[i][data_type]
    )
  
  return pre_processed_data_from_disk
    


DATASET_SIZE = "extra_small"
DATASET_NAME = f"fma_{DATASET_SIZE}_organized_by_label_resampled_rechanneled"
DATASET_FOLDER = "./data/"

dataset_path = DATASET_FOLDER + DATASET_NAME

og_audio_list = load_dataset_from_disk(
  dataset_path=dataset_path,
  data_type="waveform"
)

hop_length = 24

hopped_audio_list = resample_audio(og_audio_list, hop_length)

export_pre_processed_data(
  hopped_audio_list, 
  DATASET_FOLDER, 
  f"{DATASET_NAME}_hop_length_{hop_length}.json"
)