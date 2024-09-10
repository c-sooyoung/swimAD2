# swimAD2

2022년 중급물리실험 2를 수강하면서 Analog Discovery 2를 조작하기 위해 만들었던 간단한 파이썬 함수들을 모아놓았다.
내가 쓰기 편하게 만든 함수들이라서 전혀 체계적이지 않고 AD2의 기능 중 담지 못한 것이 엄청나게 많다.
반면 기능이 빠진 만큼 AD2를 아예 처음 조작하는 것이 막막하지 않고 단순하게, 친절하게 다가올 수 있도록 만들려고 노력했다.

> [!NOTE]
> **swimAD2가 도움이 되었다면:**
> - swimAD2를 바탕으로 실험을 한 예시들을 모으려고 합니다. 본인이 **공유하고 싶은 실험이나 코드**가 있다면, [experiments 폴더](./experiments/)에 pull request를 넣거나, 제게 이메일(c.sooyoung.me@스누메일)로 보내주세요.
> - swimAD2을 **개선하거나 기능을 새로 추가**한 것이 있다면, pull request를 넣거나 이메일을 보내주시면 정말 감사하겠습니다!
> - 마지막으로, 여기 github 링크(github.com/c-sooyoung/swimAD2)를 표시하고 공유하는 것도 큰 도움이 됩니다. 🙂


## 처음 시작한다면
Digilent Waveforms 설치 [링크](https://digilent.com/shop/software/digilent-waveforms/download) **&rightarrow; 반드시 SDK 포함해서 설치하기**

먼저 Waveforms를 설치한 후에 [`example.ipynb`](https://github.com/c-sooyoung/swimAD2/blob/main/example.ipynb) 파일을 보면 간단한 신호 발생 후 측정하는 예시가 있다.

혹시 C가 익숙하다면, [SDK 레퍼런스](https://digilent.com/reference/software/waveforms/waveforms-sdk/reference-manual)를 직접 보는 것을 추천한다.

체계적이고 완성도 있는 것을 원한다면, [pydwf](https://pypi.org/project/pydwf/) 패키지가 있다. [pydwf 레퍼런스](https://pydwf.readthedocs.io/en/latest/pydwf_api/pydwf_overview.html)

**제대로 작동하지 않는 경우 &rarr; [troubleshooting.md](troubleshooting.md) 문서 참조**


## 함수 소개
[`swimAD2.py`](https://github.com/c-sooyoung/swimAD2/blob/main/swimAD2.py)에는 AD2의 Wavegen과 Oscilloscope의 기초적인 조작만 할 수 있는 함수들만 있다. (학기 말에 가서야 Waveforms SDK가 조금이나마 익숙해지기 시작해서ㅠㅠ)

### AD2 연결
#### `connect(number=0)` &rightarrow; `c_int` (`hdwf`)  
n번째 연결된 digilent 기기(`hdwf`)를 가져온다. 변수 자체는 `c_int` 형태이고, 이후 wavegen과 oscilloscope를 이용할 때 넣어주면 된다.  
(테크니컬하게는... 메모리에서 기기 핸들의 주소를 가져오는 것이다)

#### `disconnect()`  
모든 기기와의 연결을 끊는다. 예를 들어 AD2를 한 쥬피터 노트북에 연결해서 쓰다가, Waveforms 앱을 직접 사용하거나 다른 파일을 통해 조작하기 위해서는 먼저 현재 연결을 끊어줘야 한다.

### Wavegen 조작
#### `config_wavegen(hdwf, frequency, amplitude, signal_shape=dwfc.funcSine, offset=0, phase=0, symmetry=50, channel=0)`
기기번호 `hdwf`, 주파수 `frequency`, 진폭 `amplitude`는 반드시 직접 설정해주어야 한다. 나머지 변수는 설정하지 않으면 위의 기본값이 들어간다.  
`hdwf`: 기기  
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
#### `config_oscilloscope(hdwf, range0, range1, sample_rate, sample_size=8192)`
`hdwf`: 기기  
`range0`, `range1`: 각각 Oscilloscope channel 0, 1의 범위. (단위 V)  
범위는 최대 25 V이긴 하지만, 실제 AD2 Oscilloscope의 측정 간격은 High-gain(~0.3mV)과 Low-gain(~3mV) 둘 중 하나로 고정된다. 대충 1 V 이상이면 Low-gain으로 가는듯..?  
`sample_rate`: 측정 속도 (단위 Hz), 최대 100 MHz.  
`sample_size`: 측정 횟수, 최대 8192.

#### `measure_oscilloscope(hdwf)` &rightarrow; `t, v0, v1`
`config_oscilloscope()`에서 설정한대로 측정을 시작한다. `sample_size`가 모두 차면, `t`, `v0`, `v1` 각각 `numpy` 행렬로 반환한다.  
`t`는 엄밀하게는 측정된 시간이 아니라, `sample_rate`와 `sample_size`를 바탕으로 계산된 값이다.


## Waveforms SDK에 대해서
Waveforms SDK는 기본적으로 Digilent 기기들을 조작하는 C 라이브러리이다. 파이썬에서는 이 라이브러리를 `ctypes` 모듈을 통해서 사용하고, 따라서 SDK 함수들은 입출력을 C 변수형을 기본으로 한다.

Waveforms를 설치하면 SDK 폴더에 이를 이용하는 C와 파이썬 예시파일들이 있고, Digilent에서 배포한 [파이썬 데모 패키지](https://github.com/Digilent/WaveForms-SDK-Getting-Started-PY/blob/master/WF_SDK/device.py)도 있다.

`swimAD2`의 함수들은 SDK의 DwfAnalogIn과 DwfAnalogOut의 가장 기초적인 함수들 몇 가지를 묶어서 내가 쓰기 편하게 만든 것이다.
특히 C 자료형을 건드릴 필요가 없게끔 최대한 파이썬 자료형으로 번역해 놓았다.
한편 AD2로 가능하지만, swimAD2에는 없는 기능이 훨씬 더 많다. DwfAnalogOut에서의 커스텀 신호 발생, DwfAnalogIn에서 지속 측정 (8192개를 넘어서 continuous logging이 되는듯..?) DwfAnalogIO의 DC 컨트롤, DwfDigital 쪽의 모든 기능들... 등등 더 하고 싶은 것이 있으면, SDK에서 직접 꺼내 쓸 수 있을 것이다.

C를 알고, 특히 C에서의 자료형과 포인터가 익숙하면 [SDK 레퍼런스](https://digilent.com/reference/software/waveforms/waveforms-sdk/reference-manual)를 읽고 직접 조작해서 새로운 기능을 추가하는 것이 어렵지 않을 것이다.


## 기타 자료

[AD2 Specifications](https://digilent.com/reference/test-and-measurement/analog-discovery-2/specifications)

[SDK 레퍼런스](https://digilent.com/reference/software/waveforms/waveforms-sdk/reference-manual)

Digilent Github에 있는 [파이썬 데모 패키지](https://github.com/Digilent/WaveForms-SDK-Getting-Started-PY/blob/master/WF_SDK/device.py)


---

Special thanks:  
2022년 조원 현수, 하진, 이선