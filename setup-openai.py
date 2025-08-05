#!/usr/bin/env python3
"""
OpenAI API Key Setup Script
This script helps you set up your OpenAI API key for the AI Chatbot System.
"""

import os
import sys

def setup_openai_key():
    print("🔑 OpenAI API Key Setup")
    print("=" * 50)
    
    # Check if API key is already set
    current_key = os.getenv("OPENAI_API_KEY")
    if current_key and current_key != "":
        print(f"✅ OpenAI API key is already set: {current_key[:8]}...")
        return True
    
    print("❌ No OpenAI API key found.")
    print("\nTo get an OpenAI API key:")
    print("1. Go to https://platform.openai.com/account/api-keys")
    print("2. Sign up or log in to your OpenAI account")
    print("3. Click 'Create new secret key'")
    print("4. Copy the generated key")
    
    print("\n" + "=" * 50)
    
    # Ask user for API key
    api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⚠️  No API key provided. The AI features will not work.")
        print("You can set the API key later by:")
        print("1. Setting the OPENAI_API_KEY environment variable")
        print("2. Or running this script again")
        return False
    
    # Validate API key format (basic check)
    if not api_key.startswith("sk-"):
        print("❌ Invalid API key format. OpenAI API keys should start with 'sk-'")
        return False
    
    # Set environment variable for current session
    os.environ["OPENAI_API_KEY"] = api_key
    print(f"✅ API key set successfully: {api_key[:8]}...")
    
    # Instructions for permanent setup
    print("\n📝 To make this permanent:")
    print("Windows (PowerShell):")
    print(f'  $env:OPENAI_API_KEY="{api_key}"')
    print("Windows (Command Prompt):")
    print(f'  set OPENAI_API_KEY={api_key}')
    print("Linux/Mac:")
    print(f'  export OPENAI_API_KEY="{api_key}"')
    
    return True

if __name__ == "__main__":
    setup_openai_key() 