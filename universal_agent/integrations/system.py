import subprocess
import asyncio
from typing import Tuple
import pyautogui
import time

class SystemIntegration:
    def __init__(self):
        # Fail-safe: moving mouse to upper-left corner will abort
        pyautogui.FAILSAFE = True
        
    async def run_command(self, command: str) -> Tuple[str, str]:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout.decode().strip(), stderr.decode().strip()

    async def open_application(self, app_name: str):
        try:
            # Use PowerShell Start-Process to get better error handling
            # -ErrorAction Stop ensures it throws an error if app not found
            cmd = f'powershell -Command "Start-Process \'{app_name}\' -ErrorAction Stop"'
            stdout, stderr = await self.run_command(cmd)
            
            if stderr:
                # If PowerShell returns error text, it failed
                raise Exception(stderr)
                
            # Wait for app to open
            await asyncio.sleep(2) 
            return f"Opened {app_name}"
        except Exception as e:
            # Return a specific failure marker that Orchestrator can catch
            return f"FAILED_TO_OPEN: {e}"

    async def type_text(self, text: str):
        try:
            # Small delay to ensure window is focused
            await asyncio.sleep(0.5)
            
            # Run pyautogui in thread pool since it's blocking
            def _type():
                pyautogui.write(text, interval=0.05)
            
            await asyncio.to_thread(_type)
            return f"Typed: {text}"
        except Exception as e:
            return f"Failed to type text: {e}"

    async def press_key(self, key: str):
        try:
            pyautogui.press(key)
            return f"Pressed: {key}"
        except Exception as e:
            return f"Failed to press key: {e}"

    async def capture_screen(self) -> str:
        try:
            # Capture screen
            screenshot = pyautogui.screenshot()
            
            # Convert to base64
            import io
            import base64
            buffered = io.BytesIO()
            screenshot.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return img_str
        except Exception as e:
            print(f"Screen capture failed: {e}")
            return ""

    async def install_app(self, app_name: str):
        try:
            # Use winget to install
            cmd = f"winget install -e --id {app_name} --accept-source-agreements --accept-package-agreements"
            stdout, stderr = await self.run_command(cmd)
            if "Successfully installed" in stdout or "Found" in stdout:
                return f"Installed {app_name}"
            else:
                return f"Installation output: {stdout} {stderr}"
        except Exception as e:
            return f"Failed to install {app_name}: {e}"

    async def uninstall_app(self, app_name: str):
        try:
            cmd = f"winget uninstall -e --id {app_name}"
            stdout, stderr = await self.run_command(cmd)
            return f"Uninstalled {app_name}. Output: {stdout}"
        except Exception as e:
            return f"Failed to uninstall {app_name}: {e}"

    async def close_application(self, app_name: str):
        try:
            # Use taskkill
            # Note: app_name here should ideally be the process name (e.g., notepad.exe)
            # We might need a mapping or heuristic, but for now let's try the name directly
            cmd = f"taskkill /IM {app_name}.exe /F"
            stdout, stderr = await self.run_command(cmd)
            if "SUCCESS" in stdout:
                return f"Closed {app_name}"
            else:
                # Try without .exe
                cmd = f"taskkill /IM {app_name} /F"
                stdout, stderr = await self.run_command(cmd)
                return f"Closed {app_name}. Output: {stdout}"
        except Exception as e:
            return f"Failed to close {app_name}: {e}"

    async def show_notification(self, title: str, message: str):
        try:
            # PowerShell command to show a balloon tip (or just a message box for simplicity)
            # Using a simple message box for now as it's more reliable to grab attention
            ps_script = f"""
            Add-Type -AssemblyName PresentationFramework
            [System.Windows.MessageBox]::Show('{message}', '{title}')
            """
            # Run in background so it doesn't block
            cmd = f'powershell -Command "{ps_script}"'
            process = await asyncio.create_subprocess_shell(cmd)
            return "Notification sent"
        except Exception as e:
            return f"Failed to show notification: {e}"
