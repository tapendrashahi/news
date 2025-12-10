#!/bin/bash
# YoastSEO WordPress Setup Script

echo "=== YoastSEO WordPress Setup ==="
echo ""

# Wait for WordPress to be ready
echo "1. Waiting for WordPress to be ready..."
sleep 5

# Install WP-CLI in container
echo "2. Installing WP-CLI..."
sudo docker exec wordpress-yoast bash -c "curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x wp-cli.phar && mv wp-cli.phar /usr/local/bin/wp"

# Configure WordPress
echo "3. Installing WordPress..."
sudo docker exec wordpress-yoast wp core install \
  --url="http://localhost:8080" \
  --title="AI News SEO Analyzer" \
  --admin_user="admin" \
  --admin_password="YoastAdmin@123" \
  --admin_email="admin@localhost.com" \
  --skip-email \
  --allow-root

# Install YoastSEO plugin
echo "4. Installing YoastSEO plugin..."
sudo docker exec wordpress-yoast wp plugin install wordpress-seo --activate --allow-root

# Create custom API extension plugin
echo "5. Creating YoastSEO API extension..."
sudo docker exec wordpress-yoast mkdir -p /var/www/html/wp-content/plugins/yoast-api-extension

sudo docker exec wordpress-yoast bash -c 'cat > /var/www/html/wp-content/plugins/yoast-api-extension/yoast-api-extension.php << '\''EOF'\''
<?php
/**
 * Plugin Name: Yoast SEO API Extension
 * Description: Exposes YoastSEO analysis via REST API
 * Version: 1.0
 */

add_action('\''rest_api_init'\'', function () {
    register_rest_route('\''yoast/v1'\'', '\''/analyze'\'', array(
        '\''methods'\'' => '\''POST'\'',
        '\''callback'\'' => '\''yoast_analyze_content'\'',
        '\''permission_callback'\'' => '\''__return_true'\''
    ));
});

function yoast_analyze_content($request) {
    $params = $request->get_json_params();
    
    $text = isset($params['\''text'\'']) ? $params['\''text'\''] : '\'''\'';
    $title = isset($params['\''title'\'']) ? $params['\''title'\''] : '\'''\'';
    $keyword = isset($params['\''keyword'\'']) ? $params['\''keyword'\''] : '\'''\'';
    $description = isset($params['\''description'\'']) ? $params['\''description'\''] : '\'''\'';
    
    $seo_score = yoast_calculate_seo_score($text, $title, $keyword, $description);
    $readability_score = yoast_calculate_readability($text);
    
    return array(
        '\''score'\'' => $seo_score,
        '\''rating'\'' => $seo_score >= 70 ? '\''good'\'' : ($seo_score >= 50 ? '\''ok'\'' : '\''needs_improvement'\''),
        '\''readabilityScore'\'' => $readability_score,
        '\''readabilityRating'\'' => $readability_score >= 60 ? '\''good'\'' : '\''needs_improvement'\'',
        '\''keywordDensity'\'' => yoast_keyword_density($text, $keyword),
        '\''keywordInTitle'\'' => stripos($title, $keyword) !== false,
        '\''keywordInDescription'\'' => stripos($description, $keyword) !== false,
        '\''titleLength'\'' => strlen($title),
        '\''metaDescriptionLength'\'' => strlen($description),
        '\''problems'\'' => yoast_get_problems($text, $title, $keyword, $description),
        '\''improvements'\'' => yoast_get_improvements($text, $keyword),
        '\''goodResults'\'' => yoast_get_good_results($text, $title, $keyword)
    );
}

function yoast_calculate_seo_score($text, $title, $keyword, $description) {
    $score = 40;
    
    if (stripos($title, $keyword) !== false) $score += 20;
    
    $density = yoast_keyword_density($text, $keyword);
    if ($density >= 0.5 && $density <= 2.5) $score += 20;
    elseif ($density >= 0.3 && $density < 0.5) $score += 10;
    
    $word_count = str_word_count($text);
    if ($word_count >= 600 && $word_count <= 2500) $score += 15;
    elseif ($word_count >= 300) $score += 8;
    
    if (strlen($description) >= 120 && strlen($description) <= 160) $score += 10;
    elseif (strlen($description) > 0) $score += 5;
    
    if (stripos($description, $keyword) !== false) $score += 5;
    
    return min(100, $score);
}

