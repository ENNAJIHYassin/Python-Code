# Importing the dataset
dataset <- read.csv('Mall_Customers.csv')
X = dataset[4:5]

#Using the Dendrogram
dendrogram = hclust(dist(X, method ='euclidean'), method = 'ward.D')
plot(dendrogram, main = paste('Dendrogram'), xlab = "Customers", ylab = "Distances")

#Applying Hierarchical Clustering
hc = hclust(dist(X, method ='euclidean'), method = 'ward.D')
y_hc = cutree(hc, 5)

#Visualization of the results
library(cluster)
clusplot(X, 
         y_hc,
         lines = 0,
         shade = TRUE,
         color = TRUE,
         plotchar = TRUE,
         label = 4,
         span = TRUE,
         main = paste('Cluster of Clients HC'),
         ylab = "Spending Score",
         xlab = "Annual Income"
)

plot(x=X[,1], y=X[,2], col=y_hc, pch=19, 
     xlim=c(from=min(X[,1]), to=max(X[,1]+30)),
     xlab="Annual Income", ylab="Spending Score", main = 'HC')
clusters=c("Careless", "Standard", "Sensible", "Target", "Careful")
legend('bottomright', legend=clusters, col=1:5, pch=19, horiz=F)