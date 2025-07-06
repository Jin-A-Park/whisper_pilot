import whisper
import sys
import argparse
import time

#오류 계산용 패키지
import nlptutti as metrics

def transcribe_korean_audio(model_type: str, audio_path: str, language: str):
  start = time.time()
  model = whisper.load_model(model_type)
  result = model.transcribe(audio_path, language=language)
  end = time.time()
  print(f"인식된 텍스트:\n{result['text']}\n응답시간: {end-start}\n")
  return result["text"]
  
def cer(ref_path: str, preds: str):
  with open(ref_path, "r") as file:
    refs = file.read()
  result = metrics.get_cer(refs, preds)
  cer = result['cer']
  substitutions = result['substitutions']
  deletions = result['deletions']
  insertions = result['insertions']
  
  return cer
  
  
def wer(ref_path: str, preds: str):
  with open(ref_path, "r") as file:
    refs = file.read()
  result = metrics.get_wer(refs, preds)
  wer = result['wer']
  substitutions = result['substitutions']
  deletions = result['deletions']
  insertions = result['insertions']
  
  return wer


def main(args):
  audio_path = args.audio_path
  label_path = args.label_path
  model_type = args.model
  language = args.language
  preds = transcribe_korean_audio(model_type, audio_path, language)
  cer_value = cer(label_path, preds)
  wer_value = wer(label_path, preds)
  print(f"CER: {cer_value}, WER: {wer_value}\n")
#ex) whisper_performance_analysis % python main.py --audio_path kor_sample/kor_zoom_noisy.mp3 --label_path kor_sample_label/kor_zoom.txt --language Korean --model tiny

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Default Main.py for Whisper AI Performance Testing')
  parser.add_argument('--audio_path', type=str, default='kor_sample/kor_click.mp3', 
                      help='audio file path')
  parser.add_argument('--label_path', type=str, default='kor_sample_label/kor_click.txt', 
                      help='audio file\'s label path')
  parser.add_argument('--model', type=str, default='base', 
                      choices=['tiny', 'base', 'small', 'medium'], 
                      help='Select a WhisperAI Model')
  parser.add_argument('--language', type=str, default='ko', 
                      help='Select a Language for faster processing')
  args = parser.parse_args()
  main(args)