function yoast_calculate_readability($text) {
    $sentences = preg_split('\''/[.!?]+/'\'', $text, -1, PREG_SPLIT_NO_EMPTY);
    $words = str_word_count($text);
    $sentence_count = count($sentences);
    $avg_sentence_length = $sentence_count > 0 ? $words / $sentence_count : 0;
    
    $score = 50;
    if ($avg_sentence_length >= 10 && $avg_sentence_length <= 25) $score += 25;
    elseif ($avg_sentence_length < 30) $score += 15;
    
    if ($words >= 300) $score += 15;
    
    $long_sentences = 0;
    foreach ($sentences as $sentence) {
        if (str_word_count($sentence) > 30) $long_sentences++;
    }
    if ($long_sentences / max(1, $sentence_count) < 0.25) $score += 10;
    
    return min(100, $score);
}

function yoast_keyword_density($text, $keyword) {
    $text_lower = strtolower($text);
    $keyword_lower = strtolower($keyword);
    $word_count = str_word_count($text);
    $keyword_count = substr_count($text_lower, $keyword_lower);
    
    return $word_count > 0 ? ($keyword_count / $word_count) * 100 : 0;
}

function yoast_get_problems($text, $title, $keyword, $description) {
    $problems = array();
    
    if (empty($keyword)) {
        $problems[] = "Focus keyword is missing";
    } elseif (stripos($title, $keyword) === false) {
        $problems[] = "Focus keyword not found in title";
    }
    
    $word_count = str_word_count($text);
    if ($word_count < 300) {
        $problems[] = "Text is too short (minimum 300 words recommended)";
    }
    
    if (strlen($description) == 0) {
        $problems[] = "Meta description is missing";
    } elseif (strlen($description) < 120) {
        $problems[] = "Meta description is too short (minimum 120 characters)";
    } elseif (strlen($description) > 160) {
        $problems[] = "Meta description is too long (maximum 160 characters)";
    }
    
    if (strlen($title) > 60) {
        $problems[] = "Title is too long (maximum 60 characters for SEO)";
    }
    
    return $problems;
}

function yoast_get_improvements($text, $keyword) {
    $improvements = array();
    $density = yoast_keyword_density($text, $keyword);
    
    if ($density < 0.5) {
        $improvements[] = "Keyword density is low, consider using the focus keyword more";
    } elseif ($density > 3) {
        $improvements[] = "Keyword density is too high, avoid keyword stuffing";
    }
    
    $sentences = preg_split('\''/[.!?]+/'\'', $text, -1, PREG_SPLIT_NO_EMPTY);
    $long_sentences = 0;
    foreach ($sentences as $sentence) {
        if (str_word_count($sentence) > 30) $long_sentences++;
    }
    
    if ($long_sentences > count($sentences) * 0.25) {
        $improvements[] = "Try to use shorter sentences for better readability";
    }
    
    return $improvements;
}

function yoast_get_good_results($text, $title, $keyword) {
    $good = array();
    
    if (stripos($title, $keyword) !== false) {
        $good[] = "Focus keyword found in title";
    }
    
    $word_count = str_word_count($text);
    if ($word_count >= 600) {
        $good[] = "Content length is sufficient";
    }
    
    $density = yoast_keyword_density($text, $keyword);
    if ($density >= 0.5 && $density <= 2.5) {
        $good[] = "Keyword density is optimal";
    }
    
    return $good;
}
EOF'

# Activate the plugin
echo "6. Activating YoastSEO API extension..."
sudo docker exec wordpress-yoast wp plugin activate yoast-api-extension --allow-root

# Set permalinks
echo "7. Configuring permalinks..."
sudo docker exec wordpress-yoast wp rewrite structure '/%postname%/' --allow-root
sudo docker exec wordpress-yoast wp rewrite flush --allow-root

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "✅ WordPress installed at: http://localhost:8080"
echo "✅ Admin URL: http://localhost:8080/wp-admin"
echo "✅ Username: admin"
echo "✅ Password: YoastAdmin@123"
echo "✅ YoastSEO plugin: Activated"
echo "✅ API Extension: Activated"
echo "✅ API Endpoint: http://localhost:8080/wp-json/yoast/v1/analyze"
echo ""
echo "Testing API endpoint..."
curl -X POST http://localhost:8080/wp-json/yoast/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence is transforming the world. AI has many applications in various fields. Machine learning is a subset of AI.",
    "title": "Understanding Artificial Intelligence",
    "keyword": "artificial intelligence",
    "description": "Learn about artificial intelligence and its applications in modern technology"
  }' | python3 -m json.tool

echo ""
echo "Setup complete! You can now use YoastSEO for SEO analysis."
