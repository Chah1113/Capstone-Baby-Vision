# 논문 성능 측정 가이드 (benchmark.py)

> **이 문서를 보는 사람에게**  
> Docker, 서버, 카메라 등 프로젝트의 다른 부분은 전혀 몰라도 됩니다.  
> `benchmark.py`는 **인터넷 연결도, 서버 실행도 필요 없이** 단독으로 돌아갑니다.  
> Python만 설치되어 있으면 충분합니다.

---

## 측정되는 지표

| 지표 | 설명 | 논문에서 쓰는 곳 |
|------|------|-----------------|
| **Precision** | 탐지한 것 중 실제로 맞은 비율 | 모델 성능 Table |
| **Recall** | 실제 객체 중 찾아낸 비율 | 모델 성능 Table |
| **mAP@0.5** | IoU 0.5 기준 평균 정밀도 | 모델 성능 Table |
| **mAP@0.5:0.95** | IoU 0.5~0.95 구간 평균 (COCO 표준) | 모델 성능 Table |
| **Inference time (ms)** | 이미지 1장 추론하는 데 걸리는 시간 | 실시간성 입증 |
| **FPS** | 초당 처리 가능한 프레임 수 | 실시간성 입증 |
| **전처리 / 후처리 시간 (ms)** | YOLO 내부 단계별 소요 시간 | 상세 분석 |

---

## 1단계 — Python 설치 확인

터미널(명령 프롬프트)을 열고 아래를 입력하세요.

```
python --version
```

`Python 3.10.x` 또는 `3.11.x` 같이 나오면 OK입니다.  
아무것도 안 나오거나 오류가 뜨면 https://www.python.org/downloads/ 에서 Python 3.11을 설치하세요.

> **터미널 여는 법 (Windows)**  
> `Win + R` → `cmd` 입력 → 엔터

---

## 2단계 — 프로젝트 폴더로 이동

```
cd 경로\Capstone-Baby-Vision\vision
```

예시:
```
cd C:\Users\홍길동\Desktop\Capstone-Baby-Vision\vision
```

이동 후 아래 명령어로 파일 목록을 확인하세요.

```
dir
```

`benchmark.py`, `requirements.txt`, `weights` 폴더가 보이면 OK입니다.

---

## 3단계 — 필요한 패키지 설치

아래 명령어 한 줄로 설치됩니다. (처음 한 번만 하면 됩니다)

```
pip install ultralytics numpy pyyaml
```

> 설치 중 빨간 오류가 나도 마지막 줄에 `Successfully installed` 가 있으면 괜찮습니다.

---

## 4단계 — 파일 구조 확인

실행 전에 아래 구조대로 파일이 있는지 확인하세요.

```
vision/
├── benchmark.py         ← 실행할 스크립트
├── weights/
│   └── best.pt          ← 학습된 모델 파일 (이미 있음)
└── test_images/         ← 테스트 이미지 폴더 (직접 만들어야 함, 아래 설명 참고)
```

### test_images 폴더 만드는 법

1. `vision` 폴더 안에 `test_images` 라는 폴더를 새로 만드세요.
2. 테스트에 쓸 이미지(jpg, png 아무거나)를 그 안에 넣으세요.  
   → 많을수록 결과가 정확합니다. 최소 30장, 권장 100장 이상.

> **이미지가 없다면?**  
> 데이터셋 담당 팀원에게 validation 이미지를 요청하거나,  
> 학습 때 쓴 데이터셋에서 `valid/images` 폴더를 받아서 사용하세요.

---

## 5단계 — 실행

### 경우 A: 이미지 폴더만 있을 때 (속도 지표만 측정)

```
python benchmark.py --model weights/best.pt --images test_images/
```

### 경우 B: data.yaml도 있을 때 (mAP + 속도 전부 측정)

```
python benchmark.py --model weights/best.pt --data data.yaml --images test_images/
```

> **data.yaml이 뭔가요?**  
> 학습 때 사용한 데이터셋 설정 파일입니다. 있으면 Precision/Recall/mAP까지 측정 가능하고,  
> 없으면 속도(Inference time, FPS)만 측정됩니다. 속도만으로도 논문 실시간성 입증에 충분합니다.

