"""
Main application class for the Steganography App with AI Integration
"""

from src.text_steganography import TextSteganography
from src.audio_steganography import AudioSteganography
from src.ai_analyzer import AIAnalyzer

class SteganographyApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the steganography application"""
        self.text_steganography = TextSteganography()
        self.audio_steganography = AudioSteganography()
        self.ai_analyzer = AIAnalyzer()
        
    def run(self):
        """Run the main application loop"""
        print("Steganography App with AI Integration")
        print("=" * 40)
        print("Starting application...")
        
        # Initialize components
        self._initialize_components()
        
        # Run the main interface
        self._run_interface()
        
    def _initialize_components(self):
        """Initialize all application components"""
        print("Initializing components...")
        # Components are initialized in __init__
        
    def _run_interface(self):
        """Run the main user interface"""
        while True:
            print("\nSteganography App Menu:")
            print("1. Text Steganography")
            print("2. Audio Steganography")
            print("3. AI Analysis")
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                self._text_steganography_menu()
            elif choice == "2":
                self._audio_steganography_menu()
            elif choice == "3":
                self._ai_analysis_menu()
            elif choice == "4":
                print("Exiting application...")
                break
            else:
                print("Invalid choice. Please try again.")
                
    def _text_steganography_menu(self):
        """Handle text steganography operations"""
        print("\nText Steganography Menu:")
        print("1. Embed message in text")
        print("2. Extract message from text")
        print("3. Back to main menu")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            self._embed_text_message()
        elif choice == "2":
            self._extract_text_message()
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")
            
    def _audio_steganography_menu(self):
        """Handle audio steganography operations"""
        print("\nAudio Steganography Menu:")
        print("1. Embed message in audio")
        print("2. Extract message from audio")
        print("3. Back to main menu")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            self._embed_audio_message()
        elif choice == "2":
            self._extract_audio_message()
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")
            
    def _ai_analysis_menu(self):
        """Handle AI analysis operations"""
        print("\nAI Analysis Menu:")
        print("1. Analyze text for steganography")
        print("2. Analyze audio for steganography")
        print("3. Back to main menu")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            self._analyze_text()
        elif choice == "2":
            self._analyze_audio()
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")
            
    def _embed_text_message(self):
        """Embed a message in text"""
        cover_text = input("Enter the cover text: ")
        secret_message = input("Enter the secret message: ")
        
        # Analyze text for optimal method
        analysis = self.ai_analyzer.analyze_text_for_steganography(cover_text)
        method = analysis["recommended_method"]
        
        print(f"AI recommends using '{method}' method (confidence: {analysis['confidence']:.2f})")
        
        try:
            stego_text = self.text_steganography.embed_message(cover_text, secret_message, method)
            print("\nSteganographic text created successfully!")
            print("Result:")
            print(stego_text)
        except Exception as e:
            print(f"Error embedding message: {e}")
            
    def _extract_text_message(self):
        """Extract a message from text"""
        stego_text = input("Enter the steganographic text: ")
        
        # Try different methods
        methods = ["whitespace", "synonym"]
        extracted = None
        
        for method in methods:
            try:
                extracted = self.text_steganography.extract_message(stego_text, method)
                if extracted:
                    print(f"\nExtracted message using '{method}' method:")
                    print(extracted)
                    break
            except Exception as e:
                print(f"Error with {method} method: {e}")
                
        if not extracted:
            print("Could not extract message. The text may not contain hidden data.")
            
    def _embed_audio_message(self):
        """Embed a message in audio"""
        audio_file = input("Enter the path to the audio file: ")
        secret_message = input("Enter the secret message: ")
        output_file = input("Enter the path for the output steganographic audio: ")
        
        try:
            # Analyze audio for optimal method
            analysis = self.audio_steganography.analyze_audio(audio_file)
            if "error" in analysis:
                print(f"Error analyzing audio: {analysis['error']}")
                return
                
            method = analysis["recommended_method"]
            print(f"AI recommends using '{method}' method (confidence: {analysis['confidence']:.2f})")
            
            success = self.audio_steganography.embed_message(audio_file, secret_message, output_file, method)
            if success:
                print("\nSteganographic audio created successfully!")
            else:
                print("Error creating steganographic audio.")
        except Exception as e:
            print(f"Error embedding message: {e}")
            
    def _extract_audio_message(self):
        """Extract a message from audio"""
        stego_audio = input("Enter the path to the steganographic audio file: ")
        
        try:
            extracted = self.audio_steganography.extract_message(stego_audio)
            if extracted:
                print("\nExtracted message:")
                print(extracted)
            else:
                print("Could not extract message. The audio may not contain hidden data.")
        except Exception as e:
            print(f"Error extracting message: {e}")
            
    def _analyze_text(self):
        """Analyze text using AI"""
        text = input("Enter the text to analyze: ")
        
        analysis = self.ai_analyzer.analyze_text_for_steganography(text)
        
        print("\nAI Analysis Results:")
        print(f"Word count: {analysis['word_count']}")
        print(f"Character count: {analysis['char_count']}")
        print(f"Average word length: {analysis['avg_word_length']:.2f}")
        print(f"Recommended method: {analysis['recommended_method']}")
        print(f"Confidence: {analysis['confidence']:.2f}")
        print(f"Estimated capacity: {analysis['estimated_capacity']} characters")
        
    def _analyze_audio(self):
        """Analyze audio using AI"""
        audio_file = input("Enter the path to the audio file: ")
        
        try:
            # Get basic info first
            analysis = self.audio_steganography.analyze_audio(audio_file)
            if "error" in analysis:
                print(f"Error analyzing audio: {analysis['error']}")
                return
                
            ai_analysis = self.ai_analyzer.analyze_audio_for_steganography(analysis)
            
            print("\nAI Analysis Results:")
            print(f"Duration: {analysis['duration']:.2f} seconds")
            print(f"Sample rate: {analysis['sample_rate']} Hz")
            print(f"Channels: {analysis['channels']}")
            print(f"Recommended method: {ai_analysis['recommended_method']}")
            print(f"Confidence: {ai_analysis['confidence']:.2f}")
            print(f"Estimated capacity: {ai_analysis['estimated_capacity']} bytes")
        except Exception as e:
            print(f"Error analyzing audio: {e}")