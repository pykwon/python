from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.datasets import load_iris
plt.rc('font', family='malgun gothic')

# iris data로 차원축소 연습 ---------
# 사이킷런의 iris data 중에서 10개의 표본을 선택하여 꽃받침 길이와 꽃받침 폭 데이터를 그래프로 출력 
# 첫 번째 그래프는 가로축을 특성의 종류, 세로축을 특성의 값으로 나타낸 것이다. 
# 이 그림에서 꽃받침 길이가 크면 꽃받침 폭도 같이 커진다는 규칙을 알 수 있다.
iris = load_iris()
n = 10  # 10송이만 선택
X = iris.data[:n, :2]  # 꽃받침 길이와 꽃받침 폭만 선택
print(X)
print('차원축소 전 X : ', X)

plt.plot(X.T, 'o:')
plt.xticks(range(4), ["꽃받침 길이", "꽃받침 폭"])
plt.xlim(-0.5, 2)
plt.ylim(2.5, 6)
plt.title("붓꽃 크기 특성")
plt.legend(["표본 {}".format(i + 1) for i in range(n)])
plt.show()

# 두 번째 그래프는 가로축을 꽃받침 길이, 세로축을 꽃받침 폭으로 하는 플롯으로 나타낸 것이다. 
# 데이터를 나타내는 점들이 양의 기울기를 가지기 때문에 꽃받침 길이가 크면 꽃받침 폭도 같이 커진다는 규칙을 알 수 있다.
ax = sns.scatterplot(0, 1, data=pd.DataFrame(X), s=100, color=".2", marker="s")
for i in range(n):
    ax.text(X[i, 0] - 0.05, X[i, 1] + 0.03, "표본 {}".format(i + 1))
plt.xlabel("꽃받침 길이")
plt.ylabel("꽃받침 폭")
plt.title("붓꽃 크기 특성 (2차원 표시)")
plt.axis("equal")
plt.show()
 
# 사이킷런의 PCA 기능
# decomposition 패키지는 PCA 분석을 위한 PCA 클래스를 제공
# 입력 인수: n_components : 정수
# 메서드:
#   fit_transform() : 특징행렬을 낮은 차원의 근사행렬로 변환
#   inverse_transform() : 변환된 근사행렬을 원래의 차원으로 복귀
# 속성:
#   mean_ : 평균 벡터
#   components_ : 주성분 벡터
    
# 아래 코드는 붓꽃 데이터를 1차원으로 차원축소하는 코드다.
# fit_transform() 메서드로 구한 X_low는 1차원 근사 데이터의 집합이다. 
# 이 값을 inverse_transform() 메서드에 넣어서 구한 X2는 다시 2차원으로 복귀한 근사 데이터의 집합이다.

pca1 = PCA(n_components=1)
X_low = pca1.fit_transform(X)
print('X_low : ', X_low) # fit_transform() 메서드로 구한 X_low는 1차원 근사 데이터의 집합이다. 

X2 = pca1.inverse_transform(X_low) # 이 값을  inverse_transform() 메서드에 넣어서 구한 X2는 다시 2차원으로 복귀한 근사 데이터의 집합이다.
print('차원축소 후 X2 : ', X2)
print(X_low[7])
print(X2[7, :])

sns.scatterplot(0, 1, data=pd.DataFrame(X), s=100, color=".2", marker="s")

for i in range(n):
    d = 0.03 if X[i, 1] > X2[i, 1] else -0.04
    ax.text(X[i, 0] - 0.065, X[i, 1] + d, "표본 {}".format(i + 1))
    plt.plot([X[i, 0], X2[i, 0]], [X[i, 1], X2[i, 1]], "k--")

plt.plot(X2[:, 0], X2[:, 1], "o-", color='b', markersize=10)
plt.plot(X[:, 0].mean(), X[:, 1].mean(), markersize=10, marker="D")
plt.axvline(X[:, 0].mean(), c='r')
plt.axhline(X[:, 1].mean(), c='r')
plt.xlabel("꽃받침 길이")
plt.ylabel("꽃받침 폭")
plt.title("Iris data의 1차원 차원축소")
plt.show()