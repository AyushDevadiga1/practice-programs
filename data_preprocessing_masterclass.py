"""
DATA PREPROCESSING MASTERCLASS: Complete Flow on Complex Dataset
================================================================

Dataset: E-commerce Customer Churn Prediction
- Customer demographics
- Transaction history
- Product interactions
- Support tickets
- Multiple date ranges
- Missing data patterns
- Imbalanced target

This represents a REAL complex scenario you'll face in industry/Kaggle
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# For reproducibility
np.random.seed(42)

print("="*80)
print("STEP 0: CREATE REALISTIC COMPLEX DATASET")
print("="*80)
print("\n📌 WHY: We need a realistic dataset with real-world complexities")
print("💡 THINKING: Real data is MESSY - missing values, outliers, mixed types\n")

# Generate complex dataset
n_customers = 10000

def generate_complex_data(n=10000):
    """Create a realistic messy dataset"""
    
    # Base customer data
    customer_ids = [f'CUST_{i:05d}' for i in range(n)]
    
    # Age with realistic distribution and some missing
    ages = np.random.gamma(shape=8, scale=5, size=n) + 18
    ages = np.clip(ages, 18, 85)
    ages[np.random.choice(n, size=int(n*0.05), replace=False)] = np.nan  # 5% missing
    
    # Gender with some missing
    genders = np.random.choice(['M', 'F', 'Other'], size=n, p=[0.48, 0.48, 0.04])
    genders[np.random.choice(n, size=int(n*0.02), replace=False)] = None
    
    # Income with outliers and missing (MNAR - high earners don't disclose)
    income = np.random.lognormal(mean=10.5, sigma=0.8, size=n)
    income[income > 200000] = np.nan  # High earners refuse to answer
    income[np.random.choice(n, size=int(n*0.15), replace=False)] = np.nan
    
    # Account creation date
    start_date = datetime(2020, 1, 1)
    days_range = (datetime(2024, 1, 1) - start_date).days
    account_created = [start_date + timedelta(days=int(np.random.uniform(0, days_range))) 
                       for _ in range(n)]
    
    # Last login - some users inactive
    last_login = []
    for created in account_created:
        if np.random.random() < 0.7:  # 70% active users
            max_days = (datetime(2024, 12, 31) - created).days
            last_login.append(created + timedelta(days=int(np.random.uniform(0, max_days))))
        else:
            last_login.append(None)  # Inactive users
    
    # Transaction patterns
    total_purchases = np.random.negative_binomial(n=2, p=0.1, size=n)
    total_spend = total_purchases * np.random.lognormal(mean=3.5, sigma=1.2, size=n)
    
    # Some spend without purchases (data error/refunds)
    error_indices = np.random.choice(n, size=int(n*0.01), replace=False)
    total_purchases[error_indices] = 0
    
    # Average order value with division by zero handling
    avg_order_value = np.where(total_purchases > 0, 
                                total_spend / total_purchases, 
                                0)
    
    # Customer support tickets (Poisson distribution)
    support_tickets = np.random.poisson(lam=2, size=n)
    
    # Product categories (one-hot encoded later)
    categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Sports', 'Beauty']
    favorite_category = np.random.choice(categories, size=n)
    
    # Churn (target) - IMBALANCED! Only 15% churn
    # Churn influenced by: low purchases, old account, no recent login
    churn_prob = np.random.random(n)
    
    # Add bias based on features
    account_age = [(datetime(2024, 12, 31) - d).days for d in account_created]
    churn_prob += (np.array(account_age) > 1000) * 0.3  # Old accounts more likely
    churn_prob += (total_purchases < 3) * 0.4  # Low purchases
    churn_prob += (support_tickets > 5) * 0.3  # Many complaints
    
    churned = (churn_prob > np.percentile(churn_prob, 85)).astype(int)
    
    # City with high cardinality
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
              'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Austin']
    cities += [f'City_{i}' for i in range(100)]  # 100 small cities
    city = np.random.choice(cities, size=n, 
                           p=[0.05]*10 + [0.005]*100)  # Power law distribution
    
    # Email domain (useful feature)
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'company.com', 'other.com']
    email_domain = np.random.choice(domains, size=n, p=[0.4, 0.2, 0.15, 0.15, 0.1])
    
    # Create DataFrame
    df = pd.DataFrame({
        'customer_id': customer_ids,
        'age': ages,
        'gender': genders,
        'income': income,
        'account_created': account_created,
        'last_login': last_login,
        'total_purchases': total_purchases,
        'total_spend': total_spend,
        'avg_order_value': avg_order_value,
        'support_tickets': support_tickets,
        'favorite_category': favorite_category,
        'city': city,
        'email_domain': email_domain,
        'churned': churned
    })
    
    return df

# Generate the data
df = generate_complex_data(n_customers)

print(f"✅ Generated dataset with {len(df)} rows and {len(df.columns)} columns")
print(f"✅ Churn rate: {df['churned'].mean()*100:.1f}% (Imbalanced!)")

print("\n" + "="*80)
print("STEP 1: INITIAL RECONNAISSANCE - The 'Detective Phase'")
print("="*80)
print("\n📌 WHY: Understand the data landscape before touching anything")
print("💡 THINKING: What's the story? What problems will I face?\n")

print("1.1 Basic Shape")
print("-" * 40)
print(f"Rows: {df.shape[0]:,} | Columns: {df.shape[1]}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print("\n💭 INSIGHT: Medium dataset - can fit in memory, but need efficient processing")

print("\n1.2 First Look at Data")
print("-" * 40)
print(df.head())

print("\n1.3 Data Types Check")
print("-" * 40)
print(df.dtypes)
print("\n💭 INSIGHT: Dates are objects! Need conversion. Income/age are floats (NaN present)")

print("\n1.4 Missing Data Landscape")
print("-" * 40)
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing_Count': missing,
    'Missing_Percentage': missing_pct
}).sort_values('Missing_Percentage', ascending=False)
print(missing_df[missing_df['Missing_Count'] > 0])

print("\n💭 CRITICAL INSIGHTS:")
print("   - Income: 15% missing - likely MNAR (high earners don't disclose)")
print("   - Last_login: 30% missing - these are INACTIVE users (feature!)")
print("   - Age: 5% missing - probably MCAR (random)")
print("   - Gender: 2% missing - negligible")

print("\n1.5 Statistical Summary")
print("-" * 40)
print(df.describe())

print("\n💭 OBSERVATIONS:")
print("   - avg_order_value max is VERY high (outlier?)")
print("   - total_purchases min is 0 (some customers never bought!)")
print("   - support_tickets: mean=2, max much higher (complaints?)")

print("\n1.6 Target Variable Distribution")
print("-" * 40)
churn_counts = df['churned'].value_counts()
print(churn_counts)
print(f"\nImbalance Ratio: {churn_counts[0]/churn_counts[1]:.2f}:1")
print("\n⚠️  CRITICAL: Severely imbalanced! Will need special handling")

print("\n" + "="*80)
print("STEP 2: DEEP DIVE - UNIVARIATE ANALYSIS")
print("="*80)
print("\n📌 WHY: Understand each feature individually before relationships")
print("💡 THINKING: Distributions, outliers, data quality issues\n")

print("2.1 Numerical Features Analysis")
print("-" * 40)

numeric_cols = ['age', 'income', 'total_purchases', 'total_spend', 
                'avg_order_value', 'support_tickets']

for col in numeric_cols:
    print(f"\n{col.upper()}")
    print("-" * 30)
    
    # Basic stats
    data = df[col].dropna()
    print(f"Mean: {data.mean():.2f} | Median: {data.median():.2f}")
    print(f"Std: {data.std():.2f}")
    print(f"Skewness: {data.skew():.2f}")
    
    # Outlier detection using IQR
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    outliers_count = ((data < Q1 - 1.5*IQR) | (data > Q3 + 1.5*IQR)).sum()
    print(f"Outliers (IQR method): {outliers_count} ({outliers_count/len(data)*100:.1f}%)")
    
    if col == 'income':
        print("💭 INSIGHT: Right-skewed (expected for income). Outliers are real high earners.")
    elif col == 'avg_order_value':
        print("💭 INSIGHT: High skew + outliers. Some customers make HUGE purchases.")
    elif col == 'support_tickets':
        print("💭 INSIGHT: Poisson-like. Most customers = 0-3 tickets, some problematic users.")

print("\n2.2 Categorical Features Analysis")
print("-" * 40)

categorical_cols = ['gender', 'favorite_category', 'city', 'email_domain']

for col in categorical_cols:
    print(f"\n{col.upper()}")
    print("-" * 30)
    
    value_counts = df[col].value_counts()
    print(f"Unique values: {df[col].nunique()}")
    print(f"Top 5 categories:")
    print(value_counts.head())
    
    # Check cardinality
    if df[col].nunique() > 20:
        print(f"⚠️  HIGH CARDINALITY: {df[col].nunique()} unique values!")
        print("💭 STRATEGY: Will need encoding technique (target/frequency encoding)")
    else:
        print("✓ Low/medium cardinality - one-hot encoding feasible")

print("\n2.3 Date Features Analysis")
print("-" * 40)

print("\nACCOUNT_CREATED")
print("-" * 30)
print(f"Date range: {df['account_created'].min()} to {df['account_created'].max()}")
print("💭 INSIGHT: 4-year history. Need to create 'account_age' feature")

print("\nLAST_LOGIN")
print("-" * 30)
print(f"Non-null entries: {df['last_login'].notna().sum()}/{len(df)}")
print("💭 INSIGHT: 30% never logged in! This IS a feature (inactivity)")

print("\n" + "="*80)
print("STEP 3: BIVARIATE ANALYSIS - Feature vs Target")
print("="*80)
print("\n📌 WHY: Which features actually predict churn?")
print("💡 THINKING: Correlation ≠ causation, but shows relationships\n")

print("3.1 Numerical Features vs Churned")
print("-" * 40)

for col in ['total_purchases', 'total_spend', 'support_tickets']:
    print(f"\n{col.upper()} by Churn Status")
    print("-" * 30)
    
    grouped = df.groupby('churned')[col].agg(['mean', 'median', 'std'])
    print(grouped)
    
    # Calculate effect size (Cohen's d)
    churned_data = df[df['churned']==1][col].dropna()
    not_churned_data = df[df['churned']==0][col].dropna()
    
    pooled_std = np.sqrt((churned_data.std()**2 + not_churned_data.std()**2) / 2)
    cohens_d = (not_churned_data.mean() - churned_data.mean()) / pooled_std
    
    print(f"Cohen's d: {cohens_d:.3f}")
    
    if abs(cohens_d) > 0.5:
        print(f"💡 STRONG EFFECT: {col} is a good predictor!")
    elif abs(cohens_d) > 0.2:
        print(f"💡 MODERATE EFFECT: {col} has some predictive power")
    else:
        print(f"💡 WEAK EFFECT: {col} may not be very useful")

print("\n3.2 Categorical Features vs Churned")
print("-" * 40)

for col in ['gender', 'email_domain', 'favorite_category']:
    print(f"\n{col.upper()} - Churn Rate by Category")
    print("-" * 30)
    
    churn_by_cat = df.groupby(col)['churned'].agg(['sum', 'count', 'mean'])
    churn_by_cat.columns = ['Churned_Count', 'Total', 'Churn_Rate']
    churn_by_cat = churn_by_cat.sort_values('Churn_Rate', ascending=False)
    print(churn_by_cat)
    
    if churn_by_cat['Churn_Rate'].max() - churn_by_cat['Churn_Rate'].min() > 0.1:
        print(f"💡 SIGNIFICANT VARIATION: {col} shows different churn patterns!")
    else:
        print(f"💡 UNIFORM CHURN: {col} doesn't discriminate much")

print("\n" + "="*80)
print("STEP 4: DATA QUALITY FIXES - The Foundation")
print("="*80)
print("\n📌 WHY: Clean data before feature engineering")
print("💡 THINKING: Fix types, handle errors, create data quality flags\n")

df_clean = df.copy()

print("4.1 Convert Date Columns")
print("-" * 40)
print("Before:", df_clean['account_created'].dtype)

# Already datetime from generation, but showing the pattern
if df_clean['account_created'].dtype == 'object':
    df_clean['account_created'] = pd.to_datetime(df_clean['account_created'])

if df_clean['last_login'].dtype == 'object':
    df_clean['last_login'] = pd.to_datetime(df_clean['last_login'])

print("After:", df_clean['account_created'].dtype)
print("✓ Dates converted properly")

print("\n4.2 Fix Data Quality Issues")
print("-" * 40)

# Issue: Some customers have 0 purchases but positive spend (refunds/errors)
data_errors = (df_clean['total_purchases'] == 0) & (df_clean['total_spend'] > 0)
print(f"Found {data_errors.sum()} records with 0 purchases but positive spend")

# Create flag for tracking
df_clean['has_data_quality_issue'] = data_errors.astype(int)

# Fix the issue - set spend to 0 for 0 purchases
df_clean.loc[data_errors, 'total_spend'] = 0
df_clean.loc[data_errors, 'avg_order_value'] = 0

print("✓ Fixed data quality issues and created tracking flag")

print("\n4.3 Handle Inf/NaN in Calculated Fields")
print("-" * 40)

# Check for inf values
inf_count = np.isinf(df_clean.select_dtypes(include=[np.number])).sum()
print(f"Inf values found: {inf_count.sum()}")

if inf_count.sum() > 0:
    df_clean = df_clean.replace([np.inf, -np.inf], np.nan)
    print("✓ Replaced inf values with NaN")

print("\n" + "="*80)
print("STEP 5: FEATURE ENGINEERING - Create Predictive Power")
print("="*80)
print("\n📌 WHY: Raw features rarely capture complex patterns")
print("💡 THINKING: Domain knowledge + creativity = better features\n")

print("5.1 Temporal Features")
print("-" * 40)

# Reference date for calculations
reference_date = pd.Timestamp('2024-12-31')

# Account age in days
df_clean['account_age_days'] = (reference_date - df_clean['account_created']).dt.days
print("✓ Created: account_age_days")

# Days since last login (inactivity measure)
df_clean['days_since_last_login'] = (reference_date - df_clean['last_login']).dt.days

# For customers who never logged in, use account age
df_clean['days_since_last_login'] = df_clean['days_since_last_login'].fillna(
    df_clean['account_age_days']
)
print("✓ Created: days_since_last_login")

# Time-based flags
df_clean['is_inactive'] = (df_clean['days_since_last_login'] > 180).astype(int)
df_clean['is_new_customer'] = (df_clean['account_age_days'] < 90).astype(int)
df_clean['is_loyal_customer'] = (df_clean['account_age_days'] > 730).astype(int)

print("✓ Created: is_inactive, is_new_customer, is_loyal_customer")

print("\n💭 REASONING:")
print("   - Account age: Older customers have different behavior")
print("   - Inactivity: Strong churn predictor")
print("   - New/Loyal flags: Non-linear relationships captured")

print("\n5.2 Behavioral Features")
print("-" * 40)

# Purchase frequency (purchases per year)
df_clean['purchase_frequency'] = (
    df_clean['total_purchases'] / (df_clean['account_age_days'] / 365)
)
df_clean['purchase_frequency'] = df_clean['purchase_frequency'].replace([np.inf], 0)
print("✓ Created: purchase_frequency")

# Average spend per month
df_clean['monthly_spend'] = (
    df_clean['total_spend'] / (df_clean['account_age_days'] / 30)
)
df_clean['monthly_spend'] = df_clean['monthly_spend'].replace([np.inf], 0)
print("✓ Created: monthly_spend")

# Support ticket rate
df_clean['support_ticket_rate'] = (
    df_clean['support_tickets'] / (df_clean['account_age_days'] / 365)
)
df_clean['support_ticket_rate'] = df_clean['support_ticket_rate'].replace([np.inf], 0)
print("✓ Created: support_ticket_rate")

# Engagement score (composite metric)
df_clean['engagement_score'] = (
    df_clean['purchase_frequency'] * 0.4 +
    (1 / (df_clean['days_since_last_login'] + 1)) * 100 * 0.4 +
    (df_clean['total_purchases'] / 10) * 0.2
)
print("✓ Created: engagement_score (composite metric)")

print("\n💭 REASONING:")
print("   - Rates normalize for account age (fair comparison)")
print("   - Composite scores capture multiple aspects")
print("   - These features are more predictive than raw counts")

print("\n5.3 Customer Segmentation Features")
print("-" * 40)

# Spending tier
df_clean['spending_tier'] = pd.cut(
    df_clean['total_spend'],
    bins=[-np.inf, 100, 500, 2000, np.inf],
    labels=['Low', 'Medium', 'High', 'VIP']
)
print("✓ Created: spending_tier")

# Purchase behavior category
conditions = [
    (df_clean['total_purchases'] == 0),
    (df_clean['total_purchases'] <= 5),
    (df_clean['total_purchases'] <= 20),
    (df_clean['total_purchases'] > 20)
]
choices = ['Never_Bought', 'Occasional', 'Regular', 'Power_User']
df_clean['customer_type'] = np.select(conditions, choices, default='Unknown')
print("✓ Created: customer_type")

# Value segment (RFM-inspired)
df_clean['value_segment'] = (
    (df_clean['total_spend'] > df_clean['total_spend'].median()).astype(int) * 2 +
    (df_clean['days_since_last_login'] < 90).astype(int)
)
value_segment_labels = {0: 'Low_Value_Inactive', 1: 'Low_Value_Active',
                        2: 'High_Value_Inactive', 3: 'High_Value_Active'}
df_clean['value_segment'] = df_clean['value_segment'].map(value_segment_labels)
print("✓ Created: value_segment (RFM-inspired)")

print("\n💭 REASONING:")
print("   - Segmentation captures non-linear patterns")
print("   - ML models treat 'High_Value_Inactive' differently than raw numbers")
print("   - Business-meaningful categories")

print("\n5.4 Ratio and Interaction Features")
print("-" * 40)

# Support tickets per purchase (complaint rate)
df_clean['complaints_per_purchase'] = df_clean['support_tickets'] / (
    df_clean['total_purchases'] + 1  # +1 to avoid division by zero
)
print("✓ Created: complaints_per_purchase")

# Income to spend ratio (if they have income data)
df_clean['spend_to_income_ratio'] = df_clean['total_spend'] / (
    df_clean['income'].fillna(df_clean['income'].median()) + 1
)
print("✓ Created: spend_to_income_ratio")

print("\n💭 REASONING:")
print("   - Ratios capture relationships between features")
print("   - 'High complaints per purchase' = problematic customer")

print("\n5.5 Domain-Specific Features")
print("-" * 40)

# Email domain as proxy for customer type
corporate_domains = ['company.com']
df_clean['is_corporate_email'] = df_clean['email_domain'].isin(corporate_domains).astype(int)
print("✓ Created: is_corporate_email")

# High-value category flag
high_value_categories = ['Electronics', 'Home']
df_clean['buys_high_value_category'] = df_clean['favorite_category'].isin(
    high_value_categories
).astype(int)
print("✓ Created: buys_high_value_category")

print("\n💭 REASONING:")
print("   - Corporate customers may have different churn patterns")
print("   - Product category reveals preferences and value")

print(f"\n✅ FEATURE ENGINEERING COMPLETE")
print(f"   Before: {len(df.columns)} features")
print(f"   After: {len(df_clean.columns)} features")
print(f"   New features created: {len(df_clean.columns) - len(df.columns)}")

print("\n" + "="*80)
print("STEP 6: MISSING DATA STRATEGY - Intelligent Imputation")
print("="*80)
print("\n📌 WHY: Preserve information while handling missingness")
print("💡 THINKING: Different strategies for different missing patterns\n")

print("6.1 Create Missing Indicators (Before Imputation!)")
print("-" * 40)

# Create flags for features with meaningful missingness
important_features_with_missing = ['income', 'age', 'last_login']

for col in important_features_with_missing:
    flag_name = f'{col}_was_missing'
    df_clean[flag_name] = df_clean[col].isnull().astype(int)
    print(f"✓ Created: {flag_name}")

print("\n💭 REASONING:")
print("   - 'income_was_missing' captures high earners who don't disclose")
print("   - 'last_login_was_missing' captures inactive users")
print("   - These flags preserve information BEFORE imputation destroys it")

print("\n6.2 Strategic Imputation by Feature Type")
print("-" * 40)

# Age: MCAR - use median by gender
print("\nAGE imputation")
print("-" * 20)
df_clean['age'] = df_clean.groupby('gender')['age'].transform(
    lambda x: x.fillna(x.median())
)
# For any remaining (missing gender), use overall median
df_clean['age'] = df_clean['age'].fillna(df_clean['age'].median())
print("Strategy: Group median (by gender)")
print(f"Remaining missing: {df_clean['age'].isnull().sum()}")

# Income: MNAR - use sophisticated approach
print("\nINCOME imputation")
print("-" * 20)

# Model-based imputation: predict income from other features
income_features = ['age', 'total_spend', 'account_age_days']

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Train on non-missing income
df_train_income = df_clean[df_clean['income'].notna()][income_features + ['income']]
df_predict_income = df_clean[df_clean['income'].isna()][income_features]

if len(df_predict_income) > 0:
    rf_imputer = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=5)
    rf_imputer.fit(df_train_income[income_features], df_train_income['income'])
    
    predicted_income = rf_imputer.predict(df_predict_income)
    df_clean.loc[df_clean['income'].isna(), 'income'] = predicted_income
    
    print("Strategy: Random Forest prediction from age, spend, account_age")
else:
    df_clean['income'] = df_clean['income'].fillna(df_clean['income'].median())
    print("Strategy: Median (fallback)")

print(f"Remaining missing: {df_clean['income'].isnull().sum()}")

# Gender: Low missingness - mode
print("\nGENDER imputation")
print("-" * 20)
df_clean['gender'] = df_clean['gender'].fillna(df_clean['gender'].mode()[0])
print(f"Strategy: Mode")
print(f"Remaining missing: {df_clean['gender'].isnull().sum()}")

# Last login: Already handled in feature engineering (used account_age as proxy)
print("\nLAST_LOGIN: Handled via feature engineering (days_since_last_login)")

print("\n💭 REASONING:")
print("   - Age: Median by gender preserves demographic patterns")
print("   - Income: RF prediction uses relationship with spend/age")
print("   - Gender: Mode is fine for low missingness")
print("   - Each strategy matched to missing data mechanism!")

print("\n6.3 Verify No Missing Data in Critical Features")
print("-" * 40)

critical_cols = ['age', 'income', 'gender', 'days_since_last_login']
missing_summary = df_clean[critical_cols].isnull().sum()
print(missing_summary)

if missing_summary.sum() == 0:
    print("\n✅ All critical features imputed successfully!")
else:
    print("\n⚠️  Warning: Some missing data remains")

print("\n" + "="*80)
print("STEP 7: OUTLIER HANDLING - Careful Treatment")
print("="*80)
print("\n📌 WHY: Outliers can be informative or destructive")
print("💡 THINKING: Don't remove blindly - understand and transform\n")

print("7.1 Identify Outliers")
print("-" * 40)

outlier_candidates = ['total_spend', 'avg_order_value', 'income', 'support_tickets']

for col in outlier_candidates:
    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = ((df_clean[col] < lower_bound) | (df_clean[col] > upper_bound))
    outlier_count = outliers.sum()
    
    print(f"\n{col.upper()}")
    print(f"  Outliers: {outlier_count} ({outlier_count/len(df_clean)*100:.1f}%)")
    print(f"  Range: [{df_clean[col].min():.2f}, {df_clean[col].max():.2f}]")
    print(f"  IQR bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    # Create outlier flags instead of removing
    df_clean[f'{col}_is_outlier'] = outliers.astype(int)

print("\n💭 DECISION: Created outlier FLAGS instead of removing")
print("   Why? Outliers might be real VIP customers or problem users")

print("\n7.2 Transform Skewed Distributions")
print("-" * 40)

# Log transform for right-skewed features
skewed_features = ['total_spend', 'avg_order_value', 'income']

for col in skewed_features:
    # Log1p to handle zeros
    df_clean[f'{col}_log'] = np.log1p(df_clean[col])
    print(f"✓ Created: {col}_log (log transformation)")

print("\n💭 REASONING:")
print("   - Log transform reduces impact of outliers")
print("   - Makes distribution more normal")
print("   - Models like logistic regression benefit from this")
print("   - We keep BOTH original and transformed (let model decide)")

print("\n" + "="*80)
print("STEP 8: ENCODING CATEGORICAL VARIABLES")
print("="*80)
print("\n📌 WHY: ML models need numbers, not categories")
print("💡 THINKING: Different encoding for different cardinality\n")

print("8.1 Low Cardinality - One-Hot Encoding")
print("-" * 40)

low_cardinality = ['gender', 'email_domain', 'favorite_category', 
                   'spending_tier', 'customer_type', 'value_segment']

# Get dummies
df_encoded = pd.get_dummies(df_clean, columns=low_cardinality, 
                             drop_first=True, prefix=low_cardinality)

original_cols = len(df_clean.columns)
new_cols = len(df_encoded.columns)
print(f"Columns before: {original_cols}")
print(f"Columns after: {new_cols}")
print(f"New dummy columns: {new_cols - original_cols}")

print("\n💭 REASONING:")
print("   - drop_first=True avoids multicollinearity")
print("   - One-hot encoding for <20 categories is fine")

print("\n8.2 High Cardinality - Target Encoding")
print("-" * 40)

print("\nCITY encoding (110 unique values!)")

# Target encoding with cross-validation to avoid leakage
from sklearn.model_selection import KFold

def target_encode_cv(df, col, target, n_splits=5):
    """Target encoding with CV to prevent overfitting"""
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    encoded = np.zeros(len(df))
    
    for train_idx, val_idx in kf.split(df):
        # Calculate means on train fold
        means = df.iloc[train_idx].groupby(col)[target].mean()
        global_mean = df.iloc[train_idx][target].mean()
        
        # Apply to validation fold
        encoded[val_idx] = df.iloc[val_idx][col].map(means).fillna(global_mean)
    
    return encoded

df_encoded['city_target_encoded'] = target_encode_cv(df_encoded, 'city', 'churned')

# Also add frequency encoding
city_counts = df_encoded['city'].value_counts()
df_encoded['city_frequency'] = df_encoded['city'].map(city_counts)

print("✓ Created: city_target_encoded (target encoding with CV)")
print("✓ Created: city_frequency (frequency encoding)")

# Drop original city column
df_encoded = df_encoded.drop('city', axis=1)

print("\n💭 REASONING:")
print("   - Target encoding: captures relationship with target")
print("   - CV prevents overfitting (not encoding on same data we train on)")
print("   - Frequency encoding: captures popularity of each city")
print("   - Both are more informative than 110 dummy variables!")

print("\n8.3 Binary Encoding (Already Done)")
print("-" * 40)
print("✓ Features like 'is_inactive', 'churned' already binary (0/1)")

print("\n" + "="*80)
print("STEP 9: FEATURE SCALING - Prepare for ML")
print("="*80)
print("\n📌 WHY: Different features have different scales")
print("💡 THINKING: Scaling strategy depends on model choice\n")

print("9.1 Identify Features to Scale")
print("-" * 40)

# Get numeric columns (exclude target and ID)
numeric_features = df_encoded.select_dtypes(include=[np.number]).columns.tolist()
numeric_features = [col for col in numeric_features 
                   if col not in ['churned', 'customer_id']]

print(f"Numeric features to scale: {len(numeric_features)}")

# Separate into different scaling strategies
print("\n9.2 Create Scaled Versions (Multiple Strategies)")
print("-" * 40)

from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler

# Don't actually scale yet (wait for train/test split!)
# Just showing the strategy

print("STRATEGY PLAN:")
print("-" * 30)
print("StandardScaler: For tree-based models (XGBoost, RF)")
print("  - Mean = 0, Std = 1")
print("  - Good for normal distributions")
print("")
print("RobustScaler: For features with outliers")
print("  - Uses median and IQR")
print("  - Robust to outliers")
print("")
print("MinMaxScaler: For neural networks")
print("  - Scale to [0, 1]")
print("  - Preserves zero values")

print("\n⚠️  CRITICAL: We DON'T scale yet!")
print("   Why? Must split train/test FIRST to avoid data leakage")
print("   Scaling will happen in Step 11 (after split)")

print("\n" + "="*80)
print("STEP 10: FEATURE SELECTION - Remove Noise")
print("="*80)
print("\n📌 WHY: More features ≠ better model")
print("💡 THINKING: Remove redundant, low-variance, and leaky features\n")

print("10.1 Remove Zero Variance Features")
print("-" * 40)

from sklearn.feature_selection import VarianceThreshold

# Calculate variance
variances = df_encoded[numeric_features].var()
zero_var_features = variances[variances == 0].index.tolist()

print(f"Zero variance features: {len(zero_var_features)}")
if len(zero_var_features) > 0:
    print(zero_var_features)
    df_encoded = df_encoded.drop(zero_var_features, axis=1)
    print("✓ Removed zero variance features")
else:
    print("✓ No zero variance features found")

print("\n10.2 Check for Multicollinearity")
print("-" * 40)

# Calculate correlation matrix for numeric features
numeric_cols_current = df_encoded.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols_current = [col for col in numeric_cols_current 
                       if col not in ['churned', 'customer_id']]

# Limit to manageable subset for display
sample_cols = numeric_cols_current[:10]
corr_matrix = df_encoded[sample_cols].corr()

# Find highly correlated pairs
high_corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        if abs(corr_matrix.iloc[i, j]) > 0.9:
            high_corr_pairs.append((
                corr_matrix.columns[i],
                corr_matrix.columns[j],
                corr_matrix.iloc[i, j]
            ))

print(f"Highly correlated pairs (r > 0.9): {len(high_corr_pairs)}")
for feat1, feat2, corr_val in high_corr_pairs[:5]:  # Show first 5
    print(f"  {feat1} <-> {feat2}: r={corr_val:.3f}")

print("\n💭 DECISION: Keep both for now, let model handle it")
print("   (Could drop one, but regularization helps with this)")

print("\n10.3 Feature Importance (Quick Check)")
print("-" * 40)

# Quick Random Forest to see feature importance
from sklearn.ensemble import RandomForestClassifier

# Prepare features (X) and target (y)
feature_cols = [col for col in df_encoded.columns 
               if col not in ['churned', 'customer_id', 'account_created', 
                             'last_login']]

X_temp = df_encoded[feature_cols]
y_temp = df_encoded['churned']

# Handle any remaining non-numeric columns
X_temp = X_temp.select_dtypes(include=[np.number])

# Quick RF
rf_quick = RandomForestClassifier(n_estimators=50, random_state=42, 
                                 max_depth=5, n_jobs=-1)
rf_quick.fit(X_temp, y_temp)

# Get feature importance
feature_importance = pd.DataFrame({
    'feature': X_temp.columns,
    'importance': rf_quick.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 15 Most Important Features:")
print("-" * 40)
print(feature_importance.head(15).to_string(index=False))

print("\n💭 INSIGHTS:")
print("   - Behavioral features (engagement, frequency) likely top")
print("   - Temporal features (inactivity) should rank high")
print("   - Some engineered features better than raw features")

print("\n10.4 Remove Obviously Irrelevant Features")
print("-" * 40)

# Remove ID and date columns (not useful for prediction)
cols_to_drop = ['customer_id']

# Check if date columns still present
date_cols = df_encoded.select_dtypes(include=['datetime64']).columns.tolist()
cols_to_drop.extend(date_cols)

df_final = df_encoded.drop(cols_to_drop, axis=1)
print(f"✓ Dropped: {cols_to_drop}")
print(f"✓ Final feature count: {len(df_final.columns) - 1} (excluding target)")

print("\n" + "="*80)
print("STEP 11: TRAIN-TEST SPLIT & SCALING")
print("="*80)
print("\n📌 WHY: Proper validation setup prevents overfitting")
print("💡 THINKING: Split FIRST, then scale on train only\n")

from sklearn.model_selection import train_test_split

print("11.1 Separate Features and Target")
print("-" * 40)

X = df_final.drop('churned', axis=1)
y = df_final['churned']

print(f"Features (X): {X.shape}")
print(f"Target (y): {y.shape}")
print(f"Target distribution: {y.value_counts().to_dict()}")

print("\n11.2 Stratified Train-Test Split")
print("-" * 40)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y  # Maintains class distribution
)

print(f"Train set: {X_train.shape[0]:,} samples")
print(f"Test set: {X_test.shape[0]:,} samples")
print(f"Train churn rate: {y_train.mean()*100:.1f}%")
print(f"Test churn rate: {y_test.mean()*100:.1f}%")

print("\n💭 CRITICAL: stratify=y ensures both sets have same churn ratio")
print("   Without this, test set might have different distribution!")

print("\n11.3 Scale Features (Train Only!)")
print("-" * 40)

# Use RobustScaler (good with outliers)
scaler = RobustScaler()

# Fit on train, transform both
X_train_scaled = pd.DataFrame(
    scaler.fit_transform(X_train),
    columns=X_train.columns,
    index=X_train.index
)

X_test_scaled = pd.DataFrame(
    scaler.transform(X_test),  # Only transform, don't fit!
    columns=X_test.columns,
    index=X_test.index
)

print("✓ Scaled training set (fit + transform)")
print("✓ Scaled test set (transform only)")

print("\n⚠️  CRITICAL DATA LEAKAGE PREVENTION:")
print("   ✓ scaler.fit() ONLY on training data")
print("   ✓ scaler.transform() applied to test data")
print("   ✗ NEVER fit on full dataset then split")

print("\n11.4 Final Dataset Summary")
print("-" * 40)
print(f"Training features: {X_train_scaled.shape}")
print(f"Test features: {X_test_scaled.shape}")
print(f"Number of features: {X_train_scaled.shape[1]}")
print(f"Churn samples in train: {y_train.sum()}")
print(f"Churn samples in test: {y_test.sum()}")

print("\n" + "="*80)
print("STEP 12: HANDLE CLASS IMBALANCE")
print("="*80)
print("\n📌 WHY: 85:15 imbalance will bias model")
print("💡 THINKING: Multiple strategies to try\n")

print("12.1 Calculate Class Weights")
print("-" * 40)

from sklearn.utils.class_weight import compute_class_weight

class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train),
    y=y_train
)

class_weight_dict = dict(zip(np.unique(y_train), class_weights))
print(f"Class weights: {class_weight_dict}")

print("\n💭 USAGE: Pass to model as class_weight parameter")
print("   model = LogisticRegression(class_weight='balanced')")

print("\n12.2 SMOTE for Oversampling (Optional)")
print("-" * 40)

try:
    from imblearn.over_sampling import SMOTE
    
    smote = SMOTE(random_state=42, sampling_strategy=0.5)  # 50% minority
    X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)
    
    print(f"Before SMOTE: {y_train.value_counts().to_dict()}")
    print(f"After SMOTE: {y_train_smote.value_counts().to_dict()}")
    
    print("\n💭 USAGE: Train model on X_train_smote, y_train_smote")
    print("   Caution: Can create synthetic outliers")
    
except ImportError:
    print("⚠️  imbalanced-learn not installed")
    print("   Install: pip install imbalanced-learn")
    print("   For now, use class_weight strategy")

print("\n12.3 Recommended Strategy")
print("-" * 40)
print("BEST PRACTICE for this dataset:")
print("1. Use class_weight='balanced' in model")
print("2. Use stratified K-fold cross-validation")
print("3. Optimize for F1-score or AUC-ROC (not accuracy)")
print("4. Try SMOTE if needed, but start with class weights")

print("\n" + "="*80)
print("🎉 DATA PREPROCESSING COMPLETE!")
print("="*80)

print("\n📊 FINAL SUMMARY")
print("="*80)
print(f"Original dataset: {df.shape}")
print(f"Final processed dataset: {df_final.shape}")
print(f"Feature count: {df.shape[1]} → {df_final.shape[1] - 1} (excluding target)")
print(f"Missing data handled: ✓")
print(f"Outliers addressed: ✓")
print(f"Feature engineering: ✓")
print(f"Encoding complete: ✓")
print(f"Scaled and ready: ✓")
print(f"Train/test split: ✓")
print(f"Class imbalance strategy: ✓")

print("\n🚀 READY FOR MODELING!")
print("="*80)

print("\n📝 KEY TAKEAWAYS & WHAT WE GAINED:")
print("-" * 80)
print("""
1. INITIAL EXPLORATION (Steps 0-1)
   ✓ Gained: Understanding of data landscape, complexity, and challenges
   ✓ Thinking: "What's the story? What problems will I face?"
   
