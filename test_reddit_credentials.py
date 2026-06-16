"""Test Reddit API credentials"""
import os
from pathlib import Path

# Load .env manually
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    for line in env_file.read_text().strip().split("\n"):
        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()

print("="*70)
print("REDDIT API CREDENTIALS TEST")
print("="*70)

print("\nEnvironment variables loaded:")
print(f"  ✓ REDDIT_CLIENT_ID: {os.getenv('REDDIT_CLIENT_ID')}")
print(f"  ✓ REDDIT_USER_AGENT: {os.getenv('REDDIT_USER_AGENT')}")
client_secret = os.getenv('REDDIT_CLIENT_SECRET', '')
print(f"  ✓ REDDIT_CLIENT_SECRET: {client_secret[:20]}...")

print("\n" + "="*70)
print("Testing Reddit API connection...")
print("="*70)

try:
    from src.data_collection.reddit_client import create_reddit_client
    
    print("\n🔄 Creating Reddit client...")
    reddit = create_reddit_client()
    
    print("🔄 Fetching posts from r/india...")
    subreddit = reddit.subreddit("india")
    posts = list(subreddit.hot(limit=3))
    
    print(f"\n✅ SUCCESS! Reddit API is working!")
    print(f"✅ Fetched {len(posts)} posts from r/india")
    
    print("\n📰 Sample posts:")
    for i, post in enumerate(posts, 1):
        print(f"\n  {i}. {post.title[:70]}")
        print(f"     └─ Score: {post.score} | Comments: {post.num_comments}")
    
    print("\n" + "="*70)
    print("✅ All systems ready for real-time sentiment analysis!")
    print("="*70)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\n" + "-"*70)
    print("TROUBLESHOOTING STEPS:")
    print("-"*70)
    print("\n1. Verify Reddit App Credentials:")
    print("   - Go to: https://www.reddit.com/prefs/apps")
    print("   - Find your app 'divyanshi'")
    print("   - Copy the Client ID (below app name)")
    print("   - Copy the Client Secret (click 'edit')")
    print("   - Update .env file with correct values")
    print("\n2. Verify App Configuration:")
    print("   - App type should be: 'script'")
    print("   - Redirect URI should be: 'http://localhost:8000'")
    print("\n3. Check Credentials:")
    print(f"   - Current Client ID: {os.getenv('REDDIT_CLIENT_ID')}")
    print(f"   - Current Secret: {os.getenv('REDDIT_CLIENT_SECRET')[:20]}...")
    print("\n4. If still failing, regenerate Client Secret:")
    print("   - Go to app page and click 'regenerate secret'")
    print("   - Update .env file with new value")
