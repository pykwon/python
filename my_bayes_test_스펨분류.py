from test1.my_bayes import MyBayesianFilter 

bfmodel = MyBayesianFilter()

# 학습
bfmodel.fit("파격 세일 - 오늘까지만 20% 할인", "광고")
bfmodel.fit("쿠폰 선물 & 무료 배송", "광고")
bfmodel.fit("신세계 백화점 세일", "광고")
bfmodel.fit("찾아온 따뜻한 신제품 소식", "광고")
bfmodel.fit("인기 제품 한정 세일", "광고")
bfmodel.fit("오늘 일정 확인", "중요")
bfmodel.fit("프로젝트 진행 상황 보고", "중요")
bfmodel.fit("처리가 순조롭게 잘 되었네요", "중요")
bfmodel.fit("회의 일정이 등록되었습니다.", "중요")
bfmodel.fit("오늘 일정이 없습니다.", "중요")
bfmodel.fit("지역별 프로젝트 진행 원활.", "중요")

# 예측 
pre, slist = bfmodel.predict("재고 정리, 인기  세일")
print("결과는 ", pre)
print(slist)
print()
pre, slist = bfmodel.predict("한국인, 현재 제주, 전남, 광주, 남해동부 먼 바다, \
                                    남해 서북 앞 바다와 먼 바다, 서해남부 먼 바다에 경보가 발령됐다")
print("결과는 ", pre)
print(slist)
