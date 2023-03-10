import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

#1. 데이터
x = np.array([1,2,3,4,5,6,7,8,9,10])    # (10, )
y = np.array(range(10))

# 실습: 넘파이 리스트 슬라이싱!! 7:3으로 잘라라!!!
# x_train = x[0:7]        # x[:7] x[:-3]
# x_test = x[7:10]        # x[7:] x[-3:]
# y_train = y[0:7]        # y[:7] y[:-3]
# y_test = y[7:10]        # y[7:] y[-3:]

# [검색] train과 test를 섞어서 7:3으로 만들어라.
# 힌트: 사이킷런
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=123)

print(x_train)
print(x_test)
print(y_train)
print(y_test)

'''
#2. 모델구성
model = Sequential()
model.add(Dense(10, input_dim=1))
model.add(Dense(28))
model.add(Dense(450))
model.add(Dense(65))
model.add(Dense(21))
model.add(Dense(1))     # output

#3. 컴파일, 훈련
model.compile(loss='mae', optimizer='adam')
model.fit(x_train, y_train, epochs=250, batch_size=25)

#4. 평가, 예측
loss = model.evaluate(x_test, y_test)
print('loss: ', loss)
result = model.predict([11])
print('11의 결과: ', result)


결과: 10.1

'''