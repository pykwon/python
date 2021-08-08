# 연관규칙분석
# 연관성 분석은 흔히 장바구니 분석 또는 서열 분석이라고도 함
# 기업의 데이터베이스에서 상품의 구매, 서비스 등 일련의 거래 또는 사건들 간의 규칙을 발견하기 위해 적용
# 장바구니 분석 : 장바구니에 무엇이 같이 들어 있는지에 대한 분석
# 
# 연관규칙의 측도
# 산업의 특성에 따라 지지도, 신뢰도, 향상도 값을 잘 보고 규칙을 선택
# 지지도 : 
#   전체 거래 중 항목 A와 항목 B를 동시에 포함하는 거래의 비율
#   지지도 = A와 B가 동시에 포함된 거래수/전체 거래수
# 신뢰도 : 
#   항목 A를 포함하는 거래 중에서 항목 A와 항목 B가 같이 포함될 확률
#   연관성의 정도
#   신뢰도 = A,B가 동시에 포함된 거래수/A를 포함하는 거래수
# 향상도 : 
#   A가 구매되지 않았을 때 품목 B의 구매확률에 비해 A가 구매됐을 때 품목 B의 구매확률의 증가 비
#   연관규칙 A->B는 품목 A와 품목 B의 구매가 서로 관련이 없는 경우에 향상도가 1이 됨
#   향상도 = A,B동시구매/A구매*B구매

# 연관분석 : 지지도, 신뢰도 향상도 : https://it-license.tistory.com/29

# 참조 페이지  https://m.blog.naver.com/eqfq1/221444712369
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori #pip install mlxtent
#일단 필요한 패키지 로드
 
dataset=[['사과','치즈','생수'],
    ['생수','호두','치즈','고등어'],
    ['수박','사과','생수'],
    ['생수','호두','치즈','옥수수']]
 
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_) #위에서 나온걸 보기 좋게 데이터프레임으로 변경
print(df)
# 여기가 좀 어려운데 가나다 순으로 Column값을 생성해서(고등어,사과,생수,수박,옥수수,치즈,호두) 
# 첫번쨰 (사과,치즈.생수) 데이터에 고등어가 표시되어이있므면 True값으로 없으면 False값으로 표시한다. 
# 다음 사과도 첫번쨰 데이터에 사과가 있으면 1값으로 없으면 0값으로 표시한다. 이러한 것을 반복하면 4X7행렬이 생성된다. 

# 지지도를 0.5로 놓고  apriori를 돌려보면 아래와 같이 결과가 출력된다.
frequent_itemsets = apriori(df, min_support=0.5, use_colnames=True)
print(frequent_itemsets) 

#예를 들어 설명하면 사과를 살 확률은 0.5(데이터셋 4개 중에 2개가 사과가 포함되어있다),(치즈,생수)를 같이 살 확률은 0.75인 것 이다.
#(연관분석에 지지도, 신뢰도,항상도,확신도 찾아보면 된다.)
from mlxtend.frequent_patterns import association_rules
print(association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3))


print("-----------------------------------------------------------------")
# 참조 페이지  https://zephyrus1111.tistory.com/119
import matplotlib.pyplot as plt
import matplotlib.colors as mcl
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
store_df = pd.read_csv('store_data.csv', header=None)
#Python에서는 mlxtend 라이브러리를 이용하여 연관 규칙 분석을 수행할 수 있다. 먼저 빈발 품목 집합을 구해보자. 
#우선 각 행에 대해서 품목을 리스트로 만들어주고 이를 다시 리스트로 모아줘야 한다. 즉, 리스트의 리스트를 만들어줘야 한다.
print(store_df.head(2))

records = []
for i in range(len(store_df)):
    records.append([str(store_df.values[i,j]) \
        for j in range(len(store_df.columns)) if not pd.isna(store_df.values[i,j])])
print(records)

te = TransactionEncoder()
te_ary = te.fit(records).transform(records, sparse=True)
te_df = pd.DataFrame.sparse.from_spmatrix(te_ary, columns=te.columns_)
print(te_df)

