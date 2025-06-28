#!/usr/bin/env python3

"""
Debug script to check if subscribe form is working
"""

import asyncio
import sys
import subprocess
import time
from playwright.async_api import async_playwright

async def debug_full_page():
    """Debug the full page to see if subscribe form is there"""
    
    # Start HTTP server
    print("Starting local HTTP server on port 8080...")
    server_process = subprocess.Popen([
        sys.executable, '-m', 'http.server', '8080'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Give server time to start
    time.sleep(2)
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # Show browser
            page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
            
            # Capture console messages
            console_messages = []
            def log_console(msg):
                console_messages.append(f"{msg.type}: {msg.text}")
                print(f"CONSOLE {msg.type}: {msg.text}")
            
            page.on('console', log_console)
            page.on('pageerror', lambda err: print(f"PAGE ERROR: {err}"))
            
            await page.goto('http://localhost:8080')
            
            # Wait for page to fully load
            await page.wait_for_timeout(5000)
            
            # Check if subscribe section exists
            subscribe_section = await page.locator('#newsletter').count()
            print(f"Subscribe section found: {subscribe_section > 0}")
            
            if subscribe_section > 0:
                # Get subscribe section visibility
                is_visible = await page.locator('#newsletter').is_visible()
                print(f"Subscribe section visible: {is_visible}")
                
                # Get the subscribe section position
                box = await page.locator('#newsletter').bounding_box()
                if box:
                    print(f"Subscribe section position: y={box['y']}, height={box['height']}")
                
                # Scroll to subscribe section
                await page.locator('#newsletter').scroll_into_view_if_needed()
                await page.wait_for_timeout(2000)
            
            # Take a very long screenshot
            await page.screenshot(path='debug-full-page.png', full_page=True)
            print("Full page screenshot saved: debug-full-page.png")
            
            # Get page height
            page_height = await page.evaluate('document.body.scrollHeight')
            print(f"Total page height: {page_height}px")
            
            # Check for all sections
            sections = ['#home', '#about', '#blog', '#newsletter', '#contact']
            for section in sections:
                count = await page.locator(section).count()
                visible = await page.locator(section).is_visible() if count > 0 else False
                print(f"Section {section}: exists={count > 0}, visible={visible}")
            
            # Keep browser open for manual inspection
            print("\nBrowser will stay open for 30 seconds for manual inspection...")
            await page.wait_for_timeout(30000)
            
            await browser.close()
            
    finally:
        # Stop server
        server_process.terminate()
        server_process.wait()
        print("\nLocal server stopped")

if __name__ == "__main__":
    asyncio.run(debug_full_page())