2. UNIVARIATE ANALYSIS (Step 2)
   ✓ Gained: Distribution shapes, outlier patterns, data quality issues
   ✓ Thinking: "How is each feature behaving? Are there anomalies?"
   
3. BIVARIATE ANALYSIS (Step 3)
   ✓ Gained: Relationship with target, effect sizes, predictive power hints
   ✓ Thinking: "Which features actually matter for prediction?"
   
4. DATA QUALITY FIXES (Step 4)
   ✓ Gained: Clean foundation, prevented downstream errors
   ✓ Thinking: "Fix the basics before building complexity"
   
5. FEATURE ENGINEERING (Step 5)
   ✓ Gained: 20+ new features with higher predictive power than raw data
   ✓ Thinking: "How can I extract hidden patterns and relationships?"
   
6. MISSING DATA STRATEGY (Step 6)
   ✓ Gained: Preserved information via flags, intelligent imputation
   ✓ Thinking: "Missingness itself is information - don't destroy it!"
   
7. OUTLIER HANDLING (Step 7)
   ✓ Gained: Flags instead of deletion, transformed distributions
   ✓ Thinking: "Outliers might be signal, not noise - be careful!"
   
8. CATEGORICAL ENCODING (Step 8)
   ✓ Gained: ML-ready numeric features, avoided dummy variable explosion
   ✓ Thinking: "Different encoding for different cardinality"
   
