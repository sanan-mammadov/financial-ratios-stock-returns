          #Data Preprocessing
#Checking if there are missing values
data <- read.csv("final_data.csv")

colSums(is.na(data)) #Summing missing values
#Output shows no missing values

#Data types
str(data)
#Convert categorical data to factor for some statistical methods
data$Stock.Symbol <- as.factor(data$Stock.Symbol)
allqs <- c("2016_Q1", "2016_Q2", "2016_Q3", "2016_Q4",
           "2017_Q1", "2017_Q2", "2017_Q3", "2017_Q4",
           "2018_Q1", "2018_Q2", "2018_Q3", "2018_Q4",
           "2019_Q1", "2019_Q2", "2019_Q3", "2019_Q4",
           "2020_Q1", "2020_Q2", "2020_Q3", "2020_Q4",
           "2021_Q1", "2021_Q2", "2021_Q3", "2021_Q4",
           "2022_Q1", "2022_Q2", "2022_Q3", "2022_Q4",
           "2023_Q1", "2023_Q2", "2023_Q3", "2023_Q4")
data$Quarter <- factor(data$Quarter, 
                       levels = allqs,
                       ordered = TRUE)

summary(data)
#No issues exist as all of them are handled in python
          #Descriptive Statistics
#Checking outliers
detect_outliers <- function(data) {

  numeric_vars <- sapply(data, is.numeric)
  numeric_data <- data[, numeric_vars]
  
  outliers_list <- list()
  
  for (var in colnames(numeric_data)) {
    #Calculating IQR and bounds
    Q1 <- quantile(numeric_data[[var]], 0.25, na.rm = TRUE)
    Q3 <- quantile(numeric_data[[var]], 0.75, na.rm = TRUE)
    IQR <- Q3 - Q1
    lower_bound <- Q1 - 1.5 * IQR
    upper_bound <- Q3 + 1.5 * IQR
    
    #Identifing outliers
    outliers <- numeric_data[[var]][numeric_data[[var]] < lower_bound | numeric_data[[var]] > upper_bound]
    outliers_list[[var]] <- outliers
  }
  
  return(outliers_list)
}

outliers <- detect_outliers(data)

for (var in names(outliers)) {
  cat("Number of Outliers for:", var, ": ", length(outliers[[var]]), "\n")
}
# Create a data frame to store the outlier results
outlier_results <- data.frame(
  Variable = c(
    "Change.in.ROA..in...", 
    "Change.in.ROE..in...", 
    "Change.in.Net.Income.Margin..in...", 
    "Change.in.EBITDA.Margin..in...", 
    "Change.in.Current.Ratio", 
    "Change.in.Quick.Ratio", 
    "Change.in.Cash.Ratio", 
    "Change.in.Debt.to.Equity", 
    "Quarterly.Return"
  ),
  Number_of_Outliers = c(67, 75, 144, 135, 72, 50, 77, 71, 59)
)

# Print the table using the following packages
#install.packages("knitr")
#install.packages("kableExtra")
library(knitr)
library(kableExtra)
#Table 2
kable(outlier_results, caption = "Table 2: Number of Outliers") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
#There are several outliers for each variable
columns <- c("Change.in.ROA..in...","Change.in.ROE..in...", 
             "Change.in.Net.Income.Margin..in...", 
             "Change.in.EBITDA.Margin..in...", "Change.in.Current.Ratio", 
             "Change.in.Quick.Ratio", "Change.in.Cash.Ratio", "Change.in.Debt.to.Equity", 
             "Quarterly.Return")
#Basic descriptive statistics
descriptive_stats <- sapply(data[, columns], 
                            function(x) c(mean = mean(x, na.rm = TRUE),
                                          sd = sd(x, na.rm = TRUE),
                                          min = min(x, na.rm = TRUE),
                                          max = max(x, na.rm = TRUE),
                                          median = median(x, na.rm = TRUE),
                                          IQR = IQR(x, na.rm = TRUE)))
descriptive_stats_t <- as.data.frame(t(descriptive_stats))
print(descriptive_stats_t)

#Table 1
kable(descriptive_stats_t, caption = "Table 1: Descriptive Statistics") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)

#Correlation
correlation_matrix <- cor(data[, columns], 
                          use = "complete.obs")
print(correlation_matrix)

library(reshape2)
library(ggplot2)
cor_melt <- melt(correlation_matrix)
ggplot(cor_melt, aes(x = Var1, y = Var2, fill = value)) +
  geom_tile() +
  scale_fill_gradient2(low = "red", high = "green", mid = "white", midpoint = 0) +
  theme_minimal() +
  labs(title = "Figure 1: Correlation Heatmap", x = "", y = "", fill = "Correlation") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


          #Regression model
