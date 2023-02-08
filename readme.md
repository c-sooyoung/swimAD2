# swimAD2

2022년 중급물리실험 2를 수강하면서 Analog Discovery 2를 조작하기 위해 만들었던 간단한 파이썬 함수들을 모아놓았다.

## 처음 시작한다면
Digilent Waveforms 설치 [링크](https://digilent.com/shop/software/digilent-waveforms/download) **&rightarrow; 반드시 SDK 포함해서 설치하기**

먼저 Waveforms를 설치한 후에, [`example.ipynb`](https://github.com/c-sooyoung/swimAD2/blob/main/example.ipynb) 파일을 보면 간단한 신호 발생 후 측정하는 예시가 있다.


## 함수 소개
[`swimAD2.py`](https://github.com/c-sooyoung/swimAD2/blob/main/swimAD2.py)에는 AD2의 Wavegen과 Oscilloscope의 기초적인 조작만 할 수 있는 함수들만 있다. (학기 말에 가서야 Waveforms SDK가 조금이나마 익숙해지기 시작해서ㅠㅠ)

### AD2 연결
#### `connect(number=0)` &rightarrow; `c_int` (`hdwf`)  
n번째 (기본값 0) 연결된 digilent 기기(기기번호/handle &rightarrow; `hdwf`)를 가져온다. 변수 자체는 `c_int` 형태이고, 이후 wavegen과 oscilloscope를 이용할 때 넣어주면 된다. 

#### `disconnect()`  
모든 기기와의 연결을 끊는다. 예를 들어 AD2를 한 쥬피터 노트북에 연결해서 쓰다가, Waveforms 앱을 직접 사용하거나 다른 파일을 통해 조작하기 위해서는 먼저 현재 연결을 끊어줘야 한다.

### Wavegen 조작
#### `config_wavegen(hdwf, frequency, amplitude, signal_shape=dwfc.funcSine, offset=0, phase=0, symmetry=50, channel=0)`
Wavegen에서 발생할 신호를 설정한다.  
기기번호 `hdwf`, 주파수 `frequency`, 진폭 `amplitude`는 반드시 직접 설정해주어야 한다. 나머지 변수는 설정하지 않으면 위의 기본값이 들어간다.  
`hdwf`: 기기번호  
`frequency`: 주파수 (단위 Hz), 최대 10 MHz  
`amplitude`: 진폭 (단위 V), 최대 5 V  
`signal_shape`: 기본값 사인함수 (`swimAD2.dwfc.funcSine`) 외에 `funcSquare`, `funcTriangle` 등 다른 함수 모양은 [SDK 레퍼런스](https://digilent.com/reference/software/waveforms/waveforms-sdk/reference-manual) 참고.  
`offset`: 신호의 DC offset. DC + 진폭 < max 5 V. 순수 DC 신호는 진폭을 0으로 하고 offset 값을 설정해서 얻을 수 있지만, stabilization time이 조금 필요하다.  
`phase`: 신호의 시작 위상. (단위 &deg;)  
`symmetry`: 설명하기 애매함... Waveforms로 직접 보면 편함.   
`channel`: Wavegen channel 번호. AD2에는 channel이 0, 1이 있고, 두 개를 동시에 설정하고 싶으면 -1로 설정.

#### `start_wavegen(hdwf, channel)`
Wavegen에서 신호 발생 시작. 뒤에 `stop_wavegen()`이나 `reset_wavegen()`이 나타날 때까지 신호가 발생된다.

#### `stop_wavegen(hdwf, channel)`, `reset_wavegen(hdwf, channel)`
각각 신호 정지, Wavegen 설정 초기화.

### Oscilloscope 조작
#### `config_oscilloscope`
#### `measure_oscilloscope`


## Waveforms SDK에 대한 간단한 소개