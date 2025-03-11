import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import configparser

config = configparser.ConfigParser()
config.read('config.properties')

# Get the template folder path from the properties file
product_catalog_file_path = config.get('ProductCatalog', 'file_path')

# Load the catalog (assuming you have the catalog in a CSV file)
catalog_df = pd.read_csv(product_catalog_file_path)




def recommend_products(input_description, catalog_df, top_n=5):
    '''
    Function to recommend products based on description and name similarity
    This function can be however improved taking other mertics into consideration
    or can be implimented as RAG model
    
    '''
    # Combine product name and description to create a combined field
    catalog_df['combined'] = catalog_df['description']
    
    # Combine input description and the product descriptions from the catalog
    input_combined = input_description  # Here input is treated as "input_combined" (name + description)
    
    # Add the input combined field at the start of the descriptions
    descriptions = catalog_df['combined'].tolist()
    descriptions.insert(0, input_combined)  # Add the input description at the start

    # Use TF-IDF vectorizer to convert descriptions to numerical vectors
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions)

    # Calculate cosine similarity between input combined description and all catalog descriptions
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()


    # Get top N most similar products
    similar_indices = cosine_similarities.argsort()[-top_n:][::-1]
    
    recommendations = []
    for idx in similar_indices:
        product = catalog_df.iloc[idx]
        recommendations.append({
            'Product Name': product['name'],
            'Description': product['description'],
            'Price': product['price'],
            'Product Link': product['link'],
            'Cosine Similarity': cosine_similarities[idx]  # Add the similarity score for debugging
        })

    return recommendations



def checkRecommendation(prod_list):
    '''
    method to check the recommendation, it will loop through the list and gets the most similar product
    based on cosinie similarity
    '''
    list_items = []
    for item in prod_list:
        item = item.strip()
        rec = recommend_products(item, catalog_df)
        list_items.append(rec)  # Store recommendations if needed
    return list_items