model <- lm(Quarterly.Return ~ Change.in.ROA..in... + Change.in.ROE..in... 
            + Change.in.Net.Income.Margin..in...
            + Change.in.EBITDA.Margin..in... + Change.in.Current.Ratio
            + Change.in.Quick.Ratio + Change.in.Cash.Ratio
            + Change.in.Debt.to.Equity, data = data)
summary(model)
#Extracting coefficients from the model summary for table
coefficients <- summary(model)$coefficients

#Convert coefficients into a data frame
coefficients_table <- data.frame(
  Term = rownames(coefficients),               # Variable names
  Estimate = coefficients[, 1],               # Coefficient estimates
  Std_Error = coefficients[, 2],              # Standard errors
  t_value = coefficients[, 3],                # t-values
  p_value = coefficients[, 4]                 # p-values
)

#Adding a column for significance stars
coefficients_table$Significance <- cut(
  coefficients_table$p_value,
  breaks = c(-Inf, 0.001, 0.01, 0.05, 0.1, Inf),
  labels = c("***", "**", "*", ".", "")
)
#Table 3
kable(coefficients_table, caption = "Table 3: OLS Regression") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE) %>%
  add_footnote("Significance codes: *** p<0.001, ** p<0.01, * p<0.05, . p<0.1", notation = "none")


#Checking each variable
variables <- c(
  "Change.in.ROA..in...", 
  "Change.in.ROE..in...", 
  "Change.in.Net.Income.Margin..in...",
  "Change.in.EBITDA.Margin..in...",
  "Change.in.Current.Ratio",
  "Change.in.Quick.Ratio",
  "Change.in.Cash.Ratio",
  "Change.in.Debt.to.Equity"
)

results <- data.frame(
  Variable = character(),
  Estimate = numeric(),
  Std_Error = numeric(),
  t_value = numeric(),
  p_value = numeric(),
  R_squared = numeric(),
  Adjusted_R_squared = numeric(),
  stringsAsFactors = FALSE
)

for (var in variables) {
  formula <- as.formula(paste("Quarterly.Return ~", var))
  model <- lm(formula, data = data)
  model_summary <- summary(model)
  
  coefficients <- model_summary$coefficients[2, ]  # Only the independent variable row
  
  results <- rbind(
    results, 
    data.frame(
      Variable = var,
      Estimate = coefficients[1],
      Std_Error = coefficients[2],
      t_value = coefficients[3],
      p_value = coefficients[4],
      R_squared = model_summary$r.squared,
      Adjusted_R_squared = model_summary$adj.r.squared
    )
  )
}
results$Significance <- cut(
  results$p_value,
  breaks = c(-Inf, 0.001, 0.01, 0.05, 0.1, Inf),
  labels = c("***", "**", "*", ".", "")
)

#Table 4
kable(results, caption = "Table 4: Individual OLS Regression for each Ratio") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)%>%
  add_footnote("Significance codes: *** p<0.001, ** p<0.01, * p<0.05, . p<0.1", notation = "none")
#model suggest that the relathionship between the ratios and stock returns
#is not significant, I will try some other method to see if the results change
        

            #Refining the model
#Using Robust Regression as there are lot of outliers
#install.packages("robustbase") #provides Robust Linear Model
library("robustbase")
#This model downweigh the outliers
robust_model <- lmrob(
  Quarterly.Return ~ Change.in.ROA..in... + Change.in.ROE..in... +
    Change.in.Net.Income.Margin..in... + Change.in.EBITDA.Margin..in... +
    Change.in.Current.Ratio + Change.in.Quick.Ratio + Change.in.Cash.Ratio +
    Change.in.Debt.to.Equity,
  data = data
)
summary(robust_model)

robust_summary <- summary(robust_model)

robust_coefficients <- data.frame(
  Term = rownames(robust_summary$coefficients),
  Estimate = robust_summary$coefficients[, 1],
  Std_Error = robust_summary$coefficients[, 2],
  t_value = robust_summary$coefficients[, 3],
  p_value = robust_summary$coefficients[, 4]
)

robust_coefficients$Significance <- cut(
  robust_coefficients$p_value,
  breaks = c(-Inf, 0.001, 0.01, 0.05, 0.1, Inf),
  labels = c("***", "**", "*", ".", "")
)
robust_stats <- data.frame(
  Metric = c("Robust Residual Standard Error", "Multiple R-squared", "Adjusted R-squared"),
  Value = c(
    robust_summary$sigma,
    robust_summary$r.squared,
    robust_summary$adj.r.squared
  )
)


#Table 5
kable(robust_coefficients, caption = "Table 5: Robust Regression Coefficients") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE) %>%
  add_footnote("Significance codes: *** p<0.001, ** p<0.01, * p<0.05, . p<0.1", notation = "none")

