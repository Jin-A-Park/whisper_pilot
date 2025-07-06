# whisper 성능평가
### 배경 information

참고: https://github.com/hyeonsangjeon/computing-Korean-STT-error-rates

1. WER(word error rate): 단어 오류율 (얼마나 많은 단어를 틀렸는지)
2. CER(character error rate): 낱말 오류율 (얼마나 많은 문자를 틀렸는지)

<p>
<img width="70%" alt="Image" src="https://github.com/user-attachments/assets/46527ea4-f8a5-4ab1-b2b2-9fa4322d0d08" />
</p>

- S : 대체 오류, 철자가 틀린 외자(uniliteral)/단어(word) 횟수
- D : 삭제 오류, 외자/단어의 누락 횟수
- I : 삽입 오류, 잘못된 외자/단어가 포함된 횟수
- C : Ground truth와 hypothesis 간 올바른 외자/단어(기호)의 합계, (N - D - S)
- N : 참조의(Ground truth) 외자/단어 수
- insertion이 증가할 수록 오류율이 0~1 범위를 넘어서기 때문에 cer같은 경우 정규화 필수(ER_normalized)

### 분석 모델

- base 이상의 사이즈 모델은 모바일 환경에 접목하기에 무리. 간단한 성능차이 확인을 위해 우선 미디움 레벨 모델까지 비교. 추후 필요 시 large size 모델 성능 평가 예정.

### 데이터 수집 과정

- sample audio file 위치: ./kor_sample
- sample audio label(정답 텍스트) 위치: ./kor_sample_label
- 수집 과정:
    - 온라인 TTS 사이트로 텍스트 변환 + librosa 패키지로 노이즈 데이터 증강

### 노이즈 계수

noise_aug.py > add_noise() > noise_level

참고 블로그: https://ks-jun.tistory.com/187

디폴트: 0.005 → 0.1

### 실행 예시
```python
whisper_performance_analysis % python main.py --audio_path kor_sample/kor_zoom_noisy.mp3 --label_path kor_sample_label/kor_zoom.txt --language Korean --model tiny
```