frequent_itemset = apriori(te_df,
                           min_support=0.005, 
                           max_len=3, 
                           use_colnames=True, 
                           verbose=1)
frequent_itemset['length'] = frequent_itemset['itemsets'].map(lambda x: len(x))
frequent_itemset.sort_values('support', ascending=False, inplace=True)
print(frequent_itemset)

print('--')
association_rules_df = association_rules(frequent_itemset, 
                                         metric='confidence', 
                                         min_threshold=0.005)
all_confidences = []
collective_strengths = []
cosine_similarities = []
for _,row in association_rules_df.iterrows():
    all_confidence_if = list(row['antecedents'])[0]
    all_confidence_then = list(row['consequents'])[0]
    if row['antecedent support'] <= row['consequent support']:
        all_confidence_if = list(row['consequents'])[0]
        all_confidence_then = list(row['antecedents'])[0]
    all_confidence = {all_confidence_if+' => '+all_confidence_then : \
                      row['support']/max(row['antecedent support'], row['consequent support'])}
    all_confidences.append(all_confidence)
    
    violation = row['antecedent support'] + row['consequent support'] - 2*row['support']
    ex_violation = 1-row['antecedent support']*row['consequent support'] - \
                    (1-row['antecedent support'])*(1-row['consequent support'])
    collective_strength = (1-violation)/(1-ex_violation)*(ex_violation/violation)
    collective_strengths.append(collective_strength)
    
    cosine_similarity = row['support']/np.sqrt(row['antecedent support']*row['consequent support'])
    cosine_similarities.append(cosine_similarity)
    
association_rules_df['all-confidence'] = all_confidences
association_rules_df['collective strength'] = collective_strengths
association_rules_df['cosine similarity'] = cosine_similarities
print(association_rules_df.head(3))

print()
max_i = 4
for i, row in association_rules_df.iterrows():
    print("Rule: " + list(row['antecedents'])[0] + " => " + list(row['consequents'])[0])
    print("Support: " + str(round(row['support'],2)))
    print("Confidence: " + str(round(row['confidence'],2)))
    print("Lift: " + str(round(row['lift'],2)))
    print("=====================================")
    if i==max_i:
        break

max_i = 4
for i, row in association_rules_df.iterrows():
    print("Rule: " + list(row['antecedents'])[0] + " => " + list(row['consequents'])[0])
    print("Support: " + str(round(row['support'],2)))
    print("Confidence: " + str(round(row['confidence'],2)))
    print("Lift: " + str(round(row['lift'],2)))
    print("=====================================")
    if i==max_i:
        break
    
support = association_rules_df['support']
confidence = association_rules_df['confidence']
 
h = 347
s = 1
v = 1
colors = [
    mcl.hsv_to_rgb((h/360, 0.2, v)),
    mcl.hsv_to_rgb((h/360, 0.55, v)),
    mcl.hsv_to_rgb((h/360, 1, v))
]
cmap = LinearSegmentedColormap.from_list('my_cmap', colors, gamma=2)
 
measures = ['lift', 'leverage', 'conviction', 
            'all-confidence', 'collective strength', 'cosine similarity']
 
fig = plt.figure(figsize=(10,7))
fig.set_facecolor('white')
for i, measure in enumerate(measures):
    ax = fig.add_subplot(320+i+1)
    if measure != 'all-confidence':
        scatter = ax.scatter(support, confidence, c=association_rules_df[measure],cmap=cmap)
    else:
        scatter = ax.scatter(support,confidence, \
                    c=association_rules_df['all-confidence'].map(lambda x: [v for k,v in x.items()][0]),cmap=cmap)
    ax.set_xlabel('support')
    ax.set_ylabel('confidence')
    ax.set_title(measure)
    fig.colorbar(scatter, ax=ax)
    
fig.subplots_adjust(wspace=0.2, hspace=0.5)
plt.show()

