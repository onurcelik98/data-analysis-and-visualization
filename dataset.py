import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

print(pd.__version__)
plt.close("all")
rg = np.random.default_rng(1)

np.set_printoptions(threshold=sys.maxsize)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('expand_frame_repr', False)


class ProductList:
    def __init__(self, df, filterBy=None, filterValue=None, orderBy=None, ascending=False, showFields=None, cropped=False, fromHead=True, numberOfLines=None):
        # parsing the csv into a dataframe object with appropriate dtypes
        self.df = df
        self.list = df
        df["item_id"] = df["item_id"].astype("string")
        df["user_id"] = df["user_id"].astype("string")
        df["rating"] = df["rating"].astype("int64")
        df["timestamp"] = df["timestamp"].astype("datetime64[ns]")
        df["size"] = df["size"].astype("float64")
        df["fit"] = df["fit"].astype("category")
        df["user_attr"] = df["user_attr"].astype("category")
        df["model_attr"] = df["model_attr"].astype("category")
        df["category"] = df["category"].astype("category")
        df["brand"] = df["brand"].astype("string")
        df["year"] = pd.to_datetime(df["year"], format='%Y')
        df["split"] = df["split"].astype("category")

        # setting the filtering and ordering preferences
        self.filterBy = filterBy
        self.filterValue = filterValue
        self.orderBy = orderBy
        self.ascending = ascending
        self.showFields = showFields
        self.cropped = cropped
        self.fromHead = fromHead
        self.numberOfLines = numberOfLines

    def setFilter(self, filterBy, filterValue):
        self.filterBy = filterBy
        self.filterValue = filterValue
        self.renderList()

    def setOrder(self, orderBy, ascending):
        self.orderBy = orderBy
        self.ascending = ascending
        self.renderList()

    def setSelection(self, showFields):
        self.showFields = showFields
        self.renderList()

    def setCropping(self, cropped, fromHead, numberOfLines):
        self.cropped = cropped
        self.fromHead = fromHead
        self.numberOfLines = numberOfLines
        self.renderList()

    def dropMissing(self):
        self.df = self.df.dropna(how="any")
        self.renderList()

    def getTypes(self):
        print(self.df.dtypes)

    def renderList(self):
        result = self.df
        if (self.filterBy != None):
            result = result[result[self.filterBy] == self.filterValue]
        if (self.orderBy != None):
            result = result.sort_values(by=self.orderBy, ascending=self.ascending)
        if (self.cropped):
            if (self.fromHead):
                result = result.head(self.numberOfLines)
            else:
                result = result.tail(self.numberOfLines)
        if ((self.showFields != None) and (self.showFields != [])):
            result = result[self.showFields]
        self.list = result

    def printList(self):
        print(self.list)
        f = open("temp_data.txt", "w")
        f.write(self.list.to_string())
        f.close()


df = pd.read_csv('dataset.csv')
df["item_id"] = df["item_id"].astype("string")
df["user_id"] = df["user_id"].astype("string")
df["rating"] = df["rating"].astype("int64")
df["timestamp"] = df["timestamp"].astype("datetime64[ns]")
df["size"] = df["size"].astype("float64")
df["fit"] = df["fit"].astype("category")
df["user_attr"] = df["user_attr"].astype("category")
df["model_attr"] = df["model_attr"].astype("category")
df["category"] = df["category"].astype("category")
df["brand"] = df["brand"].astype("string")
df["year"] = pd.to_datetime(df["year"], format='%Y')
df["split"] = df["split"].astype("category")
print(df.dtypes)

#%% Test
temp = df.groupby("category").count()
print(temp)
plt.show()

#%% Top 20 highest-rated items in "Outerwear" category.
# Useful to determine the best items in this category.
productList = ProductList(df)
productList.renderList()
productList.setFilter("category", "Outerwear")
productList.list = productList.list.groupby("item_id")["rating"].mean().sort_values(ascending=True).tail(20)
productList.printList()
plt.title('Top 20 highest-rated items in "Outerwear" category.')
productList.list.plot.barh(figsize=(10.24,7.68))
plt.xlabel("Rating (out of 5)")
plt.savefig('plots/bar_1.png')
plt.show()

#%% 20 most-rated items in "Outerwear" category.
# Useful to determine the best items in this category.
productList = ProductList(df)
productList.renderList()
productList.setFilter("category", "Outerwear")
productList.list = productList.list.groupby("item_id")["rating"].count().sort_values(ascending=True).tail(20)
productList.printList()
plt.title('Top 20 most-rated items in "Outerwear" category.')
productList.list.plot.barh(figsize=(10.24,7.68))
plt.xlabel("Number of ratings")
plt.savefig('plots/bar_2.png')
plt.show()