#Table 6
kable(robust_stats, caption = "Table 6: Robust Regression Model Statistics") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)

#Checking each variable
vars_to_check <- c(
  "Change.in.ROA..in...",
  "Change.in.ROE..in...",
  "Change.in.Net.Income.Margin..in...",
  "Change.in.EBITDA.Margin..in...",
  "Change.in.Current.Ratio",
  "Change.in.Quick.Ratio",
  "Change.in.Cash.Ratio",
  "Change.in.Debt.to.Equity"
)
robust_summaries <- list()

for (var_name in vars_to_check) {
  formula_str <- paste("Quarterly.Return ~", var_name)
  frm <- as.formula(formula_str)
  robust_model_single <- lmrob(frm, data = data)
  robust_summaries[[var_name]] <- summary(robust_model_single)
}

for (var_name in vars_to_check) {
  cat("\n------------------\n")
  cat("Robust regression for:", var_name, "\n")
  print(robust_summaries[[var_name]])
  cat("\n")
}

robust_results <- data.frame(
  Variable = character(),
  Estimate = numeric(),
  Std_Error = numeric(),
  t_value = numeric(),
  p_value = numeric(),
  R_squared = numeric(),
  Adjusted_R_squared = numeric(),
  stringsAsFactors = FALSE
)

for (var_name in vars_to_check) {
  coef_summary <- robust_summaries[[var_name]]$coefficients[2, ]  # Second row for the independent variable
  model_stats <- robust_summaries[[var_name]] 
  
  robust_results <- rbind(
    robust_results,
    data.frame(
      Variable = var_name,
      Estimate = coef_summary[1],
      Std_Error = coef_summary[2],
      t_value = coef_summary[3],
      p_value = coef_summary[4],
      R_squared = model_stats$r.squared,
      Adjusted_R_squared = model_stats$adj.r.squared
    )
  )
}
robust_results$Significance <- cut(
  robust_results$p_value,
  breaks = c(-Inf, 0.001, 0.01, 0.05, 0.1, Inf),
  labels = c("***", "**", "*", ".", "")
)

#Table 7
kable(robust_results, caption = "Table 7: Robust Regression Results for each Ratio") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE) %>%
  add_footnote("Significance codes: *** p<0.001, ** p<0.01, * p<0.05, . p<0.1", notation = "none")



#Using Regularization as there is Multicollinearity like ROE, ROA, and Net Income Margin 
#install.packages("glmnet")
library(glmnet)


x_vars <- c("Change.in.ROA..in...", "Change.in.ROE..in...", 
            "Change.in.Net.Income.Margin..in...",
            "Change.in.EBITDA.Margin..in...", "Change.in.Current.Ratio",
            "Change.in.Quick.Ratio", "Change.in.Cash.Ratio",
            "Change.in.Debt.to.Equity")

X <- as.matrix(data[, x_vars])       
y <- data$Quarterly.Return            

#Lasso model (alpha=1) with cross-validation to choose lambda
cv_lasso <- cv.glmnet(X, y, alpha = 1)
best_lambda <- cv_lasso$lambda.min

lasso_model <- glmnet(X, y, alpha = 1, lambda = best_lambda)
coef(lasso_model)

              #Machine learning
# install.packages("randomForest")

library(randomForest)

x_vars <- c("Change.in.ROA..in...", "Change.in.ROE..in...", 
            "Change.in.Net.Income.Margin..in...",
            "Change.in.EBITDA.Margin..in...", 
            "Change.in.Current.Ratio", "Change.in.Quick.Ratio", 
            "Change.in.Cash.Ratio", "Change.in.Debt.to.Equity")
X <- data[, x_vars]    #data frame of predictors
y <- data$Quarterly.Return  #target

set.seed(123)
N <- nrow(data)
trainSize <- floor(0.8 * N)
trainIndex <- sample(seq_len(N), size = trainSize)

X_train <- X[trainIndex, ]
y_train <- y[trainIndex]

X_test <- X[-trainIndex, ]
y_test <- y[-trainIndex]

#Random forest
rf_fit <- randomForest(
  x = X_train, 
  y = y_train,
  ntree = 500,
  mtry = 3
)

#Predict
rf_pred <- predict(rf_fit, newdata = X_test)

rf_mse <- mean((rf_pred - y_test)^2)
rf_mae <- mean(abs(rf_pred - y_test))
rf_r2  <- 1 - sum((rf_pred - y_test)^2)/sum((mean(y_test) - y_test)^2)

cat("Random Forest:\nMSE =", rf_mse, " | MAE =", rf_mae, " | R2 =", rf_r2, "\n\n")


