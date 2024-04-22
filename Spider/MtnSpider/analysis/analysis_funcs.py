# analysis_funcs.py
import matplotlib.pyplot as plt

def hist(df, column, title='Histogram', xlabel=None, ylabel='Frequency'):
    """Plots a histogram for a specified DataFrame column."""
    count_data = df[column].value_counts()
    plt.figure(figsize=(10, 5))
    plt.bar(count_data.index, count_data.values, color='blue')
    plt.title(title)
    plt.xlabel(xlabel if xlabel else column)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()
