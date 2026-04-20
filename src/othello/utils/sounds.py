# src/othello/utils/sounds.py

import os

# Optional pygame import
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class SoundManager:
    """Manages game sounds (optional feature)."""
    
    def __init__(self, sound_dir: str = None):
        """
        Initialize sound manager.
        
        Args:
            sound_dir: Directory containing sound files (optional)
        """
        self.sounds = {}
        self.enabled = PYGAME_AVAILABLE
        
        if not self.enabled:
            print("SOUND: Disabled (pygame not available)")  # ADD DEBUG
            return
        
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

            print(f"SOUND: Initialized successfully, loading from {sound_dir}")  # ADD DEBUG
            
            # Default sound directory
            if sound_dir is None:
                sound_dir = os.path.join(os.path.dirname(__file__), 'sounds')
            
            # Load sounds (optional, won't fail if missing)
            self._load_sound('place.wav', sound_dir)
            self._load_sound('flip.wav', sound_dir)
            self._load_sound('pass.wav', sound_dir)
            self._load_sound('game_over.wav', sound_dir)
            
        except Exception as e:
            # If pygame fails, sounds will be disabled
            print(f"Sound initialization failed: {e}")
            self.enabled = False
    
    def _load_sound(self, filename: str, directory: str) -> None:
        """Load a sound file."""
        if not PYGAME_AVAILABLE:
            return
            
        try:
            path = os.path.join(directory, filename)
            if os.path.exists(path):
                self.sounds[filename.replace('.wav', '')] = pygame.mixer.Sound(path)
        except Exception:
            # Silently fail if sound file is missing
            pass
    
    def play(self, sound_name: str) -> None:
        """
        Play a sound effect.
        
        Args:
            sound_name: Name of the sound to play
        """
        if not self.enabled:
            return
        
        sound = self.sounds.get(sound_name)
        if sound:
            try:
                sound.play()
            except Exception:
                pass
    
    def stop(self) -> None:
        """Stop all sounds."""
        if self.enabled:
            pygame.mixer.stop()
    
    def set_volume(self, volume: float) -> None:
        """
        Set master volume (0.0 to 1.0).
        
        Args:
            volume: Volume level
        """
        if self.enabled:
            pygame.mixer.set_volume(volume)