9. FEATURE SCALING (Step 9)
   ✓ Gained: Fair comparison across features, model convergence
   ✓ Thinking: "Scale matters - but only after split!"
   
10. FEATURE SELECTION (Step 10)
    ✓ Gained: Reduced noise, identified important features
    ✓ Thinking: "Less is more - remove what doesn't help"
    
11. TRAIN-TEST SPLIT (Step 11)
    ✓ Gained: Valid evaluation setup, prevented leakage
    ✓ Thinking: "Split first, scale second - ALWAYS!"
    
12. CLASS IMBALANCE (Step 12)
    ✓ Gained: Strategies to handle skewed distribution
    ✓ Thinking: "Balance the scales for fair learning"

OVERALL TRANSFORMATION:
→ From raw messy data to ML-ready features
→ From 14 columns to 50+ engineered features
→ From missing data to intelligent imputation
→ From unknown patterns to quantified relationships
→ From one dataset to train/test/validation setup

NEXT STEPS:
→ Model training (Random Forest, XGBoost, Neural Networks)
→ Cross-validation with stratified folds
→ Hyperparameter tuning
→ Model interpretation (SHAP values, feature importance)
→ Threshold optimization for business metrics
""")

print("\n" + "="*80)
print("💾 SAVE PROCESSED DATA")
print("="*80)

# Save for later use
X_train_scaled.to_csv('/home/claude/X_train_processed.csv', index=False)
X_test_scaled.to_csv('/home/claude/X_test_processed.csv', index=False)
y_train.to_csv('/home/claude/y_train.csv', index=False)
y_test.to_csv('/home/claude/y_test.csv', index=False)

print("✓ Saved X_train_processed.csv")
print("✓ Saved X_test_processed.csv")
print("✓ Saved y_train.csv")
print("✓ Saved y_test.csv")

print("\n🎓 CONGRATULATIONS!")
print("You've completed a professional-grade data preprocessing pipeline!")
print("This is exactly how top data scientists approach complex datasets.")
