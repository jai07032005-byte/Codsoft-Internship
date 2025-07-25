import streamlit as st
import pandas as pd

# Use Streamlit's caching to load the data only once, improving performance.
@st.cache_data
def load_data(filepath):
    """
    Loads the restaurant dataset from a CSV file.
    Returns a pandas DataFrame.
    """
    try:
        df = pd.read_csv('Dataset .csv')
        # Basic cleaning: Fill missing Cuisines with 'Unknown'
        df['Cuisines'] = df['Cuisines'].fillna('Unknown')
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{filepath}' was not found. Please make sure it's in the same directory as the script.")
        return None

def recommend_restaurants(df, cuisine, location, price_range):
    """
    This is the core of the Rule-Based AI.
    It filters and ranks restaurants based on explicit, hard-coded rules.
    
    Args:
        df (pd.DataFrame): The full dataframe of restaurants.
        cuisine (str): The desired cuisine to filter by.
        location (str): The desired city to filter by.
        price_range (int): The desired price range (1-4).
        
    Returns:
        pd.DataFrame: A dataframe of recommended restaurants.
    """
    st.write("---")
    st.write("🤖 **AI Assistant:** Applying the following rules...")
    
    # Start with a copy of the full dataset
    filtered_df = df.copy()
    
    # --- RULE 1: Filter by Cuisine ---
    if cuisine:
        st.write(f"- Rule: Must contain the cuisine '{cuisine}'.")
        # The 'str.contains' function is our programmed rule for matching text.
        filtered_df = filtered_df[filtered_df['Cuisines'].str.contains(cuisine, case=False)]

    # --- RULE 2: Filter by Location ---
    if location:
        st.write(f"- Rule: Must be in the city '{location}'.")
        filtered_df = filtered_df[filtered_df['City'].str.contains(location, case=False)]

    # --- RULE 3: Filter by Price Range ---
    if price_range != "Any":
        st.write(f"- Rule: Must have a price range of '{price_range}'.")
        # A direct equality check is our rule for price.
        filtered_df = filtered_df[filtered_df['Price range'] == price_range]
        
    # --- RULE 4: Rank the results based on a quality score ---
    # This formula is another human-defined rule to determine "best".
    if not filtered_df.empty:
        st.write("- Rule: Rank results by 'Aggregate rating' multiplied by 'Votes'.")
        filtered_df['quality_score'] = filtered_df['Aggregate rating'] * filtered_df['Votes']
        ranked_df = filtered_df.sort_values(by='quality_score', ascending=False)
        return ranked_df
    else:
        return pd.DataFrame() # Return an empty dataframe if no matches

# --- Main Streamlit App Interface ---
def main():
    st.title("🍽️ Restaurant Recommendation System")
    st.write(
        "This AI uses a set of **pre-programmed rules** to recommend restaurants. "
        "It does **not** learn from data like a Machine Learning model would."
    )
    
    df = load_data('Dataset.csv')

    if df is not None:
        st.sidebar.header("Your Preferences")
        
        # --- THE MENU (As requested: 1-7) ---
        menu_choice = st.sidebar.radio(
            "On what basis would you like a recommendation?",
            [
                "1. Cuisine, Location, and Price Range",
                "2. Cuisine and Location",
                "3. Cuisine and Price Range",
                "4. Location and Price Range",
                "5. Only by Cuisine",
                "6. Only by Location",
                "7. Only by Price Range"
            ]
        )
        
        # Initialize variables
        cuisine = None
        location = None
        price_range = "Any" # Default to 'Any'
        
        # --- Get User Input Based on Menu Choice ---
        choice_num = int(menu_choice.split('.')[0])
        
        if choice_num in [1, 2, 3, 5]:
            cuisine = st.sidebar.text_input("Enter the desired cuisine (e.g., Italian, Japanese):")
        
        if choice_num in [1, 2, 4, 6]:
            location = st.sidebar.text_input("Enter the desired location (city e.g., Chennai, London):")
        
        if choice_num in [1, 3, 4, 7]:
            price_range = st.sidebar.selectbox(
                "Select the desired price range:",
                ("Any", 1, 2, 3, 4)
            )
        
        # --- The Button to Trigger the AI ---
        if st.sidebar.button("Find Restaurants"):
            if not cuisine and not location and price_range == "Any":
                st.warning("Please provide at least one preference.")
            else:
                results_df = recommend_restaurants(df, cuisine, location, price_range)
                
                st.subheader("🏆 Your Top Recommendations")
                if not results_df.empty:
                    # Display the top 10 results
                    st.dataframe(results_df[['Restaurant Name', 'Cuisines', 'City', 'Price range', 'Aggregate rating', 'Votes']].head(10))
                else:
                    st.error("Sorry, no restaurants found matching your specific rules. Please try a different combination.")

if __name__ == "__main__":
    main()