### 옵션 상세 설명

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--model` | (필수) | 모델 파일 경로. `weights/best.pt` 그대로 쓰면 됩니다. |
| `--data` | 없음 | data.yaml 경로. 없으면 생략. |
| `--images` | 없음 | 테스트 이미지 폴더. |
| `--conf` | `0.5` | 탐지 신뢰도 임계값. 바꾸지 않아도 됩니다. |
| `--imgsz` | `640` | 입력 이미지 크기. 바꾸지 않아도 됩니다. |
| `--n` | `100` | 속도 측정에 쓸 이미지 수. 이미지가 100장 미만이면 자동으로 줄어듭니다. |
| `--out` | `results` | 결과 저장 폴더 이름. |

---

## 6단계 — 출력 확인

실행이 끝나면 터미널에 이렇게 출력됩니다:

```
============================================================
  EyeCatch AI — YOLOv8 Benchmark
  Model : weights/best.pt
  conf=0.5  imgsz=640  n=100
============================================================

[1/2] Model Quality — yolo val
────────────────────────────────────────────────────────────
┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│    Class     │  Precision   │    Recall    │   mAP@0.5    │ mAP@0.5:0.95 │
├──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│     all      │    0.920     │    0.880     │    0.910     │    0.720     │
│     baby     │    0.930     │    0.890     │    0.920     │    0.740     │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘

[2/2] Runtime Speed — 100 images
────────────────────────────────────────────────────────────
  측정 대상: 100장
  Preprocess :    1.2 ms  (±0.1)
  Inference  :   12.3 ms  (±0.8)
  Postprocess:    0.8 ms  (±0.1)
  ─────────────────────────────
  Total      :   14.3 ms  (±0.9)
  FPS        :   69.9

Saved → results/benchmark_results.json
Saved → results/benchmark_results.csv

완료.
```

---

## 7단계 — 결과 파일 읽기

실행 후 `vision/results/` 폴더가 생기고 두 파일이 저장됩니다.

### benchmark_results.csv (엑셀로 열기)

엑셀이나 구글 시트에서 바로 열 수 있습니다.  
논문 Table에 넣을 숫자가 여기 정리되어 있습니다.

### benchmark_results.json (메모장으로 열기)

```json
{
  "model": "weights/best.pt",
  "timestamp": "2026-04-17T15:30:00",
  "val_metrics": {
    "all":  { "precision": 0.92, "recall": 0.88, "mAP50": 0.91, "mAP50_95": 0.72 },
    "baby": { "precision": 0.93, "recall": 0.89, "mAP50": 0.92, "mAP50_95": 0.74 }
  },
  "speed_ms": {
    "inference_mean": 12.3,
    "fps": 69.9,
    ...
  }
}
```

---

## 자주 묻는 문제

### Q. `ModuleNotFoundError: No module named 'ultralytics'` 가 뜬다

3단계 설치 명령어를 다시 실행하세요.

```
pip install ultralytics numpy pyyaml
```

### Q. `python` 명령어가 안 먹힌다

`python` 대신 `python3` 을 써보세요.

```
python3 benchmark.py --model weights/best.pt --images test_images/
```

### Q. `FileNotFoundError: weights/best.pt` 가 뜬다

현재 위치가 `vision/` 폴더인지 확인하세요. `cd` 명령어로 이동 후 다시 실행하세요.

### Q. 이미지가 30장밖에 없는데 `--n 100` 으로 해도 되나요?

네, 자동으로 있는 이미지 수만큼만 측정합니다.

### Q. GPU가 없는데 실행 가능한가요?

네, CPU로도 실행됩니다. 다만 추론 시간이 GPU 환경보다 길게 나옵니다.  
논문에 CPU/GPU 환경을 명시해 주세요.

---

## 서버 주소 관련 참고 (무시해도 됩니다)

프로젝트 다른 파일(`main_vision.py`)에는 Docker 내부 서버 주소(`http://api:8000`, `mediamtx`)가 하드코딩되어 있습니다.  
**`benchmark.py`는 서버와 전혀 통신하지 않으므로** 이 주소들을 바꿀 필요가 없습니다.  
Docker나 서버를 실행하지 않아도 벤치마크는 정상 동작합니다.
