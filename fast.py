#!/usr/bin/env python3
"""
AWS DevOps Strands Agent - Fast Entry Point

Ultra-fast knowledge-only agent for instant responses.

This entry point provides a lightweight interface to the fast agent,
optimized for quick AWS DevOps questions without external tool calls.

Usage:
    python3 fast.py

Features:
    - Instant responses (< 1 second)
    - Knowledge-only (no external API calls)
    - Optimized for common AWS DevOps questions
    - Interactive CLI interface
"""

import sys
import os
from pathlib import Path

def setup_path() -> None:
    """Add src directory to Python path for module imports."""
    src_path = Path(__file__).parent / 'src'
    if src_path.exists() and str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

def main() -> int:
    """Main entry point with proper error handling."""
    try:
        setup_path()
        from core.fast_agent import main as fast_main
        return fast_main()
    except ImportError as e:
        print(f"❌ Failed to import required modules: {e}")
        print("💡 Make sure you're running from the project root directory")
        print("💡 Install dependencies with: pip install -r requirements.txt")
        return 1
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Check your AWS credentials and configuration")
        return 1

if __name__ == "__main__":
    sys.exit(main())