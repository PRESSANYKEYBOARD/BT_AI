# 데스크탑에서 세팅하고 다시 복습용으로 생성했습니다. 블루스크린 나쁜 놈 ㅠㅠㅠ

# CPU: intel Core i7-8700 3.20Ghz (6C12T)
# GPU: Nvidia Geforce RTX2070 SUPER
# RAM: Samsung DDR4-3200 16GB x2 = 32GB
# SSD: ADATA 8200XP 1TB
# HDD: Western Digital 1TB 7200rpm

import numpy as np                                                                  # 넘파이를 임포트시키고 간단하게 np로 명시해준다.
import tensorflow as tf                                                             # 텐서플로를 임포트시키고 tf라고 명시
from tensorflow.keras.models import Sequential, Model, load_model                               # Sequential은 레이어에 순차적으로 연산
from tensorflow.keras.layers import Dense, Input, Dropout, Conv2D, Flatten, MaxPooling2D                                    # Dense는 완전 연결층을 구현하는 레이어 모델
from sklearn.model_selection import train_test_split                                # 사이킷런(scikit-learn)의 model_selection 패키지 안에 train_test_split 모듈을 활용하여 손쉽게 train set(학습 데이터 셋)과 test set(테스트 셋)을 분리할 수 있다.
from sklearn.metrics import mean_squared_error, r2_score                            # RMSE 함수는 아직 없어서 직접 만들어 사용. - 회귀 분석 모델 / 사이킷런에서도 rmse는 제공하지 않음. / MSE 함수 불러옴.
                                                                                    # MSE보다 이상치에 덜 민감하다. 이상치에 대한 민감도가 MSE보단 적고 MAE보단 크기 때문에 이상치를 적절히 잘 다룬다고 간주되는 경향이 있다고 한다.
from sklearn.datasets import load_boston                                            # sklearn에서 제공하는 load_boston 가져오기
from sklearn.preprocessing import MinMaxScaler, StandardScaler

path = './_save/'
# path = '.._save/'
# path = 'c:/study/_save/'                                                          # 셋 다 모두 동일함.

#1. 데이터
dataset= load_boston()
x = dataset.data                                                                    # 집에 대한 데이터
y = dataset.target                                                                  # 집 값

x_train, x_test, y_train, y_test = train_test_split(                                # 파라미터 (x와 y에 값을 대입) 
    x, y, train_size=0.7, random_state=123)                                         # 데이터셋에서 70%(x_train) # 데이터셋에서 30%(x_test) / 둘 중 하나만 명시해주면 된다. 
                                                                                    # test_size default=0.25
                                                                                    # shuffle=True 무작위 추출, False=순차적 추출 / default=True
                                                                                    # random_state로 잡아주면 그다음 데이터도 동일한 데이터로 들어감. 아무런 의미 없는 값을 넣어도 상관없다.

scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train) # (354, 13) (데이터 개수, 열)
# conv2D를 위해서 reshape: (354, 13, 1, 1) 흑백 이미지로 치환
x_test = scaler.transform(x_test) # (152, 13)

x_train = x_train.reshape(354, 13, 1, 1)
x_test = x_test.reshape(152, 13, 1, 1)

print(x_train.shape, x_test.shape)

'''
print(x)
print(x.shape) #(506,13)

print(y)
print(y.shape) #(506, )

print(dataset.feature_names)
# ['CRIM' 'ZN' 'INDUS' 'CHAS' 'NOX' 'RM' 'AGE' 'DIS' 'RAD' 'TAX' 'PTRATIO' 'B' 'LSTAT']

print(dataset.DESCR)                                                                # 데이터셋의 description 볼 수 있음.

'''

#2. 모델
model = Sequential()
model.add(Conv2D(128, (2,1), padding='same', activation='relu', input_shape=(13,1,1)))
# kernel_size: (1, 1) 의미 X, (2, 2) -> 이미지 사이즈 (13, 1) 컬러=흑백, 그러므로 (2,1) 사용
model.add(MaxPooling2D(pool_size=(2, 1)))
'''
맥스 풀링 default pool_size=(2,2)
(13*1) -> pool_size 조절 = (2,1)
'''
model.add(Conv2D(64, (2,1), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 1)))
model.add(Conv2D(32, (2,1), padding='same', activation='relu'))
model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(16, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1)) # 분류모델이 아니므로 끝이 softmax가 아니어도 됨
model.summary()
                                                                                    
'''
summray
node를 random하게 추출하여 훈련을 수행 -> 과적합 문제 해결
summary는 dropout된 node를 나누지 않음
predict 시에는 dropout 사용 X
Total params: 8,225
Trainable params: 8,225
Non-trainable params: 0

'''

#3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam',     
             metrics=['mae'])

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
es = EarlyStopping(monitor='val_loss', patience=20, mode='min',
                            #   restore_best_weights=False,
                              verbose=1, )

import datetime                                                                 # 데이터 타임 임포트해서 명시해준다.
date = datetime.datetime.now()                                                  # 현재 날짜와 시간이 date로 반환된다.

print(date)                                                                     # 2023-01-12 14:57:54.345489
print(type(date))                                                               # <class 'datetime.datetime'>
date = date.strftime("%m%d_%H%M")                                               # date를 str(문자형)으로 바꾼다.
                                                                                # 0112_1457
print(date)
print(type(date))                                                               # <class 'str'>

filepath = './_save/MCP/'
filename = '{epoch:04d}-{val_loss:.4f}.hdf5'                                    # -는 연산 -가 아니라 글자이다. str형이기 때문에...
                                                                                # 0037-0.0048.hdf5

mcp = ModelCheckpoint(monitor='val_loss', mode='auto', verbose=1,
                      save_best_only=True,
                    #   filepath=path + 'MCP/keras31_ModelCheckPoint3.hdf5')
                      filepath = filepath + 'k39_01' + date + '_' + filename
)
                                                                                       
model.fit(x_train, y_train, epochs=5000, batch_size=32,
          validation_split=0.2,
          callbacks=[es, mcp],
          verbose=1)                                                    # val_loss 즉, 검증할 때 손실값이 출력된다.
                                                                        # 기준을 잡을 때, val_loss로 기준을 잡는다.
                                                                        
model.save(path+'keras39_dropout01_save_model.h5')                      # 가중치 및 모델 세이브
                                                                    
#4. 평가, 예측
print("=============== 1. 기본 출력 ========================")
mse, mae = model.evaluate(x_test, y_test)
print('mse:', mse)

y_predict = model.predict(x_test)
print("y_test(원래값):", y_test)
r2 = r2_score(y_test, y_predict)
print("r2스코어:", r2)

"""
CPU
r2스코어: 0.147001593653438

GPU
r2스코어: 0.17117110134309232

cnn
r2스코어: 0.40929509992636937

"""

