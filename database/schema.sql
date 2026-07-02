-- =====================================================
-- ShopSmart AI Database
-- =====================================================



USE ai_shopping_copilot;

-- =====================================================
-- USERS
-- =====================================================

CREATE TABLE users (

    user_id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(150) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- =====================================================
-- PRODUCTS
-- =====================================================

CREATE TABLE products (

    product_id INT PRIMARY KEY,

    product_name VARCHAR(300),

    product_description TEXT,

    brand VARCHAR(150),

    category VARCHAR(100),

    subcategory VARCHAR(100),

    price DECIMAL(10,2),

    rating DECIMAL(3,2),

    rating_count INT,

    image_url TEXT,

    product_url TEXT,

    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
-- =====================================================
-- WISHLIST
-- =====================================================

CREATE TABLE wishlist (

    wishlist_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,

    product_id INT,

    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)

        REFERENCES users(user_id)

        ON DELETE CASCADE,

    FOREIGN KEY (product_id)

        REFERENCES products(product_id)

        ON DELETE CASCADE

);

-- =====================================================
-- SEARCH HISTORY
-- =====================================================

CREATE TABLE search_history (

    search_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,

    query TEXT,

    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)

        REFERENCES users(user_id)

        ON DELETE CASCADE

);

-- =====================================================
-- CHAT HISTORY
-- =====================================================

CREATE TABLE chatbot_history (

    chat_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,

    user_message TEXT,

    ai_response TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)

        REFERENCES users(user_id)

        ON DELETE CASCADE

);
-- =====================================================
-- PRODUCT REVIEWS
-- =====================================================

CREATE TABLE product_reviews (

    review_id INT AUTO_INCREMENT PRIMARY KEY,

    product_id INT,

    review_text TEXT,

    rating DECIMAL(3,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id)

        REFERENCES products(product_id)

        ON DELETE CASCADE

);

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX idx_product_category

ON products(category);

CREATE INDEX idx_product_brand

ON products(brand);

CREATE INDEX idx_product_price

ON products(price);

CREATE INDEX idx_product_rating

ON products(rating);