#%% 20 highest- and lowest-rated items in "Outerwear" category.
# Useful to determine the best and the worst items in this category.
productList = ProductList(df)
productList.renderList()
# plot 1:
productList.setFilter("category", "Outerwear")
productList.list = productList.list.groupby("item_id")["rating"].mean().sort_values(ascending=True).tail(20)
productList.printList()
plt.subplot(1, 2, 1)
plt.xlim([0, 5.1])
plt.title('20 highest-rated Outerwear.')
productList.list.plot.barh(figsize=(10.24,7.68))
plt.xlabel("Rating (out of 5)")
# plot 2:
productList.setFilter("category", "Outerwear")
productList.list = productList.list.groupby("item_id")["rating"].mean().sort_values(ascending=True).head(20)
productList.printList()
plt.subplot(1, 2, 2)
plt.xlim([0, 5.1])
plt.title('20 lowest-rated Outerwear.')
productList.list.plot.barh(figsize=(10.24,7.68))
plt.xlabel("Rating (out of 5)")
plt.ylabel("")
# save and show
plt.savefig('plots/bar_3.png')
plt.show()

#%% Top 20 users with most ratings of all time.
# Useful to determine the most helpful users of all time.
productList = ProductList(df)
productList.renderList()
productList.list = productList.list.groupby("user_id")["rating"].count().sort_values(ascending=True).tail(20)
productList.printList()
plt.title('Top 20 users with most ratings of all time.')
productList.list.plot.barh(figsize=(10.24,7.68))
plt.xlabel("Number of ratings")
plt.savefig('plots/bar_4.png')
plt.show()

#%% Sales share of brands in "year" 2016.
# Useful to compare the performances of several brands during this year.
productList = ProductList(df)
productList.renderList()
productList.list = productList.list[productList.list["timestamp"].dt.year == 2016]
productList.list = productList.list.groupby("brand").size()
threshold = 50
temp = productList.list[productList.list >= threshold]
temp = temp.sort_values()
temp["Other"] = productList.list[productList.list < threshold].sum()
productList.list = temp
productList.printList()
myexplode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2]
plt.title('Sales percentages by brand in 2016.')
productList.list.plot.pie(shadow=True, explode=myexplode, autopct='%1.1f%%', label="", fontsize=9, figsize=(10.24,7.68))
plt.savefig('plots/pie_1.png')
plt.show()

#%% All-time size distribution of items that mostly satisfied customers.
# Useful to determine the most frequent sizes that are bought by the targeted customer group.
productList = ProductList(df)
productList.renderList()
# productList.setFilter("year", "2017")
productList.list = productList.list[(productList.list["fit"] == "Slightly small") | (productList.list["fit"] == "Just right") | (productList.list["fit"] == "Slightly large")]
temp = productList.list.groupby("size").size()
print(temp)
productList.list = productList.list["size"].dropna()
# productList.printList()
plt.title('All-time size distribution of items that mostly fitted customers.')
productList.list.plot.hist(bins=8, figsize=(10.24,7.68))
plt.xlabel("Size")
plt.savefig('plots/hist_1.png')
plt.show()

#%% Sales trends of top 3 "brand"s by month/year.
# Useful to compare the success of top brands over time.
productList = ProductList(df)
productList.renderList()

temp1 = productList.list[productList.list["brand"] == "ModCloth"]
temp1 = temp1.groupby([(productList.list["timestamp"].dt.year),(productList.list["timestamp"].dt.month)]).size()
print(temp1)
temp2 = productList.list[productList.list["brand"] == "Chi Chi London"]
temp2 = temp2.groupby([(productList.list["timestamp"].dt.year),(productList.list["timestamp"].dt.month)]).size()

temp3 = productList.list[productList.list["brand"] == "Retrolicious"]
temp3 = temp3.groupby([(productList.list["timestamp"].dt.year),(productList.list["timestamp"].dt.month)]).size()

temp4 = pd.concat([temp1, temp2, temp3], axis=1)
temp4.rename(columns={0: "ModCloth", 1: "Chi Chi London", 2: "Retrolicious"}, inplace=True)
print(temp4)
temp4.plot(figsize=(10.24,7.68))

plt.title('Sales trends of 3 biggest competitors between Jan. 2011 and Jun. 2019.')
plt.xlabel('Time')
plt.ylabel('Number of sales')
plt.savefig('plots/line_1.png')
plt.show()

#%% 20 highest-rated items in "Dresses" category, with the number of ratings of each.
# Useful to determine the best items in this category with higher validity.
temp_df1 = df[df["category"] == "Dresses"].groupby("item_id")["rating"].mean().sort_values(ascending=True).tail(20)
print(temp_df1)
temp_index1 = temp_df1.index.values
print(temp_index1)
plt.subplot(1, 2, 1)
plt.title('20 highest-rated Outerwear.')
temp_df1.plot.barh(figsize=(10.24,7.68))
plt.xlabel("Rating (out of 5)")
# plot 2:
temp_df2 = df[df["item_id"].isin(temp_index1)].groupby("item_id")["rating"].count().reindex(temp_index1)
print(temp_df2)
print(df["item_id"])
print(temp_index1)
plt.subplot(1, 2, 2)
plt.title('Their rating counts.')
temp_df2.plot.barh(figsize=(10.24,7.68))
plt.xlabel("Number of ratings")
# save and show
plt.savefig('plots/bar_3.png')
plt.show()

