import pandas as pd


def get_country_brand_df(min_sales: int = 500) -> pd.DataFrame:
    # retrieving data and changing columns names
    cars_sales_path = r'https://github.com/Chelovek2002/pechenye-Yubileynoye/blob/3758b9b47eb2db3c5891ba980208eb0489470751/data/cars_data.html'
    rename_dict = {
        'Country': 'country',
        'Group': 'group',
        'Type': 'car_type',
        'Maker/Brand': 'brand',
        '2018': 'car_sales'}

    country_brand = (
        pd.read_html(cars_sales_path)[0]
        .dropna()
        .rename(columns=rename_dict)
        .astype({'car_sales': 'int64'})
    )

    # remove total brand sales and unknown sales
    country_brand = country_brand[~country_brand.brand.str.contains('Total')]
    country_brand = country_brand[~country_brand.group.str.contains('Other')]

    # remove total sales of different car types
    for ct in country_brand.car_type.unique():
        country_brand = country_brand[~country_brand.group.str.contains(ct, regex=False)]

    # group by country and brand
    country_brand = (
        country_brand[['country', 'brand', 'car_sales']]
        .groupby(['country', 'brand']).sum()
        .drop(index=['Uzbekistan', 'Belarus'])  # bad info on these countries
        .reset_index()
    )

    # filter countries with close ot zero sales, as most likely due to bad data
    country_brand = country_brand[country_brand.car_sales > min_sales]

    # compute total sales over each country
    country_total = (
        country_brand[['country', 'car_sales']]
        .groupby('country').sum()
        .rename(columns={'car_sales': 'country_total'})
        .reset_index()
    )

    # compute market shares
    country_brand = (
        country_brand
        .merge(country_total, on='country')
        .assign(share=lambda x: x.car_sales / x.country_total)
    )

    # removing parenthesis in brand names (like `Pontiac (2010)`)
    country_brand.brand = country_brand.brand.str.replace(r' \(.*', '', regex=True)

    # make the brands' names match ones in the survey
    replace_dict = {
        'Mercedes-Benz': 'Mercedes Benz',
        'Chrysler/Jeep': 'Chrysler',
        'Chevrolet/GMC': 'Chevrolet',
        'Opel/Chevrolet': 'Opel',
        'Hyundai/Inokom': 'Hyundai',
        'VW': 'Volkswagen',
        'Volvo Cars': 'Volvo'
    }
    country_brand = country_brand.replace(replace_dict)

    return country_brand


def get_gdp_data() -> pd.DataFrame:
    gdp_path = r'https://github.com/Chelovek2002/pechenye-Yubileynoye/blob/3758b9b47eb2db3c5891ba980208eb0489470751/data/country_gdp.csv'
    # make countries' names match ones in country_brand
    replace_dict = {
        'Czechia': 'Czech Republic',
        'Egypt, Arab Rep.': 'Egypt',
        'Korea, Rep.': 'Korea',
        'Russian Federation': 'Russia',
        'Slovak Republic': 'Slovakia',
        'Turkiye': 'Turkey',
        'United Kingdom': 'UK',
        'United States': 'USA'
    }

    rename_dict = {'Country Name': 'country',
                   '2018 [YR2018]': 'gdp_per_capita'}

    country_gdp = (
        pd.read_csv(gdp_path)
        .rename(columns=rename_dict)
        [['country', 'gdp_per_capita']]
        .dropna()
        .replace(replace_dict)
    )

    # str to int without overflow
    country_gdp.gdp_per_capita = country_gdp.gdp_per_capita.astype(float).astype('int64')

    return country_gdp


def get_country_gdp_brand_df(brand_df: pd.DataFrame, gdp_df: pd.DataFrame) -> pd.DataFrame:
    country_gdp_brand = gdp_df.merge(brand_df, on='country')

    # list of all car brands in the survey
    cats_path = r'https://github.com/Chelovek2002/pechenye-Yubileynoye/blob/3758b9b47eb2db3c5891ba980208eb0489470751/data/Categories.csv'
    cats = pd.read_csv(cats_path).dropna()
    car_brands_list = cats.Brand[cats.Category == "Cars"].tolist()

    country_gdp_brand = country_gdp_brand[country_gdp_brand.brand.isin(car_brands_list)]

    return country_gdp_brand


country_brand_df = get_country_brand_df()
country_gdp_df = get_gdp_data()
country_gdp_brand_df = get_country_gdp_brand_df(country_brand_df, country_gdp_df)

if __name__ == '__main__':
    country_brand_df.to_csv('data/country_brand.csv', index=False)
    country_gdp_brand_df.to_csv('data/country_gdp_brand.csv', index=False)
