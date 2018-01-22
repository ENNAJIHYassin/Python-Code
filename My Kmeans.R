# Importing the dataset
dataset <- read.csv('Mall_Customers.csv')
X = dataset[4:5]

#Using the Elbow Method
set.seed(6)
wcss = vector()
for (i in 1:10) wcss[i] = sum(kmeans(X, i)$withinss)
plot(1:10, wcss, type = 'b', main = paste('Cluster of Clients'), xlab = "Number of Clusters", ylab = "WCSS")

#Applying K-means
set.seed(29)
kmeans = kmeans(X, 5, iter.max = 300, nstart = 10)

#visualising the clusters
library(cluster)
clusplot(X, 
         kmeans$cluster,
         lines = 0,
         shade = TRUE,
         color = TRUE,
         plotchar = TRUE,
         label = 4,
         span = TRUE,
         main = paste('Cluster of Clients'),
         ylab = "Spending Score",
         xlab = "Annual Income"
)

plot(x=X[,1], y=X[,2], col=kmeans$cluster, pch=19, 
     xlim=c(from=min(X[,1]), to=max(X[,1]+30)),
     xlab="Annual Income", ylab="Spending Score")
clusters=c("Careless", "Standard", "Sensible", "Target", "Careful")
legend('bottomright', legend=clusters, col=1:5, pch=19, horiz=F)
