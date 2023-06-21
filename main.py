import pandas as pd
import csv



def process_user_data(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Perform data processing and clustering
    # Here, we'll group the data by age, gender, and yearly income
    clusters = df.groupby(['age', 'gender', 'yearly_income']).apply(lambda x: x.to_dict('records')).to_dict()



    # Prepare the results in the desired format
    result = {}
    i = 0;
    for key, value in clusters.items():
        cluster_name = 'cluster|' + '|'.join(str(i) for i in key)

        splittedData = cluster_name.split("|")
        age = splittedData[1]
        gender = splittedData[2]
        salaryRange = splittedData[3]

        key_string = 'cluster' + str(i)
        result[key_string] = {
            'age': age,
            'gender': gender,
            'salaryRange': salaryRange,
            'users': value
        }
        i = i + 1
    
    return result


import statistics

def calculate_average_website_value(result):
    cluster_averages = {}
    totalNumberOfUsers = 0

    for cluster_key, cluster_data in result.items():
        if cluster_key != 'insights':
            age = cluster_data['age']
            gender = cluster_data['gender']
            salary_range = cluster_data['salaryRange']
            users = cluster_data['users']
            
            totalNumberOfUsers += len(users)
            
            website_values = [user['website_value'] for user in users]
            platform_decisions = [user['platform_decision'] for user in users]
            tracking_platforms = [user['narrative_tracking_platform'] for user in users]
            premium_onedollar = [user['premium_onedollar'] for user in users]
            use_tradingview = [user['use_tradingview.com'] for user in users]
            platform_historical_stock = [user['platform_historical_stock'] for user in users]
            investment_types = [user['investment_types'] for user in users]  # Added investment_type column

            # Calculate average website value
            average_website_value = sum(website_values) / len(website_values)

            # Get most common platform decision and tracking platform
            most_common_decision = max(set(platform_decisions), key=platform_decisions.count)
            most_common_platform = max(set(tracking_platforms), key=tracking_platforms.count)
            most_common_premium = max(set(premium_onedollar), key=premium_onedollar.count)
            most_common_tradingview = max(set(use_tradingview), key=use_tradingview.count)
            most_common_historical_stock = max(set(platform_historical_stock), key=platform_historical_stock.count)
            most_common_investment_type = statistics.mode(investment_types)  # Get most common investment_type

            cluster_averages[cluster_key] = {
                'age': age,
                'gender': gender,
                'salaryRange': salary_range,
                'average_website_value': average_website_value,
                'most_common_decision': most_common_decision,
                'most_common_platform': most_common_platform,
                'most_common_premium': most_common_premium,
                'most_common_tradingview': most_common_tradingview,
                'most_common_historical_stock': most_common_historical_stock,
                'most_common_investment_type': most_common_investment_type,  # Added most_common_investment_type
                'num_records': len(users)
            }


    sorted_keys = sorted(cluster_averages.keys(), key=lambda x: cluster_averages[x]['average_website_value'], reverse=True)


    sorted_data = {key: cluster_averages[key] for key in sorted_keys}

    print(sorted_data)

    return sorted_data





clusters = process_user_data('data.csv')

cluster_avgs = calculate_average_website_value(clusters)



print(cluster_avgs)
