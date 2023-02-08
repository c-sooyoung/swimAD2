# swimAD2

2022년 중급물리실험 2를 수강하면서 Analog Discovery 2를 조작하기 위해 만들었던 간단한 파이썬 함수들을 모아놓았다.

## 처음 시작한다면
Digilent Waveforms 설치 [링크](https://digilent.com/shop/software/digilent-waveforms/download) **&rightarrow; 반드시 SDK 포함해서 설치하기**

먼저 Waveforms를 설치한 후에, [`example.ipynb`](https://github.com/c-sooyoung/swimAD2/blob/main/example.ipynb) 파일을 보면 간단한 신호 발생 후 측정하는 예시가 있다.


## 함수 소개
[`swimAD2.py`](https://github.com/c-sooyoung/swimAD2/blob/main/swimAD2.py)에는 AD2의 Wavegen과 Oscilloscope의 기초적인 조작만 할 수 있는 함수들만 있다. (학기 말에 가서야 Waveforms SDK가 조금이나마 익숙해지기 시작해서ㅠㅠ)

### AD2 연결
#### `connect`, `disconnect`
`connect(number=0)` &rightarrow; `c_int`  
n번째 (기본값 0) 연결된 digilent 기기(기기번호/handle)를 가져온다. 변수 자체는 `c_int` 형태이고, 이후 wavegen과 oscilloscope를 이용할 때 넣어주면 된다.  
<span style="color: gray;">원래는 반환값 없이 기기 한 개만 연결한 채로 나머지 모든 함수가 그 기기에 적용되는 방식이었다가, 동시에 기기 2개 이상을 조작해야 될 필요가 생겨서 기기번호를 불러오는 식으로 변경했다.</span>

`disconnect()`  
모든 기기의 연결을 지운다.

#### `config_wavegen`
#### `start_wavegen`
#### `stop_wavegen`, `reset_wavegen`

#### `config_oscilloscope`
#### `measure_oscilloscope`


## Waveforms SDK에 대한 간단한 소개