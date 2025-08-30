#!/usr/bin/env python3
"""
Strands Agent Persistent Conversation System - Knowledge Base Enhanced Implementation

This implementation uses specific Strands API knowledge from the knowledge base
to create a robust session management system with both local and cloud storage options.
"""

import os
import sys
import time
import boto3
from typing import Optional

# Strands imports - exact paths from knowledge base
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands.session.s3_session_manager import S3SessionManager


class PersistentConversationManager:
    """
    Manages persistent conversations using Strands session management.
    
    Based on knowledge base information about FileSessionManager and S3SessionManager,
    this implementation provides both local and cloud-based session persistence.
    """
    
    def __init__(self, session_id: str, use_s3: bool = False, 
                 s3_bucket: Optional[str] = None, storage_dir: Optional[str] = None):
        """
        Initialize the conversation manager with appropriate session storage.
        
        Args:
            session_id: Unique identifier for the session
            use_s3: Whether to use S3 for session storage (default: False for local)
            s3_bucket: S3 bucket name (required if use_s3=True)
            storage_dir: Local storage directory (optional, defaults to temp)
        """
        self.session_id = session_id
        self.use_s3 = use_s3
        
        # Create session manager based on storage type
        if use_s3:
            if not s3_bucket:
                raise ValueError("S3 bucket name required when use_s3=True")
            
            # Create S3 session manager with knowledge base configuration
            boto_session = boto3.Session(region_name="us-west-2")
            self.session_manager = S3SessionManager(
                session_id=session_id,
                bucket=s3_bucket,
                prefix="strands-sessions/",  # Organize sessions with prefix
                boto_session=boto_session,
                region_name="us-west-2"
            )
            print(f"✅ Initialized S3 session manager (bucket: {s3_bucket})")
        else:
            # Create file session manager with knowledge base configuration
            self.session_manager = FileSessionManager(
                session_id=session_id,
                storage_dir=storage_dir or "./sessions"  # Default to local sessions dir
            )
            print(f"✅ Initialized file session manager (dir: {storage_dir or './sessions'})")
        
        # Create agent with session manager - automatic persistence enabled
        self.agent = Agent(session_manager=self.session_manager)
        print(f"✅ Agent created with session ID: {session_id}")
    
    def start_conversation(self):
        """
        Start or resume a conversation with the agent.
        
        The session manager automatically handles:
        - Agent initialization with existing state
        - Message persistence on each interaction
        - State synchronization after agent invocation
        """
        print(f"\n🤖 Starting conversation with session: {self.session_id}")
        print("💡 Type 'quit' to exit, 'restart' to simulate app restart")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() == 'quit':
                    print("👋 Goodbye! Session has been saved.")
                    break
                elif user_input.lower() == 'restart':
                    print("🔄 Simulating application restart...")
                    self._simulate_restart()
                    continue
                elif not user_input:
                    continue
                
                # Agent call with automatic persistence
                # Knowledge base shows this pattern persists messages automatically
                response = self.agent(user_input)
                print(f"\nAgent: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Session saved. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Session state has been preserved.")
    
    def _simulate_restart(self):
        """
        Simulate application restart by recreating the agent with same session.
        
        This demonstrates the session persistence capability - the agent
        should resume with all previous conversation history and state intact.
        """
        print("📱 Recreating agent from persisted session...")
        
        # Recreate session manager and agent - same configuration
        if self.use_s3:
            boto_session = boto3.Session(region_name="us-west-2")
            self.session_manager = S3SessionManager(
                session_id=self.session_id,
                bucket=self.session_manager.bucket,  # Use same bucket
                prefix="strands-sessions/",
                boto_session=boto_session,
                region_name="us-west-2"
            )
        else:
            self.session_manager = FileSessionManager(
                session_id=self.session_id,
                storage_dir=self.session_manager.storage_dir  # Use same directory
            )
        
        # Create new agent instance - should restore from session automatically
        self.agent = Agent(session_manager=self.session_manager)
        print("✅ Agent recreated - conversation history should be restored!")
        print("💬 Try asking: 'What did we talk about before?'")


def main():
    """
    Main function demonstrating both local and cloud session management.
    """
    print("🎯 Strands Agent Persistent Conversation Demo")
    print("=" * 50)
    
    # Get session configuration from user
    session_id = input("Enter session ID (or press Enter for 'demo-session'): ").strip()
    if not session_id:
        session_id = "demo-session"
    
    storage_choice = input("Use S3 storage? (y/N): ").strip().lower()
    use_s3 = storage_choice == 'y'
    
    s3_bucket = None
    storage_dir = None
    
    if use_s3:
        s3_bucket = input("Enter S3 bucket name: ").strip()
        if not s3_bucket:
            print("❌ S3 bucket name required for S3 storage")
            return
    else:
        storage_dir = input("Enter storage directory (or press Enter for './sessions'): ").strip()
        if not storage_dir:
            storage_dir = "./sessions"
    
    try:
        # Create conversation manager with knowledge base-informed configuration
        manager = PersistentConversationManager(
            session_id=session_id,
            use_s3=use_s3,
            s3_bucket=s3_bucket,
            storage_dir=storage_dir
        )
        
        # Start the conversation
        manager.start_conversation()
        
    except Exception as e:
        print(f"❌ Failed to initialize conversation manager: {e}")
        print("💡 Make sure you have proper AWS credentials if using S3")
        print("💡 Make sure the strands library is installed: pip install strands")


if __name__ == "__main__":
    main()
