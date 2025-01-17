# PREDICTING WITH TREES
########################

library(ggplot2)
data(iris)
names(iris)

table(iris$Species)    


inTrain <- createDataPartition(y=iris$Species,p=0.7,list=FALSE)
training <- iris[ inTrain,]
testing  <- iris[-inTrain,]

dim(training);dim(testing)

qplot(Petal.Width,Sepal.Width,colour=Species,data=training)


require(caret)

modFit <- train(Species ~. , method="rpart",data=training)

print(modFit$finalModel)

plot(modFit$finalModel,uniform=TRUE,main="Classification Tree")
text(modFit$finalModel,use.n=TRUE,all=TRUE,cex=.8)



# FANCIER

install.packages("rattle")
library(rattle)
fancyRpartPlot(modFit$finalModel)



predict(modFit,newdata=testing)