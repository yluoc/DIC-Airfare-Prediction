library(haven)
library(dplyr)
#library(tidyr)

data <- read.csv("./data/raw_data.csv")
data

#inspect data
head(data, n = 10)
tail(data, n = 10)

#data types in data
data_types <- sapply(data, class)
print(data_types)

#count the number of missing values(NaNs) in each column
na_num <- sapply(data, function(x) sum(is.na(x)))
print(na_num)

#drop the NaNs values
data <- Filter(function(x) !any(is.na(x)), data)
data

#check again
na_num <- sapply(data, function(x) sum(is.na(x)))
print(na_num)

#To Count 'Unknown' values in each column
unknown_num <- sapply(data, function(x) sum(x == "Unknown", na.rm = TRUE))
#print(unknown_num)

for(column in names(unknown_num)) {
  count <- unknown_num[column]
  if(count > 0) {
    cat(sprintf("Column '%s' has %d 'Unknown' values.\n", column, count))
  }
}

#drop the row with Unknown in any column
data <- data[apply(data, 1, function(row) all(row != "Unknown")), ]
#reset the indices after dropping the rows
rownames(data) <- NULL
data

#count the number of 'nan' values in every column
nan_num <- sapply(data, function(x) sum(x == "nan", na.rm = TRUE))

for (column in names(nan_num)) {
  count <- nan_num[column]
  if(count > 0) {
    cat(sprintf("Column '%s' has %d 'nan' values.\n", column, count))
  }
}

#drop the row with nan in any column
data <- data[apply(data, 1, function(row) all(row != "nan")), ]
#reset the indices after dropping the rows
rownames(data) <- NULL
data

