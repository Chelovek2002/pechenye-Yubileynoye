# Marketing Analytics. Final Project Report.

*Biktimirova Inna, Batina Viktoria, Smirnova Ksenia, Khasanov Tagir*

## The Problem Overview

Different brands have different associations. 
Brands might strategically influence their customers to create these associations or, vice versa, 
they might adjust their policy to already existing associations. 
In this project we attempted to examine, what is the relation between an association that a brand has, and its sales. 
We were particularly interested in the following question: how associations affect sales of car brands? 
Or, to be more specific – do associations play a role in the difference of sales over countries?

This is a **descriptive** problem, but the results have practical usage. 
They can help decide how a brand should advertise in a given country or, 
if the brand is unable to change already existing associations, what countries it should enter.

Working over the project included several steps:
1. Data collection and processing
2. Exploring brands’ associations, creating relevant topics
3. Scoring brands to match them to derived topics
4. Running regression models:
   - general model 
   - country-specific model
   - additional model
5. Interpreting the results

## Step 1. Data collection and processing

The project extends the second home assignment. Therefore, the used datasets include:
- collage_words.csv (the first dataset from HA2, includes data about associations of people with each brand)
- Categories.csv (the second dataset from HA2, shows categories corresponding to each brand. We used it to extract data specifically on car brands)
- We also scrapped data on car brands’ sales in different countries for the corresponding year from [marklines.com](marklines.com )
and downloaded data on real GDP per capita in 2018 from [worldbank.org](worldbank.org) (in 2015 US dollars).

![country_gdp_brand](https://github.com/Chelovek2002/pechenye-Yubileynoye/blob/0d3315a1ad84c1970ca084ee1556a29acd1d488c/images/img00_country_gdp_brand.png)

## Step 2. Creating relevant topics 

We used LDA to allocate words associated with car brands into topics. 
Testing different values for the number of topics, we figured out that five topics produce the best results 
(easily interpretable topics with little intersection between them). 
We call these topics luxury, rural, power, patriotism (note, that responses were collected in the USA, 
so for other countries it’s most likely an association with the USA, not local patriotism) and finance.

![topics_word_clouds](https://github.com/Chelovek2002/pechenye-Yubileynoye/blob/0d3315a1ad84c1970ca084ee1556a29acd1d488c/images/img01_topics_word_clouds.png)

Then, we used TF–IDF to find the frequencies of all words for every car brand. 
Finally, we picked out the top-50 words for each topic and each car brand from the previous results. 
This data will be used in the following section.

## Step 3. Calculating scores

The goal was to rate to what extent brands are similar to each topic. To do this, we used the jaccard similarity:

![jaccard_similarity_formula](https://github.com/Chelovek2002/pechenye-Yubileynoye/blob/e54e7f578fdf0c5773467d0ac78e220554b46c5d/images/img02_jaccard_similarity_formula.png)

Why not use the scores that LDA provided?
- LDA gives scores so that the sum of scores for categories is equal to one. 
- So, each brand is at least 25% similar to at least one topic. 
- But this is not necessarily true, as a brand may belong to some other categories that do not appear in the collages for some reason.

Why use Jaccard similarity?
- Jaccard similarity ignores duplicates, which is useful in our case. 
The logic is that all words in top-50 are equally related to brand/topic 
- and the difference in scores is only due to the variance in usage of words for describing collages.

However, there is also some noise in the estimation of similarity due to words-outliers. 
Therefore, we also nullified all entries with the score less than 10%. 
Here’s what we obtained (example sample of 5 brands):

![scores](https://github.com/Chelovek2002/pechenye-Yubileynoye/blob/0d3315a1ad84c1970ca084ee1556a29acd1d488c/images/img03_scores.png)

## Step 4. Running regression models 

In order to check if, indeed, there is some relation between the car brand’s sales and the fact that it 
is associated with these five topics, we ran some regression models, 
regressing market shares of brands in different countries on topic scores. 

### General model

We chose the following specification:

![general_reg](https://github.com/Chelovek2002/pechenye-Yubileynoye/blob/0d3315a1ad84c1970ca084ee1556a29acd1d488c/images/img04_general_reg.png)

The obtained results are as follows:

![general_reg_results](https://github.com/Chelovek2002/pechenye-Yubileynoye/blob/0d3315a1ad84c1970ca084ee1556a29acd1d488c/images/img05_general_reg_results.png)

All coefficients on the variables of interest are statistically significant, meaning that indeed, there is a general influence of associations with these five topics on the brand’s market share. For example, associating with luxury decreases the brand’s share by 0.1 and associating with power increases it by 0.1. The full version of the table can be found in the file with code.

### Country specific model

The second regression that was implemented is country-focused. It estimates the dependence of brand’s market share on topic scores in each of 57 countries separately. Thus, we found coefficients that show how one percent change in the score affects car sales. However, as we can see from the example of China (in the table below), there are some countries in which all coefficients are statistically insignificant. It means that residents of such countries rely on some other factors when choosing a car. Associations with topics are not important for them.

Other countries have 1 (in the majority of cases) or even more statistically significant coefficients. For example, in Italy if some brand is associated with luxury, its market share here decreases by 12.44%. Hence, while other topics are not really substantial for Italians, the luxury of some cars reduces their sales in this country. 

One more example is Greece, whereas many as 3 topics are significant. As we can see in the table, power and patriotism positively affect car sales, while associations with finance have the negative effect.

### Additional model of GDP-scores relationship

We also wanted to know if associations depend on GDP and not some innate quality. So we ran a simple linear regression of coefficients on GDP.

![additional_reg_results](https://github.com/Chelovek2002/pechenye-Yubileynoye/blob/0d3315a1ad84c1970ca084ee1556a29acd1d488c/images/img06_additional_reg_results.png)

The only significant coefficient is for luxury, but it isn’t big in a real-world sense.

## Summing up the results

![summary_corr_plot](https://github.com/Chelovek2002/pechenye-Yubileynoye/blob/0d3315a1ad84c1970ca084ee1556a29acd1d488c/images/img07_summary_corr_plot.png)

We came up with this table of correlative results. We can see that associations mostly don’t correlate with brands’ market shares (it means that other qualities, such as, for example, quality, affect them). An example of interpretation is: “rural” brands perform very well in India, compared to other brands.

As for recommendations for brands, an example would be: “rural” brands perform very well in India, compared to other brands, so you should advertise your brand as rural if it is sensical. 
Also, luxurious brands should maybe avoid more wealthy countries.

However, all these recommendations are for brands that want to have a prominent quantity share of cars.  Profit isn’t taken into account due to peculiarity of data.

### Notes about results validity

There are several things that could be potentially improved if extending this research:

1. We used market shares, based on quantity, due to scarcity of data. However, revenue-based market shares would probably better reflect positions of brands in the market;
2. Some control variables could be included into regressions to separate the effect of associations from other effects on market shares;
3. We had the dataset for one year only, but looking at dynamics in car sales and associations would be helpful.


