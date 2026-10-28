"""R5 Page Objects package."""
from .base_page import BasePage, norm
from .portal import Portal
from .paper_applications_page import PaperApplicationsPage

__all__ = ["BasePage", "norm", "Portal", "PaperApplicationsPage"]
