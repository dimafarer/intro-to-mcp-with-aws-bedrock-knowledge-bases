#!/usr/bin/env python3
"""
Proper MCP protocol test following initialization sequence
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path

async def test_mcp_protocol():
    """Test MCP server following proper protocol sequence"""
    
    print("🔄 Testing MCP Protocol Sequence")
    print("=" * 40)
    
    server_path = Path(__file__).parent / "src" / "mcp_bedrock_kb" / "server.py"
    
    try:
        process = subprocess.Popen(
            [sys.executable, str(server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Step 1: Initialize
        print("1. Initializing...")
        init_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1.0"}
            }
        }
        
        process.stdin.write(json.dumps(init_msg) + "\n")
        process.stdin.flush()
        
        init_response = process.stdout.readline()
        print(f"   Response: {init_response.strip()}")
        
        # Step 2: Send initialized notification
        print("2. Sending initialized notification...")
        initialized_msg = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }
        
        process.stdin.write(json.dumps(initialized_msg) + "\n")
        process.stdin.flush()
        
        # Step 3: List tools
        print("3. Listing tools...")
        tools_msg = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        process.stdin.write(json.dumps(tools_msg) + "\n")
        process.stdin.flush()
        
        tools_response = process.stdout.readline()
        print(f"   Response: {tools_response.strip()}")
        
        # Step 4: Call tool
        print("4. Calling tool...")
        call_msg = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "query_strands_docs",
                "arguments": {"query": "What is AWS Strands?"}
            }
        }
        
        process.stdin.write(json.dumps(call_msg) + "\n")
        process.stdin.flush()
        
        call_response = process.stdout.readline()
        print(f"   Response: {call_response.strip()}")
        
        print("\n✅ MCP protocol test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'process' in locals():
            process.terminate()
            process.wait()

if __name__ == "__main__":
    asyncio.run(test_mcp_protocol())
