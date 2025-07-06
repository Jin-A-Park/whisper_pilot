import os
import numpy as np
import librosa
import soundfile as sf

# 오디오 데이터에 노이즈를 추가하는 함수
def add_noise(data, noise_level=0.1):
  noise = np.random.randn(len(data))  # 정규 분포를 따르는 노이즈 생성
  augmented_data = data + noise_level * noise  # 데이터에 노이즈 추가
  augmented_data = np.clip(augmented_data, -1, 1)  # 값이 -1과 1 사이로 유지되도록 함
  return augmented_data

# 오디오의 시간을 늘리거나 줄이는 함수
def time_stretch(data, rate=0.8):
  return librosa.effects.time_stretch(data, rate)  # rate < 1.0은 늘림, > 1.0은 줄임

# 오디오의 피치를 변경하는 함수
def pitch_shift(data, sr, n_steps):
  return librosa.effects.pitch_shift(data, sr, n_steps)  # n_steps만큼 피치 이동

# 오디오의 볼륨을 조절하는 함수
def change_volume(data, volume_factor=0.5):
  return data * volume_factor  # 볼륨 조절

# 증강된 오디오 데이터를 저장하는 함수
def augment_and_save(file_path, sr, data, augmentation_function, augmentation_name):
  # 피치 변화 시 n_steps를 지정해야 하므로 조건문 사용
  if augmentation_name == 'pitch_shift':
    augmented_data = augmentation_function(data, sr, n_steps=4)
  else:
    # 볼륨 조절은 volume_factor가 필요하므로 별도 처리
    augmented_data = augmentation_function(data) if augmentation_function != change_volume else augmentation_function(data, volume_factor=0.5)
  new_file_path = file_path.replace('.mp3', f'_{augmentation_name}.mp3')  # 새 파일 경로 생성
  sf.write(new_file_path, augmented_data, sr)  # 파일 저장

# 지정된 폴더의 모든 WAV 파일에 대해 데이터 증강을 수행하는 함수
def process_folder(folder_path, target_sr=16000):
  for subdir, dirs, files in os.walk(folder_path):  # 모든 하위 디렉토리 순회
    for file in files:
      if file.endswith('.mp3'):  # .wav 파일인지 확인
        file_path = os.path.join(subdir, file)  # 파일의 전체 경로
        data, sr = librosa.load(file_path, sr=target_sr)  # 파일 로드 및 샘플링 레이트 설정
        '''
        # 적용할 데이터 증강 기법 목록
        augmentations = [
          (add_noise, 'noisy'),
          (time_stretch, 'stretch'),
          (pitch_shift, 'pitch_shift'),
          (change_volume, 'volume')
        ]
        
        # 각 증강 기법을 순회하며 적용
        for augmentation_function, augmentation_name in augmentations:
          augment_and_save(file_path, sr, data, augmentation_function, augmentation_name)
        '''
        augment_and_save(file_path, sr, data, add_noise, 'noisy')

# 데이터셋의 경로 - 실제 경로로 변경 필요
dataset_path = './kor_sample'
process_folder(dataset_path)  # 함수 호출