import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def pr_evolution(data, start_date = None ,end_date = None):
    
    if start_date:
        data = data[data.index >= start_date]
    if end_date:
        data = data[data.index <= end_date]
    if not start_date:
        start_date = data.index.min().strftime('%Y-%m-%d')
    if not end_date:
        end_date = data.index.max().strftime('%Y-%m-%d')
    data = data.copy()

#======== Calculations part =================================#
    
    # For Red line: 30 days average PR value
    data['30d_mean'] = data['PR'].rolling(window =30).mean()

    # For Dark green line:
    target_textannotations = "----- Target Budget Yield Performance Ratio [1Y-73.9%"
    year_flag = 2
    date_range = pd.date_range(start=start_date, end=end_date, freq='YS-JUL') #The Budget line changes every year in July 
    target_budget = pd.Series(index=data.index)
    value = 73.900
    for date in target_budget.index:
        if (date in date_range)and(date !=start_date):
            value *= 0.992
            target_textannotations += f", {year_flag}Y-{value:.1f}%"
        target_budget[date] = round(value,1)
    data['Target_budget'] = target_budget
    target_textannotations += "]"

    # GHI color coded:
    def classify_ghi(ghi):
        if ghi < 2:
            return 'navy'
        elif 2 <= ghi < 4:
            return 'lightblue'
        elif 4 <= ghi < 6:
            return 'orange'
        else:
            return 'brown'
    data['GHI_color'] = data['GHI'].apply(classify_ghi)

    # Calculate PR points above target budget PR
    data['above_target'] = data['PR'] > target_budget
    percentage_above_target = (data['above_target'].sum() / len(data)) * 100

    # Add annotations for average PR
    avg_pr_7d = f"{data['PR'].tail(7).mean():.1f}"
    avg_pr_30d = f"{data['PR'].tail(30).mean():.1f}"
    avg_pr_60d = f"{data['PR'].tail(60).mean():.1f}"
    avg_pr_90d = f"{data['PR'].tail(90).mean():.1f}"
    avg_pr_365d = f"{data['PR'].tail(365).mean():.1f}"
    avg_pr_lifetime = f"{data['PR'].mean():.1f}"

    data.index = pd.to_datetime(data.index)
#==============================================================#

#======== Plotting Part =======================================#
   
    fig, ax = plt.subplots(figsize=(18,12))

    # To Add GHI value points (Scatter PLot)
    scatter = ax.scatter(data.index, data['PR'], c=data['GHI_color'], s=20)

    # Titles
    plt.title(f'Performance Ratio Evolution\nFrom {start_date} to {end_date}\n',fontsize=16)

    # Text Annotations for Scatter Plot
    plt.text(
    0.16, 0.978,
    "Daily Irradiation [kWh/m²]",
    color='black',
    transform=ax.transAxes,
    fontsize = 15,
    verticalalignment='top',
    horizontalalignment='center')

    # Text Annotations for Percentage of Points over Target
    plt.text(
    0.5, 0.42, 
    f"Points above Target Budget PR = {data['above_target'].sum()}/{len(data)} = {percentage_above_target:.1f}%",
    color='black',
    transform=ax.transAxes,
    fontweight = 'bold',
    fontsize = 10,
    verticalalignment='top',
    horizontalalignment='center')

    # Text Annotations for 30-d Moving average of PR
    plt.text(
    0.42, 0.45, 
    "----- 30-d Moving average of PR",
    color='red',
    transform=ax.transAxes,
    fontsize = 10,
    fontweight= 'bold',
    verticalalignment='top',
    horizontalalignment='center')

    
     # Text Annotations for Target Budget Yield
    plt.text(
    0.5, 0.48, 
    target_textannotations,
    transform=ax.transAxes,
    color='green',
    fontsize = 10,
    fontweight= 'bold',
    verticalalignment='top',
    horizontalalignment='center')
    
    # Text Annotations for Average PR:
    textstr = f"Average PR last 7-d: {avg_pr_7d} %\n\nAverage PR last 30-d: {avg_pr_30d} %\n\nAverage PR last 60-d: {avg_pr_60d} %\n\nAverage PR last 90-d: {avg_pr_90d} %\n\nAverage PR last 365-d: {avg_pr_365d} %\n"
    bold_text = f"Average PR Lifetime: {avg_pr_lifetime} %"
    text_obj = plt.text(0.95, 0.04, textstr, transform=ax.transAxes, fontsize=15, verticalalignment='bottom', horizontalalignment='right')
    bold_text_obj = plt.text(0.96, 0.0197, bold_text, transform=ax.transAxes, fontsize=15, fontweight='bold', verticalalignment='bottom', horizontalalignment='right')

    # Scatter Plot legend
    colors = {'navy': '< 2', 'lightblue': '2 ~ 4', 'orange': '4 ~ 6', 'brown': '> 6'}
    for color, label in colors.items():
        ax.scatter([], [], c=color, label=label)
    first_legend = ax.legend(loc='upper center', ncol=len(colors), prop={'size': 12})

     # Line plot for 30-day moving average of PR
    line1, = ax.plot(data.index, data['30d_mean'], color='red', linewidth=2.7)

    # Line plot for the target budget yield performance ratio
    line2, = ax.plot(data.index, target_budget, color='green', linewidth=2.7)
    
    #X-axis and Y-axis
    plt.ylim(0,100)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    plt.xlabel('Date')
    plt.ylabel('Performance Ratio [%]')
    plt.grid(color='lightgray', linestyle='-', linewidth=0.7, alpha=0.5)
    
    plt.show()

#==============================================================    
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PR Evolution Graph Generator")
    parser.add_argument("--start_date", type=str, required=False, help="Start date for the graph in YYYY-MM-DD format")
    parser.add_argument("--end_date", type=str, required=False, help="End date for the graph in YYYY-MM-DD format")

    args = parser.parse_args()
    data = pd.read_csv('pv_plant.csv', index_col='Date', parse_dates=True)
    pr_evolution(data, start_date=args.start_date, end_date=args.end_date)
