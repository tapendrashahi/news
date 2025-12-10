#!/usr/bin/env python
"""Test Groq API integration"""
import os
from dotenv import load_dotenv

load_dotenv()

# Test 1: Direct Groq API
print("=" * 60)
print("Test 1: Testing Groq API directly")
print("=" * 60)

try:
    from groq import Groq
    
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Write a one-sentence news headline about AI."}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    print(f"✅ Groq API working!")
    print(f"Model: llama-3.3-70b-versatile")
    print(f"Response: {completion.choices[0].message.content}")
    print()
    
except Exception as e:
    print(f"❌ Groq API failed: {e}")
    print()

# Test 2: LangChain Groq
print("=" * 60)
print("Test 2: Testing LangChain Groq integration")
print("=" * 60)

try:
    from langchain_groq import ChatGroq
    
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        groq_api_key=os.getenv('GROQ_API_KEY')
    )
    
    response = llm.invoke("Write a one-sentence news headline about technology.")
    
    print(f"✅ LangChain Groq working!")
    print(f"Response: {response.content}")
    print()
    
except Exception as e:
    print(f"❌ LangChain Groq failed: {e}")
    print()

# Test 3: Compare Groq vs Gemini speed
print("=" * 60)
print("Test 3: Speed comparison - Groq vs Gemini")
print("=" * 60)

import time

# Test Groq speed
try:
    from langchain_groq import ChatGroq
    
    llm_groq = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv('GROQ_API_KEY')
    )
    
    start = time.time()
    response = llm_groq.invoke("Write a 50-word news article about artificial intelligence.")
    groq_time = time.time() - start
    
    print(f"⚡ Groq (Llama 3.3 70B): {groq_time:.2f}s")
    print(f"Response length: {len(response.content)} chars")
    print()
    
except Exception as e:
    print(f"❌ Groq speed test failed: {e}")
    groq_time = None

# Test Gemini speed
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    llm_gemini = ChatGoogleGenerativeAI(
        model="gemini-exp-1206",
        google_api_key=os.getenv('GEMINI_API_KEY')
    )
    
    start = time.time()
    response = llm_gemini.invoke("Write a 50-word news article about artificial intelligence.")
    gemini_time = time.time() - start
    
    print(f"🤖 Gemini (3 Pro): {gemini_time:.2f}s")
    print(f"Response length: {len(response.content)} chars")
    print()
    
except Exception as e:
    print(f"❌ Gemini speed test failed: {e}")
    gemini_time = None

# Compare
if groq_time and gemini_time:
    if groq_time < gemini_time:
        speedup = gemini_time / groq_time
        print(f"🏆 Groq is {speedup:.1f}x faster than Gemini!")
    else:
        speedup = groq_time / gemini_time
        print(f"🏆 Gemini is {speedup:.1f}x faster than Groq!")

print()
print("=" * 60)
print("All tests completed!")
print("=" * 60)
