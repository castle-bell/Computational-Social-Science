#install.packages("tidyr")
#install.packages("dplyr")
#install.packages("reshape2")

library(tidyr)
library(dplyr)
library(reshape2)
library(lubridate)

getwd()
setwd("~/Desktop/계산사회과학/FinalProject/data_part1")

name_indoor_small <- c("넷플릭스.csv", "바둑.csv", "스팀게임.csv", "애니.csv", "인터넷 방송.csv")
name_indoor_large <- c("배드민턴.csv", "보드게임.csv", "클라이밍.csv", "탁구.csv", "헬스.csv")
name_outdoor_small <- c("여행.csv", "자전거타기.csv", "전시회.csv", "줄넘기.csv", "캠핑.csv")
name_outdoor_large <- c("놀이공원.csv", "술.csv", "야구.csv", "축구.csv", "축제.csv")

name_indoor <- c(name_indoor_large, name_indoor_small)
name_outdoor <- c(name_outdoor_large, name_outdoor_small)
name_small <- c(name_indoor_small, name_outdoor_small)
name_large <- c(name_indoor_large,  name_outdoor_large)

setwd("./Indoor_small")
indoor_small <- read.csv(name_indoor_small[1])

for(i in 2:5){
  temp = read.csv(name_indoor_small[i])
  indoor_small <- merge(indoor_small, temp, by="date")
}
names(indoor_small) = c("date", name_indoor_small)
indoor_small$date = myd(paste(indoor_small$date, '01'))
indoor_small = arrange(indoor_small, date)

setwd("../Indoor_large")
indoor_large <- read.csv(name_indoor_large[1])

for(i in 2:5){
  temp = read.csv(name_indoor_large[i])
  indoor_large <- merge(indoor_large, temp, by="date")
}
names(indoor_large) = c("date", name_indoor_large)
indoor_large$date = myd(paste(indoor_large$date, '01'))
indoor_large = arrange(indoor_large, date)

setwd("../Outdoor_small")
outdoor_small <- read.csv(name_outdoor_small[1])

for(i in 2:5){
  temp = read.csv(name_outdoor_small[i])
  outdoor_small <- merge(outdoor_small, temp, by="date")
}
names(outdoor_small) = c("date", name_outdoor_small)
outdoor_small$date = myd(paste(outdoor_small$date, '01'))
outdoor_small = arrange(outdoor_small, date)

setwd("../Outdoor_large")
outdoor_large <- read.csv(name_outdoor_large[1])

for(i in 2:5){
  temp = read.csv(name_outdoor_large[i])
  outdoor_large <- merge(outdoor_large, temp, by="date")
}
names(outdoor_large) = c("date", name_outdoor_large)
outdoor_large$date = myd(paste(outdoor_large$date, '01'))
outdoor_large = arrange(outdoor_large, date)

# Plot the graph
library(ggplot2)

#ggplot(indoor_small$date, indoor_small$넷플릭스.csv, type="o")
#lines(indoor_small$date, indoor_small$바둑.csv, type="o")
#lines(indoor_small$date, indoor_small$스팀게임.csv, type="o")
#lines(indoor_small$date, indoor_small$애니.csv, type="o")
#lines(indoor_small$date, indoor_small$인터넷 방송.csv`, type="o")
indoor <- merge(indoor_large, indoor_small, by="date")
outdoor <- merge(outdoor_large, outdoor_small, by = "date")
small <- merge(indoor_small, outdoor_small, by="date")
large <- merge(indoor_large, outdoor_large, by="date")

indoor$avg <- rowMeans(indoor[,name_indoor])
outdoor$avg <- rowMeans(outdoor[,name_outdoor])
small$avg <- rowMeans(small[,name_small])
large$avg <- rowMeans(large[,name_large])

inout <- data.frame(date = indoor$date, avg = indoor$avg - outdoor$avg)
smlg <- data.frame(date = small$date, avg = small$avg - large$avg)


ggplot(inout, aes(date, avg)) +
  geom_line() +
  geom_smooth() +
  geom_vline(xintercept=as.numeric(inout$date[37]), color = "red", linetype=2) +
  geom_vline(xintercept=as.numeric(inout$date[64]), color = "red", linetype=2) +
  ggtitle("Mean Difference between Inside vs Outside") +
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15, color = "black"))

ggplot(smlg, aes(date, avg)) +
  geom_line() +
  geom_smooth() +
  geom_vline(xintercept=as.numeric(inout$date[37]), color = "red", linetype=2) +
  geom_vline(xintercept=as.numeric(inout$date[64]), color = "red", linetype=2) +
  ggtitle("Mean Difference between Small vs Large") +
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15, color = "black"))

