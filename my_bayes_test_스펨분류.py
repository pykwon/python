from test1.my_bayes import MyBayesianFilter 

bf = MyBayesianFilter()
# 텍스트 학습 -----
bf.fit("파격 세일 - 오늘까지만 30% 할인", "광고")
bf.fit("쿠폰 선물 & 무료 배송", "광고")
bf.fit("신세계 백화점 세일", "광고")
bf.fit("찾아온 따뜻한 신제품 소식", "광고")
bf.fit("인기 제품 기간 한정 세일", "광고")
bf.fit("오늘 일정 확인", "중요")
bf.fit("프로젝트 진행 상황 보고", "중요")
bf.fit("계약 잘 부탁드립니다", "중요")
bf.fit("회의 일정이 등록되었습니다.", "중요")
bf.fit("오늘 일정이 없습니다.", "중요")

# 예측 -----
pre, scorelist = bf.predict("재고 정리, 인기  세일")
print("결과 =", pre)
print(scorelist)
print()
pre, scorelist = bf.predict("한국인, 현재 제주, 전남, 광주, 흑산도, 홍도, 남해동부 먼 바다, \
                                    남해 서북 앞 바다와 먼 바다, 서해남부 앞 바다와 먼 바다에 태풍경보가 발령됐다")
print("결과 는 ", pre)
print(scorelist)