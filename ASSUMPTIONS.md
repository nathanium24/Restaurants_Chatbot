# Assumptions and Special Decisions


## 1. Scraping Source
- Zomato’s `robots.txt` file does not allow automated scraping.
- Uses a minimal dataset (5-10 restaurants), only for this project.
- Implements respectful scraping practices:
  - Rate limiting and delays between requests
  - Proper user agent headers
  - No excessive server load
  - Data used solely for demonstration

## 2. Choice of LLM Model
- After thorough evaluation of various open-source models available on Hugging Face, I observed that their responses for restaurant-specific queries required further refinement to meet quality standards.
- Final Selection:
  - **Google's Gemini 2.0 Flash (Free Version)** emerged as the optimal choice for response generation, offering:
    - Enhanced response accuracy
    - Efficient processing times
    - Reliable accessibility


## 3. Embedding Model and Retrieval Strategy
- **Embedding Generation:**  
  Used the **llama-text-embed-v2** model integrated with Pinecone for generating high-quality embeddings, as evidenced in the vector store configuration.
- **Vector Database:**  
  Stored embeddings in **Pinecone**, chosen for its:
  - Low latency querying
  - Simple integration
  - AWS cloud deployment
  - Reliable performance
- **Retrieval Strategy:**  
  - Implemented hybrid search combining restaurant and menu item vectors
  - Namespace-based organization ("Example" namespace)
  - Top-k similarity search with configurable results
  - Async operations for better performance


## 4. Scraping Strategy
- Scraped **5 to 10 restaurants** as per the project guidelines.
- Ensured sufficient diversity in cuisine types, price ranges, and ratings.

