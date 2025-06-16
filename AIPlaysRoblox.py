import random
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread
import pygetwindow as gw
import keyboard

class KeyPressGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game Bot Tool")
        self.root.geometry("250x250")
        self.root.resizable(False, False)
        
        self.window_list = []
        self.selected_window = tk.StringVar()
        self.selected_window.set("Select window")
        self.is_running = False
        self.key_thread = None
        self.stop_key = 'p'
        self.currently_pressed_keys = set()
        self.target_window = None
        
        self.create_widgets()
        
        self.update_window_list()
        
        self.setup_keyboard_hook()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        """Create the GUI widgets"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)

        window_frame = ttk.LabelFrame(main_frame, text="Window Selection", padding="5")
        window_frame.pack(fill="x", padx=5, pady=5)

        self.window_dropdown = ttk.Combobox(window_frame, textvariable=self.selected_window, state="readonly")
        self.window_dropdown.pack(fill="x", padx=5, pady=5)

        refresh_btn = ttk.Button(window_frame, text="Refresh Windows", command=self.update_window_list)
        refresh_btn.pack(fill="x", padx=5, pady=5)

        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.pack(fill="x", padx=5, pady=5)

        self.status_label = ttk.Label(status_frame, text=f"Status: Stopped\nStop key: {self.stop_key}")
        self.status_label.pack(fill="x", padx=5, pady=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", padx=5, pady=5)

        self.toggle_button = ttk.Button(button_frame, text="Start", command=self.toggle)
        self.toggle_button.pack(side="left", fill="x", expand=True, padx=5)

        self.set_key_button = ttk.Button(button_frame, text="Set Stop Key", command=self.set_stop_key)
        self.set_key_button.pack(side="left", fill="x", expand=True, padx=5)
        
    def setup_keyboard_hook(self):
        """Set up global keyboard hook"""
        try:
            keyboard.unhook_all()
            keyboard.on_press(self.on_key_press)
        except Exception as e:
            print(f"Error setting up keyboard hook: {e}")
    
    def on_key_press(self, event):
        """Handle global key press events"""
        if self.stop_key and event.name == self.stop_key and self.is_running:
            self.stop_bot()
    
    def set_stop_key(self):
        """Wait for user to press a key to set as stop key"""
        self.status_label.config(text="Press any key to set stop key...")
        self.root.update()
        
        def wait_for_key():
            try:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    self.stop_key = event.name
                    self.root.after(0, lambda: self.status_label.config(
                        text=f"Status: Stopped\nStop key: {self.stop_key}"))
                    print(f"Stop key set to: {self.stop_key}")
            except Exception as e:
                print(f"Error setting stop key: {e}")
                self.root.after(0, lambda: self.status_label.config(
                    text="Error setting stop key"))
        
        Thread(target=wait_for_key, daemon=True).start()
    
    def stop_bot(self):
        """Stop the bot and release all keys"""
        if self.is_running:
            self.is_running = False
            self.release_all_keys()
            self.toggle_button.config(text="Start")
            self.status_label.config(text=f"Status: Stopped\nStop key: {self.stop_key}")
            print(f"Bot stopped by '{self.stop_key}' key")
    
    def release_all_keys(self):
        """Release all currently pressed keys"""
        for key in self.currently_pressed_keys.copy():
            try:
                keyboard.release(key)
                self.currently_pressed_keys.discard(key)
                print(f"Released key: {key}")
            except Exception as e:
                print(f"Error releasing key {key}: {e}")
        self.currently_pressed_keys.clear()
    
    def update_window_list(self):
        """Update the list of available windows"""
        try:
            windows = gw.getAllTitles()
            windows = [w for w in windows if w and w.strip() != ""]
            
            if not windows:
                self.window_dropdown['values'] = ["No windows found"]
                self.selected_window.set("No windows found")
                return
                
            windows.sort()
            self.window_dropdown['values'] = windows
            
            current_selection = self.selected_window.get()
            if current_selection not in windows and current_selection != "Select window":
                self.selected_window.set("Select window")
                
        except Exception as e:
            print(f"Error updating window list: {e}")
            self.window_dropdown['values'] = ["Error loading windows"]
            self.selected_window.set("Error loading windows")
    
    def focus_window(self):
        """Focus the target window"""
        try:
            if not self.target_window:
                return False
            
            if not self.target_window.isActive:
                try:
                    if self.target_window.isMinimized:
                        self.target_window.restore()
                    self.target_window.activate()
                    time.sleep(0.1)
                except Exception as e:
                    print(f"Error activating window: {e}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"Error focusing window: {e}")
            return False
    
    def toggle(self):
        """Toggle bot on/off"""
        if not self.is_running:
            selected_window = self.selected_window.get()
            if selected_window in ["Select window", "No windows found", "Error loading windows"]:
                self.status_label.config(text="Please select a valid window first")
                return
            
            try:
                windows = gw.getWindowsWithTitle(selected_window)
                if not windows:
                    self.status_label.config(text="Window not found")
                    return
                
                self.target_window = windows[0]
                self.is_running = True
                self.toggle_button.config(text="Stop")
                self.status_label.config(text=f"Status: Running\nStop key: {self.stop_key}")
                print(f"Starting bot for window: {selected_window}")
                
                self.start_key_press()
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
                print(f"Error starting bot: {e}")
        else:
            self.stop_bot()
    
    def start_key_press(self):
        """Start the key press automation with chat functionality"""
        movements = [
            (('w',), 2.0, 4.0),    
            (('a',), 1.5, 2.5),    
            (('d',), 1.5, 2.5),    
            (('s',), 1.3, 2.0),    
            (('space',), 0.3, 0.5), 
            
            (('up',), 2.0, 4.0),    
            (('right',), 1.5, 2.5), 
            (('down',), 1.3, 2.0),  
            
            (('w', 'a'), 1.5, 3.0),  
            (('w', 'd'), 1.5, 3.0),  
            (('w', 'space'), 1.0, 2.0),  
            (('a', 'space'), 1.0, 1.5),  
            (('d', 'space'), 1.0, 1.5),  
            
            (('up', 'left'), 1.5, 3.0),   
            (('up', 'right'), 1.5, 3.0),  
            (('up', 'space'), 1.0, 2.0),  
            (('left', 'space'), 1.0, 1.5), 
            (('right', 'space'), 1.0, 1.5), 
            
            (('w', 'left'), 1.5, 3.0),    
            (('w', 'right'), 1.5, 3.0),   
            (('up', 'a'), 1.5, 3.0),      
            (('up', 'd'), 1.5, 3.0),      
            
            (('w', 'a', 'space'), 1.2, 2.0),  
            (('w', 'd', 'space'), 1.2, 2.0),  
            
            (('up', 'left', 'space'), 1.2, 2.0),  
            (('up', 'right', 'space'), 1.2, 2.0), 
        ]

        weighted_movements = []
        for movement in movements:
            keys, min_hold, max_hold = movement
            if ('w' in keys or 'up' in keys) and len(keys) == 1:
                weighted_movements.extend([movement] * 8)  
            elif 'w' in keys or 'up' in keys:
                weighted_movements.extend([movement] * 4)  
            elif 'space' in keys and len(keys) == 1:
                weighted_movements.extend([movement] * 2)  
            elif 's' in keys or 'down' in keys:
                weighted_movements.extend([movement] * 1)  
            else:
                weighted_movements.extend([movement] * 3) 

        chat_messages = {
            "hi": 0.1,
            "i like cheese lol.": 0.2,
            "they are here": 0.01,
            "friend.": 0.1,
            "yo": 0.15,
            "bruh": 0.2,
            "lol": 0.2,
            "gg": 0.15,
            "ez": 0.15,
            "oof": 0.1,
            "where u at": 0.1,
            "come here": 0.1,
            "noob": 0.12,
            "nice shot!": 0.1,
            "lag": 0.12,
            "wait up": 0.1,
            "team up": 0.1,
            "follow me": 0.1,
            "i got this": 0.1,
            "bro": 0.15,
            "nah": 0.15,
            "sus": 0.15,
            "nah fam": 0.12,
            "sheesh": 0.15,
            "same": 0.1,
            "help me": 0.1,
            "behind you!": 0.1,
            "we chillin": 0.15,
            "no way lol": 0.1,
            "this game wild": 0.1,
            "i'm stuck": 0.1,
            "bro what": 0.12,
            "wait what": 0.12,
            "who did that": 0.1,
            "glitch?": 0.08,
            "not again": 0.08,
            "yo chill": 0.1,
            "run": 0.1,
            "look up": 0.08,
            "you saw that?": 0.08,
            "i swear": 0.1,
            "don't move": 0.05,
            "is that normal": 0.05,
            "free robux": 0.1,
            "not clickbait": 0.08,
            "my wifi dying": 0.08,
            "what server is this": 0.06,
            "did you hear that": 0.04,

            "he watches us all": 0.005,
             "the skybox is alive": 0.002,
            "don't trust him": 0.004,
            "it's under the map": 0.003,
            "i never left": 0.002,
            "i see you": 0.005,
            "this isn't a game": 0.003,
            "you shouldn't be here": 0.004,
            "she is behind you": 0.002,
            "stop looking": 0.003,
            "every copy is personalized": 0.002,
            "he's in your code": 0.001,
            "you glitched the wrong server": 0.001,
            "404": 0.002,
            "i remember everything": 0.003,
            "why did you return": 0.002,
            "you woke it up": 0.001,
            "watch the shadows": 0.002,
            "we can't leave": 0.003,
            "check the basement": 0.002,
            "it won't let me log out": 0.001,

            "i ate the map": 0.05,
            "my cat is playing": 0.04,
            "banana squad": 0.05,
            "i'm a chair now": 0.05,
            "beep boop": 0.05,
            "error: sanity not found": 0.04,
            "i'm speed": 0.05,
            "roblox physics moment": 0.05,
            "gravity is optional": 0.05,
            "someone stole my legs": 0.04,
            "bork bork": 0.05,
            "i speak oof": 0.05,
            "send help": 0.05,
            "this is fine": 0.05,
            "initiate pizza protocol": 0.03,
            "i tripped over a noob": 0.05,
            "bro became an npc": 0.05,
            "teleported into backrooms": 0.03,
            "fell into the void": 0.05,
            "map just blinked": 0.02,
            "npc uprising coming": 0.03,
            "admin watching rn": 0.02,
            "i hacked gravity": 0.03,
            "bricked my legs": 0.04,
            "toilet boss incoming": 0.02
        }

        def key_press_loop():
            chat_cooldown = 0  
            while self.is_running:
                try:
                    if not self.focus_window():
                        print("Lost window focus, stopping...")
                        self.root.after(0, self.stop_bot)
                        break

                    if random.random() < 0.05 and chat_cooldown <= 0:
                        self.release_all_keys()
                        time.sleep(0.5)  
                        
                        message = random.choices(
                            list(chat_messages.keys()),
                            weights=list(chat_messages.values())
                        )[0]
                        
                        print(f"Chatting: {message}")
                        keyboard.press_and_release('/')  
                        time.sleep(0.1)
                        
                        for char in message:
                            keyboard.press_and_release(char)
                            time.sleep(random.uniform(0.05, 0.1))
                        
                        keyboard.press_and_release('enter')
                        time.sleep(0.5)  
                        
                        chat_cooldown = random.randint(30, 90)
                    
                    if chat_cooldown > 0:
                        chat_cooldown -= 1
                        time.sleep(1)
                        continue

                    movement = random.choice(weighted_movements)
                    keys, min_hold, max_hold = movement
                    
                    print(f"Pressing keys: {', '.join(keys)}")
                    for key in keys:
                        try:
                            keyboard.press(key)
                            self.currently_pressed_keys.add(key)
                        except Exception as e:
                            print(f"Error pressing key {key}: {e}")
                    
                    hold_time = random.uniform(min_hold, max_hold)
                    print(f"Holding keys {keys} for {hold_time:.2f} seconds")
                    
                    sleep_time = 0
                    while sleep_time < hold_time and self.is_running:
                        time.sleep(0.1)
                        sleep_time += 0.1
                    
                    for key in keys:
                        try:
                            keyboard.release(key)
                            self.currently_pressed_keys.discard(key)
                        except Exception as e:
                            print(f"Error releasing key {key}: {e}")
                    print(f"Released keys: {', '.join(keys)}")
                    
                    if self.is_running:
                        time.sleep(random.uniform(0.1, 0.5))
                        
                except Exception as e:
                    print(f"Error in key press loop: {e}")
                    self.root.after(0, self.stop_bot)
                    break

            print("Key press loop ended")

        print("Starting key press loop...")
        self.key_thread = Thread(target=key_press_loop, daemon=True)
        self.key_thread.start()

        def key_press_loop():
            while self.is_running:
                try:
                    if not self.focus_window():
                        print("Lost window focus, stopping...")
                        self.root.after(0, self.stop_bot)
                        break
                    
                    movement = random.choice(weighted_movements)
                    keys, min_hold, max_hold = movement
                    
                    print(f"Pressing keys: {', '.join(keys)}")
                    for key in keys:
                        try:
                            keyboard.press(key)
                            self.currently_pressed_keys.add(key)
                        except Exception as e:
                            print(f"Error pressing key {key}: {e}")
                    
                    hold_time = random.uniform(min_hold, max_hold)
                    print(f"Holding keys {keys} for {hold_time:.2f} seconds")
                    
                    sleep_time = 0
                    while sleep_time < hold_time and self.is_running:
                        time.sleep(0.1)
                        sleep_time += 0.1
                    
                    for key in keys:
                        try:
                            keyboard.release(key)
                            self.currently_pressed_keys.discard(key)
                        except Exception as e:
                            print(f"Error releasing key {key}: {e}")
                    print(f"Released keys: {', '.join(keys)}")
                    
                    if self.is_running:
                        time.sleep(random.uniform(0.1, 0.5))
                        
                except Exception as e:
                    print(f"Error in key press loop: {e}")
                    self.root.after(0, self.stop_bot)
                    break
            
            print("Key press loop ended")

        print("Starting key press loop...")
        self.key_thread = Thread(target=key_press_loop, daemon=True)
        self.key_thread.start()

    def on_closing(self):
        """Handle application closing"""
        print("Closing application...")
        self.is_running = False
        self.release_all_keys()
        try:
            keyboard.unhook_all()
        except Exception as e:
            print(f"Error unhooking keyboard: {e}")
        finally:
            self.root.destroy()

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting Game Bot Tool...")
    print("Make sure to run as administrator for better compatibility!")
    try:
        app = KeyPressGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")