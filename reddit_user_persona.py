import requests
import time
from datetime import datetime

def guess_interests_with_sources(posts, comments):
    interest_keywords = {
        'Gaming': ['gaming', 'xbox', 'ps5', 'nintendo', 'steam'],
        'Technology': ['technology', 'programming', 'coding', 'python', 'ai', 'machinelearning'],
        'News & Politics': ['news', 'politics', 'worldnews', 'biden', 'modi'],
        'Memes & Humor': ['memes', 'funny', 'jokes', 'meme'],
        'Fitness & Health': ['fitness', 'gym', 'workout', 'health'],
        'Food': ['food', 'recipes', 'cooking', 'eat'],
        'Science': ['science', 'space', 'nasa', 'quantum'],
        'Relationships': ['relationships', 'dating', 'advice'],
        'Psychology': ['psychology', 'mentalhealth', 'depression', 'anxiety'],
        'Finance': ['stocks', 'investing', 'crypto', 'money'],
        'Education': ['askscience', 'explainlikeimfive', 'homeworkhelp', 'college']
    }

    interests = {}

    def match_keywords(text, source_type, source_data):
        for category, keywords in interest_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    if category not in interests:
                        interests[category] = []
                    interests[category].append((source_type, source_data))
                    return

    for post in posts:
        match_keywords(post['subreddit'], "Post", post)
        match_keywords(post['title'], "Post", post)

    for comment in comments:
        match_keywords(comment['subreddit'], "Comment", comment)
        match_keywords(comment['text'], "Comment", comment)

    return interests

def scrape_reddit_profile(username):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    print(f"\n Scraping data for u/{username}...")

    try:
        posts_url = f"https://www.reddit.com/user/{username}/submitted/.json?limit=10"
        posts_response = requests.get(posts_url, headers=headers)
        posts_response.raise_for_status()
        posts_data = posts_response.json().get('data', {}).get('children', [])

        comments_url = f"https://www.reddit.com/user/{username}/comments/.json?limit=10"
        comments_response = requests.get(comments_url, headers=headers)
        comments_response.raise_for_status()
        comments_data = comments_response.json().get('data', {}).get('children', [])

        user_posts = []
        for post in posts_data[:5]:
            post_data = post.get('data', {})
            user_posts.append({
                'title': post_data.get('title', 'No title'),
                'content': post_data.get('selftext', '')[:200] + '...' if post_data.get('selftext') else '',
                'subreddit': post_data.get('subreddit', 'Unknown'),
                'score': post_data.get('score', 0),
                'url': f"https://reddit.com{post_data.get('permalink', '')}",
                'created': datetime.utcfromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d')
            })

        user_comments = []
        for comment in comments_data[:5]:
            comment_data = comment.get('data', {})
            body = comment_data.get('body', '')
            user_comments.append({
                'text': body[:200] + '...' if len(body) > 200 else body,
                'subreddit': comment_data.get('subreddit', 'Unknown'),
                'score': comment_data.get('score', 0),
                'url': f"https://reddit.com{comment_data.get('permalink', '')}",
                'created': datetime.utcfromtimestamp(comment_data.get('created_utc', 0)).strftime('%Y-%m-%d')
            })

        interests_with_sources = guess_interests_with_sources(user_posts, user_comments)

        return {
            'username': username,
            'posts': user_posts,
            'comments': user_comments,
            'interests': interests_with_sources,
            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    except Exception as e:
        print(f" Error: {str(e)}")
        return None

def create_html_file(data):
    html = f"""
<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>Reddit Persona: u/{data['username']}</title>
<style>
body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
.container {{ max-width: 900px; margin: auto; background: #fff; padding: 20px; border-radius: 10px; }}
.tag {{ display: inline-block; background: #ffe0b2; padding: 6px 12px; margin: 5px; border-radius: 20px; }}
.meta {{ font-size: 0.9em; color: gray; }}
a {{ color: #1e88e5; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
</style></head><body><div class="container">
<h1>u/{data['username']} </h1>
<p class="meta">Generated on {data['scraped_at']}</p>
<h2>Favorites & Interests</h2>
"""

    for category, sources in data['interests'].items():
        source = sources[0][1]
        html += f"<div class='tag'>{category}</div> — based on {sources[0][0]} in <b>r/{source['subreddit']}</b>: <a href='{source['url']}' target='_blank'>View</a><br>"

    html += "<h2>Latest Posts</h2>"
    for post in data['posts']:
        html += f"<div><b>{post['title']}</b><br><p>{post['content']}</p><div class='meta'>r/{post['subreddit']} | {post['created']} | {post['score']} pts</div><a href='{post['url']}' target='_blank'>View Post</a></div><hr>"

    html += "<h2>Latest Comments</h2>"
    for comment in data['comments']:
        html += f"<div><p>{comment['text']}</p><div class='meta'>r/{comment['subreddit']} | {comment['created']} | {comment['score']} pts</div><a href='{comment['url']}' target='_blank'>View Comment</a></div><hr>"

    html += "</div></body></html>"

    with open(f"persona_{data['username']}.html", "w", encoding='utf-8') as f:
        f.write(html)
    print(f" HTML saved as persona_{data['username']}.html")

def create_text_file(data):
    lines = [
        f"User Persona for u/{data['username']}",
        f"Generated on: {data['scraped_at']}",
        "\n=== Interests (with source citations) ==="
    ]

    for category, sources in data['interests'].items():
        source_type, source = sources[0]
        lines.append(f"- {category} (from {source_type} in r/{source['subreddit']})")
        lines.append(f"  Text: {source.get('title') or source.get('text')[:80] + '...'}")
        lines.append(f"  Link: {source['url']}\n")

    lines.append("\n=== Latest Posts ===")
    for post in data['posts']:
        lines.append(f"- {post['title']} (r/{post['subreddit']}, {post['created']}, {post['score']} pts)")
        lines.append(f"  {post['url']}")

    lines.append("\n=== Latest Comments ===")
    for comment in data['comments']:
        lines.append(f"- {comment['text'][:100]} (r/{comment['subreddit']}, {comment['created']}, {comment['score']} pts)")
        lines.append(f"  {comment['url']}")

    with open(f"persona_{data['username']}.txt", "w", encoding='utf-8') as f:
        f.write("\n".join(lines))

    print(f" TXT saved as persona_{data['username']}.txt")

if __name__ == "__main__":
    print(" Reddit Persona Generator ")
    print("----------------------------------------")

    while True:
        url = input("\nEnter Reddit profile URL (e.g., https://www.reddit.com/user/kojied/): ").strip()

        if not url.startswith("https://www.reddit.com/user/"):
            print(" Please enter a valid Reddit profile URL.")
            continue

        username = url.strip('/').split('/')[-1]

        start_time = time.time()
        user_data = scrape_reddit_profile(username)

        if user_data:
            create_html_file(user_data)
            create_text_file(user_data)
            print(f"\n Done in {time.time() - start_time:.2f} seconds")
        else:
            print(" Could not generate persona (user may not exist or is private).")

        again = input("\nGenerate another persona? (y/n): ").strip().lower()
        if again != 'y':
            print(" Exiting...")
            break 