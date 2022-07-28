# Links of douban Top250.
links = ['https://movie.douban.com/top250?start=' + str(i) + '&filter='.format(str(i)) for i in range(0, 250, 25)]

# Name of the Excel file that stores the data.
filename = 'douban_top250_data.xlsx'

# Interval between requests.
interval = 1
