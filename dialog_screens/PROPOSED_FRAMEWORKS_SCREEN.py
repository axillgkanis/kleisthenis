import customtkinter as ctk
from dialog_screens.frameManager import frameManager
from dialog_screens.FRAMEWORK_SCREEN import FRAMEWORK_SCREEN
from dialog_screens.DIALOGUE_SCREEN import DIALOGUE_SCREEN

class PROPOSED_FRAMEWORKS_SCREEN(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.all_frames = []  # Αποθηκεύει όλα τα frames από το αρχείο
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self.render_frame_list())

        # Τίτλος
        ctk.CTkLabel(self, text="Προτεινομενα Πλαίσια", font=("Arial", 20, "bold")).pack(pady=(10, 5))

        # Search / Filtering Entry
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(pady=(0, 10), fill="x", padx=20)

        ctk.CTkLabel(search_frame, text="Search:", font=("Arial", 12)).pack(side="left", padx=5)
        ctk.CTkEntry(search_frame, textvariable=self.search_var, width=300, placeholder_text="Filter by title...").pack(side="left")

        # Frame List container
        self.list_container = ctk.CTkFrame(self, fg_color="transparent")
        self.list_container.pack(pady=10, fill="both", expand=True)
        
        # Initialize frame manager
        self.frame_manager = frameManager()
        
        # Load frames when initialized
        self.displayProposedFrameworksScreen()
        
    def displayProposedFrameworksScreen(self):
        """Initializes the screen and loads frameworks from database"""
        # Clear existing frames
        for widget in self.list_container.winfo_children():
            widget.destroy()
            
        # Get frameworks from database through frameManager
        self.displayProposedFrameworks()
        
        # Render the list
        self.render_frame_list()
        
    def displayProposedFrameworks(self):
        """Gets proposed frameworks from the database using frameManager"""
        try:
            # Try to get frameworks from database
            db_frameworks = self.frame_manager.searchProposedFrameworks()
            
            if db_frameworks and isinstance(db_frameworks, list):
                self.all_frames = db_frameworks
            else:
                message="Δεν βρέθηκαν προτεινόμενα πλαίσια."
                DIALOGUE_SCREEN().displayFail(message)
                
        except Exception as e:
            message = "Σφάλμα κατά την ανάκτηση των προτεινόμενων πλαισίων."
            DIALOGUE_SCREEN().displayFail(message)            
    
    def render_frame_list(self):
        """Renders the list of proposed frameworks with filtering"""
        # Clear existing list
        for widget in self.list_container.winfo_children():
            widget.destroy()

        # Get filter keyword
        keyword = self.search_var.get().lower()

        # Filter frameworks by title
        filtered = [
            f for f in self.all_frames
            if keyword in f.get("title", "").lower()
        ]

        if not filtered:
            ctk.CTkLabel(self.list_container, text="Δεν βρέθηκαν προτεινόμενα πλαίσια.", text_color="gray").pack(pady=10)
            return

        # Create a frame for each framework
        for frame_data in filtered:
            frame_row = ctk.CTkFrame(self.list_container, fg_color="#1e293b", corner_radius=8)
            frame_row.pack(fill="x", padx=30, pady=5)
            
            # Framework title
            title = frame_data.get("title", "Untitled")
            
            # Create a function that closes over the frame_data for the view button
            def make_view_callback(frame=frame_data):
                return lambda: self.displayProposedFramework(frame)
            
            # Title label
            title_label = ctk.CTkLabel(
                frame_row, 
                text=title,
                anchor="w",
                font=("Arial", 13, "bold"),
                text_color="#e2e8f0"
            )
            title_label.pack(side="left", padx=10, pady=8, fill="x", expand=True)
            
            # Status indicator based on vote status
            if frame_data.get("vote", 0) == 1:
                status_label = ctk.CTkLabel(
                    frame_row,
                    text="Ψηφισμένο",
                    font=("Arial", 11),
                    text_color="#10b981"
                )
                status_label.pack(side="left", padx=5)
            
            # View button
            view_btn = ctk.CTkButton(
                frame_row,
                text="Προβολή",
                fg_color="#334155",
                hover_color="#475569",
                command=make_view_callback()
            )
            view_btn.pack(side="right", padx=10, pady=5)
            
    def displayProposedFramework(self, frame_data):
        """Opens a popup to display the selected framework details"""
        try:
            # If we have a database ID, get details from database
            if "id" in frame_data:
                framework_id = frame_data["id"]
                details = self.frame_manager.searchProposedFrameDetails(framework_id)
                if details:
                    frame_data = details
            
            # Display the framework in a popup
            popup = FrameViewerPopup(self, frame_data)
            
            # Wait for the popup to close and then refresh the list
            self.wait_window(popup)
            
            # Refresh the list to show updated status
            self.displayProposedFrameworksScreen()
            
        except Exception as e:
            message = "Σφάλμα κατά την προβολή του πλαισίου."
            DIALOGUE_SCREEN().displayFail(message)
