# -*- coding: utf-8 -*-
"""1_1_numpy_tensorflow_pytorch.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UQ8U7KTT9WKWdaZT4hiRS6IeD_UesJgp

# 1_1_numpy_tensorflow_pytorch.ipynb
구글 코랩을 이용한 코드 작성 첫번째 파일  
PyTorch 설치전 : 런타임 메뉴 > 런타임 유형 변경 > GPU 지정  
PyTorch 철치 (매 세션마다 설치 필요)  
*주피터 노트북의 설치는 !pip3 로 시작*
"""

!pip3 install torch
!pip3 install torchvision

"""# Framework Comparsion (패키지 비교)

* Numpy vs Tensorflow vs Pytorch
* output = x * y + z

"""

import numpy as np
from datetime import datetime

start = datetime.now()

np.random.seed(0) # 랜덤값 발생 고정시킴

N, D = 3, 4

x = np.random.randn(N, D) # 3행 4열 배열에 0 ~ 1 사이의 랜덤값 채움
y = np.random.randn(N, D)
z = np.random.randn(N, D)

a = x * y
b = a + z
c = np.sum(b)

grad_c = 1.0
grad_b = grad_c * np.ones((N, D))
grad_a = grad_b.copy()
grad_z = grad_b.copy()
grad_y = grad_a * y
grad_x = grad_a * y

print(grad_x)
print(grad_y)
print(grad_z)

print('연산 처리 시간 : ', datetime.now() - start)

# import tensorflow as tf
import numpy as np
from datetime import datetime

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

"""# tf.placeholder() 함수 AttributeError 발생 시 해결 방법  
tensorflow 2.0 에서는 사용 못 함  
```(python)
import tensorflow.compat.v1 as tf  
tf.disable_v2_behavior()
```

"""

start_tf = datetime.now()

# 실행 동작을 미리 정의해 놓음
with tf.device('/gpu:0'):    # 실행시 gpu 0 사용을 지정
  x = tf.placeholder(tf.float32)  # 나중에 값을 넣을 공간을 만듦
  y = tf.placeholder(tf.float32)
  z = tf.placeholder(tf.float32)

  a = x * y
  b = a + z
  c = tf.reduce_sum(b)

grad_x, grad_y, grad_z = tf.gradients(c, [x, y, z])

# 준비된 공간에 값을 채우는 설정
with tf.Session() as sess:
  values = {
      x: np.random.rand(N, D),
      y: np.random.rand(N, D),
      z: np.random.rand(N, D)
  }
  out = sess.run([c, grad_x, grad_y, grad_z], feed_dict=values)
  c_val, grad_x_val, grad_y_val, grad_z_val = out

print(grad_x_val)
print(grad_y_val)
print(grad_z_val)

print('연산 처리 시간 : ', datetime.now() - start_tf)

import torch
from torch.autograd import Variable
from datetime import datetime

start = datetime.now()

N, D = 3, 4 # 생략 가능 : 위쪽 셀에서의 선언을 그대로 사용해도 됨

# 자동 미분 계산 클래스 : autograd.Variable
x = Variable(torch.randn(N, D).cuda(), requires_grad=True)
y = Variable(torch.randn(N, D).cuda(), requires_grad=True)
z = Variable(torch.randn(N, D).cuda(), requires_grad=True)

a = x * y
b = a + z
c = torch.sum(b)

# gradient(경사도) 자동 계산 수행
# 기울기(gradient)가 1.0 이라고 가정하고 최종 값인 c 에서
# backward를 통해서 역전파를 해 줌
# c.backward(gradient=torch.cuda.FloatTensor([1.0]))  # GPU 버전
c.backward(gradient=torch.tensor(1, dtype=torch.float))  # CPU 버전

print(x.grad)
print(y.grad)
print(z.grad)

print('연산 처리 시간 : ', datetime.now() - start)