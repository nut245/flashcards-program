"""
Stores all files of Widgets created and/or modified by me

#### including...
- Universals:
    - TitleWidget
    - CustomFrame
    - CustomButton
    - CustomLabel
    - VerticalScrolledFrame
    - OptionWidget
---
- TopLevelManagers:
    - SubPage
    - TopLevelButton
---
- Miscellaneous:
    - QuestionButton
    - ResultWidget
    - KeyBindsWidget
"""

from .universal_widgets.title_widget import TitleWidget
from .universal_widgets.custom_frame import CustomFrame
from .universal_widgets.custom_button import CustomButton
from .universal_widgets.custom_label import CustomLabel
from .universal_widgets.scrollable_frame import VerticalScrolledFrame
from .universal_widgets.option_widget import OptionWidget

from .top_level_managers.sub_page import SubPage
from .top_level_managers.top_level_button import TopLevelButton
from .top_level_managers.embedded_pages import EmbeddedPages

from .page_specfic_widgets.question_button import QuestionButton
from .page_specfic_widgets.result_widget import ResultWidget
from .page_specfic_widgets.key_binds_widget import KeyBindsWidget
from .page_specfic_widgets.deck_widgets.folder_details_widget import FolderDetailsWidget
from .page_specfic_widgets.deck_widgets.flashcard_details_widget import FlashcardsDetailsWidget