#!/usr/bin/env python3
"""
Simple test script to understand MCP server communication

This script demonstrates:
1. How to start our MCP server
2. Basic tool discovery
3. Simple tool execution
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path

async def test_mcp_server():
    """Test our MCP server basic functionality"""
    
    print("🧪 Testing MCP Server Basic Functionality")
    print("=" * 50)
    
    # Path to our server
    server_path = Path(__file__).parent / "src" / "mcp_bedrock_kb" / "server.py"
    
    try:
        # Start the server process
        print("1. Starting MCP server...")
        process = subprocess.Popen(
            [sys.executable, str(server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Test 1: Initialize connection
        print("2. Testing initialization...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            print(f"   ✅ Server initialized: {response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")
        
        # Test 2: List tools
        print("3. Testing tool discovery...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        process.stdin.write(json.dumps(tools_request) + "\n")
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            tools = response.get('result', {}).get('tools', [])
            print(f"   ✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"      - {tool.get('name')}: {tool.get('description')}")
        
        # Test 3: Call a tool
        print("4. Testing tool execution...")
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "query_strands_docs",
                "arguments": {"query": "What is AWS Strands?"}
            }
        }
        
        process.stdin.write(json.dumps(call_request) + "\n")
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            content = response.get('result', {}).get('content', [])
            if content:
                print(f"   ✅ Tool response: {content[0].get('text', 'No text')[:100]}...")
        
        print("\n🎉 Basic MCP server test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        if 'process' in locals():
            process.terminate()
            process.wait()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())

print("end of file")