#%% 20 highest-rated items in "Dresses" category that are rated more than 400 times, and their rating counts.
# Useful to determine the best items in this category more precisely.
temp_df1 = df[df["category"] == "Dresses"]
temp_df1 = temp_df1.set_index("item_id")
temp_df1 = temp_df1[temp_df1.groupby("item_id")["rating"].size() > 300]
temp_df2 = temp_df1.groupby("item_id")["rating"].mean().sort_values(ascending=True).tail(20)
print(temp_df2)
temp_index2 = temp_df2.index.values
print(temp_index2)
plt.subplot(1, 2, 1)
plt.title('20 highest-rated Dresses that are rated over 300 times.')
temp_df2.plot.barh(figsize=(10.24,7.68))
plt.xlabel("Rating (out of 5)")
# plot 2:
temp_df3 = df[df["item_id"].isin(temp_index2)].groupby("item_id")["rating"].count().reindex(temp_index2)
print(temp_df3)
print(df["item_id"])
print(temp_index2)
plt.subplot(1, 2, 2)
plt.title('Their rating counts.')
temp_df3.plot.barh(figsize=(10.24,7.68))
plt.xlabel("Number of ratings")
plt.ylabel("")
plt.savefig('plots/dress_over_400.png')
plt.show()

#%% Sales share of brands in "year" 2016.
# Useful to compare the performances of several brands during this year.
# (This time with percentages pre-calculated manually.)
temp_df1 = df[df["timestamp"].dt.year == 2016]
temp_df1 = temp_df1.groupby("brand").size()
threshold = 50
temp_df2 = temp_df1[temp_df1 >= threshold]
temp_df2 = temp_df2.sort_values()
temp_df2["Other"] = temp_df1[temp_df1 < threshold].sum()
total = temp_df2.sum()
percentage_series = pd.Series(temp_df2 * (100.0/total))
# temp_df3 = pd.DataFrame({"entry_count": temp_df2, "percentages": percentage_series})
print(percentage_series)
myexplode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2]
percentage_series.plot.pie(y="percentages", figsize=(10.24, 7.68), shadow=True, explode=myexplode, autopct='%1.1f%%', label="", fontsize=9, legend=False)
plt.title('Sales percentages by brand in 2016.')
plt.savefig('plots/pie_1.png')
plt.show()

#%% Number of items in each category by each brand.
# Useful to manage and monitor inventory.
item_counts_of_brands_by_category = df.groupby(["category", "brand"])["item_id"].nunique().sort_values()
print(item_counts_of_brands_by_category)
outer_index = list(set(item_counts_of_brands_by_category.index.get_level_values("category").values))
i = 0
threshold = 2
for e in outer_index:
    simplified = item_counts_of_brands_by_category[e][item_counts_of_brands_by_category[e] >= threshold].sort_values()
    simplified["Other"] = item_counts_of_brands_by_category[e][item_counts_of_brands_by_category[e] < threshold].sum()
    i += 1
    plt.subplot(2, 2, i)
    simplified.plot.pie(shadow=True, figsize=(19.20, 10.80))
    plt.ylabel("")
    plt.title('Number of items in ' + e + ' category by each brand.')
plt.savefig('plots/multi-pie_1.png')
plt.show()

#%% Most preferred brands by category.
item_counts_of_brands_by_category = df.groupby(["category", "brand"])["rating"].mean().sort_values()
print(item_counts_of_brands_by_category)
outer_index = list(set(item_counts_of_brands_by_category.index.get_level_values("category").values))
i = 0
threshold = 2
for e in outer_index:
    simplified = item_counts_of_brands_by_category[e][item_counts_of_brands_by_category[e] >= threshold].sort_values()
    simplified["Other"] = item_counts_of_brands_by_category[e][item_counts_of_brands_by_category[e] < threshold].sum()
    simplified = simplified.sort_values(ascending=True).tail(5)
    i += 1
    plt.subplot(2, 2, i)
    simplified.plot.barh(figsize=(19.20, 10.80))
    plt.ylabel("")
    plt.title('Top 5 highest-rated brands in ' + e + ' category.')
    plt.xlim([0, 5.1])
    plt.xlabel("Rating (out of 5)")
plt.savefig('plots/multi-barh_1.png')
plt.show()

#%% Unsolved relation between "timestamp" and "year"
time_and_year = df[["timestamp", "year"]].sort_values(by="timestamp", ascending=False)
time_and_year.plot.scatter(x="timestamp", y="year", figsize=(19.20, 10.80), c='green', s=30, alpha=0.25)
plt.title("Relation between timestamp and year.")
plt.savefig('plots/scatter_1.png')
plt.show()
