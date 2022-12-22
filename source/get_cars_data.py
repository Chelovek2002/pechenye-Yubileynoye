import pandas as pd


def get_country_brand_df() -> pd.DataFrame:
    rename_dict = {
        'Country': 'country',
        'Group': 'group',
        'Type': 'car_type',
        'Maker/Brand': 'brand',
        '2018': 'cars_sold'}

    data = (pd.read_html('../data/cars_data.html')[0]
            .dropna()
            .rename(columns=rename_dict)
            .astype({'cars_sold': 'int64'}))

    country_brand = data[~data.brand.str.contains('Total')]
    country_brand = country_brand[~country_brand.group.str.contains('Other')]

    for ct in country_brand.car_type.unique():
        country_brand = country_brand[~country_brand.group.str.contains(ct, regex=False)]

    country_brand = (
        country_brand
        .drop(columns=['car_type', 'group'])
        .groupby(['country', 'brand']).sum()
        .drop(index=['Uzbekistan', 'Belarus'])
        .reset_index()
    )

    country_brand = country_brand[country_brand.cars_sold > 100]

    country_total = (
        country_brand
        .loc[:, ['country', 'cars_sold']]
        .groupby('country').sum()
        .rename(columns={'cars_sold': 'country_total'})
        .reset_index()
    )

    car_brands_df = (
        country_brand
        .merge(country_total, on='country')
        .assign(share=lambda x: x.cars_sold / x.country_total)
    )
    car_brands_df.brand = car_brands_df.brand.str.replace(r' \(.*', '', regex=True)

    return car_brands_df


country_brand = get_country_brand_df()
