# 단일 입력 퍼셉트론 클래스
class Perceptron(object):
	def __init__(self, eta=0.01, iterations=10):
		"""
		퍼셉트론 초기화
		
		Parameters:
		eta: 학습률 (learning rate)
		iterations: 학습 반복 횟수
		"""
		self.lr = eta
		self.iterations = iterations
		self.w = 0.0  # 가중치 초기화
		self.bias = 0.0  # 편향 초기화


	def fit(self, X, Y):
		"""
		학습 데이터로 퍼셉트론 학습
		
		Parameters:
		X: 입력 데이터 리스트
		Y: 정답 레이블 리스트 (0.0 또는 1.0)
		"""
		self.errors = []  # 에폭마다 발생한 오류 수 저장

		# 지정된 횟수만큼 학습 반복
		for _ in range(self.iterations):
			error = 0
			# 각 학습 샘플에 대해
			for i in range(len(X)):
				x = X[i]
				y = Y[i]
				# 예측값과 실제값의 차이로 업데이트 값 계산
				update = self.lr * (y - self.predict(x))
				# 가중치와 편향 업데이트
				self.w += update * x
				self.bias += update
				# 예측이 틀린 경우 에러 카운트 증가
				error += int(update != 0.0)
			self.errors.append(error)


	def net_input(self, x):
		"""
		순입력(net input) 계산
		w*x + b
		"""
		return self.w * x + self.bias


	def predict(self, x):
		"""
		예측 함수
		순입력이 0보다 크면 1.0, 아니면 0.0 반환 (계단 활성화 함수)
		"""
		return 1.0 if self.net_input(x) > 0.0 else 0.0

# 학습 데이터: 양수는 1.0, 음수는 0.0으로 분류
x = [1, 2, 3, 10, 20, -2, -10, -100, -5, -20]
y = [1.0, 1.0, 1.0, 1.0, 1.0,  0.0, 0.0, 0.0, 0.0, 0.0]

# 모델 생성 및 학습
model = Perceptron(0.01, 10)
model.fit(x, y)

# 테스트 데이터로 예측
test_x = [30, 40, -20, -60]
for i in range(len(test_x)):
	print('input {} => predict: {}'.format(test_x[i], model.predict(test_x[i])))

# 학습된 가중치와 편향 출력
print(model.w)
print(model.bias)